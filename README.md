# MetaVault MCP Server

This MCP (Model Context Protocol) server provides tools to interact with the MetaVault smart contract on Arbitrum One blockchain.

## Features

- View allocated assets and vaults
- Get claimable assets information
- Get share pice info
- Prepare transactions for allocating, redeeming, and withdrawing assets
- All smart contract functions related to a curator exposed as tools

## Setup

### Prerequisites

- Python 3.10 or higher
- uv or another Python package manager

### Installation

1. Clone this repository
2. Install dependencies:

```bash
uv add "mcp[cli]" web3
```

3. Configure environment variables:

```bash
# Required
export CONTRACT_ADDRESS="0xYourMetaVaultContractAddress"

# Optional - defaults to public Arbitrum One RPC
export ARBITRUM_RPC_URL="https://your-arbitrum-rpc-url"
```

### Running the server

```bash
uv run metavault.py
```

## Using with Claude Desktop

1. Install Claude Desktop from [claude.ai/download](https://claude.ai/download)
2. Configure Claude Desktop to use this MCP server:

Open your Claude Desktop configuration file:
- MacOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%AppData%\Claude\claude_desktop_config.json`

Add the following to the configuration:
- MacOS:
```json
{
    "mcpServers": {
        "metavault": {
            "command": "uv",
            "args": [
                "--directory",
                "/ABSOLUTE/PATH/TO/PARENT/FOLDER/logarithm-mcp-server",
                "run",
                "metavault.py"
            ]
        }
    }
}
```
- Windows:
```json
{
    "mcpServers": {
        "metavault": {
            "command": "uv",
            "args": [
                "--directory",
                "C:\\ABSOLUTE\\PATH\\TO\\PARENT\\FOLDER\\logarithm-mcp-server",
                "run",
                "metavault.py"
            ]
        }
    }
}
```

3. Restart Claude Desktop

## Available Tools

### Read-only Functions

- `get_allocated_assets()` - Get total allocated assets
- `get_allocated_vaults()` - Get list of vaults with allocations
- `get_allocation_claimable_assets()` - Get requested and claimable assets
- `get_allocation_withdraw_keys(vault_address)` - Get withdraw keys for a vault
- `get_claimable_vaults()` - Get vaults with claimable assets
- `get_idle_assets()` - Get total idle assets
- `get_share_price()` - Get the share price

### Transaction Preparation Functions

- `prepare_allocate_transaction(from_address, targets, assets)` - Prepare allocation transaction
- `prepare_redeem_allocations_transaction(from_address, targets, shares)` - Prepare redemption transaction
- `prepare_withdraw_allocations_transaction(from_address, targets, assets)` - Prepare withdrawal transaction

## Example Usage

With Claude Desktop, you can ask:

1. "What are the current idle assets in the vault?"
2. "Show me the list of allocated vaults"
3. "Prepare a transaction to allocate 1000000000000000000 assets to 0x123...abc"
4. "Get the withdraw keys for vault 0x456...def"

## Notes

- Transaction preparation functions return JSON that needs to be signed by your wallet
- All numeric values are handled as strings to preserve precision
- Address validation is performed for all inputs
