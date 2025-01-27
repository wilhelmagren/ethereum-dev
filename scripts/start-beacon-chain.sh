#!/usr/bin/env bash

./consensus/prysm.sh beacon-chain --datadir beacon --min-sync-peers 0 --genesis-state ./genesis.ssz --bootstrap-node= --interop-eth1data-votes --chain-config-file ./chain-config.yml --contract-deployment-block 0 --chain-id 1337 --accept-terms-of-use --jwt-secret ./jwt.hex --suggested-fee-recipient 0x123463a4b065722e99115d6c222f267d9cabb524 --minimum-peers-per-subnet 0 --enable-debug-rpc-endpoints --execution-endpoint ./execution/data/geth.ipc
