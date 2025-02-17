"""
"""

import json
import time
import web3
import web3.exceptions as w3exceptions

from contextlib import asynccontextmanager
from datetime import datetime
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


def str_to_int(s: str) -> int:
    """Convert a string to an integer by converting it to bytes."""
    return int.from_bytes(s.encode("utf-8"), byteorder="big")

def int_to_str(i: int) -> str:
    """Convert an integer to a string by converting it to bytes."""
    return i.to_bytes((i.bit_length() + 7) // 8, byteorder="big")


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


@app.post("/tokenize")
async def post_tokenize_car(car: Car):
    """ """

    if not await app.web3.is_connected():
        return JSONResponse(
            status_code=500,
            content={"message": "Failed to tokenize car: could not connect to chain"},
        )

    contract = app.web3.eth.contract(
        abi=CAR_CONTRACT_ABI,
        bytecode=CAR_CONTRACT_BIN,
    )

    try:
        tx_hash = str((await contract.constructor(
            str_to_int(car.modelName),
            str_to_int(car.licensePlate),
            int(time.mktime(datetime.strptime(car.manufacturedDate, "%Y-%m-%d").timetuple())),
            str_to_int(car.uniqueId),
            str(car.owner),
        ).transact()).hex())

        tx_receipt = await app.web3.eth.wait_for_transaction_receipt(tx_hash)
        print(tx_receipt)

        return JSONResponse(
            status_code=200,
            content={"message": f"Successfully tokenized car: transaction hash 0x{tx_hash}"},
        )

    except w3exceptions.Web3RPCError as e:
        return JSONResponse(
            status_code=500,
            content={"message": f"Failed to tokenize car: {e.message}"},
        )

