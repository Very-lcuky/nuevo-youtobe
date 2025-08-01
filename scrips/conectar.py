from web3 import Web3
import json
import os
import requests
from dotenv import load_dotenv
from web3.exceptions import InvalidAddress

load_dotenv()

eth_node_url = os.getenv("RPC_URL")
my_address = os.getenv("MY_ADDRESS")
private_key = os.getenv("PRIVATE_KEY")
erc721_address = os.getenv("ERC721_ADDRESS")
erc20_address = os.getenv("ERC20_ADDRESS")

w3 = Web3(Web3.HTTPProvider(eth_node_url))

if not w3.is_connected():
    print("❌ No se pudo conectar a la blockchain")
    exit()

try:
    my_address = w3.to_checksum_address(my_address)
    erc721_address = w3.to_checksum_address(erc721_address)
    erc20_address = w3.to_checksum_address(erc20_address)
except InvalidAddress as e:
    print("⚠️ Dirección no válida:", e)
    exit()

with open("erc721_abi.json") as f:
    erc721_abi = json.load(f)

erc721_contract = w3.eth.contract(address=erc721_address, abi=erc721_abi)

def get_token_uri(token_id):
    try:
        uri = erc721_contract.functions.tokenURI(token_id).call()
        return uri
    except Exception as e:
        print(f"⚠️ Error al obtener tokenURI: {e}")
        return None

def fetch_metadata(uri):
    if uri.startswith("ipfs://"):
        uri = uri.replace("ipfs://", "https://ipfs.io/ipfs/")
    try:
        response = requests.get(uri)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"⚠️ No se pudo descargar o parsear la metadata: {e}")
        return None

def check_owner(token_id):
    try:
        owner = erc721_contract.functions.ownerOf(token_id).call()
        print(f"👑 El dueño actual del NFT {token_id} es: {owner}")
    except Exception as e:
        print("⚠️ No se pudo verificar el dueño del token:", e)

def check_royalties(token_id, sale_price_wei):
    try:
        royalty_info = erc721_contract.functions.royaltyInfo(token_id, sale_price_wei).call()
        recipient, amount = royalty_info
        print(f"💸 Regalías por venta de 1 ETH: {amount} wei ({amount/1e18} ETH) para {recipient}")
    except Exception as e:
        print("⚠️ El contrato no soporta EIP-2981 o no tiene regalías configuradas:", e)

if __name__ == "__main__":
    try:
        token_id = int(input("➡️ Ingresa el tokenId del NFT que quieras verificar: "))
        check_owner(token_id)

        uri = get_token_uri(token_id)
        if uri:
            metadata = fetch_metadata(uri)
            if metadata:
                print("\n📄 Metadata del NFT:")
                print(json.dumps(metadata, indent=2, ensure_ascii=False))

        sale_price = w3.to_wei(1, "ether")
        check_royalties(token_id, sale_price)

    except ValueError:
        print("❌ Entrada no válida. Asegúrate de ingresar un tokenId numérico.")

