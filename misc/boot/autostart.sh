#!/bin/bash

function main() {
  disable_terminal
  play_splashscreen &
  run_es
  is_shutdown && sleep infinity
  enable_terminal
}

function disable_terminal() {
  stty -echo
  tput civis
  clear
}

function play_splashscreen() {
  source /opt/retropie/configs/all/splashscreen.sh
}

function run_es() {
  emulationstation --no-confirm-quit --no-splash > /dev/null 2>&1
}

function is_shutdown() {
  [ -f /run/systemd/shutdown/scheduled ]
}

function enable_terminal() {
  tput cnorm
  stty echo
  clear
}

main
