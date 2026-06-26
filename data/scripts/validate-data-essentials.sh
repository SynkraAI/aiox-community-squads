#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SQUAD_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
REPO_ROOT="$(cd "${SQUAD_DIR}/../.." && pwd)"
WORKSPACE_ROOT="${WORKSPACE_ROOT:-${REPO_ROOT}/workspace}"

python3 - "${SQUAD_DIR}" "${REPO_ROOT}" "${WORKSPACE_ROOT}" <<'PY'
import os
import sys
from pathlib import Path

import yaml

squad_dir = Path(sys.argv[1])
repo_root = Path(sys.argv[2])
workspace_root = Path(sys.argv[3])

errors = []
warnings = []

required_scripts = [
    squad_dir / "scripts" / "bootstrap-data-workspace.sh",
    squad_dir / "scripts" / "validate-data-essentials.sh",
]

for path in required_scripts:
    if not path.exists():
        errors.append(f"missing script: {path.relative_to(repo_root)}")
    elif not os.access(path, os.X_OK):
        errors.append(f"script must be executable: {path.relative_to(repo_root)}")

for cfg_name in ("config.yaml", "squad.yaml"):
    cfg_path = squad_dir / cfg_name
    if not cfg_path.exists():
        errors.append(f"missing file: {cfg_path.relative_to(repo_root)}")
        continue

    cfg = yaml.safe_load(cfg_path.read_text(encoding="utf-8")) or {}
    ws = cfg.get("workspace_integration")
    if not isinstance(ws, dict):
        errors.append(f"{cfg_name}: missing workspace_integration block")
        continue

    if ws.get("level") != "workspace_first":
        errors.append(f"{cfg_name}: workspace_integration.level must be workspace_first")

    if ws.get("template_namespace") != "analytics":
        errors.append(f"{cfg_name}: template_namespace must be analytics")

    bootstrap = ws.get("bootstrap") or {}
    essentials = ws.get("essentials_validation") or {}
    if bootstrap.get("required") is not True:
        errors.append(f"{cfg_name}: bootstrap.required must be true")
    if bootstrap.get("script") != "scripts/bootstrap-data-workspace.sh":
        errors.append(f"{cfg_name}: bootstrap.script mismatch")
    if essentials.get("required") is not True:
        errors.append(f"{cfg_name}: essentials_validation.required must be true")
    if essentials.get("script") != "scripts/validate-data-essentials.sh":
        errors.append(f"{cfg_name}: essentials_validation.script mismatch")

    read_paths = ws.get("read_paths") or []
    write_paths = ws.get("write_paths") or []

    if not isinstance(read_paths, list) or not read_paths:
        errors.append(f"{cfg_name}: read_paths must be non-empty list")
    if not isinstance(write_paths, list) or not write_paths:
        errors.append(f"{cfg_name}: write_paths must be non-empty list")

    for rel in read_paths + write_paths:
        if rel == "workspace/domains/content/outputs/":
            errors.append(f"{cfg_name}: forbidden write path {rel}")
        path = repo_root / rel
        if not path.exists():
            errors.append(f"{cfg_name}: declared path not found: {rel}")

    allowed_workspace_writes = (
        "workspace/businesses/",
        "workspace/_templates/analytics/",
    )
    for rel in write_paths:
        if rel.startswith("workspace/") and not rel.startswith(allowed_workspace_writes):
            errors.append(
                f"{cfg_name}: workspace write path must be template-first or business-scoped: {rel}"
            )

    task_ids = {t.get("id") for t in (cfg.get("tasks") or []) if isinstance(t, dict)}
    if "load-workspace-context" not in task_ids:
        errors.append(f"{cfg_name}: task load-workspace-context must be registered")

required_templates = [
    "customer-360.yaml",
    "clv-report.yaml",
    "cohort-analysis.yaml",
    "health-score-report.yaml",
    "churn-alert.yaml",
    "attribution-report.yaml",
    "dmmm.yaml",
    "executive-report.yaml",
    "community-health.yaml",
    "learning-outcomes.yaml",
    "cohorts/segmentation-rfm.yaml",
    "cohorts/learning-journey.yaml",
    "cohorts/community-health.yaml",
    "cohorts/student-health-score.yaml",
    "cohorts/icp-deep-analysis.yaml",
    "cohorts/executive-summary.yaml",
]

