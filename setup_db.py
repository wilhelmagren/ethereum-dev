"""

File created: 2025-01-29
Last updated: 2025-01-30
"""

import sqlite3

from web3 import Web3

DATABASE = "accounts.db"
CREATE_TABLE = "CREATE TABLE IF NOT EXISTS accounts (address text PRIMARY KEY, balance INT NOT NULL);"
CREATE_ACCOUNT = "INSERT INTO accounts(address, balance) VALUES(?, 0);"


if __name__ == "__main__":

    w3 = Web3(Web3.IPCProvider("./chain/execution/data/geth.ipc"))
    account = w3.eth.accounts[0]
    w3.eth.defaultAccount = account

    with sqlite3.connect(DATABASE) as sql:
        cursor = sql.cursor()

        cursor.execute(CREATE_TABLE)
        sql.commit()
        print(f"Created table `accounts` successfully in file `{DATABASE}`.")

        cursor.execute(CREATE_ACCOUNT, (account, ))
        sql.commit()
        print(f"Added account `{account}` to db.")
