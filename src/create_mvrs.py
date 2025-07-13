import os
import json
from web3 import Web3
from eth_account import Account
from dotenv import load_dotenv

load_dotenv()

RPC_URL = os.getenv("RPC_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
ADDRESS = Web3.to_checksum_address(os.getenv("MY_ADDRESS"))

FACTORY_ADDRESS = Web3.to_checksum_address("0xc5190A86545c8bdbeEA24F6938F631AD38Fc6787")

with open("abi_TokenFactory.json") as f:
    FACTORY_ABI = json.load(f)

w3 = Web3(Web3.HTTPProvider(RPC_URL))
acct = Account.from_key(PRIVATE_KEY)
factory = w3.eth.contract(address=FACTORY_ADDRESS, abi=FACTORY_ABI)

def crear_token_advanced(
    initial_supply: int,
    max_wallet_limit: int,
    marketing_wallet: str,
    liquidity_wallet: str,
    marketing_fee: int,
    liquidity_fee: int
):
    nonce = w3.eth.get_transaction_count(ADDRESS, 'pending')
    balance = w3.eth.get_balance(ADDRESS)
    print(f"Nonce actual: {nonce}")
    print(f"Balance actual: {w3.from_wei(balance, 'ether')} ETH")

    try:
        gas_estimate = factory.functions.createMVRS(
            initial_supply,
            max_wallet_limit,
            Web3.to_checksum_address(marketing_wallet),
            Web3.to_checksum_address(liquidity_wallet),
            marketing_fee,
            liquidity_fee
        ).estimate_gas({'from': ADDRESS})
    except Exception as e:
        print(f"Error al estimar gas: {e}")
        gas_estimate = 700_000  # fallback gas

    print(f"Gas estimado: {gas_estimate}")

    # Verificar si hay balance suficiente para gas
    max_fee = w3.to_wei("100", "gwei")  # maxFeePerGas
    estimated_cost = gas_estimate * max_fee
    if balance < estimated_cost:
        print("⚠️ Balance insuficiente para pagar la comisión de gas estimada.")
        return

    tx = factory.functions.createMVRS(
        initial_supply,
        max_wallet_limit,
        Web3.to_checksum_address(marketing_wallet),
        Web3.to_checksum_address(liquidity_wallet),
        marketing_fee,
        liquidity_fee
    ).build_transaction({
        "from": ADDRESS,
        "nonce": nonce,
        "gas": gas_estimate,
        "maxFeePerGas": max_fee,
        "maxPriorityFeePerGas": w3.to_wei("10", "gwei"),
    })

    signed_tx = acct.sign_transaction(tx)

    try:
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        print(f"✅ Token MVRS creado. TX Hash: {tx_hash.hex()}")
    except Exception as e:
        print(f"Error al enviar transacción: {e}")

if __name__ == "__main__":
    initial_supply = 1_000_000_000 * 10**18
    max_wallet_limit = 1_000_000 * 10**18

    marketing_wallet = "0xc5190A86545c8bdbeEA24F6938F631AD38Fc6787"
    liquidity_wallet = "0xc5190A86545c8bdbeEA24F6938F631AD38Fc6787"

    marketing_fee = 200
    liquidity_fee = 300

    crear_token_advanced(
        initial_supply,
        max_wallet_limit,
        marketing_wallet,
        liquidity_wallet,
        marketing_fee,
        liquidity_fee
    )

