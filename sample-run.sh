#!/bin/sh

while true
do
  cd ~/POL-scripts/POL-to-blockchain-recording &&
  python3 ./send_to_blockchain.py &
  sleep 20
done
