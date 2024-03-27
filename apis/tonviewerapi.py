import httpx
from utils import convert_address


class TonViewer:
    def __init__(self, tonapi_api_key: str = None):
        self.client = httpx.AsyncClient(headers={'accept': 'application/json', 'Authorization': f'Bearer {tonapi_api_key}'})
    
    async def get_info(self, address):
        data = (await self.client.get(f"https://tonapi.io/v2/accounts/{address}")).json()
        data['address'] = convert_address(data['address'])
        return data
    
    async def get_collectibles(self, address, collection):
        data = (await self.client.get(f"https://tonapi.io/v2/accounts/{address}/nfts?"
                f"&collection={collection}"
                f"&limit=1000&offset=0")).json()
        return [item['metadata']['name']
                for item in data['nft_items']]

