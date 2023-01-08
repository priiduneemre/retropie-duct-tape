#!/bin/bash

function main() {
  schedule_reboot
  exit_es
  shutdown -r now
}

function schedule_reboot() {
  sleep 0.5
  shutdown -r
}

function exit_es() {
  killall -SIGINT emulationstation
  sleep 2
}

main > /dev/null 2>&1 &
