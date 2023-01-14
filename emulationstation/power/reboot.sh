#!/bin/bash

function main() {
  shutdown -r
  exit_es
  shutdown -r now
}

function exit_es() {
  sleep 0.5
  killall -SIGINT emulationstation
  sleep 2
}

main > /dev/null 2>&1 &
