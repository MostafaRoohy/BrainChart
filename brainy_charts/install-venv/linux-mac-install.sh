#!/bin/bash

if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo "Virtual environment created."
fi

source .venv/bin/activate

pip install -r requirements.txt
# pip install .