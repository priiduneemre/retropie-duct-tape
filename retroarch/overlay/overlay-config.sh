#!/bin/bash
script_path=$(dirname "$(readlink -f "$BASH_SOURCE")")
python3 "$script_path/overlay-config.py" "$@"
