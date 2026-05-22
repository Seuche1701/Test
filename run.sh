#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

PY=python3
if ! command -v "$PY" >/dev/null 2>&1; then
  PY=python
fi
if ! command -v "$PY" >/dev/null 2>&1; then
  echo "Python nicht gefunden. Bitte installiere Python 3.8+." >&2
  exit 1
fi

VENV=venv
if [ ! -d "$VENV" ]; then
  echo "Erstelle virtuelles Environment..."
  "$PY" -m venv "$VENV"
fi

# shellcheck source=/dev/null
. "$VENV/bin/activate"
pip install --upgrade pip
pip install -r requirements.txt

if [ -z "${DISPLAY:-}" ]; then
  if command -v xvfb-run >/dev/null 2>&1; then
    echo "Kein DISPLAY erkannt — starte mit xvfb-run."
    xvfb-run "$PY" main.py
  else
    echo "Kein DISPLAY gefunden und xvfb-run nicht verfügbar. Versuche, die App direkt zu starten..."
    "$PY" main.py || true
  fi
else
  "$PY" main.py
fi
