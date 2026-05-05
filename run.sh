#!/bin/zsh
set -e

cd "$(dirname "$0")"

if [ ! -d ".venv" ]; then
    echo "Setting up virtual environment..."
    python3 -m venv .venv
    .venv/bin/pip install -r requirements.txt --quiet
    echo "Done."
fi

exec .venv/bin/python3 main.py
