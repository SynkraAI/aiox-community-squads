"""
Dispatch Squad — Pipeline Orchestrator
Main entry point: Story → all phases → ready for execution.

Ties together routing, optimization, enrichment, validation, and wave execution.
The dispatch-chief calls this instead of improvising each phase.

Usage:
    python dispatch-orchestrator.py plan    --input story.md [--force] [--max-parallel 7] [--root .]
    python dispatch-orchestrator.py execute --run-id <ID> [--wave N] [--root .]
    python dispatch-orchestrator.py full    --input story.md [--root .]
    python dispatch-orchestrator.py resume  [--run-id <ID>] [--root .]
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

# ═══════════════════════════════════════════════════════════════════════════════
# PATH SETUP
# ═══════════════════════════════════════════════════════════════════════════════

SCRIPT_DIR = Path(__file__).resolve().parent
SQUAD_DIR = SCRIPT_DIR.parent
LIB_DIR = SQUAD_DIR / "lib"

sys.path.insert(0, str(LIB_DIR))

from pipeline_state import DispatchStateManager
from event_log import EventLog
from script_runner import run_script

# Rich progress display (graceful degradation if not installed)
try:
    from rich_progress import (
        print_plan_summary,
        print_wave_complete,
        print_final_report,
        print_cost_breakdown,
        print_error,
        print_warning,
        print_success,
        RICH_AVAILABLE,
    )
except ImportError:
    RICH_AVAILABLE = False

# ═══════════════════════════════════════════════════════════════════════════════
# REQUIRED SCRIPTS — Precondition check
# ═══════════════════════════════════════════════════════════════════════════════

REQUIRED_SCRIPTS = [
    "extract-quantities.py",
    "route-tasks.py",
    "wave-optimizer.py",
    "enrich-task.py",
    "validate-dispatch-gate.sh",
    "validate-haiku-prompt.py",
    "cost-tracker.py",
    "dispatch-health-score.py",
    "validate-wave-results.py",
    "wave-executor.py",
    "generate-execution-report.py",
]

REQUIRED_DATA = [
    "squads/dispatch/data/domain-registry.yaml",
    "squads/dispatch/data/command-registry.yaml",
]

MAX_PARALLEL_DEFAULT = 7


# ═══════════════════════════════════════════════════════════════════════════════
# PRECONDITIONS
# ═══════════════════════════════════════════════════════════════════════════════


def _validate_preconditions(project_root: str) -> dict:
    """Check ALL required scripts and data files exist. ANY missing → HALT.

    Returns:
        {"ok": True} or {"ok": False, "missing_scripts": [...], "missing_data": [...]}
    """
    root = Path(project_root)
    scripts_dir = root / "squads" / "dispatch" / "scripts"

    missing_scripts = []
    for s in REQUIRED_SCRIPTS:
        if not (scripts_dir / s).exists():
            missing_scripts.append(s)

    missing_data = []
    for d in REQUIRED_DATA:
        if not (root / d).exists():
            missing_data.append(d)

    if missing_scripts or missing_data:
        return {
            "ok": False,
            "missing_scripts": missing_scripts,
            "missing_data": missing_data,
            "error": f"Missing {len(missing_scripts)} scripts, {len(missing_data)} data files",
            "next_action": {
                "type": "halt",
                "reason": "Precondition failed: missing required files",
                "message": f"Missing {len(missing_scripts)} scripts and {len(missing_data)} data files. Restore missing files before retrying.",
                "details": {
                    "missing_scripts": missing_scripts,
                    "missing_data": missing_data,
                },
            },
        }

    return {"ok": True}


# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 0: SUFFICIENCY GATE
# ═══════════════════════════════════════════════════════════════════════════════


def _phase0_sufficiency(input_path: str, project_root: str, force: bool = False) -> dict:
    """Sufficiency gate — V0.1: input exists, V0.2: quantities extractable, V0.3: has criteria.

    Returns:
        {"ok": True, "input_type": "story", "description": "...", "quantities": {...}}
        or {"ok": False, "error": "...", "gate": "V0.X"}
    """
    root = Path(project_root)
    path = root / input_path if not Path(input_path).is_absolute() else Path(input_path)

    # V0.1: Input file exists
    if not path.exists():
        return {
            "ok": False,
            "error": f"Input file not found: {path}",
            "gate": "V0.1",
            "next_action": {
                "type": "halt",
                "reason": "Input file not found",
                "message": f"File does not exist: {path}. Verify path and retry.",
            },
        }

    content = path.read_text(encoding="utf-8")

    # Detect input type
    if "acceptance_criteria" in content.lower() or "acceptance criteria" in content.lower():
        input_type = "story"
    elif "## requirements" in content.lower() or "## overview" in content.lower():
        input_type = "prd"
    else:
        input_type = "free_text"

    # V0.2: Extract quantities
    quantities_result = run_script(
        "extract-quantities.py",
        ["--input", content[:2000]],  # First 2000 chars for quantity extraction
        project_root=project_root,
    )

    quantities = {}
    if quantities_result["ok"]:
        quantities = quantities_result["data"]
    # V0.2 is soft — missing quantities don't block

    # V0.3: Story should have acceptance criteria (soft gate unless --force)
    if input_type == "story" and "- [ ]" not in content and "- [x]" not in content:
        if not force:
            return {
                "ok": False,
                "error": "Story has no acceptance criteria checkboxes ([ ]). Use --force to override.",
                "gate": "V0.3",
                "next_action": {
                    "type": "halt",
                    "reason": "Story missing acceptance criteria",
                    "message": "Story has no acceptance criteria checkboxes. Add criteria or use --force flag to override.",
                },
            }

    # Extract description (first heading or first paragraph)
    lines = content.strip().split("\n")
    description = ""
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("# "):
            description = stripped.lstrip("# ").strip()
            break
        if stripped and not stripped.startswith("---") and not stripped.startswith(">"):
            description = stripped[:200]
            break

    return {
        "ok": True,
        "input_type": input_type,
        "input_path": str(path),
        "description": description or path.stem,
        "quantities": quantities,
        "content_length": len(content),
    }


# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 1: DECOMPOSITION REQUEST
# ═══════════════════════════════════════════════════════════════════════════════


def _phase1_decomposition_request(state, run_dir: Path, input_path: str, project_root: str) -> dict:
    """Write decomposition_request.json — instructions for wave-planner subagent.

    This phase produces a structured request that the dispatch-chief sends to a
    Sonnet subagent for LLM-based decomposition. The script cannot do this part
    deterministically — it needs LLM reasoning to break a story into tasks.

    Returns:
        {"ok": True, "decomposition_request_path": "..."}
    """
    root = Path(project_root)
    path = root / input_path if not Path(input_path).is_absolute() else Path(input_path)
    content = path.read_text(encoding="utf-8")

    request = {
        "instruction": "Decompose this input into atomic dispatch tasks",
        "input_path": str(input_path),
        "input_content": content,
        "rules": [
            "Each task MUST be atomic: 1 task = 1 deliverable",
            "Each task MUST have: task_id, name, description, output_path, acceptance_criteria, dependencies[]",
            "task_id format: T001, T002, etc.",
            "Dependencies reference other task_ids (e.g., T001 depends on T002)",
            "Worker tasks (mkdir, copy, mv) MUST have type=worker",
            "Output format: JSON array of task objects",
            "DO NOT ask questions. Decompose immediately.",
            "If task requires creative writing or judgment, mark type=create",
            "If task is deterministic (file ops, template fill), mark type=worker",
        ],
        "output_path": str(run_dir / "execution-plan.json"),
        "output_format": "json",
    }

    request_path = run_dir / "decomposition_request.json"
    with open(request_path, "w", encoding="utf-8") as f:
        json.dump(request, f, indent=2, ensure_ascii=False)

    return {
        "ok": True,
        "decomposition_request_path": str(request_path),
        "requires_llm": True,
        "instruction": "Send decomposition_request.json to a Sonnet subagent. Save output to execution-plan.json. Then call `dispatch-orchestrator.py execute --run-id {run_id}`",
    }


# ═══════════════════════════════════════════════════════════════════════════════
# PHASES 2-4.5: ROUTING → OPTIMIZATION → ENRICHMENT → GATE
# ═══════════════════════════════════════════════════════════════════════════════


def _phases2_to_4_5(
    state,
    manager: DispatchStateManager,
    log: EventLog,
    run_dir: Path,
    max_parallel: int,
    project_root: str,
) -> dict:
    """Execute phases 2 through 4.5 deterministically.

    Phase 2: route-tasks.py (domain, model, enrichment, timeout)
    Phase 3: wave-optimizer.py (DAG topological sort)
    Phase 4: enrich-task.py per task
    Phase 4.5: validate-dispatch-gate.sh per prompt

    Requires execution-plan.json to exist (produced by Phase 1 LLM decomposition).

    Returns:
        {"ok": True, "waves": N, "tasks": N, "routed": {...}, "optimized": {...}}
    """
    plan_path = run_dir / "execution-plan.json"
    if not plan_path.exists():
        return {
            "ok": False,
            "error": "execution-plan.json not found. Run Phase 1 (LLM decomposition) first.",
            "next_action": {
                "type": "halt",
                "reason": "Missing execution plan",
                "message": "execution-plan.json not found. Run Phase 1 decomposition first.",
            },
        }

    with open(plan_path, "r", encoding="utf-8") as f:
        plan_data = json.load(f)

    # Normalize: handle both raw array and {tasks: [...]} formats
    if isinstance(plan_data, list):
        tasks = plan_data
    elif isinstance(plan_data, dict):
        tasks = plan_data.get("tasks", [])
    else:
        return {
            "ok": False,
            "error": "Invalid execution-plan.json format",
            "next_action": {
                "type": "halt",
                "reason": "Invalid execution plan format",
                "message": "execution-plan.json must be either an array or an object with 'tasks' key.",
            },
        }

    if not tasks:
        return {
            "ok": False,
            "error": "No tasks in execution plan",
            "next_action": {
                "type": "halt",
                "reason": "Empty execution plan",
                "message": "execution-plan.json contains no tasks. Regenerate with valid decomposition.",
            },
        }

    log.emit("phase_started", phase=2, description="Routing")

    # ── Phase 2: Route tasks ──────────────────────────────────────────────
    # Write tasks to temp file for route-tasks.py
    tasks_file = run_dir / "tasks-for-routing.json"
    with open(tasks_file, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)

    route_result = run_script(
        "route-tasks.py",
        ["--plan", str(tasks_file), "--format", "json"],
        project_root=project_root,
        timeout=60,
    )

    if not route_result["ok"]:
        log.emit("phase_failed", phase=2, error=route_result.get("error", ""))
        return {
            "ok": False,
            "error": f"Phase 2 (routing) failed: {route_result.get('error', '')}",
            "next_action": {
                "type": "halt",
                "reason": "Routing failed",
                "message": f"Phase 2 routing failed: {route_result.get('error', '')}",
            },
        }

    routed = route_result["data"]
    routed_tasks = routed.get("routed_tasks", [])
    redirected = routed.get("redirected_tasks", [])

    log.emit("phase_completed", phase=2, routed=len(routed_tasks), redirected=len(redirected))

    if not routed_tasks:
        return {
            "ok": False,
            "error": "No tasks routable — all redirected or unroutable",
            "next_action": {
                "type": "halt",
                "reason": "All tasks redirected",
                "message": f"All {len(redirected)} tasks were redirected. Check routing rules and retry.",
                "details": {"redirected_tasks": redirected},
            },
        }

    # ── Phase 3: Wave optimization ────────────────────────────────────────
    log.emit("phase_started", phase=3, description="Wave optimization")

    # Normalize field names for wave-optimizer (expects "id" and "depends_on")
    optimizer_tasks = []
    for t in routed_tasks:
        ot = dict(t)
        # wave-optimizer uses "id", routing uses "task_id"
        if "task_id" in ot and "id" not in ot:
            ot["id"] = ot["task_id"]
        # wave-optimizer uses "depends_on", execution-plan uses "dependencies"
        if "dependencies" in ot and "depends_on" not in ot:
            ot["depends_on"] = ot["dependencies"]
        optimizer_tasks.append(ot)

    routed_file = run_dir / "routed-tasks.json"
    with open(routed_file, "w", encoding="utf-8") as f:
        json.dump({"tasks": optimizer_tasks}, f, indent=2, ensure_ascii=False)

    # First check for cycles
    cycle_result = run_script(
        "wave-optimizer.py",
        [str(routed_file), "--check-cycles-json"],
        project_root=project_root,
    )

    if cycle_result["ok"]:
        cycle_data = cycle_result["data"]
        if cycle_data.get("has_cycles", False):
            log.emit("phase_failed", phase=3, error="Dependency cycle detected",
                      cycles=cycle_data.get("cycles", []))
            return {
                "ok": False,
                "error": f"Dependency cycle detected: {cycle_data.get('cycles', [])}",
                "next_action": {
                    "type": "halt",
                    "reason": "Dependency cycle",
                    "message": f"Circular dependency detected in task graph: {cycle_data.get('cycles', [])}. Fix dependencies and retry.",
                    "details": {"cycles": cycle_data.get("cycles", [])},
                },
            }

    # Main optimization
    optimize_result = run_script(
        "wave-optimizer.py",
        [str(routed_file), "--max-parallel", str(max_parallel)],
        project_root=project_root,
    )

    if not optimize_result["ok"]:
        log.emit("phase_failed", phase=3, error=optimize_result.get("error", ""))
        return {
            "ok": False,
            "error": f"Phase 3 (optimization) failed: {optimize_result.get('error', '')}",
            "next_action": {
                "type": "halt",
                "reason": "Wave optimization failed",
                "message": f"Phase 3 optimization failed: {optimize_result.get('error', '')}",
            },
        }

    optimized = optimize_result["data"]
    waves = optimized.get("waves", [])
    total_waves = optimized.get("total_waves", len(waves))

    log.emit("phase_completed", phase=3, total_waves=total_waves,
             critical_path=optimized.get("critical_path_length", 0))

    # ── Register tasks and waves in state ─────────────────────────────────
    # Build task lookup from routed data
    task_lookup = {t.get("task_id", t.get("id", f"T{i:03d}")): t for i, t in enumerate(routed_tasks)}

    state.total_waves = total_waves
    state.status = "planning"

    for wave_info in waves:
        wnum = wave_info["wave_num"]
        wave_task_ids = wave_info.get("task_ids", [])

        state.waves[str(wnum)] = {
            "wave_num": wnum,
            "status": "pending",
            "task_ids": wave_task_ids,
            "started_at": None,
            "completed_at": None,
            "prediction": None,
            "cost_usd": 0.0,
        }

        for tid in wave_task_ids:
            t = task_lookup.get(tid, {})
            state.tasks[tid] = {
                "task_id": tid,
                "description": t.get("description", t.get("name", "")),
                "agent": t.get("agent", ""),
                "model": t.get("model", "haiku"),
                "enrichment": t.get("enrichment", "STANDARD"),
                "executor_type": t.get("executor_type", "Agent"),
                "status": "pending",
                "wave": wnum,
                "attempts": 0,
                "max_attempts": 3,
                "output_path": t.get("output_path", ""),
                "cost_usd": 0.0,
                "tokens_in": 0,
                "tokens_out": 0,
                "timeout": t.get("timeout", 120),
                "error": None,
                "started_at": None,
                "completed_at": None,
                "veto_results": {},
                "prediction": None,
            }

    # Collect unique domains
    state.domains_used = list(set(
        t.get("domain", _extract_domain(t.get("agent", "")))
        for t in routed_tasks
        if t.get("domain") or t.get("agent")
    ))

    manager.save(state)

    # ── Phase 4 + 4.5: Enrichment + Gate ──────────────────────────────────
    # These are now deferred to wave-executor.py prepare (per-wave, not upfront)
    # This ensures resume works correctly — only enrich what's about to execute.
    log.emit("phase_completed", phase="4+4.5",
             note="Deferred to wave-executor.py prepare (per-wave enrichment)")

    # ── Save routing artifacts ────────────────────────────────────────────
    routing_summary = {
        "routed_tasks": len(routed_tasks),
        "redirected_tasks": redirected,
        "total_waves": total_waves,
        "critical_path": optimized.get("critical_path", []),
        "critical_path_length": optimized.get("critical_path_length", 0),
        "optimization_ratio": optimized.get("optimization_ratio", ""),
        "domains_used": state.domains_used,
        "estimated_cost": routed.get("summary", {}).get("estimated_cost_usd", 0),
        "model_mix": routed.get("summary", {}).get("models", {}),
    }

    with open(run_dir / "routing-summary.json", "w", encoding="utf-8") as f:
        json.dump(routing_summary, f, indent=2, ensure_ascii=False)

    return {
        "ok": True,
        "waves": total_waves,
        "tasks": len(routed_tasks),
        "redirected": len(redirected),
        "routing_summary": routing_summary,
    }


# ═══════════════════════════════════════════════════════════════════════════════
# COMMANDS
# ═══════════════════════════════════════════════════════════════════════════════


def cmd_plan(input_path: str, project_root: str, force: bool = False, max_parallel: int = MAX_PARALLEL_DEFAULT) -> dict:
    """Plan phases 0-4.5. Does NOT execute.

    Flow:
        1. Validate preconditions (all scripts exist)
        2. Phase 0: Sufficiency gate
        3. Create run
        4. Phase 1: Write decomposition_request.json (needs LLM)
        5. If execution-plan.json already exists, continue to Phases 2-4.5

    Returns:
        JSON summary with run_id, phases completed, next steps
    """
    # Preconditions
    pre = _validate_preconditions(project_root)
    if not pre["ok"]:
        if RICH_AVAILABLE:
            print_error(f"Precondition failed: {pre.get('error', 'unknown')}")
        return pre  # Already includes next_action from _validate_preconditions

    # Phase 0: Sufficiency
    p0 = _phase0_sufficiency(input_path, project_root, force)
    if not p0["ok"]:
        return p0

    # Create run
    manager = DispatchStateManager(project_root)
    state = manager.create_run(
        description=p0["description"],
        input_type=p0["input_type"],
        input_path=p0["input_path"],
    )

    run_dir = manager._run_dir(state.run_id)
    log = EventLog(str(run_dir))
    log.emit("run_started", run_id=state.run_id, input_path=input_path,
             input_type=p0["input_type"])

    # Phase 1: Decomposition request
    p1 = _phase1_decomposition_request(state, run_dir, input_path, project_root)

    # Check if execution-plan.json already exists (pre-decomposed input)
    plan_exists = (run_dir / "execution-plan.json").exists()

    if plan_exists:
        # Phases 2-4.5
        p2 = _phases2_to_4_5(state, manager, log, run_dir, max_parallel, project_root)
        if not p2["ok"]:
            return {**p2, "run_id": state.run_id}

        state.status = "planned"
        manager.save(state)

        # Rich plan summary (if available)
        if RICH_AVAILABLE:
            rs = p2.get("routing_summary", {})
            task_list = [{"id": tid} for tid in state.tasks]
            wave_list = [state.waves[str(w)].get("task_ids", []) for w in range(1, p2["waves"] + 1)]
            models = {tid: state.tasks[tid].get("model", "haiku") for tid in state.tasks}
            print_plan_summary(
                description=state.description,
                tasks=task_list,
                waves=wave_list,
                models=models,
                cost_estimate=rs.get("estimated_cost", 0),
            )

        return {
            "ok": True,
            "run_id": state.run_id,
            "phases_completed": "0-4.5",
            "waves": p2["waves"],
            "tasks": p2["tasks"],
            "redirected": p2.get("redirected", 0),
            "routing_summary": p2.get("routing_summary", {}),
            "next_step": f"Execute: python dispatch-orchestrator.py execute --run-id {state.run_id}",
            "next_action": {
                "type": "call_script",
                "command": f"python squads/dispatch/scripts/dispatch-orchestrator.py execute --run-id {state.run_id} --root {project_root}",
                "parse_result": True,
                "description": "Execute wave preparation",
            },
        }
    else:
        # Phase 1 requires LLM — return instructions
        state.status = "awaiting_decomposition"
        manager.save(state)

        decomposition_request_path = p1.get("decomposition_request_path", "")

        return {
            "ok": True,
            "run_id": state.run_id,
            "phases_completed": "0-1",
            "awaiting_decomposition": True,
            "decomposition_request": decomposition_request_path,
            "next_step": p1.get("instruction", "Run LLM decomposition, then call execute"),
            "next_action": {
                "type": "create_subagent",
                "model": "sonnet",
                "prompt_instruction": f"Read {decomposition_request_path} and follow instructions to decompose the input into tasks. Save output to the specified output_path.",
                "save_result_to": str(run_dir / "execution-plan.json"),
                "then": {
                    "type": "call_script",
                    "command": f"python squads/dispatch/scripts/dispatch-orchestrator.py execute --run-id {state.run_id} --root {project_root}",
                    "parse_result": True,
                },
            },
        }


def cmd_execute(run_id: str, project_root: str, wave_start: int = None) -> dict:
    """Execute phases 5-6: wave preparation + verification + report.

    If plan hasn't been run (no routing-summary.json), attempts phases 2-4.5 first.

    Returns:
        JSON summary with wave results and report path
    """
    manager = DispatchStateManager(project_root)
    state = manager.load(run_id)

    if state is None:
        return {
            "ok": False,
            "error": f"Run {run_id} not found",
            "next_action": {
                "type": "halt",
                "reason": "Run not found",
                "message": f"Run ID {run_id} does not exist. Verify run_id or create new run with 'plan' command.",
            },
        }

    run_dir = manager._run_dir(run_id)
    log = EventLog(str(run_dir))

    # If routing hasn't been done yet (or state has no waves), do it now
    needs_routing = (
        not (run_dir / "routing-summary.json").exists()
        or not state.waves
        or state.total_waves == 0
    )

    if needs_routing:
        if not (run_dir / "execution-plan.json").exists():
            return {
                "ok": False,
                "error": "execution-plan.json not found. Run Phase 1 (LLM decomposition) first.",
                "run_id": run_id,
                "next_action": {
                    "type": "halt",
                    "reason": "Missing execution plan",
                    "message": "execution-plan.json not found. Run Phase 1 decomposition first.",
                },
            }

        p2 = _phases2_to_4_5(state, manager, log, run_dir, MAX_PARALLEL_DEFAULT, project_root)
        if not p2["ok"]:
            return {**p2, "run_id": run_id}

    # Determine wave range
    total_waves = state.total_waves or len(state.waves)
    start = wave_start if wave_start is not None else 1

    # Find first incomplete wave for resume
    if wave_start is None:
        for w in range(1, total_waves + 1):
            wave = state.waves.get(str(w), {})
            if wave.get("status") not in ("complete", "failed"):
                start = w
                break

    state.status = "executing"
    manager.save(state)

    wave_results = []

    for w in range(start, total_waves + 1):
        wave = state.waves.get(str(w), {})
        if wave.get("status") in ("complete",):
            continue  # Skip completed waves (resume support)

        # Phase 5: Prepare wave
        prep_result = run_script(
            "wave-executor.py",
            ["prepare", "--run-id", run_id, "--wave", str(w), "--root", project_root],
            project_root=project_root,
            timeout=300,
        )

        if not prep_result["ok"]:
            wave_results.append({"wave": w, "status": "prepare_failed", "error": prep_result.get("error", "")})
            log.emit("wave_failed", wave=w, phase="prepare", error=prep_result.get("error", ""))
            continue

        prep_data = prep_result["data"]

        # Check for all-vetoed
        if not prep_data.get("ok", False):
            wave_results.append({"wave": w, "status": "vetoed", "vetoed": prep_data.get("vetoed", [])})
            continue

        # Rich progress notification (if available)
        if RICH_AVAILABLE:
            print_success(f"Wave {w} prepared: {prep_data.get('tasks_ready', 0)} tasks ready")
            if prep_data.get("vetoed"):
                print_warning(f"{len(prep_data['vetoed'])} tasks vetoed in wave {w}")

        wave_results.append({
            "wave": w,
            "status": "prepared",
            "manifest_path": prep_data.get("manifest_path", ""),
            "tasks_ready": prep_data.get("tasks_ready", 0),
            "tasks_skipped": prep_data.get("tasks_skipped", 0),
            "vetoed": prep_data.get("vetoed", []),
            "awaiting_launch": True,
            "instruction": (
                f"Read launch-manifest.json at {prep_data.get('manifest_path', '')}. "
                f"Create Task/Bash tool calls for each task. "
                f"After completion, run: wave-executor.py record --run-id {run_id} --wave {w} --results <path>"
            ),
        })

        # HALT here — the LLM must launch subagents, then call record + verify
        # We return the manifest for the dispatch-chief to act on
        break  # Process one wave at a time (LLM must launch between waves)

    # Build next_action based on wave results
    next_action = None
    if wave_results:
        last_wave = wave_results[-1]
        if last_wave.get("status") == "prepared":
            manifest_path = last_wave.get("manifest_path", "")
            next_action = {
                "type": "create_parallel_subagents",
                "instruction": f"Read launch-manifest.json at {manifest_path}. Create parallel subagents for each task.",
                "manifest_path": manifest_path,
                "then": {
                    "type": "call_script",
                    "command": f"python squads/dispatch/scripts/wave-executor.py record --run-id {run_id} --wave {last_wave['wave']} --results <path>",
                    "description": "Record wave results after subagent completion",
                },
            }
        elif last_wave.get("status") == "vetoed":
            next_action = {
                "type": "report_to_user",
                "message": f"Wave {last_wave['wave']} fully vetoed. {len(last_wave.get('vetoed', []))} tasks failed validation.",
                "options": ["Inspect vetoed tasks", "Skip wave", "Abort dispatch", "Other"],
            }
        elif last_wave.get("status") in ("prepare_failed",):
            next_action = {
                "type": "halt",
                "reason": f"Wave {last_wave['wave']} preparation failed",
                "message": last_wave.get("error", "Unknown error"),
            }

    return {
        "ok": True,
        "run_id": run_id,
        "wave_results": wave_results,
        "total_waves": total_waves,
        "current_wave": start,
        "next_action": next_action,
    }


def cmd_full(input_path: str, project_root: str, max_parallel: int = MAX_PARALLEL_DEFAULT) -> dict:
    """Full pipeline: plan + execute prep.

    Returns plan result. Execute step must follow separately (needs LLM for decomposition).
    """
    return cmd_plan(input_path, project_root, max_parallel=max_parallel)


def cmd_resume(run_id: str = None, project_root: str = ".") -> dict:
    """Resume an interrupted run.

    If no run_id provided, finds the most recent resumable run.

    Returns:
        Same format as cmd_execute
    """
    manager = DispatchStateManager(project_root)

    if run_id is None:
        runs = manager.list_runs()
        resumable = [
            r for r in runs
            if r["status"] not in ("complete", "aborted")
        ]
        if not resumable:
            return {
                "ok": False,
                "error": "No resumable runs found",
                "next_action": {
                    "type": "halt",
                    "reason": "No resumable runs",
                    "message": "No incomplete dispatch runs found. Start new run with 'plan' command.",
                },
            }
        run_id = resumable[0]["run_id"]

    state = manager.load(run_id)
    if state is None:
        return {
            "ok": False,
            "error": f"Run {run_id} not found",
            "next_action": {
                "type": "halt",
                "reason": "Run not found",
                "message": f"Run {run_id} does not exist.",
            },
        }

    if state.status in ("complete", "aborted"):
        return {
            "ok": False,
            "error": f"Run {run_id} is {state.status} — cannot resume",
            "next_action": {
                "type": "halt",
                "reason": f"Run {state.status}",
                "message": f"Run {run_id} is {state.status} and cannot be resumed.",
            },
        }

    return cmd_execute(run_id, project_root)


# ═══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════════════════════


def _extract_domain(agent_path: str) -> str:
    """Extract domain from slash command path."""
    if not agent_path:
        return "general"
    parts = agent_path.strip("/").split(":")
    return parts[0] if parts else "general"


# ═══════════════════════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════════════════════


def main():
    parser = argparse.ArgumentParser(description="Dispatch Pipeline Orchestrator")
    sub = parser.add_subparsers(dest="command", required=True)

    # plan
    p_plan = sub.add_parser("plan", help="Phases 0-4.5 (no execution)")
    p_plan.add_argument("--input", required=True, help="Story/PRD/free-text file path")
    p_plan.add_argument("--force", action="store_true", help="Override soft gates")
    p_plan.add_argument("--max-parallel", type=int, default=MAX_PARALLEL_DEFAULT, help="Max parallel tasks per wave")
    p_plan.add_argument("--root", default=".", help="Project root")

    # execute
    p_exec = sub.add_parser("execute", help="Phases 5-6 (requires prior plan)")
    p_exec.add_argument("--run-id", required=True, help="Dispatch run ID")
    p_exec.add_argument("--wave", type=int, default=None, help="Start from specific wave")
    p_exec.add_argument("--root", default=".", help="Project root")

    # full
    p_full = sub.add_parser("full", help="Full pipeline (plan + execute prep)")
    p_full.add_argument("--input", required=True, help="Story/PRD/free-text file path")
    p_full.add_argument("--max-parallel", type=int, default=MAX_PARALLEL_DEFAULT, help="Max parallel tasks per wave")
    p_full.add_argument("--root", default=".", help="Project root")

    # resume
    p_resume = sub.add_parser("resume", help="Resume interrupted run")
    p_resume.add_argument("--run-id", default=None, help="Run ID (auto-detect if omitted)")
    p_resume.add_argument("--root", default=".", help="Project root")

    args = parser.parse_args()

    if args.command == "plan":
        result = cmd_plan(args.input, args.root, args.force, args.max_parallel)
    elif args.command == "execute":
        result = cmd_execute(args.run_id, args.root, args.wave)
    elif args.command == "full":
        result = cmd_full(args.input, args.root, args.max_parallel)
    elif args.command == "resume":
        result = cmd_resume(args.run_id, args.root)
    else:
        result = {"ok": False, "error": f"Unknown command: {args.command}"}

    print(json.dumps(result, indent=2))
    sys.exit(0 if result.get("ok", False) else 1)


if __name__ == "__main__":
    main()
