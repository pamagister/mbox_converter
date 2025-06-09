#!/bin/bash
# Shell script for mbox_converter
# Usage: Drag & drop an .mbox file onto this .sh file (in supporting file managers)
#        Or run via: ./mbox_converter.sh /path/to/file.mbox

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$SCRIPT_DIR/.venv"
MBOX_FILE="$1"

# Check if a file was provided
if [ -z "$MBOX_FILE" ]; then
  echo "[ERROR] Please provide an .mbox file (drag-and-drop or as an argument)."
  exit 1
fi

# Step 1: Create virtual environment if it doesn't exist
if [ ! -f "$VENV_DIR/bin/activate" ]; then
  echo "[INFO] Creating virtual environment at $VENV_DIR ..."
  python3 -m venv "$VENV_DIR"
fi

# Step 2: Activate virtual environment
# shellcheck disable=SC1090
source "$VENV_DIR/bin/activate"

# Step 3: Install dependencies if requirements.txt exists
if [ -f "$SCRIPT_DIR/requirements.txt" ]; then
  echo "[INFO] Installing dependencies ..."
  pip install -r "$SCRIPT_DIR/requirements.txt"
else
  echo "[WARNING] requirements.txt not found!"
fi

# Step 4: Run the CLI parser
echo "[INFO] Running parser..."
python -m mbox_converter.cli "$MBOX_FILE"

echo
echo "Done processing: $MBOX_FILE"
