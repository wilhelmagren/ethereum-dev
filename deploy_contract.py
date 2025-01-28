"""

This script deploys a smart contract to a local Ethereum chain over IPC running locally. 
Requires the user to provide the name of the smart contract to be deployed.

File created: 2025-01-27
Last updated: 2025-01-28

"""
import argparse
import json

from eth_account import Account
from web3 import Web3
from typing import Tuple


USAGE_STRING = """
Deploy a smart contract on a private local Ethereum chain over IPC.
"""


def read_contract_abi_and_bytecode(contract_name: str) -> Tuple[str, str]:
    """Read the abi and bytecode files for the smart contract."""
    path = "./target/" + contract_name

    with open(path + ".abi", "rb") as f:
        abi = json.loads(f.read())

    with open(path + ".bin", "r") as f:
        bytecode = f.read()

    return (abi, bytecode)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="deploy_contract",
        usage=USAGE_STRING,
    )

    parser.add_argument(
        "contract",
        action="store",
        help="the name of the contract to deploy",
    )
    parser.add_argument(
        "-p",
        "--password-file",
        action="store",
        default="./secret.txt",
        help="the file containing the password for the account",
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

    args = parser.parse_args()

    w3 = Web3(Web3.IPCProvider(args.ipc_endpoint))

    if not w3.is_connected():
        print(f"[ERROR] could not connect to the IPC endpoint at: `{args.ipc_endpoint}`")

    password_file = args.password_file
    with open(password_file, "r") as f:
        password = f.read().strip()

    print(f"[INFO] accounts: `{','.join(w3.eth.accounts)}`")

    account = w3.eth.accounts[0]

    print(f"[INFO] setting default account to: {account}")
    w3.eth.default_account = account

    abi, bytecode = read_contract_abi_and_bytecode(args.contract)
    contract = w3.eth.contract(abi=abi, bytecode=bytecode)
    tx = contract.constructor().build_transaction()
    tx["nonce"] = 1337


    print("[INFO] signing transaction...") 
    signed_tx = Account.sign_transaction(tx, private_key=password)

    print("[INFO] deploying contract...")
    tx_address = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

    print("[INFO] waiting for receipt on transaction...")
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_address)

    print(f"[INFO] contract tx address: {tx_address}")
    print(f"[INFO] contract tx receipt: {tx_receipt}")

    DEPLOYMENT_INFO_FILE = "CONTRACT_DEPLOYMENT_INFO.txt"

    with open(DEPLOYMENT_INFO_FILE, "w") as f:
        f.writelines([tx_address, tx_receipt])

    print(f"[INFO] wrote tx info to file: {DEPLOYMENT_INFO_FILE}")
    print("[INFO] all done, exiting!")
    exit(0)

