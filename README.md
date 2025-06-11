# Logarithm Vault MCP Server

This MCP (Model Context Protocol) server provides tools to interact with Logarithm Vaults on the Arbitrum One blockchain. It offers comprehensive vault information retrieval and share price history analysis capabilities.

## Features

- **Vault Information**: Get detailed information about all Logarithm vaults including total supply, assets, share prices, and cost rates
- **Share Price History**: Retrieve historical daily share price data for multiple vaults
- **Multi-Vault Support**: Query multiple vault addresses simultaneously
- **Depositor-Specific Data**: Get personalized vault information for specific depositor addresses

## Setup

### Prerequisites

- Python 3.10 or higher
- `uv` package manager
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

### Installation

1. Clone this repository
2. Install dependencies:

```bash
uv sync --locked
```

3. Configure environment variables:

Create a `.env` file in the project root:

```bash
# Optional - Your Alchemy API key for Arbitrum One
ALCHEMY_KEY=your_alchemy_key_here

# Required - Your subgraph API key for price history queries
SUBGRAPH_API_KEY=your_subgraph_api_key_here
```

### Environment Variable Setup

#### Windows PowerShell:
```powershell
$env:ALCHEMY_KEY="your_alchemy_key_here"
$env:SUBGRAPH_API_KEY="your_subgraph_api_key_here"
```

#### Windows Command Prompt:
```cmd
set ALCHEMY_KEY=your_alchemy_key_here
set SUBGRAPH_API_KEY=your_subgraph_api_key_here
```

#### Linux/macOS:
```bash
export ALCHEMY_KEY="your_alchemy_key_here"
export SUBGRAPH_API_KEY="your_subgraph_api_key_here"
```

### Running the server

```bash
uv run logarithm_vault.py
```

## Using with Claude Desktop

1. Install Claude Desktop from [claude.ai/download](https://claude.ai/download)
2. Configure Claude Desktop to use this MCP server:

Open your Claude Desktop configuration file:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%AppData%\Claude\claude_desktop_config.json`

Add the following to the configuration:

### macOS:
```json
{
    "mcpServers": {
        "logarithm-vault": {
            "command": "uv",
            "args": [
                "--directory",
                "/ABSOLUTE/PATH/TO/logarithm-mcp-server"
                "run",
                "logarithm_vault.py"
            ],
            "env": {
                "ALCHEMY_KEY": "your_alchemy_key_here",
                "SUBGRAPH_API_KEY": "your_subgraph_api_key_here"
            }
        }
    }
}
```

### Windows:
```json
{
    "mcpServers": {
        "logarithm-vault": {
            "command": "python",
            "args": [
                "--directory",
                "C:\\ABSOLUTE\\PATH\\TO\\logarithm-mcp-server"
                "run",
                "logarithm_vault.py"
            ],
            "env": {
                "ALCHEMY_KEY": "your_alchemy_key_here",
                "SUBGRAPH_API_KEY": "your_subgraph_api_key_here"
            }
        }
    }
}
```

3. Restart Claude Desktop

## Available Tools

### 1. `get_all_logarithm_vault_info(depositor=None)`

Retrieves comprehensive information about all available Logarithm vaults.

**Parameters:**
- `depositor` (optional): Ethereum address to get depositor-specific information

**Returns:**
- Vault address and name
- Symbol and total supply
- Total assets and current share price
- Entry and exit cost rates
- Idle assets and pending withdrawals
- Depositor-specific: max deposit and share balance (if depositor provided)

**Example Usage:**
```
# Get general vault information
get_all_logarithm_vault_info()

# Get vault information with depositor-specific data
get_all_logarithm_vault_info("0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6")
```

### 2. `get_share_price_history(vault_addresses, length=14)`

Retrieves historical daily share price data for specified vaults.

**Parameters:**
- `vault_addresses`: List of vault addresses to query
- `length` (optional): Number of days of history to retrieve (default: 14, max: 365)

**Returns:**
- Formatted price history with timestamps
- Vault names and addresses
- Price data sorted by timestamp (newest first)

**Example Usage:**
```
# Get 14 days of price history for multiple vaults
get_share_price_history([
    "0xe5fc579f20C2dbffd78a92ddD124871a35519659",
    "0x79f76E343807eA194789D114e61bE6676e6BBeDA"
])

# Get 30 days of price history
get_share_price_history([
    "0xe5fc579f20C2dbffd78a92ddD124871a35519659"
], 30)
```

## Example Queries with Claude Desktop

You can ask Claude Desktop:

1. **"Show me information about all Logarithm vaults"**
   - Returns comprehensive vault data including share prices and cost rates

2. **"Get vault information for depositor address 0x123...abc"**
   - Returns vault info plus depositor-specific data like balances and max deposits

3. **"Show me the share price history for vault 0xe5fc579f20C2dbffd78a92ddD124871a35519659 over the last 30 days"**
   - Returns detailed price history with timestamps

4. **"Compare share price performance of multiple vaults over the last week"**
   - Returns comparative price data for analysis

5. **"What's the current share price and total assets of all vaults?"**
   - Returns current vault metrics

## Supported Networks

- **Arbitrum One** (Chain ID: 42161)

## Notes

- All vault addresses are automatically validated and formatted
- Share prices are calculated as `total_assets / total_supply`
- Price history data comes from The Graph subgraph
- All numeric values maintain precision using decimal arithmetic
- The server supports querying multiple vaults simultaneously for efficiency

## Troubleshooting

### Common Issues

1. **"SUBGRAPH_API_KEY environment variable is not set"**
   - Ensure your `.env` file contains the API key or set it as an environment variable

2. **"Invalid vault address format"**
   - Vault addresses must be valid Ethereum addresses (42 characters starting with 0x)

3. **"No price history data found"**
   - The vault may be new or the subgraph may not have data for the requested time period

4. **Network connection errors**
   - Check your internet connection and API key validity
