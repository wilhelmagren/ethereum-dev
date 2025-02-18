"""
"""

import json
import time
import sqlite3
import web3
import web3.exceptions as w3exceptions

from pathlib import Path
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


SQL_CREATE_TABLE_ACCOUNTS = """
CREATE TABLE IF NOT EXISTS accounts(address text PRIMARY KEY, balance INT NOT NULL);
"""

SQL_CREATE_TABLE_ESCROWS = """
CREATE TABLE IF NOT EXISTS escrows(address text PRIMARY KEY, 
"""


@asynccontextmanager
async def web3_lifespan(app: FastAPI):
    app.web3 = await AsyncWeb3(web3.providers.persistent.AsyncIPCProvider("../chain/execution/data/geth.ipc"))
    app.web3.eth.default_account = (await app.web3.eth.accounts)[0]

    app.bluebank = sqlite3.connect("bluebank.db")
    app.bluebank.cursor().execute(SQL_CREATE_TABLE_ACCOUNTS)
    app.bluebank.commit()

    app.redbank = sqlite3.connect("redbank.db")
    app.redbank.cursor().execute(SQL_CREATE_TABLE_ACCOUNTS)
    app.redbank.commit()

    yield

    app.bluebank.close()
    app.redbank.close()


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


class Deposit(BaseModel):
    walletAddress: str
    amount: int


class Transfer(BaseModel):
    walletAddress: str
    amount: int
    deFi: bool


class CarListing(BaseModel):
    tokenizedAddress: str
    price: int
    lastPurchaseDate: str
    buyerAddress: str
    sellerAddress: str


with open("../target/Car.abi", "rb") as f:
    CAR_CONTRACT_ABI = json.loads(f.read())

with open("../target/Car.bin", "r") as f:
    CAR_CONTRACT_BIN = f.read()

with open("../target/CarEscrow.abi", "rb") as f:
    CAR_ESCROW_ABI = json.loads(f.read())

with open("../target/CarEscrow.bin", "r") as f:
    CAR_ESCROW_BIN = f.read()

with open("../secret.txt", "r") as f:
    ACCOUNT_PK = f.read().strip()

with open("../DEPLOYED_CONTRACTS.json") as f:
    LEDGER_INFO = json.loads(f.read())["CarLedger"]

with open("../DEPLOYED_CONTRACTS.json") as f:
    BLUETOKEN_INFO = json.loads(f.read())["BlueToken"]

with open("../DEPLOYED_CONTRACTS.json") as f:
    REDTOKEN_INFO = json.loads(f.read())["RedToken"]


def store_contract_info(name, abi, receipt):
    """"""

    CONTRACT_INFO_FILE = Path("../DEPLOYED_ESCROWS.json")
    
    info = {}

    if CONTRACT_INFO_FILE.is_file():
        with open(CONTRACT_INFO_FILE, "r") as f:
            info = json.loads(f.read())

    info[name] = {
        "block_hash": "0x" + str(receipt["blockHash"].hex()),
        "block_number": receipt["blockNumber"],
        "tx_hash": "0x" + str(receipt["transactionHash"].hex()),
        "from": receipt["from"],
        "address": receipt["contractAddress"],
        "gas_used": receipt["gasUsed"],
        "effective_gas_price": receipt["effectiveGasPrice"],
        "abi": abi,
    }

    with open(CONTRACT_INFO_FILE, "w") as f:
        json.dump(info, f)


def str_to_int(s: str) -> int:
    """Convert a string to an integer by converting it to bytes."""
    return int.from_bytes(s.encode("utf-8"), byteorder="big")


def int_to_str(i: int) -> str:
    """Convert an integer to a string by converting it to bytes."""
    return i.to_bytes((i.bit_length() + 7) // 8, byteorder="big").decode("utf-8")


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
        abi=LEDGER_INFO["abi"],
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
        abi=LEDGER_INFO["abi"],
    )

    car_address = await ledger_contract.functions.getCarAddress(str_to_int(uniqueId)).call()

    if int(car_address, 16) == 0:
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
            "tokenizedAddress": car_address,
        },
    )


@app.post("/_api/bluebank/deposit")
async def post_bluebank_deposit(deposit: Deposit):
    """ """

    walletAddress = deposit.walletAddress
    amount = deposit.amount

    cur = app.bluebank.cursor()

    cur.execute("""
    INSERT INTO accounts(address, balance)
    VALUES(?, ?) ON CONFLICT(address) DO UPDATE
    SET balance = balance + ?
    """, (walletAddress, amount, amount))

    app.bluebank.commit()

    return JSONResponse(
        status_code=200,
        content={"message": "ok"},
    )


