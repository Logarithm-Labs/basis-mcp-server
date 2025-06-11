from requests import post
from constants import SUBGRAPH_QUERY_URL
from typing import List, Optional, Dict, Any

daily_share_price_query = """
query DailyPriceHistory($vault_addresses: [Bytes!], $length: Int!) {
  vaultStats_collection(
    interval: day
    orderBy: timestamp
    orderDirection: desc
    first: $length
    where: {
        vault_: {
            address_in: $vault_addresses
        }
    }
  ) {
    timestamp
    pricePerShare
    vault {
      address
      name
    }
  }
}
"""

def format_vault_addresses(addresses: List[str]) -> List[str]:
    """Format vault addresses to lowercase for GraphQL compatibility"""
    return [addr.lower() for addr in addresses]

def send_graphql_query_to_subgraph(api_key: str, query: str, variables: Optional[Dict[str, Any]] = None):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    # Prepare the request payload
    payload = {'query': query}
    if variables:
        payload['variables'] = variables
    
    print(f"Sending GraphQL query with payload: {payload}")  # Debug print
    
    # Send the GraphQL request to the Subgraph
    response = post(SUBGRAPH_QUERY_URL, headers=headers, json=payload)

    # Check if the request was successful
    if response.status_code == 200:
        result = response.json()
        if 'errors' in result:
            raise Exception(f"GraphQL errors: {result['errors']}")
    else:
        raise Exception(f"HTTP Error {response.status_code}: {response.text}")
    
    return result

def get_share_price_history_from_subgraph(vault_addresses: List[str], length: int, api_key: str) -> dict:
    formatted_addresses = format_vault_addresses(vault_addresses)
    
    variables = {
        "vault_addresses": formatted_addresses,
        "length": length
    }
    
    res = send_graphql_query_to_subgraph(api_key, daily_share_price_query, variables)
    return process_response(res)

def process_response(res: dict) -> dict:
    if not res or 'data' not in res or not res['data']['vaultStats_collection']:
        return "No data found for the specified vaults"
    
     # Process the response to group by vault
    vault_data = {}
    
    for entry in res['data']['vaultStats_collection']:
        vault_address = entry['vault']['address']
        vault_name = entry['vault']['name']
        timestamp = int(entry['timestamp']) // 1000000  # Convert microseconds to seconds
        price_per_share = float(entry['pricePerShare'])
        
        if vault_address not in vault_data:
            vault_data[vault_address] = {
                'name': vault_name,
                'price_history': []
            }
        
        vault_data[vault_address]['price_history'].append((timestamp, price_per_share))
    
    # Sort price history by timestamp (newest first)
    for vault_address in vault_data:
        vault_data[vault_address]['price_history'].sort(key=lambda x: x[0], reverse=True)

    return vault_data
        
