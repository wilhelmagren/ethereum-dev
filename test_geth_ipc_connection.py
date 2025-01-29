from web3 import Web3

w3 = Web3(Web3.IPCProvider("./chain/execution/data/geth.ipc"))

print(w3.is_connected())

pa = w3.eth.account.from_key("0x2e0834786285daccd064ca17f1654f67b4aef298acbb82cef9ec422fb4975622")
print(pa.address)
print(pa)

