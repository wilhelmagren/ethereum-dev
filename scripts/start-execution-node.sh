#!/usr/bin/env bash

geth --http --http.api eth,net,web3 --ws --ws.api eth,net,web3 --authrpc.jwtsecret ./jwt.hex --datadir ./execution/data --nodiscover --syncmode full --allow-insecure-unlock
