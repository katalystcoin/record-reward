#!/bin/sh

while true
do
  cd ~/POL-scripts/mysql-to-POL-recording/daebak &&
  python3 ./daebak_new_choices.py
  sleep 30
done
