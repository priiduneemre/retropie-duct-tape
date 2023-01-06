#!/bin/bash
duration="1.6"
fade_in="0.3"
fade_out="0.3"
iterations="2"
pause="0.1"

fade_out_start=$(printf "%g\n" "$(bc <<< "$duration - $fade_out")")
filtergraph="fade=in:st=0:d=$fade_in,fade=out:st=$fade_out_start:d=$fade_out"
source_dir="$HOME/RetroPie/splashscreens/flv"
random_paths=(`find $source_dir -type f | shuf -n $iterations`)

for path in "${random_paths[@]}"; do
  ffplay -autoexit -vf "$filtergraph" -t $duration -i "$path" > /dev/null 2>&1
  [ "$path" != "${random_paths[-1]}" ] && sleep $pause
done
