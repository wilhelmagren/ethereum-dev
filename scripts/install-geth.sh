#!/usr/bin/env bash

git clone https://github.com/ethereum/go-ethereum.git && cd go-ethereum && make geth || exit 1
cp ./build/bin/geth /usr/bin/geth || exit 1

exit 0

