from typing import List, Dict, Any, Optional, Tuple
import json
from web3 import Web3
from web3.contract import Contract
from eth_typing import ChecksumAddress
from decimal import Decimal


def get_contract(contract_address: str, abi_file_path: str, rpc_url: Optional[str] = None) -> Contract:
    """Get a smart contract contract instance on Arbitrum One."""
    w3 = Web3(Web3.HTTPProvider(rpc_url))

    # Verify connection
    if not w3.is_connected():
        raise ConnectionError(f"Failed to connect to {rpc_url}")
    
    # Use checksum address
    address = validate_address(contract_address)
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

def from_wei(value: str) -> Decimal:
    """Convert a value in wei to a decimal with the specified number of decimals."""
    return quantize_decimal(Decimal(value) / Decimal(1e18))

def from_szabo(value: str) -> Decimal:
    """Convert a value in szabo to a decimal with the specified number of decimals."""
    return quantize_decimal(Decimal(value) / Decimal(1e6))

def quantize_decimal(value: Decimal, decimals: int = 6) -> Decimal:
    """Quantize a decimal to the specified number of decimals."""
    return value.quantize(Decimal(f'1e-{decimals}'))

def get_function_selector(abi, function_name):
    """Get function selector from ABI"""
    for item in abi:
        if item['type'] == 'function' and item['name'] == function_name:
            return Web3.keccak(text=f"{function_name}({','.join([input['type'] for input in item['inputs']])})")[:4].hex()
    return None

def encode_calldata(abi, function_name, args=None):
    """Encode function call data using ABI"""
    if args is None:
        args = []
    
    # Find the function in ABI
    function_abi = None
    for item in abi:
        if item['type'] == 'function' and item['name'] == function_name:
            function_abi = item
            break
    
    if not function_abi:
        raise ValueError(f"Function {function_name} not found in ABI")
    
    # Get function selector
    selector = get_function_selector(abi, function_name)
    
    # Encode parameters
    if args:
        encoded_args = Web3().codec.encode_abi(
            [input['type'] for input in function_abi['inputs']],
            args
        ).hex()
    else:
        encoded_args = ''
    
    return f"0x{selector}{encoded_args}"

def decode_string(data: bytes) -> str:
    len = int.from_bytes(data[32:64], byteorder='big')
    return Web3.to_text(data[64:64+len])

def decode_uint256(data: bytes) -> int:
    """Decode uint256 from bytes."""
    return int.from_bytes(data, byteorder='big')

def decode_bool(data: bytes) -> bool:
    """Decode bool from bytes."""
    return bool(int.from_bytes(data, byteorder='big'))

def decode_multicall_try_block_and_aggregate_result(result: Tuple[int, bytes, List[Tuple[bool, bytes]]]) -> Tuple[int, List[Tuple[bool, bytes]]]:
    """Decode multicall result tuple.
    
    Args:
        result: Tuple containing (block_number, block_hash, [(success, return_data), ...])
    
    Returns:
        Tuple of (block_number, list of (success, return_data))
    """
    block_number = result[0]
    return block_number, result[2]  # Skip block_hash (result[1])
    r