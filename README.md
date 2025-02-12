# Private Proof-of-Stake Ethereum devnet toolbox

Scripts and smart contracts for Ethereum web3 development.


## Setting up the blockchain

Create a directory where you want to store all of the devnet chain data.
I ususally call mine `chain`, and inside that directory you want to create
two additional directories called:

- `execution`: this directory will store all of the execution layer nodes and [clef](https://geth.ethereum.org/docs/tools/clef/introduction) data,
- `consensus`: this directory will store the software to run the Proof-of-Stake (PoS) consensus nodes.

Generate the necessary genesis state file modifications by running:

```
./consensus/prysmctl testnet generate-gensis \
  --fork capella \
  --num-validators 10 \
  --genesis-time-delay 600 \
  --chain-config-file ./chain-config.yml \
  --geth-gensis-json-in ./original-genesis.json \
  --geth-gensis-json-out ./genesis.json ¿
  --output-ssz ./genesis.ssz

```

which will move the genesis time forward into the future by 10 minutes (600 seconds).

Prepare your account by running:

```
geth --datadir ./execution/data account import ./secret.txt
geth --dataidr ./execution/data init ./genesis.json

```


## Deploying contracts

You can use the script [deploy_contract.py](./deploy_contract.py) to deploy contracts to the chain.

```
py deploy_contract.py --help

usage:
        Deploy a smart contract to a private PoS Ethereum devnet over IPC.

positional arguments:
  contract              the name of the contract to deploy

optional arguments:
  -h, --help            show this help message and exit
  -i IPC_ENDPOINT, --ipc-endpoint IPC_ENDPOINT
                        the IPC endpoint to connect to (default: ./chain/execution/data/geth.ipc)
  -a ARGS [ARGS ...], --args ARGS [ARGS ...]
                        optional positional arguments for the constructor of the contract
  -p PARSE_ARGS [PARSE_ARGS ...], --parse-args PARSE_ARGS [PARSE_ARGS ...]

Don't you dare go hollow.

```


## Interacting with contracts

You can use the script [interact_with_contract.py](./interact_with_contract.py) to call/transact with contract methods.

```
py interact_with_contract.py --help

usage: interact_with_contract.py [-h] [-a ARGS [ARGS ...]] [--parse-args PARSE_ARGS [PARSE_ARGS ...]] [-i IPC_ENDPOINT] [-p PRIVATE_KEY] [--gas GAS] [--gas-price GAS_PRICE]
                                 contract function {call,transact}

positional arguments:
  contract              the name of the contract to interact with
  function              the name of the function to call/transact
  {call,transact}       how to use the contract function

optional arguments:
  -h, --help            show this help message and exit
  -a ARGS [ARGS ...], --args ARGS [ARGS ...]
                        optional positional arguments to pass to the contract function
  --parse-args PARSE_ARGS [PARSE_ARGS ...]
  -i IPC_ENDPOINT, --ipc-endpoint IPC_ENDPOINT
                        the IPC endpoint to connect to (default: ./chain/execution/data/geth.ipc)
  -p PRIVATE_KEY, --private-key PRIVATE_KEY
                        the file containing the private key for the account to use (default: ./secret.txt)
  --gas GAS             the price that you are prepared to pay to execute a transaction (default: 3000000)
  --gas-price GAS_PRICE
                        the amount that you are willing to pay per unit of gas (default: 10)

```

...

