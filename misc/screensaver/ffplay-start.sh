#!/bin/bash
pattern="$HOME/RetroPie/screensavers/flv/*.flv"
script_path=$(dirname "$(readlink -f "$BASH_SOURCE")")

(
  while true; do
    source "$script_path/ffplay-random.sh" "$pattern" 150
  done
) &
