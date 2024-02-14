import asyncio
import requests

from pyrogram import Client, filters
from pyrogram.types import Message

from utils.misc import modules_help, prefix
from utils.scripts import format_exc, import_library

requests = import_library("requests")

APIURL = "https://api.waifu.pics"

ENDPOINTS = {
    "SFW": [
        ["waifu", "/sfw/waifu"],
        ["neko", "/sfw/neko"],
        ["shinobu", "/sfw/shinobu"],
        ["megumin", "/sfw/megumin"],
        ["bully", "/sfw/bully"],
        ["cuddle", "/sfw/cuddle"],
        ["cry", "/sfw/cry"],
        ["hug", "/sfw/hug"],
        ["awoo", "/sfw/awoo"],
        ["kiss", "/sfw/kiss"],
        ["lick", "/sfw/lick"],
        ["pat", "/sfw/pat"],
        ["smug", "/sfw/smug"],
        ["bonk", "/sfw/bonk"],
        ["yeet", "/sfw/yeet"],
        ["blush", "/sfw/blush"],
        ["smile", "/sfw/smile"],
        ["wave", "/sfw/wave"],
        ["highfive", "/sfw/highfive"],
        ["handhold", "/sfw/handhold"],
        ["nom", "/sfw/nom"],
        ["bite", "/sfw/bite"],
        ["glomp", "/sfw/glomp"],
        ["slap", "/sfw/slap"],
        ["kill", "/sfw/kill"],
        ["kick", "/sfw/kick"],
        ["happy", "/sfw/happy"],
        ["wink", "/sfw/wink"],
        ["poke", "/sfw/poke"],
        ["dance", "/sfw/dance"],
        ["cringe", "/sfw/cringe"]
    ],
    "NSFW": [
        ["waifu", "/nsfw/waifu"],
        ["neko", "/nsfw/neko"],
        ["trap", "/nsfw/trap"],
        ["blowjob", "/nsfw/blowjob"]
    ]
}

def fetch_image_url(url):
    try:
        response = requests.get(f"{APIURL}{url}")
        if response.status_code == 200:
            data = response.json()
            return data.get("url")  # Возвращает только URL изображения
        else:
            return {"error": "Failed to fetch image."}
    except Exception as e:
        return {"error": str(e)}

def get_item_url(category, item_name):
    for item in ENDPOINTS.get(category, []):
        if item[0] == item_name:
            return item[1]
    return None


@Client.on_message(filters.command("waifu", prefix) & filters.me)
async def waifu(client, message: Message):
    if len(message.command) < 3:
        await message.edit(
            "<b>waifu type isn't provided</b>\n\n"
            f"<b>Usage:</b> <b>{prefix}waifu [sfw/nsfw]* [query]* [pic/doc]*</b>\n"
            f"<b>Example:</b> <code>{prefix}waifu sfw waifu pic</code>\n"
            f"<b>You can get available waifu types with</b> <code>{prefix}waifu_types</code>"
        )
        return

    category = message.command[1]
    query = message.command[2]
    type = message.command[3] if len(message.command) > 3 else 'pic'

    if category not in ["sfw", "nsfw"]:
        await message.edit("Invalid category. Use 'sfw' or 'nsfw'.")
        return

    await message.edit("<b>Loading...</b>")
    try:
        category_name = "SFW" if category == "sfw" else "NSFW"
        item_url = get_item_url(category_name, query)
        if item_url:
            image_url = fetch_image_url(item_url)
            if type == "doc":
                await client.send_document(chat_id=message.chat.id, document=image_url)
            elif type == "pic":
                await client.send_photo(chat_id=message.chat.id, photo=image_url)
            else:
                await client.send_photo(chat_id=message.chat.id, photo=image_url)
            await message.delete()
        else:
            await message.edit(f"Waifu type '{query}' not found in category '{category}'.")
    except Exception as e:
        await message.edit(format_exc(e))


@Client.on_message(filters.command(["waifutypes", "waifu_types"], prefix) & filters.me)
async def waifu_types_func(client, message: Message):
    waifu_types = []
    for category, items in ENDPOINTS.items():
        if waifu_types:
            waifu_types.append("")  # Пустая строка между категориями
        waifu_types.append(f"{category.upper()} Categories:")
        for item in items:
            waifu_types.append(f"<code>{item[0]}</code>")

    response_text = "\n".join(waifu_types)
    await message.edit(response_text)

@Client.on_message(filters.command(["waifuspam", "waifu_spam"], prefix) & filters.me)
async def waifu_spam(client: Client, message: Message):
    if len(message.command) < 4:
        await message.edit(
            "<b>waifuspam type isn't provided</b>\n\n"
            f"<b>Usage:</b> <code>{prefix}waifuspam [sfw/nsfw]* [query]* [amount]* [pic/doc]*</code>\n"
            f"<b>Example:</b> <code>{prefix}waifuspam sfw waifu 5 pic</code> \n"
            f"<b>You can get available waifu types with</b> <code>{prefix}waifu_types</code>"
        )
        return

    category = message.command[1]
    query = message.command[2]
    amount = int(message.command[3])
    type = message.command[4] 

    if category not in ["sfw", "nsfw"]:
        await message.edit("Invalid category. Use 'sfw' or 'nsfw'.")
        return

    await message.delete()

    for _ in range(amount):
        category_name = "SFW" if category == "sfw" else "NSFW"
        item_url = get_item_url(category_name, query)
        if item_url:
            image_url = fetch_image_url(item_url)
            if type == "pic":
                await client.send_photo(chat_id=message.chat.id, photo=image_url)
            elif type == "doc":

                await client.send_document(chat_id=message.chat.id, document=image_url)

    await asyncio.sleep(1)


modules_help["waifu"] = {
    "waifu [category]* [query]* [type]* ": "Get waifu media",
    "waifu_types": "Available waifu types",
    "waifu_spam [category]* [query]* [type]* [amount]*": "Start spam with waifu media",
}
