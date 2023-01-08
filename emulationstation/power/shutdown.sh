#!/bin/bash

function main() {
  schedule_halt
  exit_es
  shutdown -h now
}

function schedule_halt() {
  sleep 0.5
  shutdown -h
}

function exit_es() {
  killall -SIGINT emulationstation
  sleep 2
}

main > /dev/null 2>&1 &
