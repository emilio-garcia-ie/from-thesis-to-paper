#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
export PYTHONPATH="$ROOT/python${PYTHONPATH:+:${PYTHONPATH}}"
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
MODE="${1:-smoke}"
case "$MODE" in
  smoke) exec "$PY" -m pytest tests/ -m smoke -q ;;
  unit)  exec "$PY" -m pytest tests/ -q ;;
  integration) exec "$PY" -m pytest tests/integration -q ;;
  all)
    "$PY" -m pytest tests/ -m smoke -q
    exec "$PY" -m pytest tests/ -q
    ;;
  *) echo "Usage: $0 {smoke|unit|integration|all}" >&2; exit 1 ;;
esac
