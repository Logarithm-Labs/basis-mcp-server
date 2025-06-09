from typing import List, Dict, Any, Optional, Tuple
from mcp.server.fastmcp import FastMCP
from web3_utils import get_contract, encode_calldata, decode_string, decode_uint256, decode_multicall_try_block_and_aggregate_result, from_wei, from_szabo
from constants import LOGARITHM_VAULT_ADDRESSES, MULTICALL_ADDRESSES, LOGARITHM_VAULT_ABI_PATH, MULTICALL_ABI_PATH, ALCHEMY_RPC_URLS
import json

# Initialize FastMCP server
mcp = FastMCP("Logarithm-vault")

@mcp.tool()
async def get_all_logarithm_vault_info(depositor: Optional[str] = None) -> str:
    """Returns a list of all available Logarithm vaults along with their information.

    Args:
        depositor: The address of the depositor. If provided, additional information related to the depositor will be returned.
    """

    chain_id = 42161 # only support arbitrum for now
    
    # Load ABIs
    with open(LOGARITHM_VAULT_ABI_PATH, 'r') as f:
        vault_abi = json.load(f)
    
    calls = []
    
    for address in LOGARITHM_VAULT_ADDRESSES[chain_id]:
        # derive calldata for each function using ABI
        name_calldata = encode_calldata(vault_abi, 'name')
        symbol_calldata = encode_calldata(vault_abi, 'symbol')
        totalSupply_calldata = encode_calldata(vault_abi, 'totalSupply')
        totalAssets_calldata = encode_calldata(vault_abi, 'totalAssets')
        entryCost_calldata = encode_calldata(vault_abi, 'entryCost')
        exitCost_calldata = encode_calldata(vault_abi, 'exitCost')
        idleAssets_calldata = encode_calldata(vault_abi, 'idleAssets')
        totalPendingWithdraw_calldata = encode_calldata(vault_abi, 'totalPendingWithdraw')
        
        # Create list of calls for multicall
        calls.extend([
            (address, name_calldata),
            (address, symbol_calldata),
            (address, totalSupply_calldata),
            (address, totalAssets_calldata),
            (address, entryCost_calldata),
            (address, exitCost_calldata),
            (address, idleAssets_calldata),
            (address, totalPendingWithdraw_calldata)
        ])
        
        if depositor:
            maxDeposit_calldata = encode_calldata(vault_abi, 'maxDeposit', [depositor])
            balanceOf_calldata = encode_calldata(vault_abi, 'balanceOf', [depositor])
            calls.extend([
                (address, maxDeposit_calldata),
                (address, balanceOf_calldata)
            ])
    
    # Execute multicall
    multicall = get_contract(MULTICALL_ADDRESSES[chain_id], MULTICALL_ABI_PATH, ALCHEMY_RPC_URLS[chain_id])
    result = multicall.functions.tryBlockAndAggregate(False, calls).call()
    
    # Decode results
    block_number, return_data = decode_multicall_try_block_and_aggregate_result(result)
    
    # Process results for each vault
    infos = {}
    current_index = 0
    calls_per_vault = len(calls) // len(LOGARITHM_VAULT_ADDRESSES[chain_id])
    for address in LOGARITHM_VAULT_ADDRESSES[chain_id]:
        # Parse results for this vault
        infos[address] = {
            f'name': decode_string(return_data[current_index][1]),
            f'symbol': decode_string(return_data[current_index + 1][1]),
            f'totalSupply': from_szabo(decode_uint256(return_data[current_index + 2][1])),
            f'totalAssets': from_szabo(decode_uint256(return_data[current_index + 3][1])),
            f'entryCostRate': from_wei(decode_uint256(return_data[current_index + 4][1])),
            f'exitCostRate': from_wei(decode_uint256(return_data[current_index + 5][1])),
            f'idleAssets': from_szabo(decode_uint256(return_data[current_index + 6][1])),
            f'totalPendingWithdraw': from_szabo(decode_uint256(return_data[current_index + 7][1]))
        }
        if depositor:
            infos[address].update({
                f'maxDeposit': from_szabo(decode_uint256(return_data[current_index + 8][1])),
                f'balanceOf': from_szabo(decode_uint256(return_data[current_index + 9][1]))
            })
        
        current_index += calls_per_vault

    result = f"### Logarithm Vaults (Chain ID: {chain_id}, Block Number: {block_number})\n\n"
    for address, info in infos.items():
        result += f"Address: {address}\n"
        result += f"Name: {info[f'name']}\n"
        result += f"Symbol: {info[f'symbol']}\n"
        result += f"Total Supply: {info[f'totalSupply']}\n"
        result += f"Total Assets: {info[f'totalAssets']}\n"
        result += f"Entry Cost Rate: {info[f'entryCostRate']}\n"
        result += f"Exit Cost Rate: {info[f'exitCostRate']}\n"
        result += f"Idle Assets: {info[f'idleAssets']}\n"
        if depositor:
            result += f"Pending Withdraw: {info[f'totalPendingWithdraw']}\n"
            result += f"Max Deposit: {info[f'maxDeposit']}\n"
            result += f"Share Balance: {info[f'balanceOf']}\n\n"
        else:
            result += f"Pending Withdraw: {info[f'totalPendingWithdraw']}\n\n"

    return result

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')