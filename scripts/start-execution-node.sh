#!/usr/bin/env bash

geth --http --http.api eth,net,web3 --ws --ws.api eth,net,web3 --authrpc.jwtsecret ./jwt.hex --datadir ./execution/data --nodiscover --syncmode full --allow-insecure-unlock --unlock 0x123463a4b065722e99115d6c222f267d9cabb524
