#!/usr/bin/env bash
# Run the maintainer-only FRAMEWORK_SMOKE walkthrough in a disposable workspace.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PY="${FTTP_PYTHON:-python3}"
TMP_BASE="${TMPDIR:-/tmp}"
PARENT="${FTTP_SMOKE_PARENT:-$(mktemp -d "${TMP_BASE%/}/fttp-framework-smoke-XXXXXX")}"
SLUG="fttp-framework-smoke"
WORKSPACE="$PARENT/$SLUG"
PIPELINE_LOG="$PARENT/pipeline.log"

if [[ ! -x "$PY" ]] && ! command -v "$PY" >/dev/null 2>&1; then
  echo "FAIL: Python interpreter not found: $PY" >&2
  exit 1
fi
if [[ -e "$WORKSPACE" ]]; then
  echo "FAIL: disposable workspace already exists: $WORKSPACE" >&2
  exit 1
fi

export PYTHONPATH="$ROOT/python${PYTHONPATH:+:$PYTHONPATH}"

"$PY" -m fttp scaffold --slug "$SLUG" --parent "$PARENT"

(
  cd "$WORKSPACE"
  "$PY" -m fttp doctor
)

if (
  cd "$WORKSPACE"
  "$PY" -m fttp pipeline
) >"$PIPELINE_LOG" 2>&1; then
  echo "FAIL: an unconfigured pipeline unexpectedly succeeded" >&2
  exit 1
fi
if ! grep -Eqi 'tables' "$PIPELINE_LOG"; then
  echo "FAIL: placeholder pipeline did not report the tables stage" >&2
  exit 1
fi

printf '\nFRAMEWORK_SMOKE_EDIT_SENTINEL\n' >> "$WORKSPACE/README.md"
README_SHA="$(shasum -a 256 "$WORKSPACE/README.md" | awk '{print $1}')"
"$PY" -m fttp scaffold --slug "$SLUG" --parent "$PARENT" --force
if [[ "$(shasum -a 256 "$WORKSPACE/README.md" | awk '{print $1}')" != "$README_SHA" ]]; then
  echo "FAIL: --force changed an existing README.md" >&2
  exit 1
fi

printf 'FRAMEWORK_SMOKE OK\n'
printf 'workspace=%s\n' "$WORKSPACE"
printf 'pipeline_log=%s\n' "$PIPELINE_LOG"
printf 'doctor_exit=0 pipeline_exit=1 force_exit=0 readme_preserved=yes\n'
