#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SQUAD_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
REPO_ROOT="$(cd "${SQUAD_DIR}/../.." && pwd)"
WORKSPACE_ROOT="${WORKSPACE_ROOT:-${REPO_ROOT}/workspace}"
DOCS_DATA_ROOT="${REPO_ROOT}/docs/data"

usage() {
  cat <<'USAGE'
Usage:
  bootstrap-data-workspace.sh [business_slug] [--scaffold all|tpl1,tpl2] [--force]

Examples:
  bash squads/data/scripts/bootstrap-data-workspace.sh
  bash squads/data/scripts/bootstrap-data-workspace.sh aiox
  bash squads/data/scripts/bootstrap-data-workspace.sh aiox --scaffold clv-report,executive-report,cohorts/executive-summary
  bash squads/data/scripts/bootstrap-data-workspace.sh aiox --scaffold all --force
USAGE
}

business_slug=""
scaffold_targets=""
force=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help)
      usage
      exit 0
      ;;
    --scaffold)
      shift
      [[ $# -eq 0 ]] && { echo "error: --scaffold requires value" >&2; exit 1; }
      scaffold_targets="$1"
      ;;
    --force)
      force=1
      ;;
    *)
      if [[ -z "$business_slug" ]]; then
        business_slug="$1"
      else
        echo "error: unexpected argument '$1'" >&2
        usage
        exit 1
      fi
      ;;
  esac
  shift
done

created_dirs=0
created_files=0
warnings=0

mkdir_if_missing() {
  local dir="$1"
  if [[ ! -d "$dir" ]]; then
    mkdir -p "$dir"
    created_dirs=$((created_dirs + 1))
    echo "created_dir: $dir"
  fi
}

copy_if_needed() {
  local src="$1"
  local dst="$2"
  if [[ ! -f "$src" ]]; then
    warnings=$((warnings + 1))
    echo "warning: missing source template $src"
    return 0
  fi

  if [[ -f "$dst" && "$force" -ne 1 ]]; then
    return 0
  fi

  mkdir -p "$(dirname "$dst")"
  cp "$src" "$dst"
  created_files=$((created_files + 1))
  echo "write: $dst"
}

mkdir_if_missing "$WORKSPACE_ROOT"
mkdir_if_missing "$WORKSPACE_ROOT/businesses"
mkdir_if_missing "$WORKSPACE_ROOT/_templates"
mkdir_if_missing "$WORKSPACE_ROOT/_templates/analytics"
mkdir_if_missing "$WORKSPACE_ROOT/_templates/analytics/cohorts"
mkdir_if_missing "$DOCS_DATA_ROOT"

# Canonical analytics templates (template-first for workspace outputs)
declare -a ROOT_SRC_TEMPLATES=(
  "customer-360-tmpl.yaml"
  "clv-report-tmpl.yaml"
  "cohort-analysis-tmpl.yaml"
  "health-score-report-tmpl.yaml"
  "churn-alert-tmpl.yaml"
  "attribution-report-tmpl.yaml"
  "dmmm-tmpl.yaml"
  "executive-report-tmpl.yaml"
  "community-health-tmpl.yaml"
  "learning-outcomes-tmpl.yaml"
)

declare -a ROOT_DST_TEMPLATES=(
  "customer-360.yaml"
  "clv-report.yaml"
  "cohort-analysis.yaml"
  "health-score-report.yaml"
  "churn-alert.yaml"
  "attribution-report.yaml"
  "dmmm.yaml"
  "executive-report.yaml"
  "community-health.yaml"
  "learning-outcomes.yaml"
)

declare -a PACK_SRC_TEMPLATES=(
  "cohorts/segmentation-rfm-tmpl.yaml"
  "cohorts/learning-journey-tmpl.yaml"
  "cohorts/community-health-cohort-tmpl.yaml"
  "cohorts/student-health-score-tmpl.yaml"
  "cohorts/icp-deep-analysis-tmpl.yaml"
  "cohorts/executive-summary-tmpl.yaml"
)

declare -a PACK_DST_TEMPLATES=(
  "cohorts/segmentation-rfm.yaml"
  "cohorts/learning-journey.yaml"
  "cohorts/community-health.yaml"
  "cohorts/student-health-score.yaml"
  "cohorts/icp-deep-analysis.yaml"
  "cohorts/executive-summary.yaml"
)

for i in "${!ROOT_SRC_TEMPLATES[@]}"; do
  src="${SQUAD_DIR}/templates/${ROOT_SRC_TEMPLATES[$i]}"
  dst="${WORKSPACE_ROOT}/_templates/analytics/${ROOT_DST_TEMPLATES[$i]}"
  copy_if_needed "$src" "$dst"
done

for i in "${!PACK_SRC_TEMPLATES[@]}"; do
  src="${SQUAD_DIR}/templates/${PACK_SRC_TEMPLATES[$i]}"
  dst="${WORKSPACE_ROOT}/_templates/analytics/${PACK_DST_TEMPLATES[$i]}"
  copy_if_needed "$src" "$dst"
done

scaffold_template_to_business() {
  local template_ref="$1"
  local normalized="${template_ref%.yaml}"
  local src="${WORKSPACE_ROOT}/_templates/analytics/${normalized}.yaml"
  local dst="${WORKSPACE_ROOT}/businesses/${business_slug}/analytics/${normalized}.yaml"
  copy_if_needed "$src" "$dst"
}

if [[ -n "$business_slug" ]]; then
  mkdir_if_missing "${WORKSPACE_ROOT}/businesses/${business_slug}"
  mkdir_if_missing "${WORKSPACE_ROOT}/businesses/${business_slug}/analytics"
  mkdir_if_missing "${WORKSPACE_ROOT}/businesses/${business_slug}/analytics/cohorts"
  mkdir_if_missing "${WORKSPACE_ROOT}/businesses/${business_slug}/evidence"
  mkdir_if_missing "${DOCS_DATA_ROOT}/${business_slug}"

  if [[ -n "$scaffold_targets" ]]; then
    if [[ "$scaffold_targets" == "all" ]]; then
      for dst in "${ROOT_DST_TEMPLATES[@]}"; do
        scaffold_template_to_business "${dst%.yaml}"
      done
      for dst in "${PACK_DST_TEMPLATES[@]}"; do
        scaffold_template_to_business "${dst%.yaml}"
      done
    else
      IFS=',' read -r -a requested <<< "$scaffold_targets"
      for item in "${requested[@]}"; do
        normalized="${item%.yaml}"
        scaffold_template_to_business "$normalized"
      done
    fi
  else
    echo "info: business '${business_slug}' ready. No analytics templates scaffolded."
    echo "info: use --scaffold all or --scaffold clv-report,executive-report,cohorts/executive-summary"
  fi
fi

echo "bootstrap-data-workspace: created_dirs=${created_dirs} created_files=${created_files} warnings=${warnings}"
