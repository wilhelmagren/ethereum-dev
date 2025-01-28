#!/usr/bin/env bash

./consensus/prysm.sh validator --datadir ./consensus/validator --accept-terms-of-use --interop-num-validators 10 --chain-config-file ./chain-config.yml
