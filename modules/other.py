import datetime
import asyncio
import os

from pyrogram import Client, filters
from pyrogram.types import Message

from utils.misc import modules_help, prefix


@Client.on_message(filters.command('time', prefixes=prefix) & filters.me)
async def info(client, message):
    data = datetime.datetime.now().strftime("%Y-%m-%d"+" "+"%H:%M:%S")
    await message.edit_text(data)


modules_help["other"] = {
    "time": "send time",
}
