#!/bin/bash

function main() {
  local path_pattern="$1"
  local iterations="$2"
  local shuffled_list
  shuffled_list=$(get_playlist "$path_pattern" "$iterations")
  play_all "$shuffled_list"
}

function get_playlist() {
 yes "$(ffplaylist "$1")" | head -n "$2" | shuf
}

function play_all() {
  ffplay -autoexit -f concat -safe 0 -i <(printf '%s' "$1") > /dev/null 2>&1
}

main "$@"
