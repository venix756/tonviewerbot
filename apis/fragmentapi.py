from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import httpx

class Fragment:
    def __init__(self, key):
        self.key = key
        self.client = httpx.AsyncClient()
        
        if key.startswith('@'):
            self.type = 'username'
            self.key = self.key.replace('@', '')
        elif key.startswith('+888'):
            self.type = 'number'
            self.key = self.key.replace('+', '')
        else:
            return None

    async def get_address(self):
        self.key = self.key
        self.user_agent = UserAgent()
        self.random_user_agent = self.user_agent.random
        self.headers = {'User-Agent': self.random_user_agent,'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8','Accept-Language': 'en-US,en;q=0.5','Accept-Encoding': 'gzip, deflate, br','Connection': 'keep-alive','Upgrade-Insecure-Requests': '1','Sec-Fetch-Dest': 'document','Sec-Fetch-Mode': 'navigate','Sec-Fetch-Site': 'none','Sec-Fetch-User': '?1','TE': 'trailers',}
        try:
            self.response = await self.client.get(f'https://fragment.com/{self.type}/{self.key}', headers=self.headers)
            soup = BeautifulSoup(self.response.text, 'html.parser')
            self.address = soup.find(class_="tm-wallet").text
            return self.address
        except Exception:
            return None
