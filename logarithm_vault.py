from typing import List, Dict, Any, Optional, Tuple
from mcp.server.fastmcp import FastMCP
from web3_utils import get_contract, validate_address, to_hex, validate_address_list, get_transaction_count, format_transaction_data
import os

LOGARITHM_VAULT_ABI_PATH = "abis/LogarithmVault.abi.json"

# Available Logarithm contract addresses
AVAILABLE_CONTRACTS = [
    "0x55d9615C3bEfe4B991d864892db2AaA6bcefc16C",
    "0xa4885f18cb744aC5e48Bc8932fe4829B0022Df84",
    "0x7b1E49EE1f796f3337ADD57edDE071C49F3CA8A3",
    "0xddAF1C0B6aeDf286D0a50ab9386c3DE254af1b13"
]

# Initialize FastMCP server
mcp = FastMCP("logarithmvault")

# Read-only functions
@mcp.tool()
async def get_asset(contract_address: str) -> str:
    """Get the underlying asset address of the vault.

    Args:
        contract_address (str): Address of the LogarithmVault contract
        
    Returns:
        str: The address of the underlying asset
    """
    contract = get_contract(contract_address, LOGARITHM_VAULT_ABI_PATH)
    result = contract.functions.asset().call()
    return result

@mcp.tool()
async def get_assets_to_claim(contract_address: str) -> str:
    """Get the total assets that are available to claim.

    Args:
        contract_address (str): Address of the LogarithmVault contract
        
    Returns:
        str: The total claimable assets as a string (to preserve full precision)
    """
    contract = get_contract(contract_address, LOGARITHM_VAULT_ABI_PATH)
    result = contract.functions.assetsToClaim().call()
    return str(result)

@mcp.tool()
async def get_balance_of(contract_address: str, account: str) -> str:
    """Get the balance of shares for a specific account.
    
    Args:
        contract_address (str): Address of the LogarithmVault contract
        account (str): Address of the account to check
        
    Returns:
        str: The balance of shares as a string (to preserve full precision)
    """
    contract = get_contract(contract_address, LOGARITHM_VAULT_ABI_PATH)
    checksum_address = validate_address(account)
    result = contract.functions.balanceOf(checksum_address).call()
    return str(result)

@mcp.tool()
async def convert_to_assets(contract_address: str, shares: str) -> str:
    """Convert a given amount of shares to the equivalent amount of assets.
    
    Args:
        contract_address (str): Address of the LogarithmVault contract
        shares (str): Amount of shares to convert (as string to preserve precision)
        
    Returns:
        str: The equivalent amount of assets as a string
    """
    contract = get_contract(contract_address, LOGARITHM_VAULT_ABI_PATH)
    result = contract.functions.convertToAssets(int(shares)).call()
    return str(result)

@mcp.tool()
async def convert_to_shares(contract_address: str, assets: str) -> str:
    """Convert a given amount of assets to the equivalent amount of shares.
    
    Args:
        contract_address (str): Address of the LogarithmVault contract
        assets (str): Amount of assets to convert (as string to preserve precision)
        
    Returns:
        str: The equivalent amount of shares as a string
    """
    contract = get_contract(contract_address, LOGARITHM_VAULT_ABI_PATH)
    result = contract.functions.convertToShares(int(assets)).call()
    return str(result)

@mcp.tool()
async def get_decimals(contract_address: str) -> int:
    """Get the number of decimals used by the vault shares.

    Args:
        contract_address (str): Address of the LogarithmVault contract
        
    Returns:
        int: The number of decimals
    """
    contract = get_contract(contract_address, LOGARITHM_VAULT_ABI_PATH)
    result = contract.functions.decimals().call()
    return result

@mcp.tool()
async def get_entry_cost(contract_address: str) -> str:
    """Get the current entry cost for the vault.

    Args:
        contract_address (str): Address of the LogarithmVault contract
        
    Returns:
        str: The entry cost as a string (to preserve full precision)
    """
    contract = get_contract(contract_address, LOGARITHM_VAULT_ABI_PATH)
    result = contract.functions.entryCost().call()
    return str(result)

