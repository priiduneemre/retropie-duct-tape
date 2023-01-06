#!/bin/bash
disable_terminal() {
  stty -echo
  tput civis
  clear
}

enable_terminal() {
  tput cnorm
  stty echo
  clear
}

is_shutdown() {
  [ -f /run/systemd/shutdown/scheduled ]
}

play_splashscreen() {
  source /opt/retropie/configs/all/splashscreen.sh
}

run_es() {
  emulationstation --no-confirm-quit --no-splash > /dev/null 2>&1
}

disable_terminal
play_splashscreen &
run_es
is_shutdown && sleep infinity
enable_terminal
