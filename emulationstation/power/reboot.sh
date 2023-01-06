#!/bin/bash
(
  sleep 0.5
  shutdown -r
  killall -SIGINT emulationstation
  sleep 2
  shutdown -r now
) > /dev/null 2>&1 &
