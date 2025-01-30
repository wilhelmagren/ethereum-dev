"""

Withdraw an amount of money from the database and token contract. 

File created: 2025-01-30
Last updated: 2025-01-30
"""

import json
import argparse
import sqlite3
import web3

from eth_account import Account
from web3 import Web3

DATABASE = "accounts.db"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("amount")

    args = parser.parse_args()

    query = "UPDATE accounts SET balance = balance - ? WHERE address = ?"
    w3 = Web3(Web3.IPCProvider("./chain/execution/data/geth.ipc"))
    account = w3.eth.accounts[0]
    amount = int(args.amount)

    with sqlite3.connect(DATABASE) as sql:
        cursor = sql.cursor()
        cursor.execute(query, (amount, account))
        sql.commit()
        print(f"Removing {args.amount} SEK from local db account `{account}`.")

    w3.eth.defaultAccount = account

    with open("./CONTRACT_DEPLOYMENT_INFO.json", "r") as f:
        token_info = json.loads(f.read())

    contract = w3.eth.contract(
        address=token_info["CONTRACT_ADDRESS"],
        abi=token_info["CONTRACT_ABI"],
    )

    with open("./secret.txt") as f:
        password = f.read().strip()

    print("Building chain transaction to burn tokens...")
    
    tx = contract.functions.burn(account, amount).build_transaction({
        "from": account,
        "nonce": w3.eth.get_transaction_count(account),
        "gas": 3000000,
        "gasPrice": web3.Web3.to_wei("20", "gwei"),
    })

    print(f"Signing transaction using private key of account `{account}`")
    signed_tx = Account.sign_transaction(tx, private_key=password)
    print("Sending transaction...")
    tx_hash = str(w3.eth.send_raw_transaction(signed_tx.raw_transaction).hex())
    print("OK!")