@mcp.tool()
async def get_exit_cost(contract_address: str) -> str:
    """Get the current exit cost for the vault.

    Args:
        contract_address (str): Address of the LogarithmVault contract
        
    Returns:
        str: The exit cost as a string (to preserve full precision)
    """
    contract = get_contract(contract_address, LOGARITHM_VAULT_ABI_PATH)
    result = contract.functions.exitCost().call()
    return str(result)

@mcp.tool()
async def get_idle_assets(contract_address: str) -> str:
    """Get the total idle assets in the vault.

    Args:
        contract_address (str): Address of the LogarithmVault contract
        
    Returns:
        str: The total idle assets as a string (to preserve full precision)
    """
    contract = get_contract(contract_address, LOGARITHM_VAULT_ABI_PATH)
    result = contract.functions.idleAssets().call()
    return str(result)

@mcp.tool()
async def is_shutdown(contract_address: str) -> bool:
    """Check if the vault is currently shutdown.

    Args:
        contract_address (str): Address of the LogarithmVault contract
        
    Returns:
        bool: True if the vault is shutdown, False otherwise
    """
    contract = get_contract(contract_address, LOGARITHM_VAULT_ABI_PATH)
    return contract.functions.isShutdown().call()

@mcp.tool()
async def get_max_deposit(contract_address: str, receiver: str) -> str:
    """Get the maximum amount of assets that can be deposited for a receiver.
    
    Args:
        contract_address (str): Address of the LogarithmVault contract
        receiver (str): Address that will receive the shares
        
    Returns:
        str: The maximum deposit amount as a string
    """
    contract = get_contract(contract_address, LOGARITHM_VAULT_ABI_PATH)
    checksum_address = validate_address(receiver)
    result = contract.functions.maxDeposit(checksum_address).call()
    return str(result)

@mcp.tool()
async def get_max_mint(contract_address: str, receiver: str) -> str:
    """Get the maximum amount of shares that can be minted for a receiver.
    
    Args:
        contract_address (str): Address of the LogarithmVault contract
        receiver (str): Address that will receive the shares
        
    Returns:
        str: The maximum mint amount as a string
    """
    contract = get_contract(contract_address, LOGARITHM_VAULT_ABI_PATH)
    checksum_address = validate_address(receiver)
    result = contract.functions.maxMint(checksum_address).call()
    return str(result)

@mcp.tool()
async def get_max_redeem(contract_address: str, owner: str) -> str:
    """Get the maximum amount of shares that can be redeemed by an owner.
    
    Args:
        contract_address (str): Address of the LogarithmVault contract
        owner (str): Address of the shares owner
        
    Returns:
        str: The maximum redeem amount as a string
    """
    contract = get_contract(contract_address, LOGARITHM_VAULT_ABI_PATH)
    checksum_address = validate_address(owner)
    result = contract.functions.maxRedeem(checksum_address).call()
    return str(result)

@mcp.tool()
async def get_max_withdraw(contract_address: str, owner: str) -> str:
    """Get the maximum amount of assets that can be withdrawn by an owner.
    
    Args:
        contract_address (str): Address of the LogarithmVault contract
        owner (str): Address of the shares owner
        
    Returns:
        str: The maximum withdraw amount as a string
    """
    contract = get_contract(contract_address, LOGARITHM_VAULT_ABI_PATH)
    checksum_address = validate_address(owner)
    result = contract.functions.maxWithdraw(checksum_address).call()
    return str(result)

@mcp.tool()
async def get_vault_info(contract_address: str) -> Dict[str, str]:
    """Get the basic information about the vault (name and symbol).

    Args:
        contract_address (str): Address of the LogarithmVault contract
        
    Returns:
        Dict[str, str]: Dictionary containing name and symbol of the vault
    """
    contract = get_contract(contract_address, LOGARITHM_VAULT_ABI_PATH)
    name = contract.functions.name().call()
    symbol = contract.functions.symbol().call()
    return {
        "name": name,
        "symbol": symbol
    }

