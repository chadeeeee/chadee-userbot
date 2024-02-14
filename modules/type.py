import asyncio
import time

from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import Message

from utils.misc import modules_help, prefix


@Client.on_message(filters.command(["type", "typewriter"], prefix) & filters.me)
async def type_cmd(_, message: Message):
    text = message.text.split(maxsplit=1)[1]
    typed = ""
    typing_symbol = "▒"

    for char in text:
        await message.edit(typed + typing_symbol)
        await asyncio.sleep(0.1)
        typed += char
        await message.edit(typed)
        await asyncio.sleep(0.1)


modules_help["type"] = {
    "type</code> <code>| </code><code>typewriter [text]*": "Typing emulation. Don't use a lot of characters, you can receive a lot of floodwaits!"
}
