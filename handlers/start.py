from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from middlewares.throttling import ThrottlingMiddleware

router = Router()
router.message.middleware(ThrottlingMiddleware())


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(f"Hello, {message.from_user.first_name}! This bot allows you to get information about TON addresses. To get information, use the /get command. For example, /get @username or /get +88812345678")