@app.post("/_api/redbank/deposit")
async def post_redbank_deposit(deposit: Deposit):
    """ """

    walletAddress = deposit.walletAddress
    amount = deposit.amount

    cur = app.redbank.cursor()

    cur.execute("""
    INSERT INTO accounts(address, balance)
    VALUES(?, ?) ON CONFLICT(address) DO UPDATE
    SET balance = balance + ?
    """, (walletAddress, amount, amount))

    app.bluebank.commit()

    return JSONResponse(
        status_code=200,
        content={"message": "ok"},
    )


@app.post("/_api/bluebank/transfer")
async def post_bluebank_transfer_balance(transfer: Transfer):
    """ """

    walletAddress = transfer.walletAddress
    amount = transfer.amount

    cur = app.bluebank.cursor()

    cur.execute("SELECT * FROM accounts WHERE address=?", (walletAddress,))
    result = cur.fetchall()

    tradFi_balance = 0 if result == [] else result[0][1]

    token_contract = app.web3.eth.contract(
        address=BLUETOKEN_INFO["address"],
        abi=BLUETOKEN_INFO["abi"],
    )

    deFi_balance = await token_contract.functions.balanceOf(walletAddress).call()

    tx_hash = None

    # transfer to defi from tradfi
    if transfer.deFi:
        if amount > tradFi_balance:
            # can not transfer, not enough balance
            return JSONResponse(
                status_code=500,
                content={"message": f"Could not transfer {amount}, not enough balance"},
            )

        cur.execute("""
        INSERT INTO accounts(address, balance)
        VALUES(?, ?) ON CONFLICT(address) DO UPDATE
        SET balance = balance - ?;
        """, (walletAddress, amount, amount))
        
        mint_tx = await token_contract.functions.mint(walletAddress, amount).build_transaction({
            "from": walletAddress,
            "nonce": await app.web3.eth.get_transaction_count(walletAddress),
            "gas": 3000000,
            "gasPrice": web3.Web3.to_wei(10, "gwei"),
        })

        signed_mint_tx = Account.sign_transaction(mint_tx, private_key=ACCOUNT_PK)
        tx_hash = str((await app.web3.eth.send_raw_transaction(
            signed_mint_tx.raw_transaction,
        )).hex())
        
    else:
        if amount > deFi_balance:
            # can not transfer, not enough balance
            return JSONResponse(
                status_code=500,
                content={"message": f"Could not transfer {amount}, not enough balance"},
            )

        cur.execute("""
        INSERT INTO accounts(address, balance)
        VALUES(?, ?) ON CONFLICT(address) DO UPDATE
        SET balance = balance + ?;
        """, (walletAddress, amount, amount))
        
        burn_tx = await token_contract.functions.burn(walletAddress, amount).build_transaction({
            "from": walletAddress,
            "nonce": await app.web3.eth.get_transaction_count(walletAddress),
            "gas": 3000000,
            "gasPrice": web3.Web3.to_wei(10, "gwei"),
        })

        signed_burn_tx = Account.sign_transaction(burn_tx, private_key=ACCOUNT_PK)
        tx_hash = str((await app.web3.eth.send_raw_transaction(
            signed_burn_tx.raw_transaction,
        )).hex())

    return JSONResponse(
        status_code=200,
        content={"message": f"Successfully transfered {amount}: tx hash '0x{tx_hash}'"},
    )


