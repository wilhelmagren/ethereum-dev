"""
"""

import web3
import json

from eth_account import Account
from web3 import Web3


if __name__ == "__main__":
    with open("./CONTRACT_DEPLOYMENT_INFO.json", "r") as f:
        token_info = json.loads(f.read())


    w3 = Web3(Web3.IPCProvider("./chain/execution/data/geth.ipc"))
    account = w3.eth.accounts[0]

    w3.eth.default_account = account

    contract = w3.eth.contract(
        address=token_info["CONTRACT_ADDRESS"],
        abi=token_info["CONTRACT_ABI"],
    )

    """
    tx_name_hash = str(contract.functions.name().build_transaction({
        "from": account,
        "nonce": w3.eth.get_transaction_count(account),
        "gas": 300000,
        "gasPrice": web3.Web3.to_wei("20", "gwei"),
    }).send_transaction().hex())

    tx_name_receipt = w3.eth.wait_for_transaction_receipt(tx_name_hash)
    print(tx_name_receipt)
    """

    name = str(contract.functions.totalSupply().call())
    print(name)

