import os
import re

from apis.fragmentapi import Fragment
from apis.tonviewerapi import TonViewer

from aiogram import Router
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message

import datetime

router = Router()

tonviewer = TonViewer(os.getenv('TONAPI_TOKEN'))

@router.message(CommandStart())
async def start(message: Message):
    await message.answer(f"Hello, {message.from_user.first_name}! This bot allows you to get information about TON addresses. To get information, use the /get command. For example, /get @username or /get +88812345678")

@router.message(Command("get"))
async def get(message: Message, command: CommandObject):

    args = command.args.replace(" ", "")

    username_regex = r'^@[\w\d_]+$'
    number_regex = r'^\+888\d{8,}$'
    address_regex = r'^(EQ|UQ).{46}$'
    domain_regex = r'^[a-zA-Z0-9-]+\.(ton)$'

    if re.match(username_regex, args) or re.match(number_regex, args):
        address = await Fragment(args).get_address()
    
    elif re.match(address_regex, args) or re.match(domain_regex, args):
        address = args
    
    else:
        return await message.answer("Unknown format")
    
    if address is None:
        return await message.answer("Not found")

    try:
        info = await tonviewer.get_info(address)
        time = datetime.datetime.fromtimestamp((info[1]['last_activity']), tz=datetime.timezone.utc)
        
        usernames = await tonviewer.get_collectibles(address, os.getenv('USERNAMES_COLLECTION_ADDRESS'))
        numbers = await tonviewer.get_collectibles(address, os.getenv('NUMBERS_COLLECTION_ADDRESS'))

        answer = f"<b>Address</b>: {info[0]}\n" \
                 f"<b>Balance</b>: {info[1]['balance']/10**9} TON\n" \
                 f"<b>Last Activity</b>: {time.strftime('%Y-%m-%d %H:%M:%S')} (UTC+0)\n" \
                 f"<b>Interfaces</b>: {', '.join(info[1]['interfaces'])}, {info[1]['status']}\n\n" \

        if usernames:
            usernames_info = ', '.join(usernames)
            answer += f"<b>Usernames Collection:</b> {usernames_info}\n\n"

        if numbers:
            numbers_info = ', '.join(numbers)
            answer += f"<b>Numbers Collection:</b> {numbers_info}"

        return await message.answer(answer)

    except Exception:
        return await message.answer(f"An error occurred while processing the request.")
