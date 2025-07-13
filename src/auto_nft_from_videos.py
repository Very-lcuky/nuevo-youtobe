import os
import json
from pathlib import Path
from web3 import Web3
from eth_account import Account
from dotenv import load_dotenv

load_dotenv()  # carga las variables del .env

RPC_URL = os.getenv("RPC_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
ADDRESS = os.getenv("MY_ADDRESS")

FACTORY_ADDRESS = "0xTU_FACTORY_ADDRESS"  # cambia esta a tu factory real

with open("abi/VideoNFTFactory.json") as f:
    FACTORY_ABI = json.load(f)

VIDEO_DIR = Path("./tmp_videos")  # o donde tengas tus videos

w3 = Web3(Web3.HTTPProvider(RPC_URL))
acct = Account.from_key(PRIVATE_KEY)
factory = w3.eth.contract(address=FACTORY_ADDRESS, abi=FACTORY_ABI)

def crear_nft_para_video(video_path: Path):
    name = video_path.stem[:32]
    symbol = "VYTB"
    royalty = 500

    tx = factory.functions.createVideoNFT(name, symbol, royalty).build_transaction({
        "nonce": w3.eth.get_transaction_count(ADDRESS),
        "gas": 500_000,
        "maxFeePerGas": w3.to_wei("50", "gwei"),
        "maxPriorityFeePerGas": w3.to_wei("2", "gwei"),
    })
    signed = acct.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
    print(f"✅ NFT de {video_path.name} mint pendiente: {tx_hash.hex()}")

def main():
    for video in VIDEO_DIR.glob("*.webm"):
        crear_nft_para_video(video)

if __name__ == "__main__":
    main()
