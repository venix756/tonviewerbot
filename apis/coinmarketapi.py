import httpx

import httpx


class CoinMarketCapAPI:
    def __init__(self):
        self.url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
        self.parameters = {
            'symbol': 'TON',
            'convert': 'USD',
        }
        self.headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': 'COIN_TOKEN',
        }
        self.client = httpx.AsyncClient()

    async def get_ton_price(self):
        response = await self.client.get(self.url, headers=self.headers, params=self.parameters)
        data = response.json()
        ton_price = data["data"]["TON"]["quote"]["USD"]["price"]
        return ton_price


