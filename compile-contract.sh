#!/usr/bin/env bash

set -euo pipefail

solc --abi --bin $1 -o target || exit 1

exit 0
