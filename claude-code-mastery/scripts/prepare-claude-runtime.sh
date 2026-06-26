#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="${1:-$(pwd)}"

echo "Preparando runtime Claude Code em: ${ROOT_DIR}"

mkdir -p "${ROOT_DIR}/.claude" "${ROOT_DIR}/.claude/hooks"

if [[ ! -f "${ROOT_DIR}/.claude/settings.json" ]]; then
  cat > "${ROOT_DIR}/.claude/settings.json" <<'JSON'
{
  "permissions": {
    "deny": [
      "Read(./.env)",
      "Read(./.env.*)",
      "Bash(rm -rf *)"
    ],
    "allow": [],
    "defaultMode": "acceptEdits"
  }
}
JSON
fi

echo "Runtime base preparado."
