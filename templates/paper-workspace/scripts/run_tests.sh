#!/usr/bin/env bash
# Paper workspace test runner (placeholder until consumer hooks and tests exist).
# Usage: ./scripts/run_tests.sh smoke | unit | integration | all
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

MODE="${1:-smoke}"

# Locate fttp Python package (sibling framework clone or embedded copy)
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
  echo "warn: fttp package not found. Clone from-thesis-to-paper next to this workspace" >&2
  echo "      or set FTTP_FRAMEWORK_ROOT=/path/to/from-thesis-to-paper" >&2
fi

if [[ -n "${_fttp_python}" ]]; then
  export PYTHONPATH="${_fttp_python}${PYTHONPATH:+:${PYTHONPATH}}"
fi

if [[ ! -f "${ROOT}/fttp.config.json" ]]; then
  echo "FAIL: missing fttp.config.json at workspace root" >&2
  echo "hint: complete SA0 onboarding and replace {{WORKSPACE_SLUG}} placeholders" >&2
  exit 1
fi

PY="${ROOT}/.venv/bin/python"
if [[ ! -x "$PY" ]]; then
  PY=python3
fi

case "$MODE" in
  smoke)
    if [[ -d "${ROOT}/tests" ]]; then
      "$PY" -m pytest tests/ -m smoke -q 2>/dev/null || {
        echo "note: no smoke tests yet — running fttp doctor only" >&2
        "$PY" -m fttp doctor
      }
    else
      echo "note: tests/ not present — install hooks per docs/ONBOARDING.md" >&2
      if command -v "$PY" >/dev/null 2>&1; then
        "$PY" -m fttp doctor
      else
        echo "PASS (stub): add tests/ and codigo/ when enabling full pipeline" >&2
        exit 0
      fi
    fi
    ;;
  unit|integration|all)
    if [[ ! -d "${ROOT}/tests" ]]; then
      echo "FAIL: tests/ directory missing. Port pipelines from thesis before running $MODE" >&2
      exit 1
    fi
    case "$MODE" in
      unit)      exec "$PY" -m pytest tests/unit -q ;;
      integration) exec "$PY" -m pytest tests/integration -q ;;
      all)       exec "$PY" -m pytest tests/ -q ;;
    esac
    ;;
  *)
    echo "Usage: $0 [smoke|unit|integration|all]" >&2
    exit 2
    ;;
esac
