#!/bin/bash

function exit_es() {
  sleep 0.5
  killall -SIGINT emulationstation
}

exit_es > /dev/null 2>&1 &
