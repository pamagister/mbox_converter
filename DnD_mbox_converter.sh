#!/bin/bash

# Batch file for Poetry-based mbox_converter
# Usage: ./run-mbox-converter.sh path/to/file.mbox

# Get the full path of the .mbox file
MBOX_FILE="$1"

if [[ -z "$MBOX_FILE" ]]; then
  echo "[ERROR] Please pass an .mbox file as argument."
  echo "Usage: ./run-mbox-converter.sh /path/to/example.mbox"
  exit 1
fi

# Move to the script's directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR" || exit 1

# Check if Poetry is installed
if ! command -v poetry &> /dev/null; then
  echo "[ERROR] Poetry is not installed. Please install Poetry first:"
  echo "https://python-poetry.org/docs/#installation"
  exit 1
fi

# Install dependencies (if not already installed)
echo "[INFO] Installing dependencies via Poetry ..."
poetry install --no-interaction --no-root

# Run the script
echo "[INFO] Running mbox_converter ..."
poetry run python -m mbox_converter.cli "$MBOX_FILE"

echo
echo "Done processing: $MBOX_FILE"
