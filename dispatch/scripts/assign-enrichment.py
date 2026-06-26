#!/usr/bin/env python3
"""
Assign enrichment level for dispatch tasks.

Usage:
  # Single task
  python scripts/assign-enrichment.py --task '{"domain": "copy", "type": "create", "model": "haiku"}'

  # Batch from file
  python scripts/assign-enrichment.py --tasks-file execution-plan.yaml

  # Pipe from stdin
  echo '{"domain": "organization", "type": "index"}' | python scripts/assign-enrichment.py --stdin

Output (JSON):
  {
    "enrichment": "STANDARD",
    "token_budget": 1500,
    "kb_files": ["squads/copy/data/copywriting-kb.md"],
    "rationale": "Rule 4: domain=copy, default STANDARD"
  }

Determination Algorithm (priority order):
  1. IF type IN [move, delete, validate, rename] → MINIMAL
  2. IF domain == organization OR type IN [index, gitkeep] → MINIMAL
  3. IF domain == copy (marketing_copy) → FULL
  4. IF domain IN [ac_automation, bh_automation, youtube, dev, design] → STANDARD
  5. DEFAULT → STANDARD

Source: squads/dispatch/data/enrichment-rules.yaml
Version: 1.0.0
Date: 2026-02-10
"""

import argparse
import json
import sys
from pathlib import Path

# ═══════════════════════════════════════════════════════════════════════════════
# ENRICHMENT CLASSIFICATION RULES
# ═══════════════════════════════════════════════════════════════════════════════

# Rule 1: MINIMAL types — no context needed
MINIMAL_TYPES = {
    "move", "delete", "validate", "rename", "mkdir",
    "copy", "gitkeep", "index", "organize",
}

# Rule 2: MINIMAL domains
MINIMAL_DOMAINS = {"organization"}

# Rule 3: FULL domains — maximum context needed
FULL_DOMAINS = {"copy", "squad_creator"}

# Rule 4: STANDARD domains (explicit, but also the default)
STANDARD_DOMAINS = {
    "ac_automation", "bh_automation", "youtube", "dev",
    "data_engineer", "design", "qa", "curator", "etl",
    "data", "mmos", "ralph",
}

# Token budgets per level
TOKEN_BUDGETS = {
    "MINIMAL": 500,
    "STANDARD": 1500,
    "FULL": 3000,
}

# Domain registry path for KB file lookup
DOMAIN_REGISTRY_PATH = Path("squads/dispatch/data/domain-registry.yaml")

# Fallback KB files per domain (used when YAML unavailable)
FALLBACK_KB = {
    "copy": ["squads/copy/data/copywriting-kb.md"],
    "curator": ["squads/curator/data/moment-types.yaml"],
    "design": ["squads/design/data/atomic-design-principles.md"],
    "ac_automation": ["MCPs/activecampaign/CLAUDE.md"],
    "bh_automation": ["MCPs/beehiiv/CLAUDE.md"],
}


