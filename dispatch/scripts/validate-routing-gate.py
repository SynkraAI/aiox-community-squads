#!/usr/bin/env python3
"""
Validate routed tasks against QG-ROUTE quality gate.

Implements routing completeness checks from routing-quality-gate.yaml.
Pure CODE — no LLM. Deterministic validation of 10 veto conditions.

Usage:
  # Validate using run ID
  python squads/dispatch/scripts/validate-routing-gate.py --run-id {run_id}

  # Validate using explicit file path
  python squads/dispatch/scripts/validate-routing-gate.py --tasks-file path/to/routed-tasks.json

  # Auto-fix notation issues
  python squads/dispatch/scripts/validate-routing-gate.py --run-id {run_id} --auto-fix

  # Output formats
  python squads/dispatch/scripts/validate-routing-gate.py --run-id {run_id} --format json
  python squads/dispatch/scripts/validate-routing-gate.py --run-id {run_id} --format report

Output (JSON):
  {
    "status": "PASS|WARN|FAIL",
    "total_tasks": 10,
    "scores": {
      "completeness": 1.0,
      "notation": 0.9,
      "constraint": 1.0,
      "routing_quality": 0.96
    },
    "blocking_issues": [],
    "warnings": [],
    "issues": []
  }

Exit codes:
  0 = PASS (>= 1.0)
  2 = WARN (>= 0.90)
  1 = FAIL (< 0.90)

Source: squads/dispatch/data/routing-quality-gate.yaml
Version: 1.0.0
Date: 2026-02-12
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import List, Dict, Tuple, Any

# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════

VALID_MODELS = ["worker", "haiku", "sonnet", "opus"]
VALID_ENRICHMENT = ["MINIMAL", "STANDARD", "FULL"]
MCP_DOMAINS = ["automation_ac", "automation_bh", "automation_clickup"]
ARCHITECTURE_INDICATORS = ["architecture", "strategic", "PRD", "decision"]

# ═══════════════════════════════════════════════════════════════════════════════
# LOAD VALID DOMAINS
# ═══════════════════════════════════════════════════════════════════════════════

def load_valid_domains() -> List[str]:
    """Load valid domains from domain-registry.yaml."""
    registry_path = Path("squads/dispatch/data/domain-registry.yaml")
    if not registry_path.exists():
        print(f"ERROR: domain-registry.yaml not found at {registry_path}", file=sys.stderr)
        sys.exit(1)

    # Simple YAML parsing — extract domain names from 'domains:' section
    domains = []
    with open(registry_path, 'r', encoding='utf-8') as f:
        in_domains_section = False
        for line in f:
            if line.strip() == "domains:":
                in_domains_section = True
                continue
            if in_domains_section:
                # Domain entries are at indent level 2 (e.g., "  ac_automation:")
                if line.startswith("  ") and not line.startswith("    ") and ":" in line:
                    domain = line.strip().rstrip(":")
                    domains.append(domain)
                elif line.strip() and not line.startswith(" "):
                    # End of domains section
                    break

    return domains

# ═══════════════════════════════════════════════════════════════════════════════
# VETO CHECKS (VR.1 - VR.10)
# ═══════════════════════════════════════════════════════════════════════════════

def check_vr1_domain(task: Dict, valid_domains: List[str]) -> Tuple[bool, str]:
    """VR.1: Task must have valid domain from domain-registry.yaml."""
    domain = task.get("domain")
    if not domain:
        return False, "Missing domain assignment"
    if domain not in valid_domains:
        return False, f"Invalid domain '{domain}' (not in domain-registry.yaml)"
    return True, ""

def check_vr2_agent(task: Dict) -> Tuple[bool, str]:
    """VR.2: Task must have agent path (slash notation)."""
    agent = task.get("agent")
    if not agent:
        return False, "Missing agent assignment"
    if not agent.startswith("/"):
        return False, f"Agent path must use slash notation, got '{agent}'"
    return True, ""

def check_vr3_model(task: Dict) -> Tuple[bool, str]:
    """VR.3: Task must have valid model assignment."""
    model = task.get("model")
    if not model:
        return False, "Missing model assignment"
    if model not in VALID_MODELS:
        return False, f"Invalid model '{model}' (must be one of {VALID_MODELS})"
    return True, ""

def check_vr4_enrichment(task: Dict) -> Tuple[bool, str]:
    """VR.4: Task must have valid enrichment_level."""
    enrichment = task.get("enrichment_level")
    if not enrichment:
        return False, "Missing enrichment_level"
    if enrichment not in VALID_ENRICHMENT:
        return False, f"Invalid enrichment_level '{enrichment}' (must be one of {VALID_ENRICHMENT})"
    return True, ""

def check_vr5_timeout(task: Dict) -> Tuple[bool, str]:
    """VR.5: Task must have numeric timeout_ms > 0."""
    timeout = task.get("timeout_ms")
    if timeout is None:
        return False, "Missing timeout_ms"
    if not isinstance(timeout, (int, float)) or timeout <= 0:
        return False, f"Invalid timeout_ms '{timeout}' (must be numeric > 0)"
    return True, ""

def check_vr6_slash_notation(task: Dict) -> Tuple[bool, str]:
    """VR.6: Agent references must use / prefix (not @)."""
    agent = task.get("agent", "")
    if agent.startswith("@"):
        return False, f"Agent uses @ notation instead of / (got '{agent}')"
    return True, ""

def check_vr7_forward_slashes(task: Dict) -> Tuple[bool, str]:
    """VR.7: File paths must use forward slashes (not backslashes)."""
    # Check common file path fields
    for field in ["agent", "template", "kb_files", "output_path"]:
        value = task.get(field)
        if isinstance(value, str) and "\\" in value:
            return False, f"Field '{field}' contains backslashes (value: '{value}')"
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, str) and "\\" in item:
                    return False, f"Field '{field}' contains backslashes (value: '{item}')"
    return True, ""

def check_vr8_mcp_foreground(task: Dict) -> Tuple[bool, str]:
    """VR.8: MCP tasks must be flagged as MCP_FOREGROUND."""
    domain = task.get("domain", "")
    if domain in MCP_DOMAINS:
        flags = task.get("flags", [])
        if "MCP_FOREGROUND" not in flags:
            return False, f"MCP task (domain: {domain}) not flagged as MCP_FOREGROUND"
    return True, ""

def check_vr9_architecture_no_dispatch(task: Dict) -> Tuple[bool, str]:
    """VR.9: Architecture/strategic tasks must be flagged as DO_NOT_DISPATCH."""
    description = task.get("description", "").lower()
    for indicator in ARCHITECTURE_INDICATORS:
        if indicator.lower() in description:
            flags = task.get("flags", [])
            if "DO_NOT_DISPATCH" not in flags:
                return False, f"Architecture task (contains '{indicator}') not flagged as DO_NOT_DISPATCH"
            break
    return True, ""

def check_vr10_no_multi_domain(task: Dict) -> Tuple[bool, str]:
    """VR.10: Task must not span multiple domains."""
    domains = task.get("domains", [])
    if isinstance(domains, list) and len(domains) > 1:
        return False, f"Task spans multiple domains: {domains} (must be split)"
    return True, ""

# ═══════════════════════════════════════════════════════════════════════════════
# AUTO-FIX
# ═══════════════════════════════════════════════════════════════════════════════

def auto_fix_task(task: Dict) -> bool:
    """Auto-fix VR.6 and VR.7 notation issues. Returns True if fixes applied."""
    fixed = False

    # VR.6: Convert @ to /
    if task.get("agent", "").startswith("@"):
        task["agent"] = "/" + task["agent"][1:]
        fixed = True

    # VR.7: Convert backslashes to forward slashes
    for field in ["agent", "template", "output_path"]:
        if field in task and isinstance(task[field], str):
            if "\\" in task[field]:
                task[field] = task[field].replace("\\", "/")
                fixed = True

    # VR.7: Fix kb_files list
    if "kb_files" in task and isinstance(task["kb_files"], list):
        for i, item in enumerate(task["kb_files"]):
            if isinstance(item, str) and "\\" in item:
                task["kb_files"][i] = item.replace("\\", "/")
                fixed = True

    return fixed

# ═══════════════════════════════════════════════════════════════════════════════
# VALIDATION
# ═══════════════════════════════════════════════════════════════════════════════

def validate_tasks(tasks: List[Dict], valid_domains: List[str], auto_fix: bool = False) -> Dict:
    """Run all veto checks on tasks. Returns validation result."""

    total_tasks = len(tasks)
    if total_tasks == 0:
        return {
            "status": "FAIL",
            "total_tasks": 0,
            "scores": {"completeness": 0, "notation": 0, "constraint": 0, "routing_quality": 0},
            "blocking_issues": ["No tasks found in routed-tasks.json"],
            "warnings": [],
            "issues": []
        }

    issues = []
    blocking_issues = []
    warnings = []

    completeness_pass = 0
    notation_pass = 0
    constraint_pass = 0

    fixes_applied = []

    for idx, task in enumerate(tasks):
        task_id = task.get("id", f"task_{idx}")

        # Auto-fix if enabled
        if auto_fix:
            if auto_fix_task(task):
                fixes_applied.append(task_id)

        # Completeness checks (VR.1-VR.5) — BLOCKING
        vr1_pass, vr1_msg = check_vr1_domain(task, valid_domains)
        vr2_pass, vr2_msg = check_vr2_agent(task)
        vr3_pass, vr3_msg = check_vr3_model(task)
        vr4_pass, vr4_msg = check_vr4_enrichment(task)
        vr5_pass, vr5_msg = check_vr5_timeout(task)

        completeness_checks = [vr1_pass, vr2_pass, vr3_pass, vr4_pass, vr5_pass]
        if all(completeness_checks):
            completeness_pass += 1

        for veto_id, passed, msg in [
            ("VR.1", vr1_pass, vr1_msg),
            ("VR.2", vr2_pass, vr2_msg),
            ("VR.3", vr3_pass, vr3_msg),
            ("VR.4", vr4_pass, vr4_msg),
            ("VR.5", vr5_pass, vr5_msg)
        ]:
            if not passed:
                issue = {"task_id": task_id, "veto_id": veto_id, "severity": "BLOCKING", "message": msg}
                issues.append(issue)
                blocking_issues.append(f"[{task_id}] {veto_id}: {msg}")

        # Notation checks (VR.6-VR.7) — WARNING (auto-fixable)
        vr6_pass, vr6_msg = check_vr6_slash_notation(task)
        vr7_pass, vr7_msg = check_vr7_forward_slashes(task)

        notation_checks = [vr6_pass, vr7_pass]
        if all(notation_checks):
            notation_pass += 1

        for veto_id, passed, msg in [
            ("VR.6", vr6_pass, vr6_msg),
            ("VR.7", vr7_pass, vr7_msg)
        ]:
            if not passed:
                issue = {"task_id": task_id, "veto_id": veto_id, "severity": "WARNING", "message": msg}
                issues.append(issue)
                if auto_fix:
                    warnings.append(f"[{task_id}] {veto_id}: {msg} (AUTO-FIXED)")
                else:
                    warnings.append(f"[{task_id}] {veto_id}: {msg} (use --auto-fix)")

        # Constraint checks (VR.8-VR.10) — BLOCKING
        vr8_pass, vr8_msg = check_vr8_mcp_foreground(task)
        vr9_pass, vr9_msg = check_vr9_architecture_no_dispatch(task)
        vr10_pass, vr10_msg = check_vr10_no_multi_domain(task)

        constraint_checks = [vr8_pass, vr9_pass, vr10_pass]
        if all(constraint_checks):
            constraint_pass += 1

        for veto_id, passed, msg in [
            ("VR.8", vr8_pass, vr8_msg),
            ("VR.9", vr9_pass, vr9_msg),
            ("VR.10", vr10_pass, vr10_msg)
        ]:
            if not passed:
                issue = {"task_id": task_id, "veto_id": veto_id, "severity": "BLOCKING", "message": msg}
                issues.append(issue)
                blocking_issues.append(f"[{task_id}] {veto_id}: {msg}")

    # Calculate scores
    completeness_score = completeness_pass / total_tasks
    notation_score = notation_pass / total_tasks
    constraint_score = constraint_pass / total_tasks

    routing_quality = (completeness_score * 0.50) + (notation_score * 0.20) + (constraint_score * 0.30)

    # Determine status
    if routing_quality >= 1.0:
        status = "PASS"
    elif routing_quality >= 0.90:
        status = "WARN"
    else:
        status = "FAIL"

    result = {
        "status": status,
        "total_tasks": total_tasks,
        "scores": {
            "completeness": round(completeness_score, 2),
            "notation": round(notation_score, 2),
            "constraint": round(constraint_score, 2),
            "routing_quality": round(routing_quality, 2)
        },
        "blocking_issues": blocking_issues,
        "warnings": warnings,
        "issues": issues
    }

    if fixes_applied:
        result["fixes_applied"] = fixes_applied

    return result

# ═══════════════════════════════════════════════════════════════════════════════
# OUTPUT FORMATTING
# ═══════════════════════════════════════════════════════════════════════════════

def format_report(result: Dict) -> str:
    """Format validation result as human-readable report."""
    status = result["status"]
    total = result["total_tasks"]
    scores = result["scores"]

    # Header
    if status == "PASS":
        header = f"✅ QG-ROUTE PASS: {total} tasks, all fields complete, notation valid"
    elif status == "WARN":
        header = f"⚠️ QG-ROUTE WARN: {len(result['warnings'])} warnings detected"
    else:
        header = f"❌ QG-ROUTE FAIL: {len(result['blocking_issues'])} blocking issues"

    lines = [
        "═" * 80,
        header,
        "═" * 80,
        "",
        f"Total Tasks: {total}",
        f"Routing Quality Score: {scores['routing_quality']}",
        "",
        f"Completeness Score: {scores['completeness']} (weight: 0.50)",
        f"Notation Score: {scores['notation']} (weight: 0.20)",
        f"Constraint Score: {scores['constraint']} (weight: 0.30)",
        ""
    ]

    # Blocking issues
    if result["blocking_issues"]:
        lines.append("BLOCKING ISSUES:")
        for issue in result["blocking_issues"]:
            lines.append(f"  • {issue}")
        lines.append("")

    # Warnings
    if result["warnings"]:
        lines.append("WARNINGS:")
        for warning in result["warnings"]:
            lines.append(f"  • {warning}")
        lines.append("")

    # Auto-fixes
    if "fixes_applied" in result and result["fixes_applied"]:
        lines.append(f"AUTO-FIXES APPLIED: {len(result['fixes_applied'])} tasks")
        lines.append("")

    # Next action
    if status == "PASS":
        lines.append("✅ Proceed to Phase 4 (Enrichment)")
    elif status == "WARN":
        lines.append("⚠️ Proceeding with warnings. Review post-execution.")
    else:
        lines.append("❌ Return to Phase 2 (Routing) for resolution.")

    lines.append("═" * 80)

    return "\n".join(lines)

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="Validate routed tasks against QG-ROUTE quality gate")
    parser.add_argument("--run-id", help="Run ID (auto-loads from _temp/dispatch/runs/{id}/routed-tasks.json)")
    parser.add_argument("--tasks-file", help="Path to routed-tasks.json")
    parser.add_argument("--format", choices=["json", "report"], default="report", help="Output format")
    parser.add_argument("--auto-fix", action="store_true", help="Auto-fix VR.6 and VR.7 notation issues")

    args = parser.parse_args()

    # Determine tasks file path
    if args.tasks_file:
        tasks_file = Path(args.tasks_file)
    elif args.run_id:
        tasks_file = Path(f"_temp/dispatch/runs/{args.run_id}/routed-tasks.json")
    else:
        print("ERROR: Must provide --run-id or --tasks-file", file=sys.stderr)
        sys.exit(1)

    if not tasks_file.exists():
        print(f"ERROR: Tasks file not found: {tasks_file}", file=sys.stderr)
        sys.exit(1)

    # Load tasks
    with open(tasks_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        tasks = data.get("tasks", [])

    # Load valid domains
    valid_domains = load_valid_domains()

    # Validate
    result = validate_tasks(tasks, valid_domains, auto_fix=args.auto_fix)

    # Save auto-fixes back to file
    if args.auto_fix and result.get("fixes_applied"):
        data["tasks"] = tasks
        with open(tasks_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        print(f"Auto-fixes applied and saved to {tasks_file}", file=sys.stderr)

    # Output
    if args.format == "json":
        print(json.dumps(result, indent=2))
    else:
        print(format_report(result))

    # Exit code
    if result["status"] == "PASS":
        sys.exit(0)
    elif result["status"] == "WARN":
        sys.exit(2)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