@mcp.tool()
async def preview_deposit(contract_address: str, assets: str) -> str:
    """Preview the amount of shares that would be minted for a deposit.
    
    Args:
        contract_address (str): Address of the LogarithmVault contract
        assets (str): Amount of assets to deposit (as string to preserve precision)
        
    Returns:
        str: The amount of shares that would be minted
    """
    contract = get_contract(contract_address, LOGARITHM_VAULT_ABI_PATH)
    result = contract.functions.previewDeposit(int(assets)).call()
    return str(result)

@mcp.tool()
async def preview_mint(contract_address: str, shares: str) -> str:
    """Preview the amount of assets needed for minting shares.
    
    Args:
        contract_address (str): Address of the LogarithmVault contract
        shares (str): Amount of shares to mint (as string to preserve precision)
        
    Returns:
        str: The amount of assets needed
    """
    contract = get_contract(contract_address, LOGARITHM_VAULT_ABI_PATH)
    result = contract.functions.previewMint(int(shares)).call()
    return str(result)

@mcp.tool()
async def preview_redeem(contract_address: str, shares: str) -> str:
    """Preview the amount of assets that would be received for redeeming shares.
    
    Args:
        contract_address (str): Address of the LogarithmVault contract
        shares (str): Amount of shares to redeem (as string to preserve precision)
        
    Returns:
        str: The amount of assets that would be received
    """
    contract = get_contract(contract_address, LOGARITHM_VAULT_ABI_PATH)
    result = contract.functions.previewRedeem(int(shares)).call()
    return str(result)

@mcp.tool()
async def preview_withdraw(contract_address: str, assets: str) -> str:
    """Preview the amount of shares needed to withdraw assets.
    
    Args:
        contract_address (str): Address of the LogarithmVault contract
        assets (str): Amount of assets to withdraw (as string to preserve precision)
        
    Returns:
        str: The amount of shares needed
    """
    contract = get_contract(contract_address, LOGARITHM_VAULT_ABI_PATH)
    result = contract.functions.previewWithdraw(int(assets)).call()
    return str(result)

@mcp.tool()
async def get_total_assets(contract_address: str) -> str:
    """Get the total assets managed by the vault.

    Args:
        contract_address (str): Address of the LogarithmVault contract
        
    Returns:
        str: The total assets as a string (to preserve full precision)
    """
    contract = get_contract(contract_address, LOGARITHM_VAULT_ABI_PATH)
    result = contract.functions.totalAssets().call()
    return str(result)

@mcp.tool()
async def get_total_supply(contract_address: str) -> str:
    """Get the total supply of vault shares.

    Args:
        contract_address (str): Address of the LogarithmVault contract
        
    Returns:
        str: The total supply as a string (to preserve full precision)
    """
    contract = get_contract(contract_address, LOGARITHM_VAULT_ABI_PATH)
    result = contract.functions.totalSupply().call()
    return str(result)

@mcp.tool()
async def get_user_deposit_limit(contract_address: str) -> str:
    """Get the maximum deposit limit per user.

    Args:
        contract_address (str): Address of the LogarithmVault contract
        
    Returns:
        str: The user deposit limit as a string (to preserve full precision)
    """
    contract = get_contract(contract_address, LOGARITHM_VAULT_ABI_PATH)
    result = contract.functions.userDepositLimit().call()
    return str(result)

@mcp.tool()
async def get_vault_deposit_limit(contract_address: str) -> str:
    """Get the maximum total deposit limit for the vault.

    Args:
        contract_address (str): Address of the LogarithmVault contract
        
    Returns:
        str: The vault deposit limit as a string (to preserve full precision)
    """
    contract = get_contract(contract_address, LOGARITHM_VAULT_ABI_PATH)
    result = contract.functions.vaultDepositLimit().call()
    return str(result)

@mcp.tool()
async def get_available_contracts() -> List[str]:
    """Get the list of available Logarithm contract addresses.

    Returns:
        List[str]: List of available contract addresses
    """
    return AVAILABLE_CONTRACTS

if __name__ == "__main__":
    # Run the MCP server
    mcp.run(transport='stdio')
