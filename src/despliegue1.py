from solcx import compile_standard, install_solc, set_solc_version
import json
import os
from web3 import Web3

# Configura aquí tu RPC, clave privada y dirección
RPC_URL = "https://blockchain.googleapis.com/v1/projects/useful-memory-464107-d6/locations/us-central1/endpoints/ethereum-mainnet/rpc?key=AIzaSyCTmJX7pr_wBLHDv1iPE4RKbGuv9eK9nUE"
PRIVATE_KEY = "tu_clave_privada_aqui"
MY_ADDRESS = "tu_direccion_aqui"

solc_version = "0.8.17"

# Intenta fijar la versión de solc, y si no está instalada la instala
try:
    set_solc_version(solc_version)
except Exception:
    install_solc(solc_version)
    set_solc_version(solc_version)

# Leemos el contrato principal desde contracts/VideoViewToken.sol
with open("contracts/VideoViewToken.sol", "r") as f:
    source_code = f.read()

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {
            "VideoViewToken.sol": {"content": source_code}
        },
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "evm.bytecode"]
                }
            }
        },
    },
    base_path=os.path.abspath("contracts"),           # Base path para los imports
    allow_paths=[os.path.abspath("contracts")],       # Permitir solo esa ruta para imports
    solc_version=solc_version,
)

# Guardamos el resultado compilado para inspección (opcional)
with open("compiled_code.json", "w") as f:
    json.dump(compiled_sol, f, indent=4)

# Extraemos ABI y bytecode
contract_id = list(compiled_sol["contracts"]["VideoViewToken.sol"].keys())[0]
abi = compiled_sol["contracts"]["VideoViewToken.sol"][contract_id]["abi"]
bytecode = compiled_sol["contracts"]["VideoViewToken.sol"][contract_id]["evm"]["bytecode"]["object"]

# Conexión Web3
w3 = Web3(Web3.HTTPProvider(RPC_URL))
chain_id = 1  # Mainnet (cambia si usas testnet)

my_address = Web3.to_checksum_address(MY_ADDRESS)
private_key = PRIVATE_KEY

# Crear contrato
contract = w3.eth.contract(abi=abi, bytecode=bytecode)

nonce = w3.eth.get_transaction_count(my_address)

# Construir la transacción para desplegar el contrato
transaction = contract.constructor().build_transaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce,
    }
)

# Firmar y enviar la transacción
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

print(f"Transacción enviada: {tx_hash.hex()}")

# Esperar al recibo de la transacción (confirmación)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"Contrato desplegado en: {tx_receipt.contractAddress}")

