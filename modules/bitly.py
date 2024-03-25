import requests

from pyrogram import Client, filters
from pyrogram.types import Message

from utils.misc import modules_help, prefix
from utils.scripts import format_exc
from utils.config import ACCESS_TOKEN


def shorten_url(link):
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    json_data = {"long_url": link}
    response = requests.post("https://api-ssl.bitly.com/v4/shorten", json=json_data, headers=headers)
    if response.status_code == 200:
        return response.json().get("link")
    else:
        return "Error when shortening link"


@Client.on_message(filters.command(["bitly", "link"], prefix) & filters.me)
async def bitlyshorter(client: Client, message: Message):
    if len(message.command) > 1:
        link = message.command[1]
    elif message.reply_to_message:
        link = message.reply_to_message.text
    else:
        await message.edit("<b>Link isn't provided</b>")
        return

    try:
        await message.edit(f"<b>🔗 New link:</b> {shorten_url(link)}", disable_web_page_preview=True)
    except Exception as e:
        await message.edit(format_exc(e))


modules_help["bitly"] = {
    "bitly [link|reply]*": "create a short link by bit.ly",
}
