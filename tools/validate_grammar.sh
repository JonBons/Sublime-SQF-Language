#!/usr/bin/env bash
set -euo pipefail
if ! command -v xmllint >/dev/null 2>&1; then
  echo "xmllint not found (libxml2-utils). Install and retry." >&2
  exit 1
fi
xmllint --noout SQF.tmLanguage
echo "SQF.tmLanguage is well-formed XML."
