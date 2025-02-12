"""
Car register oracle. Listens for event that a car deal has been made an changes owner in
its register (local db file).
"""

import time
import json

from web3 import Web3


def update_register(event):
    event_args = event.args
    buyer = event_args.buyer
    seller = event_args.seller
    car_id = event_args.carId
    price = event_args.price

    with open("./cars_db.json", "rb") as f:
        cars = json.loads(f.read())

    cars[car_id] = {
        "owner": buyer,
        "previous_owner": seller,
        "price": price,
    }

    with open("./cars_db.json", "w") as f:
        json.dump(cars, f)


if __name__ == "__main__":
    
    w3 = Web3(Web3.IPCProvider("../chain/execution/data/geth.ipc"))

    while True:
        with open("../DEPLOYED_CONTRACTS.json", "rb") as f:
            contract_info = json.loads(f.read())["CarDeal"]

        contract = w3.eth.contract(
            address=contract_info["address"],
            abi=contract_info["abi"],
        )

        events = contract.events.CarOwnerTransfer.get_logs()

        if events != []:
            print("Got new CarOwnerTransfer event on chain, updating register...")
            update_register(events[0])
            print("OK!")
        else:
            print("No new events...")

        time.sleep(3)

