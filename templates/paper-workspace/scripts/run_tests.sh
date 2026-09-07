#!/usr/bin/env bash
# Paper workspace test runner.
# Usage: ./scripts/run_tests.sh smoke | unit | integration | all
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

MODE="${1:-smoke}"

# Locate fttp Python package (sibling framework clone or embedded copy).
_fttp_python=""
for _candidate in \
  "${ROOT}/../from-thesis-to-paper/python" \
  "${ROOT}/from-thesis-to-paper/python" \
  "${FTTP_FRAMEWORK_ROOT:-}/python"; do
  if [[ -n "${_candidate}" && -d "${_candidate}/fttp" ]]; then
    _fttp_python="${_candidate}"
    break
  fi
done

if [[ -z "${_fttp_python}" ]]; then
  echo "FAIL: fttp package not found. Clone from-thesis-to-paper next to this workspace" >&2
  echo "      or set FTTP_FRAMEWORK_ROOT=/path/to/from-thesis-to-paper" >&2
  exit 1
fi

if [[ -n "${_fttp_python}" ]]; then
  export PYTHONPATH="${_fttp_python}${PYTHONPATH:+:${PYTHONPATH}}"
fi

if [[ ! -f "${ROOT}/fttp.config.json" ]]; then
  echo "FAIL: missing fttp.config.json at workspace root" >&2
  echo "hint: complete SA0 onboarding and replace {{WORKSPACE_SLUG}} placeholders" >&2
  exit 1
fi

if [[ -n "${FTTP_PYTHON:-}" ]]; then
  PY="$FTTP_PYTHON"
elif [[ -x "${ROOT}/.venv/bin/python" ]]; then
  PY="${ROOT}/.venv/bin/python"
else
  PY="python3"
fi
if [[ ! -x "$PY" ]] && ! command -v "$PY" >/dev/null 2>&1; then
  echo "FAIL: Python interpreter not found: $PY" >&2
  exit 1
fi

run_pytest() {
  local target="$1"
  local marker="${2:-}"
  if [[ ! -d "$ROOT/$target" ]]; then
    echo "FAIL: required test directory is missing: $ROOT/$target" >&2
    return 1
  fi
  if [[ -n "$marker" ]]; then
    "$PY" -m pytest "$ROOT/$target" -m "$marker" -q
  else
    "$PY" -m pytest "$ROOT/$target" -q
  fi
}

case "$MODE" in
  smoke)
    run_pytest tests smoke
    ;;
  unit|integration|all)
    case "$MODE" in
      unit)      run_pytest tests/unit ;;
      integration) run_pytest tests/integration ;;
      all)       run_pytest tests ;;
    esac
    ;;
  *)
    echo "Usage: $0 [smoke|unit|integration|all]" >&2
    exit 2
    ;;
esac
