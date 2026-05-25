#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
PY="${ROOT}/.venv/bin/python"
[[ -x "$PY" ]] || PY=python3
MODE="${1:-smoke}"
case "$MODE" in
  smoke) exec "$PY" -m pytest tests/test_config.py -m smoke -q ;;
  unit)  exec "$PY" -m pytest tests/test_config.py -q ;;
  integration) echo "integration: no tests in framework repo (run in user workspace)"; exit 0 ;;
  all)
    "$PY" -m pytest tests/test_config.py -m smoke -q
    exec "$PY" -m pytest tests/test_config.py -q
    ;;
  *) echo "Usage: $0 {smoke|unit|integration|all}" >&2; exit 1 ;;
esac
