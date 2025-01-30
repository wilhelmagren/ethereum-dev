import json
import sqlite3

from web3 import Web3

DATABASE = "accounts.db"


if __name__ == "__main__":
    query = "SELECT * FROM accounts"

    print("Reading from local database...")

    with sqlite3.connect(DATABASE) as sql:
        cursor = sql.cursor()
        cursor.execute(query)
        row = cursor.fetchone()

    account, sql_amount = row

    print("OK!")

    w3 = Web3(Web3.IPCProvider("./chain/execution/data/geth.ipc"))
    w3.eth.defaultAccount = account

    with open("./CONTRACT_DEPLOYMENT_INFO.json", "r") as f:
        token_info = json.loads(f.read())

    contract = w3.eth.contract(
        address=token_info["CONTRACT_ADDRESS"],
        abi=token_info["CONTRACT_ABI"],
    )

    print("Reading token supply and balances on chain...")

    chain_amount = contract.functions.balanceOf(account).call()
    chain_total_amount = contract.functions.totalSupply().call()

    print(f"Amount in local db:\t\t{sql_amount}")
    print(f"Amount on chain in contract:\t{chain_amount}")
    print(f"Total supply on chain:\t\t{chain_total_amount}")

