#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-squads/etl-ops}"
fail=0

echo "== ETL-OPS Essentials =="

config_files=()
for cfg in "$ROOT"/config.yaml "$ROOT"/squad.yaml; do
  if [ -f "$cfg" ]; then
    config_files+=("$cfg")
  fi
done

if [ "${#config_files[@]}" -eq 0 ]; then
  echo "FAIL no squad config found under $ROOT"
  exit 1
fi

echo "-- check: workspace integration contract"
missing_workspace_contract=$(for cfg in "${config_files[@]}"; do
  name="$(basename "$cfg")"
  rg -q '^workspace_integration:' "$cfg" || echo "$name -> missing workspace_integration block"
  rg -q 'level:\s*workspace_first' "$cfg" || echo "$name -> workspace_integration.level must be workspace_first"
  rg -Fq 'template_namespace: etl' "$cfg" || echo "$name -> missing template_namespace etl"
  rg -Fq 'canonical_outputs_root: workspace/businesses/{slug}/etl/' "$cfg" || echo "$name -> missing canonical_outputs_root"
  rg -Fq 'custom_outputs_root: docs/etl/{slug}/' "$cfg" || echo "$name -> missing custom_outputs_root"
  rg -Fq 'legacy_outputs_root: outputs/etl/{run_id}/' "$cfg" || echo "$name -> missing legacy_outputs_root"
  rg -Fq 'script: "scripts/bootstrap-etl-workspace.sh"' "$cfg" || echo "$name -> missing bootstrap script mapping"
  rg -Fq 'script: "scripts/validate-etl-essentials.sh"' "$cfg" || echo "$name -> missing essentials_validation script mapping"
done)
if [ -n "${missing_workspace_contract}" ]; then
  echo "FAIL workspace integration contract drift:"
  echo "${missing_workspace_contract}"
  fail=1
else
  echo "PASS"
fi

echo "-- check: required tasks"
missing_tasks=$(for t in process compile enrich summarize-book extract-keyframes load-workspace-context; do
  [ -f "$ROOT/tasks/$t.md" ] || echo "$t"
done)
if [ -n "${missing_tasks}" ]; then
  echo "FAIL missing tasks:"
  echo "${missing_tasks}"
  fail=1
else
  echo "PASS"
fi

echo "-- check: task catalog registration"
missing_task_catalog=$(for cfg in "${config_files[@]}"; do
  name="$(basename "$cfg")"
  rg -q 'id:\s*load-workspace-context' "$cfg" || echo "$name -> load-workspace-context not registered"
done)
if [ -n "${missing_task_catalog}" ]; then
  echo "FAIL task catalog drift:"
  echo "${missing_task_catalog}"
  fail=1
else
  echo "PASS"
fi

echo "-- check: required agents"
missing_agents=$(for a in etl-chief etl-extractor etl-transformer; do
  [ -f "$ROOT/agents/$a.md" ] || echo "$a"
done)
if [ -n "${missing_agents}" ]; then
  echo "FAIL missing agents:"
  echo "${missing_agents}"
  fail=1
else
  echo "PASS"
fi

echo "-- check: scripts"
bootstrap="$ROOT/scripts/bootstrap-etl-workspace.sh"
validator="$ROOT/scripts/validate-etl-essentials.sh"
if [ ! -f "$bootstrap" ]; then
  echo "FAIL missing bootstrap script: $bootstrap"
  fail=1
elif [ ! -x "$bootstrap" ]; then
  echo "FAIL bootstrap script is not executable: $bootstrap"
  fail=1
fi
if [ ! -f "$validator" ]; then
  echo "FAIL missing validator script: $validator"
  fail=1
elif [ ! -x "$validator" ]; then
  echo "FAIL validator script is not executable: $validator"
  fail=1
fi
if [ "$fail" -eq 0 ]; then
  echo "PASS"
fi

echo "-- check: template namespace coverage"
missing_templates=$(for t in workspace-context.yaml source-intake.yaml etl-run-envelope.yaml artifact-index.yaml; do
  [ -f "workspace/_templates/etl/$t" ] || echo "$t"
done)
if [ -n "${missing_templates}" ]; then
  echo "FAIL missing etl templates:"
  echo "${missing_templates}"
  fail=1
else
  echo "PASS"
fi

echo "-- check: bootstrap template refs"
missing_bootstrap_template_refs=$(for t in workspace-context.yaml source-intake.yaml etl-run-envelope.yaml artifact-index.yaml; do
  rg -Fq "\${tmpl_root}/$t" "$bootstrap" || echo "$t"
done)
if [ -n "${missing_bootstrap_template_refs}" ]; then
  echo "FAIL bootstrap template coverage drift:"
  echo "${missing_bootstrap_template_refs}"
  fail=1
else
  echo "PASS"
fi

echo "-- check: process task preflight tokens"
missing_process_tokens=$(for token in "load-workspace-context.md" "bootstrap-etl-workspace.sh" "validate-etl-essentials.sh"; do
  rg -Fq "$token" "$ROOT/tasks/process.md" || echo "$token"
done)
if [ -n "${missing_process_tokens}" ]; then
  echo "FAIL process task missing workspace-first tokens:"
  echo "${missing_process_tokens}"
  fail=1
else
  echo "PASS"
fi

echo "-- check: etl-chief workspace commands"
missing_chief_tokens=$(for token in "*workspace-preflight" "*workspace-context" "load-workspace-context.md" "validate-etl-essentials.sh"; do
  rg -Fq "$token" "$ROOT/agents/etl-chief.md" || echo "$token"
done)
if [ -n "${missing_chief_tokens}" ]; then
  echo "FAIL etl-chief missing workspace-first tokens:"
  echo "${missing_chief_tokens}"
  fail=1
else
  echo "PASS"
fi

echo "-- check: README workspace commands"
missing_readme_tokens=$(for token in "*workspace-preflight" "*workspace-context" "load-workspace-context" "validate-etl-essentials.sh"; do
  rg -Fq "$token" "$ROOT/README.md" || echo "$token"
done)
if [ -n "${missing_readme_tokens}" ]; then
  echo "FAIL README missing workspace-first tokens:"
  echo "${missing_readme_tokens}"
  fail=1
else
  echo "PASS"
fi

if [ "$fail" -ne 0 ]; then
  echo "RESULT: FAIL"
  exit 1
fi

echo "RESULT: PASS"
