import asyncio
import urllib
from json import loads as json_parse

from pyrogram import Client, filters
from pyrogram.types import Message

from utils.misc import modules_help, prefix
from utils.scripts import format_exc, import_library

requests = import_library("requests")

APIURL = "https://nekos.life/api/v2"

ENDPOINTS = [
    ["tickle", "/img/tickle", "url"],
    ["slap", "/img/slap", "url"],
    ["pat", "/img/pat", "url"],
    ["neko", "/img/neko", "url"],
    ["meow", "/img/meow", "url"],
    ["kiss", "/img/kiss", "url"],
    ["hug", "/img/hug", "url"],
    ["fox_girl", "/img/fox_girl", "url"],
    ["feed", "/img/feed", "url"],
    ["cuddle", "/img/cuddle", "url"],
    ["why", "/why", "why"],
    ["cat", "/cat", "cat"],
    ["ngif", "/img/ngif", "url"],
    ["smug", "/img/smug", "url"],
    ["woof", "/img/woof", "url"],
    ["spoiler", "/spoiler?", "owo"],
    ["wallpaper", "/img/wallpaper", "url"],
    ["gecg", "/img/gecg", "url"],
    ["avatar", "/img/avatar", "url"],
    ["waifu", "/img/waifu", "url"],
    ["8ball", "/8ball", "url"],
]


def get_neko(neko_type=str, query_text=str):
    type_found = False
    neko_index = 0
    for t in ENDPOINTS:
        if neko_type == t[0]:
            type_found = True
            neko_index = ENDPOINTS.index(t)

    if not type_found:
        return f"Type \"{neko_type}\" not found."

    req_url = APIURL + eval(f"ENDPOINTS[{neko_index}][1]")

    if ENDPOINTS[neko_index][1].endswith("?"):
        if query_text:
            req_url = f"{req_url}text={urllib.parse.quote(query_text)}"

    req = requests.get(req_url).content.decode("ascii")
    resp = json_parse(req).get(eval(f"ENDPOINTS[{neko_index}][2]"))
    return resp


@Client.on_message(filters.command(["nekotypes", "neko_types"], prefix) & filters.me)
async def neko_types_func(client, message: Message):

    categories = [f"<code>{category[0]}</code>\n" for category in ENDPOINTS]
    response_text = "Categories:\n\n" + "".join(categories)
    await message.edit(response_text)


@Client.on_message(filters.command("neko", prefix) & filters.me)
async def neko(client, message: Message):
    if len(message.command) < 2:
        await message.edit(
            "<b>neko type isn't provided</b>\n"
            f"<b>You can get available neko types with</b> <code>{prefix}neko_types</code>"
        )
        return

    query = message.command[1]
    type = message.command[2] if len(message.command) > 2 else 'pic'

    await message.edit("<b>Loading...</b>")
    try:
        neko_data = get_neko(query)
        if neko_data:
            if type == 'doc':
                await client.send_document(chat_id=message.chat.id, document=neko_data)
            else:
                await client.send_photo(chat_id=message.chat.id, photo=neko_data)

            await message.delete()
        else:
            await message.edit("<b>Failed to fetch neko data.</b>")
    except Exception as e:
        await message.edit(format_exc(e))


@Client.on_message(filters.command(["nekospam", "neko_spam"], prefix) & filters.me)
async def neko_spam(client: Client, message: Message):
    if len(message.command) < 3:
        await message.edit(
            "<b>nekospam type isn't provided</b>\n\n"
            f"<b>Usage:</b> <code>{prefix}nekospam [query]* [amount]* [pic/doc]*</code>\n"
            f"<b>Example:</b> <code>{prefix}nekospam neko 5 pic</code> \n"
            f"<b>You can get available neko types with</b> <code>{prefix}neko_types</code>"
        )
        return

    query = message.command[1]
    amount = int(message.command[2])
    type = message.command[3] if len(message.command) > 3 else 'pic'

    for _ in range(amount):
        neko_data = get_neko(query)
        if neko_data:
            if type == 'doc':
                if message.reply_to_message:
                    await message.reply_to_message.reply(document=neko_data)
                else:
                    await client.send_document(chat_id=message.chat.id, document=neko_data)
            else:
                if message.reply_to_message:
                    await message.reply_to_message.reply(photo=neko_data)
                else:
                    await client.send_photo(chat_id=message.chat.id, photo=neko_data)
        else:
            await message.edit("<b>Failed to fetch neko data.</b>")

    await asyncio.sleep(1)


modules_help["neko"] = {
    "neko [type]*": "Get neko media",
    "neko_types": "Available neko types",
    "neko_spam [type]* [amount]*": "Start spam with neko media",
}
