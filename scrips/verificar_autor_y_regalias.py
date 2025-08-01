from web3 import Web3
import json
import os
from dotenv import load_dotenv
from web3.exceptions import BadFunctionCallOutput

# =======================
# Cargar variables del .env
# =======================
load_dotenv()
eth_node_url = os.getenv("RPC_URL")
erc721_address = os.getenv("ERC721_ADDRESS")
my_address = os.getenv("MY_ADDRESS")  # Tu wallet oficial

# =======================
# Conexión a la red
# =======================
w3 = Web3(Web3.HTTPProvider(eth_node_url))
if not w3.is_connected():
    print("❌ No se pudo conectar a la blockchain")
    exit()

erc721_address = w3.to_checksum_address(erc721_address)
my_address = w3.to_checksum_address(my_address)

# =======================
# ABI con ownerOf y royaltyInfo (EIP-2981)
# =======================
erc721_abi = [
    {
        "inputs": [
            {"internalType": "uint256", "name": "_tokenId", "type": "uint256"},
            {"internalType": "uint256", "name": "_salePrice", "type": "uint256"}
        ],
        "name": "royaltyInfo",
        "outputs": [
            {"internalType": "address", "name": "receiver", "type": "address"},
            {"internalType": "uint256", "name": "royaltyAmount", "type": "uint256"}
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "uint256", "name": "tokenId", "type": "uint256"}],
        "name": "ownerOf",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function"
    }
]

# =======================
# Instancia del contrato
# =======================
erc721 = w3.eth.contract(address=erc721_address, abi=erc721_abi)

# =======================
# Verificar regalías + dueño
# =======================
token_id = int(input("➡️ Ingresa el tokenId del NFT que quieras verificar: "))
sale_price = 100 * 10**18  # Simulación venta de 100 tokens

# --- Verificación de regalías ---
try:
    receiver, royalty_amount = erc721.functions.royaltyInfo(token_id, sale_price).call()
    porcentaje = (royalty_amount / sale_price) * 100

    print("\n🔹 REGALÍAS (EIP-2981)")
    print(f"   ➡️ Receptor configurado: {receiver}")
    print(f"   ➡️ Porcentaje: {porcentaje:.2f}%")

    if receiver.lower() == my_address.lower():
        print("✅ Tú eres el receptor de las regalías (derechos de autor protegidos)")
    else:
        print("⚠️ ALERTA: Las regalías están dirigidas a otra dirección, revisa el contrato.")

except BadFunctionCallOutput:
    print("\n⚠️ Este contrato NO implementa EIP-2981 (no hay regalías automáticas configuradas)")

# --- Verificación de dueño ---
try:
    owner = erc721.functions.ownerOf(token_id).call()
    print(f"\n👑 Dueño actual del token {token_id}: {owner}")

    if owner.lower() == my_address.lower():
        print("✅ Tú eres el dueño actual de este NFT")
    else:
        print("⚠️ Este NFT ya no está en tu wallet")

except:
    print("\n⚠️ No se pudo obtener el dueño. El tokenId puede no existir.")