def _load_domain_registry() -> dict:
    """Load domain registry for KB file lookup."""
    if not DOMAIN_REGISTRY_PATH.exists():
        print(f"Warning: {DOMAIN_REGISTRY_PATH} not found, using fallback KB", file=sys.stderr)
        return {}
    try:
        import yaml
        with open(DOMAIN_REGISTRY_PATH, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return data.get("domains", {})
    except ImportError:
        print("Warning: PyYAML not installed, using fallback KB", file=sys.stderr)
        return {}
    except Exception as e:
        print(f"Warning: Error loading registry: {e}, using fallback KB", file=sys.stderr)
        return {}


# Load once on import
_DOMAIN_REGISTRY = None


def _get_registry():
    global _DOMAIN_REGISTRY
    if _DOMAIN_REGISTRY is None:
        _DOMAIN_REGISTRY = _load_domain_registry()
    return _DOMAIN_REGISTRY


def get_kb_files(domain: str) -> list:
    """Resolve KB files for a domain."""
    registry = _get_registry()
    if domain in registry:
        return registry[domain].get("kb_files", [])
    return FALLBACK_KB.get(domain, [])


def assign_enrichment(task: dict) -> dict:
    """Assign enrichment level to a single task.

    Args:
        task: dict with keys: domain, type, model (all optional)

    Returns:
        dict with: enrichment, token_budget, kb_files, rationale
    """
    task_type = (task.get("type") or "").lower().strip()
    domain = (task.get("domain") or "").lower().strip()
    model = (task.get("model") or "").lower().strip()

    # ─── Rule 0: Workers always get MINIMAL ──────────────────────────────
    if model == "worker":
        return _result("MINIMAL", domain, f"Rule 0: model=worker → MINIMAL (no LLM context)")

    # ─── Rule 1: MINIMAL types ───────────────────────────────────────────
    if task_type in MINIMAL_TYPES:
        return _result("MINIMAL", domain, f"Rule 1: type={task_type} → MINIMAL")

    # ─── Rule 2: MINIMAL domains ─────────────────────────────────────────
    if domain in MINIMAL_DOMAINS:
        return _result("MINIMAL", domain, f"Rule 2: domain={domain} → MINIMAL")

    # ─── Rule 3: FULL domains ────────────────────────────────────────────
    if domain in FULL_DOMAINS:
        return _result("FULL", domain, f"Rule 3: domain={domain} → FULL")

    # ─── Rule 4: STANDARD domains ────────────────────────────────────────
    if domain in STANDARD_DOMAINS:
        return _result("STANDARD", domain, f"Rule 4: domain={domain} → STANDARD")

    # ─── Rule 5: Default ─────────────────────────────────────────────────
    return _result("STANDARD", domain, f"Rule 5: default → STANDARD")


def _result(level: str, domain: str, rationale: str) -> dict:
    """Build result dict with KB files resolved."""
    kb_files = get_kb_files(domain) if level != "MINIMAL" else []
    return {
        "enrichment": level,
        "token_budget": TOKEN_BUDGETS[level],
        "kb_files": kb_files,
        "rationale": rationale,
    }


def assign_batch(tasks: list) -> dict:
    """Assign enrichment to a list of tasks."""
    results = []
    counts = {"MINIMAL": 0, "STANDARD": 0, "FULL": 0}
    total_budget = 0

    for task in tasks:
        result = assign_enrichment(task)
        result["task_id"] = task.get("task_id", f"T{len(results)+1:03d}")
        result["task_name"] = task.get("name", task.get("description", "")[:60])
        results.append(result)
        counts[result["enrichment"]] += 1
        total_budget += result["token_budget"]

    return {
        "tasks": results,
        "summary": {
            "total": len(results),
            "MINIMAL": counts["MINIMAL"],
            "STANDARD": counts["STANDARD"],
            "FULL": counts["FULL"],
            "total_token_budget": total_budget,
        },
    }


def format_table(result: dict) -> str:
    """Format result as human-readable table."""
    lines = []
    lines.append(f"{'Task ID':<8} {'Level':<10} {'Tokens':<8} {'KB Files':<40} {'Rationale'}")
    lines.append("-" * 100)
    for t in result["tasks"]:
        kb = ", ".join(t["kb_files"][:2]) if t["kb_files"] else "-"
        if len(kb) > 38:
            kb = kb[:35] + "..."
        lines.append(
            f"{t['task_id']:<8} {t['enrichment']:<10} {t['token_budget']:<8} "
            f"{kb:<40} {t['rationale']}"
        )
    lines.append("-" * 100)
    s = result["summary"]
    lines.append(
        f"Total: {s['total']} | MINIMAL: {s['MINIMAL']} | "
        f"STANDARD: {s['STANDARD']} | FULL: {s['FULL']} | "
        f"Token budget: {s['total_token_budget']:,}"
    )
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Assign enrichment level for dispatch tasks"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--task", type=str, help="Single task as JSON string")
    group.add_argument("--tasks-file", type=str, help="YAML/JSON file with tasks list")
    group.add_argument("--stdin", action="store_true", help="Read task JSON from stdin")

    parser.add_argument(
        "--format", choices=["json", "table"], default="json",
        help="Output format (default: json)"
    )

    args = parser.parse_args()

    if args.task:
        try:
            task = json.loads(args.task)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON: {e}", file=sys.stderr)
            return 1
        result = assign_enrichment(task)
        if args.format == "json":
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(f"{result['enrichment']} ({result['token_budget']} tokens) | {result['rationale']}")
        return 0

    if args.stdin:
        try:
            task = json.loads(sys.stdin.read())
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON from stdin: {e}", file=sys.stderr)
            return 1
        if isinstance(task, list):
            result = assign_batch(task)
        else:
            result = assign_enrichment(task)
        if args.format == "json":
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            if "tasks" in result:
                print(format_table(result))
            else:
                print(f"{result['enrichment']} ({result['token_budget']} tokens) | {result['rationale']}")
        return 0

    if args.tasks_file:
        filepath = Path(args.tasks_file)
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
                print(f"Error: Cannot parse file (install PyYAML): {e}", file=sys.stderr)
                return 1

        tasks = data if isinstance(data, list) else data.get("tasks", [])
        result = assign_batch(tasks)

        if args.format == "json":
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(format_table(result))
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())
