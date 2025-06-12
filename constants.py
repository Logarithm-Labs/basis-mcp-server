import os

ALCHEMY_KEY = os.environ.get("ALCHEMY_KEY", None)
PRIVATE_KEY = os.environ.get("PRIVATE_KEY", None)
SUBGRAPH_API_KEY = os.environ.get("SUBGRAPH_API_KEY", None)

# Available Logarithm vault addresses
LOGARITHM_VAULT_ADDRESSES = {
    42161:[
        "0xe5fc579f20C2dbffd78a92ddD124871a35519659",
        "0x79f76E343807eA194789D114e61bE6676e6BBeDA",
    ]
}

MULTICALL_ADDRESSES = {
    42161: "0x842eC2c7D803033Edf55E478F461FC547Bc54EB2",
}

LOGARITHM_VAULT_ABI_PATH = "abis/LogarithmVault.abi.json"
MULTICALL_ABI_PATH = "abis/Multicall2.abi.json"

# Alchemy RPC URLs for each network
ALCHEMY_RPC_URLS = {
    42161: f"https://arb-mainnet.g.alchemy.com/v2/{ALCHEMY_KEY}" if ALCHEMY_KEY else "https://arb1.arbitrum.io/rpc",
    1: f"https://eth-mainnet.g.alchemy.com/v2/{ALCHEMY_KEY}" if ALCHEMY_KEY else "",
}

SUBGRAPH_QUERY_URL = "https://gateway.thegraph.com/api/subgraphs/id/AH842SqnNHmMM54fY6eX9sGSV4BPo8fmeoj5C3qbNsr1"
