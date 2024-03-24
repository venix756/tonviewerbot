import httpx

class TonViewer:
    def __init__(self, tonapi_api_key: str = None):
        self.tonapi_api_key = {'accept': 'application/json', 'Authorization': f'Bearer {tonapi_api_key}'}
        self.client = httpx.AsyncClient()
    
    async def get_info(self, address):
        self.address = address
        data = (await self.client.get(f"https://tonapi.io/v2/accounts/{self.address}", headers=self.tonapi_api_key)).json()
        return [address, data]
    
    async def get_collectibles(self, address, collection):
        self.address = address
        self.collection_address = collection
        data = (await self.client.get(f"https://tonapi.io/v2/accounts/{self.address}/nfts?"
                f"&collection={self.collection_address}"
                f"&limit=1000&offset=0", headers=self.tonapi_api_key)).json()
        names = [item['metadata']['name'] for item in data['nft_items']]
        return names
