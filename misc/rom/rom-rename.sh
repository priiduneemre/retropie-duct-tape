#!/bin/bash
script_path=$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")
python3 "$script_path/rom-rename.py" "$@"
