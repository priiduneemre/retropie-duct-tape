#!/bin/bash

function main() {
  shutdown -h
  exit_es
  shutdown -h now
}

function exit_es() {
  sleep 0.5
  killall -SIGINT emulationstation
  sleep 2
}

main > /dev/null 2>&1 &
