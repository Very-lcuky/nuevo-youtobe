from web3 import Web3
import os
import json
from dotenv import load_dotenv

load_dotenv()

w3 = Web3(Web3.HTTPProvider(os.getenv("RPC_URL")))

erc721_address = w3.to_checksum_address(os.getenv("ERC721_ADDRESS"))

with open("erc721_abi.json") as f:
    erc721_abi = json.load(f)

erc721_contract = w3.eth.contract(address=erc721_address, abi=erc721_abi)

token_id = 1

try:
    owner = erc721_contract.functions.ownerOf(token_id).call()
    print("Owner:", owner)
except Exception as e:
    print("Error ownerOf:", e)

try:
    token_uri = erc721_contract.functions.tokenURI(token_id).call()
    print("TokenURI:", token_uri)
except Exception as e:
    print("Error tokenURI:", e)
