#!/bin/bash
count="$2"
playlist=$(ffplaylist "$1")
shuffled_list=$(yes "$playlist" | head -n "$count" | shuf)
ffplay -autoexit -f concat -safe 0 -i <(printf '%s' "$shuffled_list") > /dev/null 2>&1
