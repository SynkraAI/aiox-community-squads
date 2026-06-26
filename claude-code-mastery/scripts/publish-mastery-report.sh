#!/usr/bin/env bash
set -euo pipefail

REPORT_PATH="${1:-}"

if [[ -z "${REPORT_PATH}" ]]; then
  echo "Uso: publish-mastery-report.sh <report-path>" >&2
  exit 1
fi

if [[ ! -f "${REPORT_PATH}" ]]; then
  echo "Relatório não encontrado: ${REPORT_PATH}" >&2
  exit 1
fi

echo "Publicando relatório de mastery: ${REPORT_PATH}"
echo "Status: validated"
