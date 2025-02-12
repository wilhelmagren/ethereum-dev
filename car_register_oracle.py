"""
Car register oracle. Listens for event that a car deal has been made an changes owner in
its register (local db file).

File created: 2025-01-30
Last updated: 2025-02-12
"""

import time
import json
import sqlite3

from web3 import Web3

UPDATE_QUERY = "UPDATE cars SET owner = ?, previous_owner = ?, price = ? WHERE id = ?"


def update_register(event, sql):
    cursor = sql.cursor()
    event_args = event.args
    buyer = event_args.buyer
    seller = event_args.seller
    car_id = event_args.carId
    price = event_args.price

    cursor.execute(UPDATE_QUERY, (buyer, seller, price, car_id))
    sql.commit()


if __name__ == "__main__":
    
    w3 = Web3(Web3.IPCProvider("./chain/execution/data/geth.ipc"))

    with sqlite3.connect("cars.db") as sql:
        while True:
            with open("./DEPLOYED_CONTRACTS.json", "rb") as f:
                contract_info = json.loads(f.read())["CarEscrow"]

            contract = w3.eth.contract(
                address=contract_info["address"],
                abi=contract_info["abi"],
            )

            events = contract.events.CarOwnerTransfer.get_logs()

            if events != []:
                print("Got new CarOwnerTransfer event on chain, updating register...")
                update_register(events[0], sql)
                print("OK!")
            else:
                print("No new events...")

            time.sleep(3)

