import os
import re

from apis.fragmentapi import Fragment
from apis.tonviewerapi import TonViewer
from utils import join_with_limit

from aiogram import Router
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message

import datetime

username_regex = r'^@[\w\d_]+$'
number_regex = r'^\+888\d{8,}$'
address_regex = r'^(EQ|UQ).{46}$'
ton_domain_regex = r'^[a-zA-Z0-9-]+\.(ton)$'
telegram_domain_regex = r'^[a-zA-Z0-9_.-]+\.t\.me$'

router = Router()

tonviewer = TonViewer(os.getenv('TONAPI_TOKEN'))

@router.message(CommandStart())
async def start(message: Message):
    await message.answer(f"Hello, {message.from_user.first_name}! This bot allows you to get information about TON addresses. To get information, use the /get command. For example, /get @username or /get +88812345678")


@router.message(Command("get"))
async def get(message: Message, command: CommandObject):
    args = command.args.replace(" ", "")
    
    try:
        if re.match(username_regex, args) or re.match(number_regex, args):
            address = await Fragment(args).get_address()
        elif re.match(address_regex, args) or re.match(ton_domain_regex, args) or re.match(telegram_domain_regex, args):
            address = args
        else:
            return await message.answer("Unknown format")
        
        info = await tonviewer.get_info(address)
        time = datetime.datetime.fromtimestamp(info['last_activity'], tz=datetime.timezone.utc)
        usernames = await tonviewer.get_collectibles(address, os.getenv('USERNAMES_COLLECTION_ADDRESS'))
        numbers = await tonviewer.get_collectibles(address, os.getenv('NUMBERS_COLLECTION_ADDRESS'))
        domains = await tonviewer.get_collectibles(address, os.getenv('DOMAINS_COLLECTION_ADDRESS'))

        answer = f"<b>Address</b>: {info['address']}\n" \
                 f"<b>Balance</b>: {info['balance']/10**9} TON\n" \
                 f"<b>Last Activity</b>: {time.strftime('%Y-%m-%d %H:%M:%S')} (UTC+0)\n" \
                 f"<b>Interfaces</b>: {', '.join(info['interfaces'])}, {info['status']}\n\n" \

        if usernames:
            answer += f"<b>Usernames Collection:</b> {join_with_limit(usernames)}\n\n"

        if numbers:
            answer += f"<b>Numbers Collection:</b> {join_with_limit(numbers)}\n\n"
        
        if domains:
            answer += f"<b>Domains Collection:</b> {join_with_limit(domains)}"

        return await message.answer(answer)
    except ValueError:
        return await message.answer("Not found")
    except Exception:
        return await message.answer("An error occurred while processing the request.")
