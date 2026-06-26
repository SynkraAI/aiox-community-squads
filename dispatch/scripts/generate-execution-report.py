"""
Dispatch Squad — Execution Report Generator
Reads state.json + events.jsonl + costs.jsonl → fills templates → writes report.md + cost-report.md

Usage:
    python generate-execution-report.py --run-id <ID> [--root .] [--format json|table]
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

# ═══════════════════════════════════════════════════════════════════════════════
# PATH SETUP
# ═══════════════════════════════════════════════════════════════════════════════

SCRIPT_DIR = Path(__file__).resolve().parent
SQUAD_DIR = SCRIPT_DIR.parent
LIB_DIR = SQUAD_DIR / "lib"
TEMPLATES_DIR = SQUAD_DIR / "templates"

sys.path.insert(0, str(LIB_DIR))

from script_runner import run_script


# ═══════════════════════════════════════════════════════════════════════════════
# TEMPLATE ENGINE — Handlebars-style, recursive, zero deps
# ═══════════════════════════════════════════════════════════════════════════════


def _resolve_var(key: str, scopes: list) -> str:
    """Resolve a variable from scope chain (innermost first).

    Handles: {{var}}, {{this.field}}, {{this}}, {{@index}}
    """
    # {{@index}} — loop index
    if key == "@index":
        for scope in scopes:
            if "@index" in scope:
                return str(scope["@index"])
        return "0"

    # {{this}} — current item itself (for arrays of strings)
    if key == "this":
        for scope in scopes:
            if "__this__" in scope:
                return str(scope["__this__"])
        return ""

    # {{this.field}} — field on current loop item
    if key.startswith("this."):
        field = key[5:]
        for scope in scopes:
            if "__this__" in scope:
                obj = scope["__this__"]
                if isinstance(obj, dict) and field in obj:
                    return str(obj[field])
                return ""
        return ""

    # Regular variable — walk scope chain
    for scope in scopes:
        if key in scope:
            return str(scope[key])
    return None


def _is_truthy(val) -> bool:
    """Handlebars truthiness: false, 0, None, "", [] are falsy."""
    if val is None:
        return False
    if val is False:
        return False
    if val == "":
        return False
    if isinstance(val, (list, dict)) and len(val) == 0:
        return False
    return True


def _resolve_value(key: str, scopes: list):
    """Resolve raw value (not stringified) for truthiness/iteration."""
    if key.startswith("this."):
        field = key[5:]
        for scope in scopes:
            if "__this__" in scope:
                obj = scope["__this__"]
                if isinstance(obj, dict):
                    return obj.get(field)
                return None
        return None

    for scope in scopes:
        if key in scope:
            return scope[key]
    return None


def _find_balanced_block(text: str, open_tag: str, close_tag: str, start: int = 0):
    """Find a balanced block, handling nesting.

    Returns (start_pos, end_pos, header, body) or None.
    header = content of the opening tag (e.g., 'each tasks')
    body = content between open and close tags
    """
    open_re = re.compile(r"\{\{#" + open_tag + r"\s+([\w.@]+)\}\}")
    close_str = "{{/" + close_tag + "}}"

    m = open_re.search(text, start)
    if not m:
        return None

    header = m.group(1)
    body_start = m.end()
    nesting = 1
    pos = body_start

    while nesting > 0 and pos < len(text):
        next_open = open_re.search(text, pos)
        next_close_pos = text.find(close_str, pos)

        if next_close_pos == -1:
            return None  # Unbalanced

        if next_open and next_open.start() < next_close_pos:
            nesting += 1
            pos = next_open.end()
        else:
            nesting -= 1
            if nesting == 0:
                body = text[body_start:next_close_pos]
                end_pos = next_close_pos + len(close_str)
                return (m.start(), end_pos, header, body)
            pos = next_close_pos + len(close_str)

    return None


def _render(template: str, scopes: list, depth: int = 0) -> str:
    """Recursive template renderer with balanced block matching.

    Supports:
        {{variable}}                          — variable lookup through scope chain
        {{this.field}}                        — current loop item field
        {{@index}}                            — 0-based loop index
        {{#each key}}...{{/each}}             — iterate arrays (nested OK)
        {{#each this.key}}...{{/each}}        — iterate nested arrays
        {{#if key}}...{{/if}}                 — conditional
        {{#if key}}...{{else}}...{{/if}}      — conditional with else
    """
    if depth > 10:
        return template  # Safety: prevent infinite recursion

    result = template

    # ── Phase 1: Process {{#each}} blocks with balanced matching ──
    for _ in range(20):  # Max iterations to process all blocks
        block = _find_balanced_block(result, "each", "each")
        if not block:
            break

        start_pos, end_pos, key, body = block
        items = _resolve_value(key, scopes)

        if not items or not isinstance(items, list):
            result = result[:start_pos] + result[end_pos:]
            continue

        parts = []
        for idx, item in enumerate(items):
            child_scope = {"__this__": item, "@index": idx}
            rendered = _render(body, [child_scope] + scopes, depth + 1)
            parts.append(rendered)

        result = result[:start_pos] + "".join(parts) + result[end_pos:]

    # ── Phase 2: Process {{#if}}...{{else}}...{{/if}} blocks ──
    # Handle if/else first (before plain if)
    for _ in range(20):
        block = _find_balanced_block(result, "if", "if")
        if not block:
            break

        start_pos, end_pos, key, body = block
        val = _resolve_value(key, scopes)

        # Check for {{else}} inside body
        else_pos = body.find("{{else}}")
        if else_pos != -1:
            if_body = body[:else_pos]
            else_body = body[else_pos + 8:]  # len("{{else}}") = 8
            if _is_truthy(val):
                rendered = _render(if_body, scopes, depth + 1)
            else:
                rendered = _render(else_body, scopes, depth + 1)
        else:
            if _is_truthy(val):
                rendered = _render(body, scopes, depth + 1)
            else:
                rendered = ""

        result = result[:start_pos] + rendered + result[end_pos:]

    # ── Phase 3: Variable substitution ──
    var_re = re.compile(r"\{\{([\w.@]+)\}\}")

    def process_var(m):
        key = m.group(1)
        val = _resolve_var(key, scopes)
        if val is not None:
            return val
        return ""

    result = var_re.sub(process_var, result)

    return result


def render_template(template: str, context: dict) -> str:
    """Render a Handlebars-style template with full nesting support.

    Supports: {{var}}, {{this.field}}, {{@index}},
              {{#each}}...{{/each}}, {{#if}}...{{else}}...{{/if}}
    """
    return _render(template, [context])


# ═══════════════════════════════════════════════════════════════════════════════
# DATA LOADING
# ═══════════════════════════════════════════════════════════════════════════════


def load_state(run_dir: Path) -> dict:
    """Load state.json from run directory."""
    path = run_dir / "state.json"
    if not path.exists():
        print(f"ERROR: state.json not found at {path}", file=sys.stderr)
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_events(run_dir: Path) -> list:
    """Load events.jsonl from run directory."""
    path = run_dir / "events.jsonl"
    events = []
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    events.append(json.loads(line))
    return events


def load_costs(run_dir: Path) -> list:
    """Load costs.jsonl from run directory."""
    path = run_dir / "costs.jsonl"
    costs = []
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    costs.append(json.loads(line))
    return costs


def load_template(name: str) -> str:
    """Load a template file from templates directory."""
    path = TEMPLATES_DIR / name
    if not path.exists():
        return f"# Report\n\nTemplate {name} not found. Raw data follows.\n"
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


# ═══════════════════════════════════════════════════════════════════════════════
# CONTEXT BUILDING
# ═══════════════════════════════════════════════════════════════════════════════


def compute_wave_stats(state: dict) -> list:
    """Compute per-wave statistics from state."""
    waves = state.get("waves", {})
    tasks = state.get("tasks", {})
    result = []

    for wave_key in sorted(waves.keys(), key=lambda k: int(k)):
        wave = waves[wave_key]
        wave_num = int(wave_key)
        wave_tasks = [t for t in tasks.values() if t.get("wave") == wave_num]

        pass_count = sum(1 for t in wave_tasks if t.get("status") == "pass")
        fail_count = sum(1 for t in wave_tasks if t.get("status") == "fail")
        retry_count = sum(1 for t in wave_tasks if t.get("attempts", 0) > 1)
        cost = sum(t.get("cost_usd", 0) for t in wave_tasks)

        # Duration
        started = wave.get("started_at", "")
        completed = wave.get("completed_at", "")
        duration_sec = 0
        if started and completed:
            try:
                t0 = datetime.fromisoformat(started)
                t1 = datetime.fromisoformat(completed)
                duration_sec = int((t1 - t0).total_seconds())
            except (ValueError, TypeError):
                pass

        result.append({
            "wave_num": wave_num,
            "task_count": len(wave_tasks),
            "pass_count": pass_count,
            "fail_count": fail_count,
            "retry_count": retry_count,
            "duration_sec": duration_sec,
            "cost_usd": f"{cost:.4f}",
            "predicted_outputs": wave.get("prediction", "N/A"),
            "actual_outputs": f"{pass_count}/{len(wave_tasks)} pass",
            "predicted_cost": "N/A",
            "actual_cost": f"{cost:.4f}",
            "delta_pct": "N/A",
        })
    return result


def compute_task_details(state: dict) -> list:
    """Build per-task detail list for the report."""
    tasks = state.get("tasks", {})
    details = []
    for tid in sorted(tasks.keys()):
        t = tasks[tid]
        # Build acceptance criteria list
        raw_ac = t.get("acceptance_criteria", [])
        ac_list = []
        if isinstance(raw_ac, list):
            for criterion in raw_ac:
                if isinstance(criterion, dict):
                    ac_list.append(criterion)
                else:
                    ac_list.append({"criterion": str(criterion), "passed": t.get("status") == "pass"})

        details.append({
            "task_id": tid,
            "description": t.get("description", ""),
            "status": t.get("status", "pending"),
            "model": t.get("model", ""),
            "agent": t.get("agent", ""),
            "executor_type": t.get("executor_type", ""),
            "wave": t.get("wave", 0),
            "attempts": t.get("attempts", 0),
            "max_attempts": t.get("max_attempts", 3),
            "cost_usd": f"{t.get('cost_usd', 0):.4f}",
            "tokens_in": t.get("tokens_in", 0),
            "tokens_out": t.get("tokens_out", 0),
            "output_path": t.get("output_path", ""),
            "error": t.get("error", ""),
            "acceptance_criteria": ac_list,
        })
    return details


def compute_failures(state: dict) -> list:
    """Build list of failed tasks for the failures section."""
    tasks = state.get("tasks", {})
    failures = []
    for tid in sorted(tasks.keys()):
        t = tasks[tid]
        if t.get("status") == "fail":
            failures.append({
                "task_id": tid,
                "error": t.get("error", "Unknown error"),
                "attempts": t.get("attempts", 0),
                "resolution": "Retry available" if t.get("attempts", 0) < t.get("max_attempts", 3) else "Max attempts reached",
            })
    return failures


def compute_per_model_stats(state: dict) -> dict:
    """Compute per-model statistics for template variables."""
    tasks = state.get("tasks", {})
    stats = {}
    for t in tasks.values():
        model = t.get("model", "unknown")
        if model not in stats:
            stats[model] = {"count": 0, "tokens_in": 0, "tokens_out": 0, "cost": 0.0}
        stats[model]["count"] += 1
        stats[model]["tokens_in"] += t.get("tokens_in", 0)
        stats[model]["tokens_out"] += t.get("tokens_out", 0)
        stats[model]["cost"] += t.get("cost_usd", 0)

    result = {}
    # Always include worker/haiku/sonnet (templates expect them), plus any other models
    all_models = set(["worker", "haiku", "sonnet"]) | set(stats.keys())
    for model in sorted(all_models):
        s = stats.get(model, {"count": 0, "tokens_in": 0, "tokens_out": 0, "cost": 0.0})
        result[f"{model}_count"] = s["count"]
        result[f"{model}_tokens_in"] = s["tokens_in"]
        result[f"{model}_tokens_out"] = s["tokens_out"]
        result[f"{model}_cost"] = f"{s['cost']:.4f}"
    return result


def compute_cost_by_model(state: dict) -> list:
    """Aggregate costs by model."""
    tasks = state.get("tasks", {})
    models = {}
    for t in tasks.values():
        model = t.get("model", "unknown")
        if model not in models:
            models[model] = {"model": model, "count": 0, "cost": 0.0, "tokens_in": 0, "tokens_out": 0}
        models[model]["count"] += 1
        models[model]["cost"] += t.get("cost_usd", 0)
        models[model]["tokens_in"] += t.get("tokens_in", 0)
        models[model]["tokens_out"] += t.get("tokens_out", 0)

    result = []
    for m in sorted(models.values(), key=lambda x: x["cost"], reverse=True):
        result.append({
            "model": m["model"],
            "count": m["count"],
            "cost_usd": f"{m['cost']:.4f}",
            "tokens_in": m["tokens_in"],
            "tokens_out": m["tokens_out"],
        })
    return result


def build_report_context(state: dict, events: list, health_score: int, health_checks: list = None) -> dict:
    """Build the full context dict for template rendering."""
    tasks = state.get("tasks", {})
    total_tasks = len(tasks)
    total_pass = sum(1 for t in tasks.values() if t.get("status") == "pass")
    total_fail = sum(1 for t in tasks.values() if t.get("status") == "fail")
    total_retry = sum(1 for t in tasks.values() if t.get("attempts", 0) > 1)

    # Duration
    started = state.get("started_at", "")
    last_updated = state.get("last_updated", "")
    duration_min = 0
    if started and last_updated:
        try:
            t0 = datetime.fromisoformat(started)
            t1 = datetime.fromisoformat(last_updated)
            duration_min = round((t1 - t0).total_seconds() / 60, 1)
        except (ValueError, TypeError):
            pass

    total_cost = state.get("total_cost_usd", 0)

    # Opus equivalent: what it would cost if all tasks ran on Opus in main context
    total_in = state.get("total_tokens_in", 0)
    total_out = state.get("total_tokens_out", 0)
    opus_cost = (total_in * 15.0 / 1_000_000) + (total_out * 75.0 / 1_000_000)
    savings_pct = round((1 - total_cost / opus_cost) * 100, 1) if opus_cost > 0 else 0

    # Health rating
    if health_score >= 12:
        health_rating = "Exemplary"
    elif health_score >= 9:
        health_rating = "Good"
    elif health_score >= 5:
        health_rating = "Needs Work"
    else:
        health_rating = "Poor"

    waves = compute_wave_stats(state)
    total_duration_sec = sum(int(w.get("duration_sec", 0)) for w in waves)

    # Failures
    failures = compute_failures(state)
    has_failures = len(failures) > 0

    # Per-model stats (worker_count, haiku_count, etc.)
    model_stats = compute_per_model_stats(state)

    # Learnings as dicts for {{#each}} with {{this}}
    learnings = state.get("learnings", [])

    # Story-related
    is_story_input = state.get("input_type") == "story"

    ctx = {
        "run_id": state.get("run_id", ""),
        "started_at": started,
        "completed_at": last_updated,
        "duration_min": duration_min,
        "status": state.get("status", ""),
        "input_type": state.get("input_type", ""),
        "input_path": state.get("input_path", ""),
        "description": state.get("description", ""),
        "total_tasks": total_tasks,
        "total_waves": state.get("total_waves", 0),
        "total_pass": total_pass,
        "total_fail": total_fail,
        "total_retry": total_retry,
        "total_cost_usd": f"{total_cost:.4f}",
        "total_tokens_in": state.get("total_tokens_in", 0),
        "total_tokens_out": state.get("total_tokens_out", 0),
        "total_duration_sec": total_duration_sec,
        "opus_equivalent_cost": f"{opus_cost:.4f}",
        "savings_pct": savings_pct,
        "health_score": health_score,
        "health_rating": health_rating,
        "waves": waves,
        "tasks": compute_task_details(state),
        "cost_by_model": compute_cost_by_model(state),
        "failures": failures,
        "has_failures": has_failures,
        "learnings": learnings,
        "domains_used": state.get("domains_used", []),
        "is_story_input": is_story_input,
        "story_acceptance": [],  # Populated by dispatch-chief after checking story
        "pre_execution_vetos": [],  # Populated from events
        "post_execution_vetos": [],  # Populated from events
        "health_items": health_checks or [],
        "next_step_1": "Review failed tasks and retry if needed",
        "next_step_2": "Update story with completion status",
        "next_step_3": "Archive run or continue with next story",
    }

    # Merge per-model stats
    ctx.update(model_stats)

    # Extract veto events from event log
    for event in events:
        etype = event.get("event", "")
        if etype == "gate_failed":
            gate = event.get("gate", "")
            veto_entry = {
                "id": gate,
                "condition": event.get("error", event.get("reason", "")),
                "result": "BLOCKED",
            }
            if gate.startswith("V1") or gate in ("enrichment", "haiku"):
                ctx["pre_execution_vetos"].append(veto_entry)
            elif gate.startswith("V2"):
                ctx["post_execution_vetos"].append(veto_entry)
        elif etype == "gate_passed":
            gate = event.get("gate", "")
            veto_entry = {"id": gate, "condition": "Check passed", "result": "PASS"}
            if gate.startswith("V1") or gate in ("enrichment", "haiku"):
                ctx["pre_execution_vetos"].append(veto_entry)
            elif gate.startswith("V2"):
                ctx["post_execution_vetos"].append(veto_entry)

    return ctx


# Per-model pricing (2026 rates per MTok)
_MODEL_RATES = {
    "haiku": {"input": 1.0, "output": 5.0},
    "sonnet": {"input": 3.0, "output": 15.0},
    "opus": {"input": 5.0, "output": 25.0},
    "worker": {"input": 0.0, "output": 0.0},
}


def _weighted_cost(tasks: dict, token_field: str, direction: str) -> float:
    """Calculate weighted cost using per-model rates instead of flat Haiku rates."""
    total = 0.0
    for t in tasks.values():
        model = t.get("model", "haiku")
        rate = _MODEL_RATES.get(model, _MODEL_RATES["haiku"])[direction]
        total += t.get(token_field, 0) * rate / 1_000_000
    return total


def _build_domain_stats(tasks: dict, total_cost: float) -> list:
    """Build per-domain cost stats from task agents."""
    domains = {}
    for t in tasks.values():
        agent = t.get("agent", "")
        # Extract domain from agent path (e.g., /copy:tasks:create-sales-page → copy)
        domain = agent.split(":")[0].lstrip("/") if ":" in agent else "unknown"
        if domain not in domains:
            domains[domain] = {"name": domain, "task_count": 0, "cost_usd": 0.0, "models": {}}
        domains[domain]["task_count"] += 1
        domains[domain]["cost_usd"] += t.get("cost_usd", 0)
        m = t.get("model", "haiku")
        domains[domain]["models"][m] = domains[domain]["models"].get(m, 0) + 1

    result = []
    for d in sorted(domains.values(), key=lambda x: x["cost_usd"], reverse=True):
        primary_model = max(d["models"], key=d["models"].get) if d["models"] else "haiku"
        pct = round(d["cost_usd"] / total_cost * 100, 1) if total_cost > 0 else 0
        result.append({
            "name": d["name"],
            "task_count": d["task_count"],
            "primary_model": primary_model,
            "cost_usd": f"{d['cost_usd']:.4f}",
            "pct": pct,
        })
    return result


def build_cost_context(state: dict) -> dict:
    """Build context for cost report template."""
    tasks = state.get("tasks", {})
    total_cost = state.get("total_cost_usd", 0)
    total_tasks = len(tasks)
    avg_cost = total_cost / total_tasks if total_tasks > 0 else 0

    total_in = state.get("total_tokens_in", 0)
    total_out = state.get("total_tokens_out", 0)
    opus_cost = (total_in * 15.0 / 1_000_000) + (total_out * 75.0 / 1_000_000)
    savings_usd = opus_cost - total_cost
    savings_pct = round((1 - total_cost / opus_cost) * 100, 1) if opus_cost > 0 else 0

    worker_count = sum(1 for t in tasks.values() if t.get("model") == "worker")
    agent_count = total_tasks - worker_count
    code_llm_recommendation = (
        "Good CODE>LLM ratio" if worker_count >= total_tasks * 0.15
        else "Consider converting more tasks to Worker type"
    )

    model_stats = compute_per_model_stats(state)
    total_in = state.get("total_tokens_in", 0)
    total_out = state.get("total_tokens_out", 0)

    code_llm_ratio = f"{worker_count}:{agent_count}" if agent_count > 0 else "N/A"
    worker_savings = f"{(worker_count * 0.007):.4f}"  # Approx savings vs haiku per task

    ctx = {
        "run_id": state.get("run_id", ""),
        "date": datetime.now().strftime("%Y-%m-%d"),
        "total_cost_usd": f"{total_cost:.4f}",
        "total_tasks": total_tasks,
        "avg_cost_per_task": f"{avg_cost:.4f}",
        "opus_equivalent_cost": f"{opus_cost:.4f}",
        "savings_pct": savings_pct,
        "savings_usd": f"{savings_usd:.4f}",
        "total_tokens_in": total_in,
        "total_tokens_out": total_out,
        "total_input_cost": f"{_weighted_cost(tasks, 'tokens_in', 'input'):.4f}",
        "total_output_cost": f"{_weighted_cost(tasks, 'tokens_out', 'output'):.4f}",
        "waves": compute_wave_stats(state),
        "cost_by_model": compute_cost_by_model(state),
        "domains": _build_domain_stats(tasks, total_cost),
        "worker_count": worker_count,
        "agent_count": agent_count,
        "code_llm_ratio": code_llm_ratio,
        "worker_savings": worker_savings,
        "code_llm_recommendation": code_llm_recommendation,
        # Cache placeholders (real values come from cost-tracker)
        "cacheable_tokens": 0,
        "cache_hits": 0,
        "cache_read_cost": "0.0000",
        "uncached_cost": "0.0000",
        "cache_savings": "0.0000",
        "cache_savings_pct": 0,
        "total_cache_savings": "0.0000",
        # Estimate vs actual placeholders
        "estimated_cost": "N/A",
        "cost_delta_pct": "N/A",
        "cost_status": "N/A",
        "estimated_tasks": total_tasks,
        "actual_tasks": total_tasks,
        "task_delta": 0,
        "task_status": "OK",
        "estimated_duration": "N/A",
        "actual_duration": "N/A",
        "duration_delta_pct": "N/A",
        "duration_status": "N/A",
        "estimated_retries": 0,
        "actual_retries": sum(1 for t in tasks.values() if t.get("attempts", 0) > 1),
        "retry_delta": 0,
        "retry_status": "OK",
        "cost_within_budget": True,
        "cost_threshold": "N/A",
    }

    # Merge per-model stats (haiku_count, haiku_tokens_in, haiku_cost, etc.)
    ctx.update(model_stats)

    # Per-model input/output costs
    for model, rate_in, rate_out in [("haiku", 1.0, 5.0), ("sonnet", 3.0, 15.0)]:
        tin = model_stats.get(f"{model}_tokens_in", 0)
        tout = model_stats.get(f"{model}_tokens_out", 0)
        ctx[f"{model}_input_cost"] = f"{(tin * rate_in / 1_000_000):.4f}"
        ctx[f"{model}_output_cost"] = f"{(tout * rate_out / 1_000_000):.4f}"
        ctx[f"{model}_total_cost"] = model_stats.get(f"{model}_cost", "0.0000")
        ctx[f"{model}_pct"] = round(float(model_stats.get(f"{model}_cost", "0")) / total_cost * 100, 1) if total_cost > 0 else 0

    return ctx


# ═══════════════════════════════════════════════════════════════════════════════
# EXTERNAL SCRIPT CALLS
# ═══════════════════════════════════════════════════════════════════════════════


def get_cost_summary(run_id: str, project_root: str) -> dict:
    """Call cost-tracker.py summary."""
    result = run_script("cost-tracker.py", ["summary", "--run-id", run_id], project_root=project_root)
    if result["ok"]:
        return result["data"]
    return {}


def get_health_score(state_path: str, project_root: str) -> dict:
    """Call dispatch-health-score.py. Returns {score: int, checks: list}."""
    result = run_script("dispatch-health-score.py", [state_path], project_root=project_root)
    if result["ok"]:
        data = result["data"]
        # dispatch-health-score.py returns score as "N/12" string — parse to int
        score_raw = data.get("score", "0/12")
        score = int(score_raw.split("/")[0]) if isinstance(score_raw, str) and "/" in score_raw else int(score_raw) if isinstance(score_raw, (int, float)) else 0
        return {"score": score, "checks": data.get("checks", [])}
    return {"score": 0, "checks": []}


# ═══════════════════════════════════════════════════════════════════════════════
# REPORT GENERATION
# ═══════════════════════════════════════════════════════════════════════════════


def generate_reports(run_id: str, project_root: str = ".") -> dict:
    """Generate execution report and cost report for a dispatch run.

    Args:
        run_id: Dispatch run ID (e.g., dispatch-20260210-143000)
        project_root: Project root directory

    Returns:
        {"run_id": ..., "report_path": ..., "cost_report_path": ...,
         "health_score": ..., "total_cost": ..., "savings_pct": ...}
    """
    root = Path(project_root)
    run_dir = root / "_temp" / "dispatch" / "runs" / run_id

    # Load data
    state = load_state(run_dir)
    events = load_events(run_dir)
    costs = load_costs(run_dir)

    # Merge per-task cost data from costs.jsonl into state tasks
    if costs:
        cost_by_task = {}
        for c in costs:
            tid = c.get("task_id")
            if tid:
                cost_by_task[tid] = c
        for tid, cost_data in cost_by_task.items():
            if tid in state.get("tasks", {}):
                t = state["tasks"][tid]
                t.setdefault("cost_usd", cost_data.get("cost_usd", 0))
                t.setdefault("tokens_in", cost_data.get("tokens_in", 0))
                t.setdefault("tokens_out", cost_data.get("tokens_out", 0))
                t.setdefault("model", cost_data.get("model", "haiku"))

    # Get health score + individual check results
    state_path = str(run_dir / "state.json")
    health_result = get_health_score(state_path, project_root)
    health_score = health_result["score"]
    health_checks = health_result["checks"]

    # Merge cost summary from cost-tracker if available
    cost_summary = get_cost_summary(run_id, project_root)
    if cost_summary:
        state["total_cost_usd"] = cost_summary.get("total_cost_usd", state.get("total_cost_usd", 0))
        state["total_tokens_in"] = cost_summary.get("total_tokens_in", state.get("total_tokens_in", 0))
        state["total_tokens_out"] = cost_summary.get("total_tokens_out", state.get("total_tokens_out", 0))

    # Build contexts
    report_ctx = build_report_context(state, events, health_score, health_checks)
    cost_ctx = build_cost_context(state)

    # Load and render templates
    exec_tmpl = load_template("execution-report-tmpl.md")
    cost_tmpl = load_template("cost-report-tmpl.md")

    exec_report = render_template(exec_tmpl, report_ctx)
    cost_report = render_template(cost_tmpl, cost_ctx)

    # Write reports
    report_path = run_dir / "report.md"
    cost_report_path = run_dir / "cost-report.md"

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(exec_report)
    with open(cost_report_path, "w", encoding="utf-8") as f:
        f.write(cost_report)

    # Update state with report info
    state["status"] = "complete"
    state["health_score"] = health_score
    state["report_path"] = str(report_path)
    state["cost_report_path"] = str(cost_report_path)
    state["last_updated"] = datetime.now().isoformat()
    with open(run_dir / "state.json", "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

    summary = {
        "run_id": run_id,
        "report_path": str(report_path),
        "cost_report_path": str(cost_report_path),
        "health_score": health_score,
        "total_cost": state.get("total_cost_usd", 0),
        "savings_pct": report_ctx.get("savings_pct", 0),
        "total_tasks": len(state.get("tasks", {})),
        "total_pass": report_ctx["total_pass"],
        "total_fail": report_ctx["total_fail"],
    }

    return summary


# ═══════════════════════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════════════════════


def main():
    parser = argparse.ArgumentParser(description="Generate dispatch execution report")
    parser.add_argument("--run-id", required=True, help="Dispatch run ID")
    parser.add_argument("--root", default=".", help="Project root directory")
    parser.add_argument("--format", choices=["json", "table"], default="json", help="Output format")
    args = parser.parse_args()

    summary = generate_reports(args.run_id, args.root)

    if args.format == "table":
        print(f"\n{'='*60}")
        print(f"  DISPATCH EXECUTION REPORT — {summary['run_id']}")
        print(f"{'='*60}")
        print(f"  Health Score: {summary['health_score']}/12")
        print(f"  Tasks: {summary['total_pass']} pass / {summary['total_fail']} fail / {summary['total_tasks']} total")
        print(f"  Cost: ${summary['total_cost']:.4f} ({summary['savings_pct']}% savings vs Opus)")
        print(f"  Report: {summary['report_path']}")
        print(f"  Cost Report: {summary['cost_report_path']}")
        print(f"{'='*60}\n")
    else:
        print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
