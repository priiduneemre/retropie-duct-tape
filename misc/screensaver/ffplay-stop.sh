#!/bin/bash

function main() {
  stop_playback
  repaint
}

function stop_playback() {
  killall -r ffplay-start.sh
  killall ffplay
}

function repaint() {
  chvt 2
  chvt 1
  # Empirical delay; try increasing this if there is artifacting
  sleep 0.02
  clear
}

main
