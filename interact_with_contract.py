"""
Interact with smart contracts on your private PoS Ethereum devnet over IPC.

File created: 2025-01-31
Last updated: 2025-01-31
"""

import argparse
import json
import web3

from eth_account import Account
from web3 import Web3


def format_args(args, hows):
    how = {
        "string": str,
        "int": int,
        "address": str,
    }
    return [how[h](a) for h, a in zip(hows, args)]


def interact_with_contract(args: argparse.Namespace) -> None:
    """ """

    w3 = Web3(Web3.IPCProvider(args.ipc_endpoint))
    if not w3.is_connected():
        print("uh oh ohxddd")
        exit(1)

    account = w3.eth.accounts[0]
    w3.eth.defaultAccount = account

    with open("./DEPLOYED_CONTRACTS.json") as f:
        contract_info = json.loads(f.read())[args.contract]

    contract = w3.eth.contract(
        address=contract_info["address"],
        abi=contract_info["abi"],
    )

    with open(args.private_key, "r") as f:
        private_key = f.read().strip()

    function = getattr(contract.functions, args.function)
    fn_args = format_args(args.args, args.parse_args)

    if args.interaction == "call":
        result = function(*fn_args).call()
        print(f"Result from function call: {result}")
    else:
        tx = function(*fn_args).build_transaction({
            "from": account,
            "nonce": w3.eth.get_transaction_count(account),
            "gas": args.gas,
            "gasPrice": web3.Web3.to_wei(args.gas_price, "gwei"),
        })

        signed_tx = Account.sign_transaction(tx, private_key=private_key)
        tx_hash = str(w3.eth.send_raw_transaction(signed_tx.raw_transaction).hex())
        print(f"Transaction successful 0x{tx_hash}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "contract",
        action="store",
        help="the name of the contract to interact with",
    )

    parser.add_argument(
        "function",
        action="store",
        help="the name of the function to call/transact",
    )

    parser.add_argument(
        "interaction",
        action="store",
        choices=["call", "transact"],
        help="how to use the contract function",
    )

    parser.add_argument(
        "-a", "--args",
        nargs="+",
        help="optional positional arguments to pass to the contract function",
    )

    parser.add_argument(
        "--parse-args",
        nargs="+",
    )

    parser.add_argument(
        "-i", "--ipc-endpoint",
        action="store",
        default="./chain/execution/data/geth.ipc",
        help="the IPC endpoint to connect to (default: ./chain/execution/data/geth.ipc)",
    )

    parser.add_argument(
        "-p", "--private-key",
        action="store",
        default="./secret.txt",
        help="the file containing the private key for the account to use (default: ./secret.txt)",
    )

    parser.add_argument(
        "--gas",
        action="store",
        default=3000000,
        help="the price that you are prepared to pay to execute a transaction (default: 3000000)",
    )

    parser.add_argument(
        "--gas-price",
        action="store",
        default=10,
        help="the amount that you are willing to pay per unit of gas (default: 10)",
    )

    interact_with_contract(parser.parse_args())
    exit(0)

