#!/bin/bash

function main() {
  local source_dir="$1"
  local iterations="$2"
  local duration="$3"
  local fade_in="$4"
  local fade_out="$5"
  local pause="$6"
  mapfile -d '' source_paths < <(get_random_paths "$source_dir" "$iterations")
  video_filter=$(get_video_filter "$duration" "$fade_in" "$fade_out")
  play_all "$duration" "$pause" "$video_filter" "${source_paths[@]}"
}

function get_random_paths() {
  find "$1" -type f -print0 | shuf -n "$2" --zero-terminated
}

function get_video_filter() {
  local fade_out_start
  fade_out_start=$(printf "%g\n" "$(bc <<< "$1 - $3")")
  echo "fade=in:st=0:d=$2,fade=out:st=$fade_out_start:d=$3"
}

function play_all() {
  local duration="$1"
  local pause="$2"
  local video_filter="$3"
  shift 3
  local paths=("$@")
  for path in "${paths[@]}"; do
    play "$path" "$duration" "$video_filter"
    [ "$path" != "${paths[-1]}" ] && sleep "$pause"
  done
}

function play() {
 ffplay -autoexit -vf "$3" -t "$2" -i "$1" > /dev/null 2>&1
}

# TODO: Pass in via CLI arguments
source_dir="$HOME/RetroPie/splashscreens/flv"
iterations="2"
duration="1.6"
fade_in="0.3"
fade_out="0.3"
pause="0.1"

main "$source_dir" "$iterations" "$duration" "$fade_in" "$fade_out" "$pause"