for name in required_templates:
    path = workspace_root / "_templates" / "analytics" / name
    if not path.exists():
        errors.append(f"missing analytics template: {path.relative_to(repo_root)}")

context_task = squad_dir / "tasks" / "load-workspace-context.md"
if not context_task.exists():
    errors.append("missing task: squads/data/tasks/load-workspace-context.md")

workflow_checks = {
    "implement-customer-360.md": [
        "*workspace-preflight",
        "*workspace-context {slug}",
        "workspace/businesses/{slug}/analytics/",
        "docs/data/{slug}/",
        "workspace/_templates/analytics/",
    ],
    "create-churn-system.md": [
        "*workspace-preflight",
        "*workspace-context {slug}",
        "workspace/businesses/{slug}/analytics/",
        "docs/data/{slug}/",
        "workspace/_templates/analytics/",
    ],
    "implement-attribution.md": [
        "*workspace-preflight",
        "*workspace-context {slug}",
        "workspace/businesses/{slug}/analytics/",
        "docs/data/{slug}/",
        "workspace/_templates/analytics/",
    ],
    "cohort-analysis-workflow.md": [
        "*workspace-preflight",
        "*workspace-context {slug}",
        "workspace/businesses/{slug}/analytics/",
        "docs/data/{slug}/",
        "workspace/_templates/analytics/",
    ],
    "fix-completion-rate.md": [
        "*workspace-preflight",
        "*workspace-context {slug}",
        "workspace/businesses/{slug}/analytics/",
        "docs/data/{slug}/",
        "workspace/_templates/analytics/",
    ],
    "optimize-community-workflow.md": [
        "*workspace-preflight",
        "*workspace-context {slug}",
        "workspace/businesses/{slug}/analytics/",
        "docs/data/{slug}/",
        "workspace/_templates/analytics/",
    ],
    "cohorts-diagnostic.md": [
        "*workspace-preflight",
        "*workspace-context {slug}",
        "workspace/businesses/{slug}/analytics/cohorts/",
        "docs/data/{slug}/",
        "workspace/_templates/analytics/cohorts/",
        "segmentation-rfm.yaml",
        "learning-journey.yaml",
        "community-health.yaml",
        "student-health-score.yaml",
        "icp-deep-analysis.yaml",
        "executive-summary.yaml",
    ],
}

for file_name, tokens in workflow_checks.items():
    wf_path = squad_dir / "workflows" / file_name
    if not wf_path.exists():
        errors.append(f"missing workflow: squads/data/workflows/{file_name}")
        continue

    raw = wf_path.read_text(encoding="utf-8")
    for token in tokens:
        if token not in raw:
            errors.append(f"workflow {file_name} missing token: {token}")

readme = squad_dir / "README.md"
if readme.exists():
    readme_raw = readme.read_text(encoding="utf-8")
    for token in (
        "bootstrap-data-workspace.sh",
        "validate-data-essentials.sh",
        "*workspace-preflight",
        "*workspace-context {slug}",
        "docs/data/{slug}/",
        "analytics/cohorts/",
    ):
        if token not in readme_raw:
            errors.append(f"README.md missing token: {token}")
else:
    errors.append("missing file: squads/data/README.md")

data_chief = squad_dir / "agents" / "data-chief.md"
if data_chief.exists():
    chief_raw = data_chief.read_text(encoding="utf-8")
    for token in (
        "*workspace-preflight",
        "*workspace-context {slug}",
        "scripts/bootstrap-data-workspace.sh",
        "scripts/validate-data-essentials.sh",
        "load-workspace-context.md",
        "workspace/_templates/analytics/",
        "workspace/_templates/analytics/cohorts/",
        "docs/data/{slug}/",
    ):
        if token not in chief_raw:
            errors.append(f"data-chief.md missing token: {token}")
else:
    errors.append("missing file: squads/data/agents/data-chief.md")

if not (repo_root / "docs" / "data").exists():
    errors.append("missing docs/data directory")

if errors:
    print("validate-data-essentials: FAIL")
    for item in errors:
        print(f"  - {item}")
    for item in warnings:
        print(f"  - warning: {item}")
    sys.exit(1)

print("validate-data-essentials: PASS")
for item in warnings:
    print(f"  - warning: {item}")
PY
