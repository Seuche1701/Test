#!/usr/bin/env bash
set -euo pipefail

# Build script to create a distributable directory using PyInstaller.
# Usage: ./build.sh

PYTHON=${PYTHON:-python3}
VENV_DIR=.venv_build

echo "Creating virtual env in ${VENV_DIR}..."
$PYTHON -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"
pip install --upgrade pip
pip install pyinstaller

echo "Running PyInstaller... (this may take a minute)"
# Use --onedir to keep data.db next to executable for persistence
pyinstaller --noconfirm --onedir --windowed --name TaschengeldApp main.py

echo "Copying runtime README and requirements to dist/TaschengeldApp..."
DIST_DIR=dist/TaschengeldApp
mkdir -p "$DIST_DIR"
cp README.md "$DIST_DIR/" || true
cp requirements.txt "$DIST_DIR/" || true

echo "Build complete. Find your app in dist/TaschengeldApp/"
deactivate
