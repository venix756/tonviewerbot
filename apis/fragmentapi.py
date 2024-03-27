from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import httpx


class Fragment:
    def __init__(self, key):
        self.key = key
        self.user_agent = UserAgent()
        self.client = httpx.AsyncClient()

        if key.startswith('@'):
            self.type = 'username'
            self.key = self.key.replace('@', '')
        elif key.startswith('+888'):
            self.type = 'number'
            self.key = self.key.replace('+', '')

    async def get_address(self):
        headers = {'User-Agent': self.user_agent.random, 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8', 'Accept-Language': 'en-US,en;q=0.5', 'Accept-Encoding': 'gzip, deflate, br',
                  'Connection': 'keep-alive', 'Upgrade-Insecure-Requests': '1', 'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'none', 'Sec-Fetch-User': '?1', 'TE': 'trailers', }
        try:
            response = await self.client.get(f'https://fragment.com/{self.type}/{self.key}', headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup.find(class_="tm-wallet").text
        except Exception:
            raise ValueError("Not found")
