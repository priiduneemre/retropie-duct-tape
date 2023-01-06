#!/bin/bash
(
  sleep 0.5
  shutdown -h
  killall -SIGINT emulationstation
  sleep 2
  shutdown -h now
) > /dev/null 2>&1 &
