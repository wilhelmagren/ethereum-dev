"""
"""

import json

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

    # name = str(contract.functions.greet().call())
    # print(name)

    n_tokens = str(contract.functions.totalSupply().call())
    print(n_tokens)


