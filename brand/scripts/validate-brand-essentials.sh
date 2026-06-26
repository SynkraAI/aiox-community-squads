#!/usr/bin/env bash
set -euo pipefail

export LC_ALL=C
export LANG=C

ROOT="${1:-squads/brand}"
fail=0

echo "== Brand Essentials =="

echo "-- check: workspace integration contract"
missing_workspace_contract=$(for cfg in "$ROOT"/config.yaml "$ROOT"/squad.yaml; do
  if [ ! -f "$cfg" ]; then
    continue
  fi
  name="$(basename "$cfg")"
  rg -q '^workspace_integration:' "$cfg" || echo "$name -> missing workspace_integration block"
  rg -q 'level:\s*workspace_first' "$cfg" || echo "$name -> workspace_integration.level must be workspace_first"
  rg -Fq 'template_namespace: brand' "$cfg" || echo "$name -> missing template_namespace brand"
  rg -Fq 'canonical_outputs_root: workspace/businesses/{brand_name}/L2-tactical/brand/' "$cfg" || echo "$name -> missing canonical_outputs_root"
  rg -Fq 'custom_outputs_root: docs/brand/{brand_name}/' "$cfg" || echo "$name -> missing custom_outputs_root"
  rg -Fq 'script: "scripts/bootstrap-brand-workspace.sh"' "$cfg" || echo "$name -> missing bootstrap script mapping"
  rg -Fq 'script: "scripts/validate-brand-essentials.sh"' "$cfg" || echo "$name -> missing essentials_validation script mapping"
done)
if [ -n "${missing_workspace_contract}" ]; then
  echo "FAIL workspace integration contract drift:"
  echo "${missing_workspace_contract}"
  fail=1
else
  echo "PASS"
fi

echo "-- check: task references"
missing_tasks=$(perl -ne 'if(/^\s*-\s*task:\s*([a-z0-9\-]+)\.md/){print "$1\n"}' "$ROOT"/workflows/*.yaml \
  | sort -u | while read -r id; do [ -f "$ROOT/tasks/$id.md" ] || echo "$id"; done)
if [ -n "${missing_tasks}" ]; then
  echo "FAIL missing tasks:"
  echo "${missing_tasks}"
  fail=1
else
  echo "PASS"
fi

echo "-- check: workflow executor references"
missing_agents=$(perl -ne 'if(/^\s*executor:\s*([a-z0-9\-]+)/){print "$1\n"}' "$ROOT"/workflows/*.yaml \
  | sort -u | while read -r id; do [ -f "$ROOT/agents/$id.md" ] || echo "$id"; done)
if [ -n "${missing_agents}" ]; then
  echo "FAIL missing executor agents:"
  echo "${missing_agents}"
  fail=1
else
  echo "PASS"
fi

echo "-- check: orchestrator reference"
orchestrator="brand-chief"
if [ ! -f "$ROOT/agents/$orchestrator.md" ]; then
  echo "FAIL missing/invalid orchestrator: ${orchestrator}"
  fail=1
else
  echo "PASS"
fi

echo "-- check: workflow call references"
missing_workflows=$(perl -ne 'if(/^\s*workflow:\s*(wf-[a-z0-9\-]+)/){print "$1\n"}' "$ROOT"/workflows/*.yaml \
  | sort -u | while read -r id; do [ -f "$ROOT/workflows/$id.yaml" ] || echo "$id"; done)
if [ -n "${missing_workflows}" ]; then
  echo "FAIL workflow_call references unknown workflows:"
  echo "${missing_workflows}"
  fail=1
else
  echo "PASS"
fi

echo "-- check: task dependency references"
missing_dep_refs=$(perl -ne '
  if(/\*\*Dependencies:\*\*/){
    while(/\[([^\]]+)\]/g){
      for $id (split(/,\s*/, $1)){
        $id =~ s/^[`\s]+|[`\s]+$//g;
        print "$id\n" if $id =~ /^[a-z0-9][a-z0-9\-]*$/;
      }
    }
  }' "$ROOT"/tasks/*.md | sort -u | while read -r id; do
    [ -f "$ROOT/tasks/$id.md" ] || [ -f "$ROOT/workflows/$id.yaml" ] || echo "$id";
  done)
