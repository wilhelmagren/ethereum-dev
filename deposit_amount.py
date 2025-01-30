"""

Deposit an amount of money to the database. 

File created: 2025-01-30
Last updated: 2025-01-30
"""

import json
import argparse
import sqlite3

from web3 import Web3

DATABASE = "accounts.db"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("account")
    parser.add_argument("amount")

    args = parser.parse_args()

    query = "INSERT INTO accounts(address,balance) VALUES(?,?);"

    with sqlite3.connect(DATABASE) as sql:
        cursor = sql.cursor()
        cursor.execute(query, (args.account, args.amount))
        sql.commit()
        print(f"Added {args.amount} SEK to account `{args.account}`.")

    w3 = Web3(Web3.IPCProvider("./chain/execution/data/geth.ipc"))
    account = w3.eth.accounts[0]
    w3.eth.defaultAccount = account

    with open("./CONTRACT_DEPLOYMENT_INFO.json", "r") as f:
        token_info = json.loads(f.read())

    contract = w3.eth.contract(
        address=token_info["CONTRACT_ADDRESS"],
        abi=token_info["CONTRACT_ABI"],
    )

    print("Submitting transaction to chain...")
    tx_hash = contract.functions.mint(args.account, args.amount).transact()
    print(f"Chain accepted transaction tx: `{tx_hash}`")

    

