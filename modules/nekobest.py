import requests

from pyrogram import Client, filters
from pyrogram.types import Message

from utils.misc import modules_help, prefix
from utils.scripts import format_exc, import_library

API_URL = "https://nekos.best/api/v2"

ENDPOINTS = [
    "neko", "waifu", "husbando", "kitsune", "lurk",
    "shoot", "sleep", "shrug", "stare", "wave",
    "poke", "smile", "peck", "wink", "blush",
    "smug", "tickle", "yeet", "think", "highfive",
    "feed", "bite", "bored",
]


def get_nekobest(endpoint):
    response = requests.get(f"{API_URL}/{endpoint}")
    data = response.json().get('results', [])
    url = data[0].get('url', None)
    return url


@Client.on_message(filters.command(["nekobesttypes", "nekobest_types"], prefix) & filters.me)
async def nekobest_types_func(client: Client, message: Message):
    categories = [f"<code>{category}</code>\n" for category in ENDPOINTS]
    response_text = "Categories:\n\n" + "".join(categories)
    await message.edit(response_text)


@Client.on_message(filters.command("nekobest", prefix) & filters.me)
async def nekobest(client: Client, message: Message):
    if len(message.command) < 2:
        await message.edit(
            "<b>nekobest type isn't provided</b>\n"
            f"<b>You can get available neko types with</b> <code>{prefix}nekobesttypes</code>"
        )
        return

    query = message.command[1]
    type = message.command[2] if len(message.command) > 2 else 'pic'

    await message.edit("<b>Loading...</b>")
    try:
        nekobest_data = get_nekobest(query)
        if nekobest_data:
            if type == 'doc':
                await client.send_document(chat_id=message.chat.id, document=nekobest_data)
            elif type == "pic":
                await client.send_photo(chat_id=message.chat.id, photo=nekobest_data)
            else:
                await client.send_photo(chat_id=message.chat.id, photo=nekobest_data)

            await message.delete()
        else:
            await message.edit("<b>Failed to fetch nekobest data.</b>")
    except Exception as e:
        await message.edit(format_exc(e))


@Client.on_message(filters.command(["nekobestspam", "nekobest_spam"], prefix) & filters.me)
async def nekobest_spam(client: Client, message: Message):
    if len(message.command) < 3:
        await message.edit(
            "<b>nekobestspam type isn't provided</b>\n\n"
            f"<b>Usage:</b> <code>{prefix}nekobest_spam [query]* [amount]* [pic/doc]*</code>\n"
            f"<b>Example:</b> <code>{prefix}nekobest_spam neko 5 pic</code> \n"
            f"<b>You can get available nekobest types with</b> <code>{prefix}nekobesttypes</code>"
        )
        return

    query = message.command[1]
    amount = int(message.command[2])
    type = message.command[3] if len(message.command) > 3 else 'pic'

    for _ in range(amount):
        nekobest_data = get_nekobest(query)
        if nekobest_data:
            if type == 'doc':
                await client.send_document(chat_id=message.chat.id, document=nekobest_data)
            elif type == "pic":
                await client.send_photo(chat_id=message.chat.id, photo=nekobest_data)
            else:
                await client.send_photo(chat_id=message.chat.id, photo=nekobest_data)
        else:
            await message.edit("<b>Failed to fetch nekobest data.</b>")

    await asyncio.sleep(1)


modules_help["nekobest"] = {
    "nekobest [type]*": "Get neko media",
    "nekobesttypes": "Available neko types",
    "nekobest_spam [type]* [amount]*": "Start spam with neko media",
}
