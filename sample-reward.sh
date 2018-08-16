#!/bin/sh

while true
do
  cd ~/POL-scripts/blockchain-POL-rewarding &&
  python3 ./read_blockchain_and_reward.py &
  sleep 5
done
