import asyncio

from pyrogram import Client, filters
from pyrogram.types import Message

from utils.misc import modules_help, prefix


@Client.on_message(filters.command(["antispam", "as",], prefix) & filters.me)
async def antispam(_, message: Message):
    status = ""
    if status == "enable":
        status = True
    if status == "disable":
        status = False
    while status:
        await message.delete(message.chat.id)



modules_help["antispam"] = {
    "antispam enable": "turns on antispam",
    "antispam disable": "turns off antispam"
}