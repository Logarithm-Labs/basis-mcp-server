from typing import List, Dict, Any, Optional, Tuple
import json
import os
from web3 import Web3
from web3.contract import Contract
from eth_typing import ChecksumAddress

# Connect to Arbitrum One
RPC_URL = os.environ.get("ARBITRUM_RPC_URL", "https://arb1.arbitrum.io/rpc")

w3 = Web3(Web3.HTTPProvider(RPC_URL))

# Verify connection
if not w3.is_connected():
    raise ConnectionError(f"Failed to connect to Arbitrum One at {RPC_URL}")

# Helper functions
def get_contract(contract_address: str, abi_file_path: str) -> Contract:
    """Get a smart contract contract instance on Arbitrum One."""
    
    if not contract_address:
        raise ValueError("CONTRACT_ADDRESS environment variable not set")
    
    # Use checksum address
    address = Web3.to_checksum_address(contract_address)
    with open(abi_file_path) as abi_file:
        abi = json.load(abi_file)
        return w3.eth.contract(address=address, abi=abi)
    
def format_transaction_data(tx_data: Dict[str, Any]) -> str:
    """Format transaction data for user to sign."""
    formatted = {
        "to": tx_data["to"],
        "from": tx_data.get("from", "YOUR_ADDRESS"),
        "data": tx_data["data"],
        "value": tx_data.get("value", 0),
        "gas": tx_data.get("gas", "AUTO"),
        "gasPrice": tx_data.get("gasPrice", "AUTO"),
        "nonce": tx_data.get("nonce", "AUTO"),
        "chainId": 42161,  # Arbitrum One
    }
    return json.dumps(formatted, indent=2)

def validate_address(address: str) -> str:
    """Validate Ethereum address."""
    try:
        return Web3.to_checksum_address(address)
    except ValueError:
        raise ValueError(f"Invalid Ethereum address: {address}")
    
def validate_address_list(addresses: List[str]) -> List[ChecksumAddress]:
    """Validate a list of Ethereum addresses."""
    return [validate_address(addr) for addr in addresses]

def to_hex(value: str) -> str:
    """Returns a hex presentation for a given value"""
    return Web3.to_hex(value)

def get_transaction_count(checksum_address: str) -> int:
    """Get a transaction count"""
    return w3.eth.get_transaction_count(checksum_address)
    