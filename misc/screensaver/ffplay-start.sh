#!/bin/bash

function main() {
  (while true; do play_random "$@"; done) &
}

function play_random() {
  local script_path
  script_path=$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")
  source "$script_path/ffplay-random.sh" "$1" "$2"
}

pattern="$HOME/RetroPie/screensavers/flv/*.flv"
playlist_length=150

main "$pattern" "$playlist_length"
