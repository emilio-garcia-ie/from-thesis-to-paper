#!/usr/bin/env sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
WHEEL=$(find "$ROOT" -maxdepth 2 -name 'fttp-*.whl' -type f | head -n 1)
if [ -z "$WHEEL" ]; then
  echo "FTTP install: no wheel was found beside this installer" >&2
  exit 1
fi
CHECKSUM=""
if [ -f "$ROOT/SHA256SUMS" ]; then
  CHECKSUM=$(awk -v name="$(basename "$WHEEL")" '$2 == name { print $1; exit }' "$ROOT/SHA256SUMS")
  if [ -z "$CHECKSUM" ]; then
    echo "FTTP install: wheel checksum is missing from SHA256SUMS" >&2
    exit 1
  fi
fi
if [ -n "$CHECKSUM" ]; then
  exec "${PYTHON:-python3}" "$ROOT/scripts/release_installer.py" --wheel "$WHEEL" --checksum "$CHECKSUM" "$@"
fi
exec "${PYTHON:-python3}" "$ROOT/scripts/release_installer.py" --wheel "$WHEEL" "$@"
