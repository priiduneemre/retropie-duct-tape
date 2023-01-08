#!/bin/bash

function main() {
  local pattern="$1"
  for path in $pattern; do
    add_item "$path"
  done
}

function add_item() {
  printf "file '%s'\n" "$1"
}

main "$@"
