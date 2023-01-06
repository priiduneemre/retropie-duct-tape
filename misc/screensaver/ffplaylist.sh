#!/bin/bash
pattern="$1"
for path in $pattern; do printf "file '%s'\n" "$path"; done
