import difflib
import time
import sqlite3
from web3 import Web3

# Load the specific contract bytecode you are looking for
with open("../target/CarEscrow.abi", "r") as f:
    CAR_ESCROW_ABI = f.read().strip()

def main():
    # Connect to the Ethereum node
    w3 = Web3(Web3.IPCProvider("../chain/execution/data/geth.ipc"))
    w3.eth.default_account = "0x123463a4B065722E99115D6c222f267d9cABb524"

    # Check if the connection is successful
    if not w3.is_connected():
        print("Failed to connect to the Ethereum node.")
        return

    print("Connected to the Ethereum node.")

    # Subscribe to new block headers
    block_filter = w3.eth.filter('latest')

    while True:
        print("#"*70)
        # Get new block hashes
        new_blocks = block_filter.get_new_entries()

        for block_hash in new_blocks:
            block = w3.eth.get_block(block_hash, full_transactions=True)

            for tx in block.transactions:
                # Check if the transaction created a contract
                if tx.to is None:
                    receipt = w3.eth.get_transaction_receipt(tx.hash)
                    contract_address = receipt.contractAddress

                    if contract_address:
                        try:
                            contract = w3.eth.contract(
                                address=contract_address,
                                abi=CAR_ESCROW_ABI
                            )

                            if hasattr(contract.functions, "withdrawDeposit"):
                                print("CarEscrow contract created at", contract_address)
                        except:
                            print("Created contract was not a CarEscrow...")
                            continue
                        
        # Sleep for a short period to avoid excessive polling
        time.sleep(1.5)

if __name__ == "__main__":
    main()
