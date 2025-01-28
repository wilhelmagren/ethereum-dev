#!/usr/bin/env bash

geth --datadir ./execution/data account import ./secret.txt || exit 1
geth --datadir ./execution/data init ./genesis.json || exit 1

exit 0
