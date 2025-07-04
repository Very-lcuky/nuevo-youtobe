import os
from dotenv import load_dotenv
from web3 import Web3
from solcx import compile_standard, install_solc
import json

load_dotenv()

RPC_URL = os.getenv("RPC_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
MY_ADDRESS = os.getenv("MY_ADDRESS")

print("RPC_URL:", RPC_URL)
print("PRIVATE_KEY:", PRIVATE_KEY[:6] + "...")
print("MY_ADDRESS:", MY_ADDRESS)

if not RPC_URL or not PRIVATE_KEY or not MY_ADDRESS:
    raise Exception("Por favor configura RPC_URL, PRIVATE_KEY y MY_ADDRESS en el archivo .env")

w3 = Web3(Web3.HTTPProvider(RPC_URL))

if not w3.is_connected():
    raise Exception("No se pudo conectar al nodo RPC")

chain_id = w3.eth.chain_id
nonce = w3.eth.get_transaction_count(MY_ADDRESS)

install_solc("0.8.0")

with open("VideoViewToken.sol", "r") as file:
    video_token_source = file.read()

compiled_sol = compile_standard({
    "language": "Solidity",
    "sources": {"VideoViewToken.sol": {"content": video_token_source}},
    "settings": {
        "outputSelection": {
            "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
        }
    }
}, solc_version="0.8.0")

abi_video = compiled_sol['contracts']['VideoViewToken.sol']['VideoViewToken']['abi']
bytecode_video = compiled_sol['contracts']['VideoViewToken.sol']['VideoViewToken']['evm']['bytecode']['object']

VideoViewToken = w3.eth.contract(abi=abi_video, bytecode=bytecode_video)

tx = VideoViewToken.constructor().build_transaction({
    "chainId": chain_id,
    "from": MY_ADDRESS,
    "nonce": nonce,
    "gasPrice": w3.toWei('50', 'gwei'),  # o w3.eth.gas_price si prefieres
})

signed_tx = w3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
print("Deploying VideoViewToken...")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"VideoViewToken deployed at {tx_receipt.contractAddress}")

nonce += 1

with open("PayPerView.sol", "r") as file:
    pay_per_view_source = file.read()

compiled_sol_ppv = compile_standard({
    "language": "Solidity",
    "sources": {"PayPerView.sol": {"content": pay_per_view_source}},
    "settings": {
        "outputSelection": {
            "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
        }
    }
}, solc_version="0.8.0")

abi_ppv = compiled_sol_ppv['contracts']['PayPerView.sol']['PayPerView']['abi']
bytecode_ppv = compiled_sol_ppv['contracts']['PayPerView.sol']['PayPerView']['evm']['bytecode']['object']

price_per_view = Web3.toWei(1, 'ether')  # Usa Web3.toWei, no w3.to_wei

PayPerView = w3.eth.contract(abi=abi_ppv, bytecode=bytecode_ppv)

tx2 = PayPerView.constructor(tx_receipt.contractAddress, price_per_view).build_transaction({
    "chainId": chain_id,
    "from": MY_ADDRESS,
    "nonce": nonce,
    "gasPrice": w3.toWei('50', 'gwei'),
})

signed_tx2 = w3.eth.account.sign_transaction(tx2, private_key=PRIVATE_KEY)
tx_hash2 = w3.eth.send_raw_transaction(signed_tx2.rawTransaction)
print("Deploying PayPerView...")
tx_receipt2 = w3.eth.wait_for_transaction_receipt(tx_hash2)
print(f"PayPerView deployed at {tx_receipt2.contractAddress}")