if [ -n "${missing_dep_refs}" ]; then
  echo "FAIL dependency refs without task/workflow:"
  echo "${missing_dep_refs}"
  fail=1
else
  echo "PASS"
fi

echo "-- check: load-workspace-context task"
if [ ! -f "$ROOT/tasks/load-workspace-context.md" ]; then
  echo "FAIL missing task: $ROOT/tasks/load-workspace-context.md"
  fail=1
else
  echo "PASS"
fi

echo "-- check: workflow output contract in tasks"
missing_output_contract=$(for task in "$ROOT"/tasks/*.md; do
  name="$(basename "$task" .md)"
  if rg -n 'workspace/businesses/\{brand_name\}/brand/|workspace/businesses/\{\{brand_name\}\}/brand/|workspace/_templates/brand/' "$task" >/dev/null 2>&1; then
    echo "$name -> legacy brand path reference"
  fi
done)
if [ -n "${missing_output_contract}" ]; then
  echo "FAIL workflow/task output contract drift:"
  echo "${missing_output_contract}"
  fail=1
else
  echo "PASS"
fi

echo "-- check: canonical workspace output paths"
bad_output_paths=$(rg -n 'workspace/businesses/\{\{brand_name\}\}/brand/|workspace/businesses/\{brand_name\}/brand/|workspace/_templates/brand/' "$ROOT"/workflows || true)
if [ -n "${bad_output_paths}" ]; then
  echo "FAIL non-canonical output paths:"
  echo "${bad_output_paths}"
  fail=1
else
  echo "PASS"
fi

echo "-- check: canonical template roots exist"
for template_root in \
  workspace/_templates/business-template \
  workspace/_templates/business-template/L2-tactical/brand; do
  if [ ! -e "$template_root" ]; then
    echo "FAIL missing template root: $template_root"
    fail=1
  fi
done
if [ "$fail" -eq 0 ]; then
  echo "PASS"
fi

echo "-- check: workflow_call required-input coverage"
missing_workflow_call_inputs=$(perl -0777 -ne '
  while(/workflow_call:\s*\n\s*workflow:\s*(wf-[a-z0-9\-]+)\s*\n\s*inputs:\s*\n((?:\s*-\s*[a-z0-9_]+\s*\n)+)/g){
    $called = $1;
    $block = $2;
    @ins = ();
    while($block =~ /-\s*([a-z0-9_]+)/g){ push @ins, $1; }
    print "$ARGV\t$called\t" . join(",", @ins) . "\n";
  }
' "$ROOT"/workflows/*.yaml | while IFS=$'\t' read -r caller called call_inputs; do
  called_file="$ROOT/workflows/$called.yaml"
  [ -f "$called_file" ] || continue
  req_inputs=$(perl -ne '
    if (/^inputs:\s*$/) { $in_inputs = 1; next; }
    if ($in_inputs && /^phases:\s*$/) { $in_inputs = 0; }
    if ($in_inputs && /^\s*required:\s*$/) { $in_req = 1; next; }
    if ($in_inputs && /^\s*optional:\s*$/) { $in_req = 0; next; }
    if ($in_inputs && $in_req && /^\s*-\s*name:\s*([a-z0-9_]+)/) { print "$1\n"; }
  ' "$called_file")
  IFS=',' read -r -a declared <<< "${call_inputs}"
  for req in ${req_inputs}; do
    found=0
    for inp in "${declared[@]}"; do
      if [ "$inp" = "$req" ]; then
        found=1
        break
      fi
    done
    if [ "$found" -eq 0 ]; then
      echo "$(basename "$caller") -> $called missing required input '$req'"
    fi
  done
done)
if [ -n "${missing_workflow_call_inputs}" ]; then
  echo "FAIL workflow_call input contract drift:"
  echo "${missing_workflow_call_inputs}"
  fail=1
else
  echo "PASS"
fi

echo "-- check: workflow preflight contract"
missing_workflow_preflight=$(for wf in "$ROOT"/workflows/*.yaml; do
  file="$(basename "$wf")"
  rg -q '^workspace_contract:' "$wf" || echo "$file -> missing workspace_contract"
  rg -q 'required_preflight:' "$wf" || echo "$file -> missing required_preflight"
  rg -q 'context_task:\s*load-workspace-context' "$wf" || echo "$file -> missing context_task load-workspace-context"
  rg -q 'task:\s*load-workspace-context\.md' "$wf" || echo "$file -> missing workspace context task call"
  rg -Fq 'bootstrap-brand-workspace.sh {{brand_name}}' "$wf" || echo "$file -> missing bootstrap preflight command"
  rg -Fq 'validate-brand-essentials.sh' "$wf" || echo "$file -> missing essentials preflight command"
done)
if [ -n "${missing_workflow_preflight}" ]; then
  echo "FAIL workflow preflight contract drift:"
  echo "${missing_workflow_preflight}"
  fail=1
else
  echo "PASS"
fi

echo "-- check: bootstrap script coverage"
bootstrap="$ROOT/scripts/bootstrap-brand-workspace.sh"
if [ ! -f "$bootstrap" ]; then
  echo "FAIL missing bootstrap script: $bootstrap"
  fail=1
elif [ ! -x "$bootstrap" ]; then
  echo "FAIL bootstrap script is not executable: $bootstrap"
  fail=1
else
  missing_bootstrap_dirs=$(for d in naming foundations positioning narrative activation; do
    rg -Fq "\${root}/$d" "$bootstrap" || echo "$d"
  done)
  if [ -n "${missing_bootstrap_dirs}" ]; then
    echo "FAIL bootstrap script coverage drift:"
    if [ -n "${missing_bootstrap_dirs}" ]; then
      echo " - missing canonical directories:"
      echo "${missing_bootstrap_dirs}"
    fi
    fail=1
  else
    echo "PASS"
  fi
fi

echo "-- check: canonical agent handles in tasks"
known_agents=$(for f in "$ROOT"/agents/*.md; do basename "$f" .md; done | tr '\n' ' ')
unknown_handles=$(rg -No '@[a-z0-9\-]+' "$ROOT"/tasks/*.md | sed 's/.*://' | sort -u | while read -r handle; do
  id="${handle#@}"
  case " ${known_agents} " in
    *" ${id} "*) ;;
    *) echo "${handle}" ;;
  esac
done)
if [ -n "${unknown_handles}" ]; then
  echo "FAIL unknown @handles in tasks:"
  echo "${unknown_handles}"
  fail=1
else
  echo "PASS"
fi

echo "-- check: veto conditions in all tasks"
missing_veto=$(for f in "$ROOT"/tasks/*.md; do rg -q '^## Veto Conditions' "$f" || echo "$f"; done)
if [ -n "${missing_veto}" ]; then
  echo "FAIL tasks without Veto Conditions:"
  echo "${missing_veto}"
  fail=1
else
  echo "PASS"
fi

echo "-- check: bootstrap command in brand-chief"
if ! rg -q '\*bootstrap-zero' "$ROOT"/agents/brand-chief.md; then
  echo "FAIL brand-chief missing *bootstrap-zero command"
  fail=1
else
  echo "PASS"
fi

echo "-- check: workspace commands in brand-chief"
missing_brand_chief_tokens=$(for token in "*workspace-preflight" "*workspace-context" "load-workspace-context.md" "validate-brand-essentials.sh"; do
  rg -Fq "$token" "$ROOT"/agents/brand-chief.md || echo "$token"
done)
if [ -n "${missing_brand_chief_tokens}" ]; then
  echo "FAIL brand-chief missing workspace-first tokens:"
  echo "${missing_brand_chief_tokens}"
  fail=1
else
  echo "PASS"
fi

echo "-- check: workspace commands in README"
missing_readme_tokens=$(for token in "*workspace-preflight" "*workspace-context" "load-workspace-context" "validate-brand-essentials.sh"; do
  rg -Fq "$token" "$ROOT"/README.md || echo "$token"
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
