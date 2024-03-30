from dotenv import load_dotenv
from handlers import start, get

import asyncio
import os
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

load_dotenv()
dp = Dispatcher()


async def main():
    bot = Bot(os.getenv('BOTAPI_TOKEN'),
              default=DefaultBotProperties(parse_mode='html'))
    lock = asyncio.Lock()
    dp["lock"] = lock
    dp.include_routers(start.router, get.router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
