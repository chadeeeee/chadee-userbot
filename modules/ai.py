import asyncio

from pyrogram import Client, filters
from pyrogram.types import Message

from utils.misc import modules_help, prefix

import google.generativeai as genai
genai.configure(api_key="AIzaSyDnI9TthL2226JKrOkRU0hRAsH5367c7yM")


@Client.on_message(filters.command(["ai", "gemini",], prefix) & filters.me)
async def antispam(_, message: Message):
    response = model.generate_content(message.text)
    res = response.text.upper()
    await message.edit_text(res)



modules_help["antispam"] = {
    "ai [question]": "ask AI something",
}