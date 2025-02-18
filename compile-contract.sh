#!/usr/bin/env bash

set -euo pipefail

solc --abi --bin --bin-runtime $1 -o target --overwrite || exit 1

exit 0
