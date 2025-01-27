#!/usr/bin/env bash

set -euo pipefail

curl https://raw.githubusercontent.com/prysmaticlabs/prysm/master/prysm.sh --output prysm.sh || exit 1
curl -L https://github.com/prysmaticlabs/prysm/releases/download/v5.2.0-linux-amd64 --output prysmctl || exit 1

exit 0
