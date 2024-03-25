import asyncio
import requests

from pyrogram import Client, filters
from pyrogram.types import Message

from utils.misc import modules_help, prefix
from utils.scripts import format_exc
from utils.config import DEV_KEY, NAME, PASS


@Client.on_message(filters.command("paste", prefix) & filters.me)
async def paste(_, message: Message):
    _, code, name, code_format = message.text.split(maxsplit=3)
    data = {
        'api_dev_key': DEV_KEY,
        'api_user_name': NAME,
        'api_user_password': PASS,
        'api_option': 'paste',
        'api_paste_code': code,
        'api_paste_name': name,
        'api_paste_format': code_format
    }
    response = requests.post('https://pastebin.com/api/api_post.php', data=data)
    try:
        await message.edit(f"<b>Creating...</b>")
        await message.edit(f"<b>Link</b>: {response.text}")
    except Exception as e:
        await message.edit(format_exc(e))


modules_help["pastebin"] = {
    "paste [code] [name] [format]": "Paste text to the Pastebin",
}
