#!/usr/bin/env bash
set -euo pipefail

if [ $# -lt 1 ]; then
  echo "Usage: $0 <business_slug> [--force]"
  exit 1
fi

business_slug="$1"
force="${2:-}"

root="workspace/businesses/${business_slug}/etl"
tmpl_root="workspace/_templates/etl"

mkdir -p \
  "${root}" \
  "${root}/runs" \
  "${root}/raw" \
  "${root}/clean" \
  "${root}/chunks" \
  "${root}/keyframes" \
  "${root}/compiled" \
  "${root}/enriched" \
  "${root}/evidence"

copy_template() {
  local src="$1"
  local dst="$2"
  if [ -f "$dst" ] && [ "$force" != "--force" ]; then
    echo "skip (exists): $dst"
    return 0
  fi
  cp "$src" "$dst"
  echo "write: $dst"
}

copy_template "${tmpl_root}/workspace-context.yaml" "${root}/workspace-context.yaml"
copy_template "${tmpl_root}/source-intake.yaml" "${root}/source-intake.yaml"
copy_template "${tmpl_root}/etl-run-envelope.yaml" "${root}/etl-run-envelope.yaml"
copy_template "${tmpl_root}/artifact-index.yaml" "${root}/artifact-index.yaml"

echo "bootstrap complete: ${root}"
