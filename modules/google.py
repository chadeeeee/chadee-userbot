from pyrogram import Client, filters
from pyrogram.types import Message

from utils.misc import modules_help, prefix
from utils.scripts import interact_with, interact_with_to_delete, format_exc

import urllib.parse
import webbrowser


@Client.on_message(filters.command("google", prefix) & filters.me)
async def googleit(_, message: Message):
    if message.reply_to_message:
        to_search = message.reply_to_message.text
    else:
        to_search = message.text.split(" ", 1)[1] if len(message.text.split(" ", 1)) > 1 else ""

    if not to_search:
        await message.edit("<b>Enter the text to search for or replay the message</b>")
        return

    url = f"https://www.google.com/search?q={urllib.parse.quote(to_search)}"
    await message.edit(f"<b>🌐 Click on [it]({url})</b>")


modules_help["google"] = {
    "google [text|reply]*": "create a google search link",
}