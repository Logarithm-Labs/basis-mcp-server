from typing import List, Dict, Any, Optional, Tuple
from mcp.server.fastmcp import FastMCP
from web3_utils import get_contract, validate_address, to_hex, validate_address_list, get_transaction_count, format_transaction_data
import os

META_VAULT_ABI_PATH = "abis/MetaVault.abi.json"
CONTRACT_ADDRESS = os.environ.get("CONTRACT_ADDRESS", "") 

# Initialize FastMCP server
mcp = FastMCP("meta vault")

# Read-only functions
@mcp.tool()
async def get_allocated_assets() -> str:
    """Get the total allocated assets across logarithm vaults.

    Returns:
        str: The total allocated assets as a string (to preserve full precision)
    """
    contract = get_contract(CONTRACT_ADDRESS, META_VAULT_ABI_PATH)
    result = contract.functions.allocatedAssets().call()
    return str(result)


@mcp.tool()
async def get_allocated_vaults() -> List[str]:
    """Get the list of logarithm vaults that currently have allocations.

    Returns:
        List[str]: List of logarithm vault addresses
    """
    contract = get_contract(CONTRACT_ADDRESS, META_VAULT_ABI_PATH)
    result = contract.functions.allocatedVaults().call()
    return [addr for addr in result]


@mcp.tool()
async def get_allocation_claimable_assets() -> Dict[str, str]:
    """Get the requested and claimable assets amounts from logarithm vaults.

    Returns:
        Dict[str, str]: Dictionary with requestedAssets and claimableAssets
    """
    contract = get_contract(CONTRACT_ADDRESS, META_VAULT_ABI_PATH)
    requested, claimable = contract.functions.allocationClaimableAssets().call()
    return {
        "requestedAssets": str(requested),
        "claimableAssets": str(claimable)
    }


@mcp.tool()
async def get_allocation_withdraw_keys(logarithm_vault_address: str) -> List[str]:
    """Get the withdrawal keys and a logarithm vault.
    
    Args:
        logarithm_vault_address (str): Address of the logarithm vault
        
    Returns:
        List[str]: List of withdraw keys as hex strings
    """
    contract = get_contract(CONTRACT_ADDRESS, META_VAULT_ABI_PATH)
    checksum_address = validate_address(logarithm_vault_address)
    result = contract.functions.allocationWithdrawKeys(checksum_address).call()
    return [to_hex(key) for key in result]


@mcp.tool()
async def get_claimable_vaults() -> List[str]:
    """Get the list of logarithm vaults that have claimable assets.

    Returns:
        List[str]: List of logarithm vault addresses
    """
    contract = get_contract(CONTRACT_ADDRESS, META_VAULT_ABI_PATH)
    result = contract.functions.claimableVaults().call()
    return [addr for addr in result]


@mcp.tool()
async def get_idle_assets() -> str:
    """Get the total idle assets.

    Returns:
        str: The total idle assets as a string (to preserve full precision)
    """
    contract = get_contract(CONTRACT_ADDRESS, META_VAULT_ABI_PATH)
    result = contract.functions.idleAssets().call()
    return str(result)

@mcp.tool()
async def get_share_price() -> str:
    """Get the share price.

    Returns:
        str: The share price as a string (to preserve full precision)
    """
    contract = get_contract(CONTRACT_ADDRESS, META_VAULT_ABI_PATH)
    total_supply = contract.functions.totalSupply().call()
    total_assets = contract.functions.totalAssets().call()
    decimals = contract.functions.decimals().call()
    result = total_assets * (10 ** decimals) // total_supply if total_supply > 0 else 0
    return str(result)



# Write functions (transaction preparation)
@mcp.tool()
async def prepare_allocate_transaction(
    from_address: str, targets: List[str], assets: List[str]
) -> str:
    """Prepare a transaction to allocate assets to multiple logarithm vaults.
    
    Args:
        from_address (str): Address that will send the transaction
        targets (List[str]): List of logarithm vault addresses to allocate to
        assets (List[str]): List of asset amounts to allocate (as strings to preserve precision)
        
    Returns:
        str: Transaction data JSON that needs to be signed
    """
    if len(targets) != len(assets):
        raise ValueError("targets and assets lists must be the same length")
    
    contract = get_contract(CONTRACT_ADDRESS, META_VAULT_ABI_PATH)
    checksum_from = validate_address(from_address)
    checksum_targets = validate_address(targets)
    
    # Convert string amounts to integers
    int_assets = [int(asset) for asset in assets]
    
    # Build transaction
    tx = contract.functions.allocate(
        checksum_targets, int_assets
    ).build_transaction({
        "from": checksum_from,
        "nonce": get_transaction_count(checksum_from),
        "gas": 0,  # Will be estimated by wallet
        "gasPrice": 0,  # Will be estimated by wallet
    })
    
    return format_transaction_data(tx)


@mcp.tool()
async def prepare_redeem_allocations_transaction(
    from_address: str, targets: List[str], shares: List[str]
) -> str:
    """Prepare a transaction to redeem shares from multiple logarithm vaults.
    
    Args:
        
        from_address (str): Address that will send the transaction
        targets (List[str]): List of logarithm vault addresses to redeem from
        shares (List[str]): List of share amounts to redeem (as strings to preserve precision)
        
    Returns:
        str: Transaction data JSON that needs to be signed
    """
    if len(targets) != len(shares):
        raise ValueError("targets and shares lists must be the same length")
    
    contract = get_contract(CONTRACT_ADDRESS, META_VAULT_ABI_PATH)
    checksum_from = validate_address(from_address)
    checksum_targets = validate_address_list(targets)
    
    # Convert string amounts to integers
    int_shares = [int(share) for share in shares]
    
    # Build transaction
    tx = contract.functions.redeemAllocations(
        checksum_targets, int_shares
    ).build_transaction({
        "from": checksum_from,
        "nonce": get_transaction_count(checksum_from),
        "gas": 0,  # Will be estimated by wallet
        "gasPrice": 0,  # Will be estimated by wallet
    })
    
    return format_transaction_data(tx)


@mcp.tool()
async def prepare_withdraw_allocations_transaction(
    from_address: str, targets: List[str], assets: List[str]
) -> str:
    """Prepare a transaction to withdraw assets from multiple logarithm vaults.
    
    Args:
        from_address (str): Address that will send the transaction
        targets (List[str]): List of logarithm vault addresses to withdraw from
        assets (List[str]): List of asset amounts to withdraw (as strings to preserve precision)
        
    Returns:
        str: Transaction data JSON that needs to be signed
    """
    if len(targets) != len(assets):
        raise ValueError("targets and assets lists must be the same length")
    
    contract = get_contract(CONTRACT_ADDRESS, META_VAULT_ABI_PATH)
    checksum_from = validate_address(from_address)
    checksum_targets = validate_address_list(targets)
    
    # Convert string amounts to integers
    int_assets = [int(asset) for asset in assets]
    
    # Build transaction
    tx = contract.functions.withdrawAllocations(
        checksum_targets, int_assets
    ).build_transaction({
        "from": checksum_from,
        "nonce": get_transaction_count(checksum_from),
        "gas": 0,  # Will be estimated by wallet
        "gasPrice": 0,  # Will be estimated by wallet
    })
    
    return format_transaction_data(tx)


if __name__ == "__main__":
    # Run the MCP server
    mcp.run(transport='stdio')