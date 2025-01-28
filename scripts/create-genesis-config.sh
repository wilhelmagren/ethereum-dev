#!/usr/bin/env bash

./consensus/prysmctl testnet generate-genesis --fork capella --num-validators 10 --genesis-time-delay 600 --chain-config-file ./chain-config.yml --geth-genesis-json-in ./original-genesis.json --geth-genesis-json-out ./genesis.json --output-ssz ./genesis.ssz