@app.post("/_api/redbank/transfer")
async def post_redbank_transfer_balance(transfer: Transfer):
    """ """

    walletAddress = transfer.walletAddress
    amount = transfer.amount

    cur = app.redbank.cursor()

    cur.execute("SELECT * FROM accounts WHERE address=?", (walletAddress,))
    result = cur.fetchall()

    tradFi_balance = 0 if result == [] else result[0][1]

    token_contract = app.web3.eth.contract(
        address=REDTOKEN_INFO["address"],
        abi=REDTOKEN_INFO["abi"],
    )

    deFi_balance = await token_contract.functions.balanceOf(walletAddress).call()

    tx_hash = None

    # transfer to defi from tradfi
    if transfer.deFi:
        if amount > tradFi_balance:
            # can not transfer, not enough balance
            return JSONResponse(
                status_code=500,
                content={"message": f"Could not transfer {amount}, not enough balance"},
            )

        cur.execute("""
        INSERT INTO accounts(address, balance)
        VALUES(?, ?) ON CONFLICT(address) DO UPDATE
        SET balance = balance - ?;
        """, (walletAddress, amount, amount))
        
        mint_tx = await token_contract.functions.mint(walletAddress, amount).build_transaction({
            "from": walletAddress,
            "nonce": await app.web3.eth.get_transaction_count(walletAddress),
            "gas": 3000000,
            "gasPrice": web3.Web3.to_wei(10, "gwei"),
        })

        signed_mint_tx = Account.sign_transaction(mint_tx, private_key=ACCOUNT_PK)
        tx_hash = str((await app.web3.eth.send_raw_transaction(
            signed_mint_tx.raw_transaction,
        )).hex())
        
    else:
        if amount > deFi_balance:
            # can not transfer, not enough balance
            return JSONResponse(
                status_code=500,
                content={"message": f"Could not transfer {amount}, not enough balance"},
            )

        cur.execute("""
        INSERT INTO accounts(address, balance)
        VALUES(?, ?) ON CONFLICT(address) DO UPDATE
        SET balance = balance + ?;
        """, (walletAddress, amount, amount))
        
        burn_tx = await token_contract.functions.burn(walletAddress, amount).build_transaction({
            "from": walletAddress,
            "nonce": await app.web3.eth.get_transaction_count(walletAddress),
            "gas": 3000000,
            "gasPrice": web3.Web3.to_wei(10, "gwei"),
        })

        signed_burn_tx = Account.sign_transaction(burn_tx, private_key=ACCOUNT_PK)
        tx_hash = str((await app.web3.eth.send_raw_transaction(
            signed_burn_tx.raw_transaction,
        )).hex())

    return JSONResponse(
        status_code=200,
        content={"message": f"Successfully transfered {amount}: tx hash '0x{tx_hash}'"},
    )



@app.get("/_api/bluebank/account/{walletAddress}")
async def get_bluebank_account_balances(walletAddress: str):
    """ """

    cur = app.bluebank.cursor()

    cur.execute("SELECT * FROM accounts WHERE address=?", (walletAddress,))
    result = cur.fetchall()

    tradFi_balance = 0 if result == [] else result[0][1]

    token_contract = app.web3.eth.contract(
        address=BLUETOKEN_INFO["address"],
        abi=BLUETOKEN_INFO["abi"],
    )

    deFi_balance = await token_contract.functions.balanceOf(walletAddress).call()

    return JSONResponse(
        status_code=200,
        content={
            "TradFi": tradFi_balance,
            "DeFi": deFi_balance,
        },
    )

@app.get("/_api/redbank/account/{walletAddress}")
async def get_redbank_account_balances(walletAddress: str):
    """ """

    cur = app.redbank.cursor()

    cur.execute("SELECT * FROM accounts WHERE address=?", (walletAddress,))
    result = cur.fetchall()

    tradFi_balance = 0 if result == [] else result[0][1]

    token_contract = app.web3.eth.contract(
        address=REDTOKEN_INFO["address"],
        abi=REDTOKEN_INFO["abi"],
    )

    deFi_balance = await token_contract.functions.balanceOf(walletAddress).call()

    return JSONResponse(
        status_code=200,
        content={
            "TradFi": tradFi_balance,
            "DeFi": deFi_balance,
        },
    )

@app.post("/_api/redbank/listCarForSale")
async def post_redbank_list_car_for_sale(carListing: CarListing):
    """ """

    car_address = carListing.tokenizedAddress
    price = carListing.price
    last_purchase_date = strdate_to_int(carListing.lastPurchaseDate)
    buyer = carListing.buyerAddress
    seller = carListing.sellerAddress

    escrow_contract = app.web3.eth.contract(
        abi=CAR_ESCROW_ABI,
        bytecode=CAR_ESCROW_BIN,
    )

    escrow_tx_hash = str((await escrow_contract.constructor(
        car_address,
        buyer,
        seller,
        price,
        last_purchase_date,
        BLUETOKEN_INFO["address"],
        REDTOKEN_INFO["address"],
    ).transact()).hex())

    escrow_tx_receipt = await app.web3.eth.wait_for_transaction_receipt(escrow_tx_hash)
    eaddr = escrow_tx_receipt["contractAddress"]
    store_contract_info(eaddr, CAR_ESCROW_ABI, escrow_tx_receipt)

    return JSONResponse(
        status_code=200,
        content={"message": f"Car sale listing successfull, contract address: '0x{eaddr}'"},
    )


@app.get("/_api/redbank/carListings")
async def get_redbank_car_listings():
    """ """

    path = Path("../DEPLOYED_ESCROWS.json")

    listings = []

    if path.is_file():
        with open("../DEPLOYED_ESCROWS.json", "rb") as f:
            info = json.loads(f.read())
        listings = list(info.keys())

    return JSONResponse(
        status_code=200,
        content={"listings": listings},
    )

