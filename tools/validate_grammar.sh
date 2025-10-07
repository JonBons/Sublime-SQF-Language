#!/usr/bin/env bash
set -euo pipefail
if ! command -v xmllint >/dev/null 2>&1; then
  echo "xmllint not found (libxml2-utils). Install and retry." >&2
  exit 1
fi

# Smart file location detection
SQF_FILE=""
if [ -f "SQF.tmLanguage" ]; then
  SQF_FILE="SQF.tmLanguage"
  echo "Found SQF.tmLanguage in current directory"
elif [ -f "../SQF.tmLanguage" ]; then
  SQF_FILE="../SQF.tmLanguage"
  echo "Found SQF.tmLanguage in parent directory"
else
  echo "Error: SQF.tmLanguage not found in current or parent directory" >&2
  exit 1
fi

# Validate the XML file
xmllint --noout "$SQF_FILE"
echo "SQF.tmLanguage is well-formed XML."
