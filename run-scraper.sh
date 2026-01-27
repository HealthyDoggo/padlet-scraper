#!/bin/bash
# Wrapper script to run padlet-scraper without manually activating venv

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Check if venv exists
if [ ! -d "$SCRIPT_DIR/venv" ]; then
    echo "Error: Virtual environment not found."
    echo "Please run ./install.sh first"
    exit 1
fi

# Activate venv and run padlet-scraper with all arguments
source "$SCRIPT_DIR/venv/bin/activate"
padlet-scraper "$@"
