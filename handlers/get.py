import os
import re

from apis.fragmentapi import Fragment
from apis.tonviewerapi import TonViewer
from middlewares.throttling import ThrottlingMiddleware
from utils import join_with_limit

from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

import datetime
import logging
import asyncio

username_regex = r'^@[\w\d_]+$'
number_regex = r'^\+888\d{8,}$'
address_regex = r'^(EQ|UQ).{46}$'
ton_domain_regex = r'^[a-zA-Z0-9-]+\.(ton)$'
telegram_domain_regex = r'^[a-zA-Z0-9_.-]+\.t\.me$'

router = Router()
router.message.middleware(ThrottlingMiddleware())

tonviewer = TonViewer(os.getenv('TONAPI_TOKEN'))


@router.message(Command("get"))
async def get(message: Message, command: CommandObject, lock: asyncio.Lock):
    args = command.args.replace(" ", "")
    msg = await message.answer("<b>Loading...</b>")
    
    try:
        if re.match(username_regex, args) or re.match(number_regex, args):
            address = await Fragment(args).get_address()
        elif re.match(address_regex, args) or re.match(ton_domain_regex, args) or re.match(telegram_domain_regex, args):
            address = args
        else:
            return await msg.edit_text("Unknown format")

        # tonapi is limited to 1 request per second :( (I'm using a free plan)
        async with lock:
            info = await tonviewer.get_info(address)
            await asyncio.sleep(1)
            usernames = await tonviewer.get_collectibles(address, os.getenv('USERNAMES_COLLECTION_ADDRESS'))
            await asyncio.sleep(1)
            numbers = await tonviewer.get_collectibles(address, os.getenv('NUMBERS_COLLECTION_ADDRESS'))
            await asyncio.sleep(1)
            domains = await tonviewer.get_collectibles(address, os.getenv('DOMAINS_COLLECTION_ADDRESS'))
            await asyncio.sleep(1)

        time = datetime.datetime.fromtimestamp(info['last_activity'], tz=datetime.timezone.utc)

        answer = f"<b>Address</b>: <a href='https://tonviewer.com/{info['address']}/'>{info['address']}</a>\n" \
                 f"<b>Balance</b>: {info['balance']/10**9} TON\n" \
                 f"<b>Last Activity</b>: {time.strftime('%Y-%m-%d %H:%M:%S')} (UTC+0)\n" \
                 f"<b>Interfaces</b>: {', '.join(info['interfaces'])}, {info['status']}\n\n" \

        if usernames:
            answer += f"<b>Usernames Collection:</b> {join_with_limit(usernames)}\n\n"

        if numbers:
            answer += f"<b>Numbers Collection:</b> {join_with_limit(numbers)}\n\n"
        
        if domains:
            answer += f"<b>Domains Collection:</b> {join_with_limit(domains)}"

        return await msg.edit_text(answer, disable_web_page_preview=True)
    except ValueError:
        return await msg.edit_text("Not found")
    except Exception as e:
        logging.exception(e)
        return await msg.edit_text("An error occurred while processing the request.")
