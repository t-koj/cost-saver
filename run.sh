#!/usr/bin/env bash
cd "$(dirname "$0")"
export PYTHONPATH=".:src:ext:$PYTHONPATH"
./.venv/bin/python main.py
