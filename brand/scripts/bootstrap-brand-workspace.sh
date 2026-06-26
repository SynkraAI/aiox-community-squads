#!/usr/bin/env bash
set -euo pipefail

if [ $# -lt 1 ]; then
  echo "Usage: $0 <brand_slug> [--force]"
  exit 1
fi

brand_slug="$1"
force="${2:-}"

root="workspace/businesses/${brand_slug}/L2-tactical/brand"
tmpl_root="workspace/_templates/business-template/L2-tactical/brand"
context_tmpl="workspace/_templates/etl/workspace-context.yaml"

mkdir -p \
  "${root}" \
  "${root}/naming" \
  "${root}/foundations" \
  "${root}/positioning" \
  "${root}/narrative" \
  "${root}/activation"

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

if [ -f "${tmpl_root}/brand-platform.yaml" ]; then
  copy_template "${tmpl_root}/brand-platform.yaml" "${root}/brand-platform.yaml"
fi

if [ -f "${tmpl_root}/positioning.yaml" ]; then
  copy_template "${tmpl_root}/positioning.yaml" "${root}/positioning.yaml"
fi

if [ -f "${context_tmpl}" ]; then
  copy_template "${context_tmpl}" "${root}/workspace-context.yaml"
fi

echo "bootstrap complete: ${root}"
