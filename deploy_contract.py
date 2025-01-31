"""

This script deploys a new smart contract to a private PoS Ethereum devnet over IPC.
Requires the user to provide the name of the smart contract to be deployed.

File created: 2025-01-27
Last updated: 2025-01-31

"""

import argparse
import json
import logging

from web3 import Web3
from typing import Tuple
from pathlib import Path


USAGE_STRING = """
Deploy a smart contract to a private PoS Ethereum devnet over IPC.
"""


class LogFormatter(logging.Formatter):

    grey = "\x1b[38;20m"
    green = "\x1b[0;32m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = " [%(asctime)s] %(message)s"

    _FORMATS = {
        logging.DEBUG: grey + "DEBUG" + reset + format,
        logging.INFO: green + "INFO " + reset + format,
        logging.WARNING: yellow + "WARN " + reset + format,
        logging.ERROR: red + "ERROR" + reset + format,
        logging.CRITICAL: bold_red + "ERROR" + reset + format,
    }

    def format(self, record: logging.LogRecord) -> str:
        log_fmt = self._FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


log = logging.getLogger("deploy_contract")
log.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

ch.setFormatter(LogFormatter())
log.addHandler(ch)


def read_contract_abi_and_bytecode(name: str) -> Tuple[str, str]:
    """"""
    
    path = "./target/" + name

    if not Path(path + ".abi").is_file() or not Path(path + ".bin").is_file():
        log.error(f"Could not fine ABI or bytecode files for contract {name} at ./target/")

    with open(path + ".abi", "rb") as f:
        abi = json.loads(f.read())

    with open(path + ".bin", "r") as f:
        bytecode = f.read()

    log.info(f"Read contract ABI and bytecode from {path}.* successfully")

    return (abi, "0x" + bytecode)


def store_contract_info(name, abi, receipt):
    """"""

    CONTRACT_INFO_FILE = Path("DEPLOYED_CONTRACTS.json")
    log.info(f"Storing contract information in the file {CONTRACT_INFO_FILE}")
    
    info = {}

    if CONTRACT_INFO_FILE.is_file():
        with open(CONTRACT_INFO_FILE, "r") as f:
            info = json.loads(f.read())

    info[name] = {
        "block_hash": "0x" + str(receipt["blockHash"].hex()),
        "block_number": receipt["blockNumber"],
        "tx_hash": "0x" + str(receipt["transactionHash"].hex()),
        "from": receipt["from"],
        "address": receipt["contractAddress"],
        "gas_used": receipt["gasUsed"],
        "effective_gas_price": receipt["effectiveGasPrice"],
        "abi": abi,
    }

    with open(CONTRACT_INFO_FILE, "w") as f:
        json.dump(info, f)


def deploy_contract(args: argparse.Namespace) -> None:
    """"""

    ipc_endpoint = args.ipc_endpoint

    w3 = Web3(Web3.IPCProvider(ipc_endpoint))
    if not w3.is_connected():
        log.critical(f"Could not connect to the IPC endpoint at {ipc_endpoint}")
        exit(1)

    log.info(f"Connected to the IPC endpoint at {ipc_endpoint}")

    contract_abi, contract_bytecode = read_contract_abi_and_bytecode(args.contract)
    
    log.info("Listing accounts, might need confirmation in clef")
    account = w3.eth.accounts[0]

    log.info(f"Setting default account to {account}")
    w3.eth.default_account = account

    contract = w3.eth.contract(abi=contract_abi, bytecode=contract_bytecode)

    log.info("Making transaction to deploy contract, need confirmation in clef")
    tx_hash = str(contract.constructor().transact().hex())
    log.info(f"Transaction ok 0x{tx_hash}")

    log.info("Waiting for transaction receipt...")
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    log.info(f"Transaction receipt ok 0x{tx_hash}")

    store_contract_info(args.contract, contract_abi, tx_receipt)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="deploy_contract",
        usage=USAGE_STRING,
        epilog="Don't you dare go hollow.",
    )

    parser.add_argument(
        "contract",
        action="store",
        help="the name of the contract to deploy",
    )

    parser.add_argument(
        "-i", "--ipc-endpoint",
        action="store",
        default="./chain/execution/data/geth.ipc",
        help="the IPC endpoint to connect to (default: ./chain/execution/data/geth.ipc)",
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="toggle verbosity (default: false)",
    )

    deploy_contract(parser.parse_args())
    exit(0)

