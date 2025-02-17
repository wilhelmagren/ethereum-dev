"""
"""

import json
import time
import web3
import web3.exceptions as w3exceptions

from contextlib import asynccontextmanager
from datetime import datetime
from eth_account import Account
from fastapi import (
    FastAPI,
    Request,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from web3 import AsyncWeb3


@asynccontextmanager
async def web3_lifespan(app: FastAPI):
    app.web3 = await AsyncWeb3(web3.providers.persistent.AsyncIPCProvider("../chain/execution/data/geth.ipc"))
    app.web3.eth.default_account = (await app.web3.eth.accounts)[0]
    yield


app = FastAPI(lifespan=web3_lifespan)


frontend_origins = [ "http://localhost:5173" ]
app.add_middleware(
    CORSMiddleware,
    allow_origins=frontend_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Car(BaseModel):
    modelName: str
    licensePlate: str
    manufacturedDate: str
    uniqueId: str
    owner: str


with open("../target/Car.abi", "rb") as f:
    CAR_CONTRACT_ABI = json.loads(f.read())

with open("../target/Car.bin", "r") as f:
    CAR_CONTRACT_BIN = f.read()

with open("../target/CarLedger.abi", "rb") as f:
    LEDGER_CONTRACT_ABI = json.loads(f.read())

with open("../target/CarLedger.bin", "r") as f:
    LEDGER_CONTRACT_BIN = f.read()

with open("../secret.txt", "r") as f:
    ACCOUNT_PK = f.read().strip()

with open("../DEPLOYED_CONTRACTS.json") as f:
    LEDGER_INFO = json.loads(f.read())["CarLedger"]


def str_to_int(s: str) -> int:
    """Convert a string to an integer by converting it to bytes."""
    return int.from_bytes(s.encode("utf-8"), byteorder="big")


def int_to_str(i: int) -> str:
    """Convert an integer to a string by converting it to bytes."""
    return str(i.to_bytes((i.bit_length() + 7) // 8, byteorder="big"))


def strdate_to_int(d: str) -> int:
    """Convert a string date to its UNIX timestamp integer format."""
    return int(time.mktime(datetime.strptime(d, "%Y-%m-%d").timetuple()))


def int_to_strdate(i: int) -> str:
    """Convert a UNIX integer timestamp to its string date format."""
    return datetime.utcfromtimestamp(i).strftime("%Y-%m-%d")


"""
# https://medium.com/@tclaitken/setting-up-a-fastapi-app-with-async-sqlalchemy-2-0-pydantic-v2-e6c540be4308
@app.on_event("startup")
async def startup_event():
    app.web3 = await AsyncWeb3(web3.providers.persistent.AsyncIPCProvider("../chain/execution/data/geth.ipc"))
    app.web3.eth.default_account = (await app.web3.eth.accounts)[0]
"""


@app.exception_handler(Exception)
async def catch_all_exception_handler(request: Request, exc: Exception):
    """ """
    return JSONResponse(
        status_code=500,
        content={"message": f"Unhandled error occured: {str(exc)}"},
    )


@app.post("/_api/tokenize")
async def post_tokenize_car(car: Car):
    """ """

    if not await app.web3.is_connected():
        return JSONResponse(
            status_code=500,
            content={"message": "Failed to tokenize car: could not connect to chain"},
        )

    ledger_contract = app.web3.eth.contract(
        address=LEDGER_INFO["address"],
        abi=LEDGER_CONTRACT_ABI,
    )

    car_contract = app.web3.eth.contract(
        abi=CAR_CONTRACT_ABI,
        bytecode=CAR_CONTRACT_BIN,
    )

    try:
        car_tx_hash = str((await car_contract.constructor(
            str_to_int(car.modelName),
            str_to_int(car.licensePlate),
            strdate_to_int(car.manufacturedDate),
            str_to_int(car.uniqueId),
            str(car.owner),
        ).transact()).hex())

        car_tx_receipt = await app.web3.eth.wait_for_transaction_receipt(car_tx_hash)

        ledger_tx = await ledger_contract.functions.registerCar(car_tx_receipt["contractAddress"]).build_transaction({
            "from": app.web3.eth.default_account,
            "nonce": await app.web3.eth.get_transaction_count(app.web3.eth.default_account),
            "gas": 3000000,
            "gasPrice": web3.Web3.to_wei(10, "gwei"),
        })

        signed_ledger_tx = Account.sign_transaction(ledger_tx, private_key=ACCOUNT_PK)
        ledger_tx_hash = str((await app.web3.eth.send_raw_transaction(
            signed_ledger_tx.raw_transaction,
        )).hex())

        return JSONResponse(
            status_code=200,
            content={"message": f"Successfully tokenized car:\n - car transaction hash '0x{car_tx_hash}'\n - ledger transaction hash '{ledger_tx_hash}'"},
        )

    except w3exceptions.Web3RPCError as e:
        return JSONResponse(
            status_code=500,
            content={"message": f"Failed to tokenize car: {e.message}"},
        )


@app.get("/_api/cars/{uniqueId}")
async def get_car_from_id(uniqueId: str):
    """ """

    ledger_contract = app.web3.eth.contract(
        address=LEDGER_INFO["address"],
        abi=LEDGER_CONTRACT_ABI,
    )

    car_address = await ledger_contract.functions.getCarAddress(str_to_int(uniqueId)).call()

    if car_address == "0x0":
        return JSONResponse(
            status_code=500,
            content={"message": "The car does not exist in the ledger"},
        )

    car_contract = app.web3.eth.contract(
        address=car_address,
        abi=CAR_CONTRACT_ABI,
    )

    car_model_name = await car_contract.functions.modelName().call()
    car_license_plate = await car_contract.functions.licensePlate().call()
    car_manufactured_date = await car_contract.functions.manufacturedDate().call()
    car_owner = await car_contract.functions.owner().call()

    return JSONResponse(
        status_code=200,
        content={
            "modelName": int_to_str(car_model_name),
            "licensePlate": int_to_str(car_license_plate),
            "manufacturedDate": int_to_strdate(car_manufactured_date),
            "owner": car_owner,
        },
    )

