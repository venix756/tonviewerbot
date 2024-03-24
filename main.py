from dotenv import load_dotenv
from handlers.message import router

import asyncio
import os
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.utils.markdown import hbold
from aiogram.client.default import DefaultBotProperties

load_dotenv()
dp = Dispatcher()

async def main():
    bot = Bot(os.getenv('BOTAPI_TOKEN'), default=DefaultBotProperties(parse_mode='html'))
    dp.include_routers(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
