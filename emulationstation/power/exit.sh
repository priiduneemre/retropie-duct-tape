#!/bin/bash
(
  sleep 0.5
  killall -SIGINT emulationstation
) > /dev/null 2>&1 &
