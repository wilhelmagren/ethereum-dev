#!/usr/bin/env bash

#
# Generate a new JWT (JSON Web Token) using OpenSSL.
#

set -euo pipefail

openssl rand -hex 32 | tr -d "\n" > "jwt.hex"
