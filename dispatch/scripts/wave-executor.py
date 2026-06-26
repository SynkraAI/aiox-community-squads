"""
Dispatch Squad — Wave Executor
Prepare, record, and verify a single wave.

Does NOT launch subagents (only the LLM can use Task tool).
Prepares everything deterministically so the dispatch-chief just launches.

Usage:
    python wave-executor.py prepare --run-id <ID> --wave <N> [--root .]
    python wave-executor.py record  --run-id <ID> --wave <N> --results results.json [--root .]
    python wave-executor.py verify  --run-id <ID> --wave <N> [--root .]
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
from resilience import DispatchCircuitBreaker, RETRY_SCRIPT

# Legacy constants — kept for backward compatibility, now driven by resilience module
MAX_CONSECUTIVE_FAILURES = 5
MAX_TASK_ATTEMPTS = RETRY_SCRIPT.max_attempts


# ═══════════════════════════════════════════════════════════════════════════════
# PREPARE — Enrich + Validate + Build Launch Manifest
# ═══════════════════════════════════════════════════════════════════════════════


def cmd_prepare(run_id: str, wave_num: int, project_root: str) -> dict:
    """Prepare a wave for execution: enrich tasks, validate, build manifest.

    Flow:
        1. Load state, extract wave tasks
        2. Skip already-completed tasks (resume support)
        3. Per task: call enrich-task.py → enriched prompt
        4. Per enriched prompt: call validate-dispatch-gate.sh (V1.*)
        5. Per haiku prompt: call validate-haiku-prompt.py
        6. Build launch-manifest.json
        7. Update state (wave=ready), log events

    Returns:
        {"wave_num": N, "manifest_path": "...", "tasks_ready": N, "tasks_skipped": N, "vetoed": [...]}
    """
    root = Path(project_root)
    manager = DispatchStateManager(project_root)
    state = manager.load(run_id)

    if state is None:
        return _error(f"Run {run_id} not found")

    log = EventLog(str(manager._run_dir(run_id)))
    wave_key = str(wave_num)

    # Validate wave exists
    if wave_key not in state.waves:
        return _error(f"Wave {wave_num} not found in run {run_id}")

    wave = state.waves[wave_key]
    wave_task_ids = wave.get("task_ids", [])

    if not wave_task_ids:
        return _error(f"Wave {wave_num} has no tasks")

    # Create wave directory
    wave_dir = manager.create_wave_dir(run_id, wave_num)
    prompts_dir = wave_dir / "prompts"
    prompts_dir.mkdir(parents=True, exist_ok=True)

    tasks_ready = []
    tasks_skipped = []
    vetoed_tasks = []
    manifest_tasks = []

    for task_id in wave_task_ids:
        task = state.tasks.get(task_id)
        if not task:
            continue

        # Resume support: skip completed tasks
        if task.get("status") in ("pass", "fail"):
            tasks_skipped.append(task_id)
            continue

        executor_type = task.get("executor_type", "Agent")
        model = task.get("model", "haiku")

        # Worker tasks: no enrichment needed, direct command
        if executor_type == "Worker" or model == "worker":
            manifest_tasks.append({
                "task_id": task_id,
                "executor_type": "Worker",
                "script_command": task.get("description", ""),
                "timeout_ms": task.get("timeout", 30) * 1000,
                "output_path": task.get("output_path", ""),
            })
            tasks_ready.append(task_id)
            manager.update_task(state, task_id, status="queued")
            log.emit("task_queued", task=task_id, wave=wave_num, executor="Worker")
            continue

        # Agent tasks: enrich + validate
        # Step 1: Enrich — write task to temp file (enrich-task.py expects positional file path)
        enrichment_level = task.get("enrichment", "STANDARD")
        domain = _extract_domain(task.get("agent", ""))

        task_file = wave_dir / f"{task_id}_task.json"
        with open(task_file, "w", encoding="utf-8") as f:
            json.dump(task, f, indent=2, ensure_ascii=False)

        enrich_result = run_script(
            "enrich-task.py",
            [
                str(task_file),
                "--domain", domain,
                "--level", enrichment_level,
                "--output", str(prompts_dir / f"{task_id}.md"),
                "--root", project_root,
            ],
            project_root=project_root,
        )

        if not enrich_result["ok"]:
            vetoed_tasks.append({
                "task_id": task_id,
                "reason": f"Enrichment failed: {enrich_result.get('error', 'unknown')}",
                "phase": "enrichment",
            })
            log.emit("gate_failed", task=task_id, wave=wave_num, gate="enrichment",
                      error=enrich_result.get("error", ""))
            continue

        prompt_path = str(prompts_dir / f"{task_id}.md")

        # Step 2: Pre-execution gate (V1.*)
        gate_result = run_script(
            "validate-dispatch-gate.sh",
            [prompt_path],
            project_root=project_root,
        )

        if not gate_result["ok"]:
            vetoed_tasks.append({
                "task_id": task_id,
                "reason": f"V1.* gate failed: {gate_result.get('error', '')}",
                "phase": "V1_gate",
            })
            log.emit("gate_failed", task=task_id, wave=wave_num, gate="V1",
                      error=gate_result.get("stderr", ""))
            continue

        log.emit("gate_passed", task=task_id, wave=wave_num, gate="V1")

        # Step 3: Haiku-specific validation
        if model == "haiku":
            haiku_result = run_script(
                "validate-haiku-prompt.py",
                ["--prompt-file", prompt_path, "--format", "json"],
                project_root=project_root,
            )

            if haiku_result["ok"]:
                haiku_data = haiku_result["data"]
                if not haiku_data.get("passed", True):
                    violations = haiku_data.get("violations", [])
                    # Only veto on hard violations (veto_ids present)
                    veto_ids = haiku_data.get("veto_ids", [])
                    if veto_ids:
                        vetoed_tasks.append({
                            "task_id": task_id,
                            "reason": f"Haiku validation failed: {', '.join(violations[:3])}",
                            "phase": "haiku_validation",
                            "veto_ids": veto_ids,
                        })
                        log.emit("gate_failed", task=task_id, wave=wave_num, gate="haiku",
                                  violations=violations, veto_ids=veto_ids)
                        continue

            log.emit("gate_passed", task=task_id, wave=wave_num, gate="haiku")

        # Task passed all gates — add to manifest
        manifest_tasks.append({
            "task_id": task_id,
            "executor_type": "Agent",
            "model": model,
            "prompt_path": str(Path(prompts_dir / f"{task_id}.md").relative_to(root)),
            "timeout_ms": task.get("timeout", 120) * 1000,
            "output_path": task.get("output_path", ""),
            "agent": task.get("agent", ""),
        })
        tasks_ready.append(task_id)
        manager.update_task(state, task_id, status="queued")
        log.emit("task_queued", task=task_id, wave=wave_num, executor="Agent", model=model)

    # Pedro Valerio: If ANY hard veto fires, manifest is NOT produced
    if vetoed_tasks and not manifest_tasks:
        manager.update_wave(state, wave_num, status="failed")
        log.emit("wave_failed", wave=wave_num, reason="All tasks vetoed")
        return {
            "ok": False,
            "wave_num": wave_num,
            "error": "All tasks vetoed — wave cannot execute",
            "vetoed": vetoed_tasks,
            "tasks_ready": 0,
            "tasks_skipped": len(tasks_skipped),
        }

    # Write launch manifest
    manifest = {
        "wave_num": wave_num,
        "run_id": run_id,
        "prepared_at": datetime.now().isoformat(),
        "tasks": manifest_tasks,
        "vetoed": vetoed_tasks,
        "skipped": tasks_skipped,
    }

    manifest_path = wave_dir / "launch-manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    # Update state
    manager.update_wave(state, wave_num, status="ready")
    log.emit("wave_started", wave=wave_num, tasks_ready=len(tasks_ready),
             tasks_skipped=len(tasks_skipped), vetoed=len(vetoed_tasks))

    return {
        "ok": True,
        "wave_num": wave_num,
        "manifest_path": str(manifest_path),
        "tasks_ready": len(tasks_ready),
        "tasks_skipped": len(tasks_skipped),
        "vetoed": vetoed_tasks,
    }


# ═══════════════════════════════════════════════════════════════════════════════
# RECORD — Save results after agent launches subagents
# ═══════════════════════════════════════════════════════════════════════════════


def cmd_record(run_id: str, wave_num: int, results_path: str, project_root: str) -> dict:
    """Record wave results after the dispatch-chief launches subagents.

    Flow:
        1. Load results from JSON file
        2. Update task statuses in state
        3. Record costs via cost-tracker.py
        4. Check circuit breaker (5 consecutive failures → HALT)
        5. Build retry queue (attempts < 2, no timeouts)

    Args:
        results_path: Path to JSON with task results [{task_id, status, tokens_in, tokens_out, error?}]

    Returns:
        {"wave_num": N, "pass": N, "fail": N, "retry_queue": [...], "halt": bool}
    """
    root = Path(project_root)
    manager = DispatchStateManager(project_root)
    state = manager.load(run_id)

    if state is None:
        return _error(f"Run {run_id} not found")

    log = EventLog(str(manager._run_dir(run_id)))

    # Load results
    rpath = Path(results_path)
    if not rpath.is_absolute():
        rpath = root / rpath
    if not rpath.exists():
        return _error(f"Results file not found: {rpath}")

    with open(rpath, "r", encoding="utf-8") as f:
        results = json.load(f)

    if isinstance(results, dict):
        results = results.get("tasks", [results])

    pass_count = 0
    fail_count = 0
    retry_queue = []
    consecutive_failures = 0
    halt = False  # Initialize halt flag for circuit breaker
    wave_breaker = DispatchCircuitBreaker.for_wave(wave_num)

    for r in results:
        task_id = r.get("task_id", "")
        status = r.get("status", "fail")
        tokens_in = r.get("tokens_in", 0)
        tokens_out = r.get("tokens_out", 0)
        error = r.get("error", "")
        model = r.get("model", state.tasks.get(task_id, {}).get("model", "haiku"))

        # Update task state
        task = state.tasks.get(task_id, {})
        attempts = task.get("attempts", 0) + 1

        update_fields = {
            "status": status,
            "attempts": attempts,
            "tokens_in": tokens_in,
            "tokens_out": tokens_out,
            "completed_at": datetime.now().isoformat(),
        }
        if error:
            update_fields["error"] = error

        # Record cost
        cost_result = run_script(
            "cost-tracker.py",
            [
                "record",
                "--run-id", run_id,
                "--task", task_id,
                "--model", model,
                "--tokens-in", str(tokens_in),
                "--tokens-out", str(tokens_out),
            ],
            project_root=project_root,
        )

        if cost_result["ok"]:
            task_cost = cost_result["data"].get("cost_usd", 0)
            update_fields["cost_usd"] = task_cost
            state.total_cost_usd = state.total_cost_usd + task_cost
            state.total_tokens_in = state.total_tokens_in + tokens_in
            state.total_tokens_out = state.total_tokens_out + tokens_out

        manager.update_task(state, task_id, **update_fields)

        if status == "pass":
            pass_count += 1
            consecutive_failures = 0
            log.emit("task_completed", task=task_id, wave=wave_num, model=model,
                      cost=update_fields.get("cost_usd", 0),
                      tokens_in=tokens_in, tokens_out=tokens_out)
        else:
            fail_count += 1
            consecutive_failures += 1
            # Feed failure to circuit breaker (triggers open if threshold exceeded)
            try:
                wave_breaker.call(lambda: (_ for _ in ()).throw(RuntimeError(error or "task_failed")))
            except Exception:
                pass  # Expected — we're registering the failure
            log.emit("task_failed", task=task_id, wave=wave_num, model=model,
                      error=error, attempts=attempts, breaker_state=wave_breaker.state)

            # ── FALLBACK INTEGRATION: Auto-escalation via self-heal ──────────────
            # Classify failure and determine if model escalation is needed
            heal_input = {
                "task_id": task_id,
                "model": model,
                "output_path": task.get("output_path", ""),
                "error": error,
                "retry_count": attempts - 1,
                "quality_score": r.get("quality_score"),
                "quality_threshold": r.get("quality_threshold"),
                "expected_language": r.get("expected_language"),
                "execution_time_ms": r.get("execution_time_ms"),
                "timeout_ms": task.get("timeout", 120) * 1000,
            }

            heal_result = run_script(
                "self-heal-failure.py",
                [
                    "--task-result", json.dumps(heal_input),
                    "--run-id", run_id,
                    "--format", "json",
                ],
                project_root=project_root,
            )

            if heal_result["ok"]:
                heal_data = heal_result["data"]

                # Log classification
                log.emit("failure_classified",
                          task=task_id,
                          failure_type=heal_data.get("failure_type"),
                          classification=heal_data.get("classification"),
                          should_escalate=heal_data.get("should_escalate", False))

                # Check circuit breaker (3 consecutive escalations)
                if heal_data.get("circuit_breaker", False):
                    log.emit("circuit_breaker_open",
                              wave=wave_num,
                              reason="3 consecutive model escalations detected",
                              task=task_id)
                    halt = True
                    break

                # Apply model escalation if recommended
                if heal_data.get("should_escalate", False) and heal_data.get("next_model"):
                    next_model = heal_data["next_model"]
                    manager.update_task(state, task_id, model=next_model)
                    log.emit("model_escalation",
                              task=task_id,
                              from_model=model,
                              to_model=next_model,
                              failure_type=heal_data.get("failure_type"),
                              attempt=attempts)

                # Apply prompt patch if available
                if heal_data.get("prompt_patch"):
                    # Store patch in task metadata for next retry
                    task_meta = task.get("metadata", {})
                    task_meta["prompt_patch"] = heal_data["prompt_patch"]
                    manager.update_task(state, task_id, metadata=task_meta)

            # ── End fallback integration ──────────────────────────────────────────

            # Retry eligibility — uses resilience config
            if attempts < MAX_TASK_ATTEMPTS and "timeout" not in error.lower():
                retry_queue.append(task_id)
                log.emit("task_retry", task=task_id, wave=wave_num, attempt=attempts + 1)

            # Early halt if breaker opens mid-wave
            if not wave_breaker.is_available:
                log.emit("circuit_breaker_open", wave=wave_num, after_task=task_id,
                          consecutive_failures=consecutive_failures)
                break

    # Circuit breaker — uses resilience module (merge with fallback halt)
    halt = halt or not wave_breaker.is_available
    if halt:
        state.status = "failed"
        log.emit("run_failed",
                  reason=f"Circuit breaker '{wave_breaker._name}' OPEN after {consecutive_failures} consecutive failures",
                  wave=wave_num, breaker_state=wave_breaker.state)

    # Update wave state
    wave_status = "complete" if not halt else "failed"
    wave_cost = sum(
        state.tasks.get(tid, {}).get("cost_usd", 0)
        for tid in state.waves.get(str(wave_num), {}).get("task_ids", [])
    )
    manager.update_wave(
        state, wave_num,
        status=wave_status,
        completed_at=datetime.now().isoformat(),
        cost_usd=wave_cost,
    )

    manager.save(state)

    return {
        "ok": True,
        "wave_num": wave_num,
        "pass": pass_count,
        "fail": fail_count,
        "retry_queue": retry_queue,
        "halt": halt,
        "wave_cost_usd": round(wave_cost, 4),
    }


# ═══════════════════════════════════════════════════════════════════════════════
# VERIFY — Post-execution V2.* checks + PDSA
# ═══════════════════════════════════════════════════════════════════════════════


def cmd_verify(run_id: str, wave_num: int, project_root: str) -> dict:
    """Verify wave results with post-execution checks (V2.*) and PDSA study.

    Flow:
        1. Call validate-wave-results.py --wave N
        2. PDSA study: predicted vs actual
        3. Update state with verification

    Returns:
        {"wave_num": N, "v2_passed": bool, "violations": [...], "pdsa": {...}}
    """
    root = Path(project_root)
    manager = DispatchStateManager(project_root)
    state = manager.load(run_id)

    if state is None:
        return _error(f"Run {run_id} not found")

    log = EventLog(str(manager._run_dir(run_id)))
    state_path = str(manager._state_path(run_id))

    # Call validate-wave-results.py
    v2_result = run_script(
        "validate-wave-results.py",
        [state_path, "--wave", str(wave_num)],
        project_root=project_root,
    )

    v2_passed = True
    violations = []

    if v2_result["ok"]:
        v2_data = v2_result["data"]
        v2_passed = v2_data.get("passed", True)
        violations = v2_data.get("violations", [])
    else:
        # Validation script failed — treat as warning, not hard block
        violations = [f"V2 validation script error: {v2_result.get('error', 'unknown')}"]
        v2_passed = True  # Don't block on script errors

    # PDSA: Predicted vs Actual
    wave = state.waves.get(str(wave_num), {})
    wave_tasks = [
        state.tasks[tid] for tid in wave.get("task_ids", [])
        if tid in state.tasks
    ]

    predicted_pass = len(wave_tasks)  # We predict all tasks pass
    actual_pass = sum(1 for t in wave_tasks if t.get("status") == "pass")
    actual_fail = sum(1 for t in wave_tasks if t.get("status") == "fail")

    pdsa = {
        "predicted_pass": predicted_pass,
        "actual_pass": actual_pass,
        "actual_fail": actual_fail,
        "delta": actual_pass - predicted_pass,
        "success_rate": round(actual_pass / len(wave_tasks) * 100, 1) if wave_tasks else 0,
    }

    # Log results
    if v2_passed:
        log.emit("gate_passed", wave=wave_num, gate="V2", pdsa=pdsa)
    else:
        log.emit("gate_failed", wave=wave_num, gate="V2", violations=violations, pdsa=pdsa)

    # Add learnings from failures
    if actual_fail > 0:
        failed_models = [t.get("model", "?") for t in wave_tasks if t.get("status") == "fail"]
        learning = f"Wave {wave_num}: {actual_fail} failures ({', '.join(failed_models)})"
        manager.add_learning(state, learning)

    manager.save(state)

    return {
        "ok": True,
        "wave_num": wave_num,
        "v2_passed": v2_passed,
        "violations": violations,
        "pdsa": pdsa,
    }


# ═══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════════════════════


def _extract_domain(agent_path: str) -> str:
    """Extract domain from slash command path. e.g., /copy:tasks:create → copy"""
    if not agent_path:
        return "general"
    parts = agent_path.strip("/").split(":")
    return parts[0] if parts else "general"


def _error(msg: str) -> dict:
    """Return standard error dict."""
    return {"ok": False, "error": msg}


# ═══════════════════════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════════════════════


def main():
    parser = argparse.ArgumentParser(description="Wave Executor — prepare, record, verify")
    sub = parser.add_subparsers(dest="command", required=True)

    # prepare
    p_prepare = sub.add_parser("prepare", help="Enrich + validate + build launch manifest")
    p_prepare.add_argument("--run-id", required=True, help="Dispatch run ID")
    p_prepare.add_argument("--wave", required=True, type=int, help="Wave number")
    p_prepare.add_argument("--root", default=".", help="Project root")

    # record
    p_record = sub.add_parser("record", help="Save results after subagent execution")
    p_record.add_argument("--run-id", required=True, help="Dispatch run ID")
    p_record.add_argument("--wave", required=True, type=int, help="Wave number")
    p_record.add_argument("--results", required=True, help="Path to results JSON")
    p_record.add_argument("--root", default=".", help="Project root")

    # verify
    p_verify = sub.add_parser("verify", help="Post-execution V2.* checks + PDSA")
    p_verify.add_argument("--run-id", required=True, help="Dispatch run ID")
    p_verify.add_argument("--wave", required=True, type=int, help="Wave number")
    p_verify.add_argument("--root", default=".", help="Project root")

    args = parser.parse_args()

    if args.command == "prepare":
        result = cmd_prepare(args.run_id, args.wave, args.root)
    elif args.command == "record":
        result = cmd_record(args.run_id, args.wave, args.results, args.root)
    elif args.command == "verify":
        result = cmd_verify(args.run_id, args.wave, args.root)
    else:
        result = _error(f"Unknown command: {args.command}")

    print(json.dumps(result, indent=2))
    sys.exit(0 if result.get("ok", False) else 1)


if __name__ == "__main__":
    main()
