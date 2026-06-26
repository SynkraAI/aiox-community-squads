#!/usr/bin/env python3
"""
Route dispatch tasks — full deterministic routing pipeline (Worker).

Replaces 60% of task-router LLM work with deterministic logic.
Orchestrates: score-domain.py → select-model.py → assign-enrichment.py → assign-timeout.py

Usage:
  # Route tasks from execution plan
  python scripts/route-tasks.py --plan _temp/dispatch/runs/RUN_ID/execution-plan.yaml

  # Route single task
  python scripts/route-tasks.py --task '{"task_id": "T001", "name": "Create newsletter", "description": "Create weekly newsletter about AI"}'

  # Batch from JSON array
  python scripts/route-tasks.py --stdin < tasks.json

  # Table output
  python scripts/route-tasks.py --plan plan.yaml --format table

Pipeline (7 phases — all deterministic):
  Phase 1: Load routing data (domain-registry, model-selection-rules, enrichment-rules, timeout-rules)
  Phase 2: Domain detection via score-domain.py
  Phase 2.5: Multi-domain splitting (50% threshold)
  Phase 3: Agent selection (registry lookup)
  Phase 4: Model selection (Q1-Q4 decision tree)
  Phase 5: Enrichment assignment (MINIMAL/STANDARD/FULL)
  Phase 6: Timeout assignment
  Phase 7: Write updated plan

Source: squads/dispatch/tasks/route-tasks.md
Version: 1.0.0
Date: 2026-02-10
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# ═══════════════════════════════════════════════════════════════════════════════
# PATHS
# ═══════════════════════════════════════════════════════════════════════════════

SCRIPTS_DIR = Path("squads/dispatch/scripts")
DATA_DIR = Path("squads/dispatch/data")

DOMAIN_REGISTRY_PATH = DATA_DIR / "domain-registry.yaml"
MODEL_RULES_PATH = DATA_DIR / "model-selection-rules.yaml"
ENRICHMENT_RULES_PATH = DATA_DIR / "enrichment-rules.yaml"
TIMEOUT_RULES_PATH = DATA_DIR / "timeout-rules.yaml"
COMMAND_REGISTRY_PATH = DATA_DIR / "command-registry.yaml"
MANUAL_OVERRIDES_PATH = DATA_DIR / "manual-overrides.yaml"

SCORE_DOMAIN_SCRIPT = SCRIPTS_DIR / "score-domain.py"

# ═══════════════════════════════════════════════════════════════════════════════
# REDIRECT DOMAINS (should NOT be dispatched)
# ═══════════════════════════════════════════════════════════════════════════════

REDIRECT_DOMAINS = {"architect", "pm", "po"}

# MCP domains that require foreground execution
MCP_DOMAINS = {"ac_automation", "bh_automation", "clickup"}

# ═══════════════════════════════════════════════════════════════════════════════
# DOMAIN REGISTRY LOADER
# ═══════════════════════════════════════════════════════════════════════════════

_DOMAIN_REGISTRY_CACHE = None


def load_domain_registry() -> dict:
    """Load domain registry with caching."""
    global _DOMAIN_REGISTRY_CACHE
    if _DOMAIN_REGISTRY_CACHE is not None:
        return _DOMAIN_REGISTRY_CACHE

    if not DOMAIN_REGISTRY_PATH.exists():
        print(f"Warning: {DOMAIN_REGISTRY_PATH} not found", file=sys.stderr)
        _DOMAIN_REGISTRY_CACHE = {}
        return _DOMAIN_REGISTRY_CACHE

    try:
        import yaml
        with open(DOMAIN_REGISTRY_PATH, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        _DOMAIN_REGISTRY_CACHE = data.get("domains", {})
    except ImportError:
        print("Warning: PyYAML not installed, domain lookup limited", file=sys.stderr)
        _DOMAIN_REGISTRY_CACHE = {}
    except Exception as e:
        print(f"Warning: Error loading domain registry: {e}", file=sys.stderr)
        _DOMAIN_REGISTRY_CACHE = {}

    return _DOMAIN_REGISTRY_CACHE


def load_command_registry() -> dict:
    """Load command registry for slash command resolution."""
    if not COMMAND_REGISTRY_PATH.exists():
        return {}
    try:
        import yaml
        with open(COMMAND_REGISTRY_PATH, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return data
    except Exception:
        return {}


# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 2: DOMAIN DETECTION
# ═══════════════════════════════════════════════════════════════════════════════

def detect_domain(task: dict) -> dict:
    """Detect domain for a task using score-domain.py.

    Returns dict with: domain, score, all_scores, is_multi_domain
    """
    text = f"{task.get('name', '')} {task.get('description', '')}"

    # Try score-domain.py first (subprocess)
    if SCORE_DOMAIN_SCRIPT.exists():
        try:
            result = subprocess.run(
                [sys.executable, str(SCORE_DOMAIN_SCRIPT), "--task", text, "--format", "json"],
                capture_output=True, text=True, timeout=10,
                cwd=str(Path.cwd()),
            )
            if result.returncode == 0:
                data = json.loads(result.stdout)
                scores = data.get("domains", data.get("scores", []))
                if scores:
                    # Filter to threshold >= 3
                    valid = [s for s in scores if s.get("score", 0) >= 3]
                    if valid:
                        primary = valid[0]
                        return {
                            "domain": primary.get("domain", primary.get("name", "")),
                            "score": primary.get("score", 0),
                            "all_scores": valid,
                            "is_multi_domain": len(valid) > 1,
                        }
        except (subprocess.TimeoutExpired, json.JSONDecodeError, Exception) as e:
            print(f"Warning: score-domain.py failed: {e}, using fallback", file=sys.stderr)

    # Fallback: simple keyword matching against domain registry
    return _fallback_domain_detection(text)


def _fallback_domain_detection(text: str) -> dict:
    """Simple keyword matching when score-domain.py unavailable."""
    registry = load_domain_registry()
    text_lower = text.lower()
    tokens = set(text_lower.split())

    scores = []
    for domain_id, domain_data in registry.items():
        triggers = domain_data.get("triggers", {})
        primary = triggers.get("primary", [])
        secondary = triggers.get("secondary", [])
        w_primary = triggers.get("weight_primary", 3)
        w_secondary = triggers.get("weight_secondary", 1)

        score = 0
        for kw in primary:
            kw_lower = kw.lower()
            if " " in kw_lower:
                if kw_lower in text_lower:
                    score += w_primary
            elif kw_lower in tokens:
                score += w_primary

        for kw in secondary:
            kw_lower = kw.lower()
            if " " in kw_lower:
                if kw_lower in text_lower:
                    score += w_secondary
            elif kw_lower in tokens:
                score += w_secondary

        if score >= 3:
            scores.append({"domain": domain_id, "score": score})

    scores.sort(key=lambda x: x["score"], reverse=True)

    if scores:
        return {
            "domain": scores[0]["domain"],
            "score": scores[0]["score"],
            "all_scores": scores,
            "is_multi_domain": len(scores) > 1,
        }

    return {
        "domain": "unknown",
        "score": 0,
        "all_scores": [],
        "is_multi_domain": False,
    }


# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 2.5: MULTI-DOMAIN SPLITTING
# ═══════════════════════════════════════════════════════════════════════════════

def split_multi_domain(task: dict, domain_info: dict) -> list:
    """Split a multi-domain task into domain-specific sub-tasks.

    Only splits if secondary domain score >= 50% of primary.
    """
    if not domain_info.get("is_multi_domain", False):
        return [task]

    all_scores = domain_info.get("all_scores", [])
    if len(all_scores) < 2:
        return [task]

    primary_score = all_scores[0]["score"]
    threshold = primary_score * 0.5

    # Only split if secondary is significant
    significant = [s for s in all_scores if s["score"] >= threshold]
    if len(significant) < 2:
        return [task]

    # Create sub-tasks
    sub_tasks = []
    for i, domain_score in enumerate(significant):
        sub_task = dict(task)
        sub_task["task_id"] = f"{task.get('task_id', 'T000')}__{domain_score['domain']}"
        sub_task["name"] = f"{task.get('name', '')} [{domain_score['domain']}]"
        sub_task["domain"] = domain_score["domain"]
        sub_task["domain_score"] = domain_score["score"]
        sub_task["split_from"] = task.get("task_id", "T000")
        sub_task["split_index"] = i
        sub_tasks.append(sub_task)

    return sub_tasks


# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 3: AGENT SELECTION
# ═══════════════════════════════════════════════════════════════════════════════

def select_agent(task: dict) -> dict:
    """Select agent for a task based on domain registry.

    Returns dict with: agent, squad, slash_command, is_redirect, foreground_only
    """
    domain = task.get("domain", "unknown")
    registry = load_domain_registry()

    # Check redirect domains
    if domain in REDIRECT_DOMAINS:
        domain_data = registry.get(domain, {})
        agent = domain_data.get("agents", {}).get("primary", f"@{domain}")
        return {
            "agent": agent,
            "squad": None,
            "slash_command": None,
            "is_redirect": True,
            "redirect_reason": f"Domain '{domain}' should NOT be dispatched — redirect to {agent}",
            "foreground_only": False,
        }

    if domain not in registry:
        return {
            "agent": None,
            "squad": None,
            "slash_command": None,
            "is_redirect": False,
            "redirect_reason": None,
            "foreground_only": False,
            "warning": f"Domain '{domain}' not in registry — UNROUTABLE",
        }

    domain_data = registry[domain]
    agents = domain_data.get("agents", {})
    primary = agents.get("primary", "")
    squad = agents.get("squad")

    # Resolve slash command
    slash_command = primary if primary and primary.startswith("/") else None

    return {
        "agent": primary,
        "squad": squad,
        "slash_command": slash_command,
        "is_redirect": False,
        "redirect_reason": None,
        "foreground_only": domain in MCP_DOMAINS,
    }


# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 4-6: MODEL + ENRICHMENT + TIMEOUT (delegate to sub-scripts)
# ═══════════════════════════════════════════════════════════════════════════════

def select_model_inline(task: dict) -> dict:
    """Inline model selection using select-model.py logic (avoid subprocess overhead)."""
    # Import the classify function directly
    from select_model import classify_task
    return classify_task(task)


def assign_enrichment_inline(task: dict) -> dict:
    """Inline enrichment assignment using assign-enrichment.py logic."""
    from assign_enrichment import assign_enrichment
    return assign_enrichment(task)


def assign_timeout_inline(task: dict) -> dict:
    """Inline timeout assignment using assign-timeout.py logic."""
    from assign_timeout import assign_timeout
    return assign_timeout(task)


# Fallback: hardcoded logic if imports fail
def _select_model_fallback(task: dict) -> dict:
    """Fallback model selection without importing sub-script."""
    task_type = (task.get("type") or "").lower()
    has_template = task.get("has_template", False)
    description = (task.get("description") or "").lower()

    worker_types = {"move", "delete", "rename", "mkdir", "copy", "gitkeep", "index", "validate", "organize"}
    sonnet_types = {"evaluate", "audit", "analyze", "review", "diagnose", "assess", "decompose", "plan"}
    redirect_types = {"architecture", "strategy", "prd", "system_design"}

    if task_type in worker_types:
        return {"model": "worker", "executor_type": "Worker", "rationale": f"Q1: type={task_type}"}
    if task_type in redirect_types:
        return {"model": "redirect", "executor_type": "Human", "rationale": f"Q4: type={task_type} → REDIRECT"}
    if has_template:
        return {"model": "haiku", "executor_type": "Agent", "rationale": "Q2: has_template=true"}
    if task_type in sonnet_types:
        return {"model": "sonnet", "executor_type": "Agent", "rationale": f"Q3: type={task_type}"}
    return {"model": "haiku", "executor_type": "Agent", "rationale": "Default → haiku"}


def _assign_enrichment_fallback(task: dict) -> dict:
    """Fallback enrichment assignment."""
    model = (task.get("model") or "").lower()
    domain = (task.get("domain") or "").lower()
    task_type = (task.get("type") or "").lower()

    if model == "worker":
        return {"enrichment": "MINIMAL", "token_budget": 500, "kb_files": [], "rationale": "worker → MINIMAL"}
    minimal_types = {"move", "delete", "validate", "rename", "mkdir", "index", "gitkeep", "organize"}
    if task_type in minimal_types or domain == "organization":
        return {"enrichment": "MINIMAL", "token_budget": 500, "kb_files": [], "rationale": f"type/domain → MINIMAL"}
    if domain in {"copy", "squad_creator"}:
        return {"enrichment": "FULL", "token_budget": 3000, "kb_files": [], "rationale": f"domain={domain} → FULL"}
    return {"enrichment": "STANDARD", "token_budget": 1500, "kb_files": [], "rationale": "default → STANDARD"}


def _assign_timeout_fallback(task: dict) -> dict:
    """Fallback timeout assignment."""
    model = (task.get("model") or "haiku").lower()
    timeouts = {"worker": 30, "haiku": 120, "sonnet": 300, "opus": 600}
    turns = {"worker": 0, "haiku": 15, "sonnet": 20, "opus": 25}
    return {
        "timeout": timeouts.get(model, 120),
        "max_turns": turns.get(model, 15),
        "rationale": f"model={model}",
    }


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN ROUTING PIPELINE
# ═══════════════════════════════════════════════════════════════════════════════

def route_task(task: dict) -> dict:
    """Route a single task through the full pipeline.

    Returns task dict enriched with routing fields.
    """
    # Phase 2: Domain detection
    domain_info = detect_domain(task)
    task["domain"] = domain_info["domain"]
    task["domain_score"] = domain_info["score"]
    task["is_multi_domain"] = domain_info["is_multi_domain"]

    # Phase 3: Agent selection
    agent_info = select_agent(task)
    task["agent"] = agent_info["agent"]
    task["squad"] = agent_info["squad"]
    task["slash_command"] = agent_info["slash_command"]
    task["is_redirect"] = agent_info["is_redirect"]
    task["foreground_only"] = agent_info["foreground_only"]

    if agent_info.get("warning"):
        task["routing_warning"] = agent_info["warning"]
    if agent_info.get("redirect_reason"):
        task["redirect_reason"] = agent_info["redirect_reason"]

    # Skip model/enrichment/timeout for redirects
    if task["is_redirect"]:
        task["model"] = "redirect"
        task["executor_type"] = "Human"
        task["enrichment"] = "N/A"
        task["timeout"] = 0
        task["max_turns"] = 0
        return task

    # Phase 4: Model selection
    try:
        model_info = select_model_inline(task)
    except (ImportError, Exception):
        model_info = _select_model_fallback(task)
    task["model"] = model_info["model"]
    task["executor_type"] = model_info.get("executor_type", "Agent")
    task["model_rationale"] = model_info["rationale"]

    # Phase 5: Enrichment assignment
    try:
        enrichment_info = assign_enrichment_inline(task)
    except (ImportError, Exception):
        enrichment_info = _assign_enrichment_fallback(task)
    task["enrichment"] = enrichment_info["enrichment"]
    task["token_budget"] = enrichment_info["token_budget"]
    task["kb_files"] = enrichment_info.get("kb_files", [])

    # Phase 6: Timeout assignment
    try:
        timeout_info = assign_timeout_inline(task)
    except (ImportError, Exception):
        timeout_info = _assign_timeout_fallback(task)
    task["timeout"] = timeout_info["timeout"]
    task["max_turns"] = timeout_info["max_turns"]

    return task


def route_batch(tasks: list) -> dict:
    """Route a batch of tasks, handling multi-domain splits."""
    routed = []
    redirected = []
    unroutable = []
    splits = 0

    for task in tasks:
        # Phase 2: Domain detection
        domain_info = detect_domain(task)

        # Phase 2.5: Multi-domain splitting
        sub_tasks = split_multi_domain(task, domain_info)
        if len(sub_tasks) > 1:
            splits += 1

        for sub_task in sub_tasks:
            if "domain" not in sub_task:
                sub_task["domain"] = domain_info["domain"]

            result = route_task(sub_task)
            if result.get("is_redirect"):
                redirected.append(result)
            elif result.get("routing_warning"):
                unroutable.append(result)
            else:
                routed.append(result)

    # Build summary
    model_counts = {"worker": 0, "haiku": 0, "sonnet": 0}
    domain_counts = {}
    for t in routed:
        model = t.get("model", "haiku")
        model_counts[model] = model_counts.get(model, 0) + 1
        domain = t.get("domain", "unknown")
        domain_counts[domain] = domain_counts.get(domain, 0) + 1

    estimated_cost = round(
        model_counts.get("haiku", 0) * 0.007
        + model_counts.get("sonnet", 0) * 0.025,
        4,
    )

    return {
        "routed_tasks": routed,
        "redirected_tasks": redirected,
        "unroutable_tasks": unroutable,
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "pipeline_version": "1.0.0",
            "total_input": len(tasks),
            "total_routed": len(routed),
            "total_redirected": len(redirected),
            "total_unroutable": len(unroutable),
            "multi_domain_splits": splits,
        },
        "summary": {
            "models": model_counts,
            "domains": domain_counts,
            "estimated_cost_usd": estimated_cost,
            "foreground_tasks": sum(1 for t in routed if t.get("foreground_only")),
        },
    }


# ═══════════════════════════════════════════════════════════════════════════════
# OUTPUT FORMATTING
# ═══════════════════════════════════════════════════════════════════════════════

def format_table(result: dict) -> str:
    """Format routing result as human-readable table."""
    lines = []

    # Header
    lines.append("=" * 120)
    lines.append("DISPATCH ROUTING REPORT")
    lines.append(f"Generated: {result['metadata']['timestamp']}")
    lines.append("=" * 120)

    # Routed tasks
    lines.append("")
    lines.append(f"ROUTED TASKS ({len(result['routed_tasks'])})")
    lines.append("-" * 120)
    lines.append(
        f"{'ID':<10} {'Domain':<16} {'Agent':<30} {'Model':<8} "
        f"{'Enrich':<10} {'Timeout':<8} {'FG':<4}"
    )
    lines.append("-" * 120)
    for t in result["routed_tasks"]:
        agent = (t.get("agent") or "-")[:28]
        fg = "yes" if t.get("foreground_only") else ""
        lines.append(
            f"{t.get('task_id', '?'):<10} {t.get('domain', '?'):<16} {agent:<30} "
            f"{t.get('model', '?'):<8} {t.get('enrichment', '?'):<10} "
            f"{t.get('timeout', 0):<8} {fg:<4}"
        )

    # Redirected tasks
    if result["redirected_tasks"]:
        lines.append("")
        lines.append(f"REDIRECTED TASKS ({len(result['redirected_tasks'])}) — DO NOT DISPATCH")
        lines.append("-" * 80)
        for t in result["redirected_tasks"]:
            lines.append(f"  {t.get('task_id', '?')}: {t.get('redirect_reason', 'N/A')}")

    # Unroutable tasks
    if result["unroutable_tasks"]:
        lines.append("")
        lines.append(f"UNROUTABLE TASKS ({len(result['unroutable_tasks'])}) — NEED MANUAL ROUTING")
        lines.append("-" * 80)
        for t in result["unroutable_tasks"]:
            lines.append(f"  {t.get('task_id', '?')}: {t.get('routing_warning', 'N/A')}")

    # Summary
    lines.append("")
    lines.append("=" * 120)
    s = result["summary"]
    m = result["metadata"]
    lines.append(
        f"Total: {m['total_input']} → Routed: {m['total_routed']} | "
        f"Redirected: {m['total_redirected']} | Unroutable: {m['total_unroutable']} | "
        f"Splits: {m['multi_domain_splits']}"
    )
    lines.append(
        f"Models: Worker={s['models'].get('worker', 0)} | "
        f"Haiku={s['models'].get('haiku', 0)} | "
        f"Sonnet={s['models'].get('sonnet', 0)} | "
        f"Foreground: {s['foreground_tasks']} | "
        f"Est. cost: ${s['estimated_cost_usd']}"
    )
    lines.append("=" * 120)

    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="Route dispatch tasks — full deterministic pipeline (Worker)"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--task", type=str, help="Single task as JSON string")
    group.add_argument("--plan", type=str, help="Execution plan file (YAML/JSON)")
    group.add_argument("--stdin", action="store_true", help="Read tasks from stdin (JSON)")

    parser.add_argument(
        "--format", choices=["json", "table"], default="json",
        help="Output format (default: json)"
    )
    parser.add_argument(
        "--output", type=str,
        help="Write result to file (otherwise stdout)"
    )

    args = parser.parse_args()

    # ─── Single task ─────────────────────────────────────────────────────
    if args.task:
        try:
            task = json.loads(args.task)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON: {e}", file=sys.stderr)
            return 1
        result = route_task(task)
        output = json.dumps(result, indent=2, ensure_ascii=False)
        if args.output:
            Path(args.output).write_text(output, encoding="utf-8")
            print(f"Written to {args.output}", file=sys.stderr)
        else:
            print(output)
        return 0

    # ─── Stdin ───────────────────────────────────────────────────────────
    if args.stdin:
        try:
            data = json.loads(sys.stdin.read())
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON from stdin: {e}", file=sys.stderr)
            return 1
        tasks = data if isinstance(data, list) else data.get("tasks", [data])
        result = route_batch(tasks)
        if args.format == "json":
            output = json.dumps(result, indent=2, ensure_ascii=False)
        else:
            output = format_table(result)
        if args.output:
            Path(args.output).write_text(output, encoding="utf-8")
            print(f"Written to {args.output}", file=sys.stderr)
        else:
            print(output)
        return 0

    # ─── Plan file ───────────────────────────────────────────────────────
    if args.plan:
        filepath = Path(args.plan)
        if not filepath.exists():
            print(f"Error: File not found: {filepath}", file=sys.stderr)
            return 1

        try:
            import yaml
            with open(filepath, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
        except ImportError:
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception as e:
                print(f"Error: Cannot parse file: {e}", file=sys.stderr)
                return 1

        tasks = data if isinstance(data, list) else data.get("tasks", [])
        result = route_batch(tasks)

        if args.format == "json":
            output = json.dumps(result, indent=2, ensure_ascii=False)
        else:
            output = format_table(result)

        if args.output:
            Path(args.output).write_text(output, encoding="utf-8")
            print(f"Written to {args.output}", file=sys.stderr)
        else:
            print(output)
        return 0

    return 1


if __name__ == "__main__":
    # Add scripts dir to path for inline imports
    sys.path.insert(0, str(SCRIPTS_DIR))
    sys.exit(main())
