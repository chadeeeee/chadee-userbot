from pyrogram import Client, filters
from pyrogram.types import Message
from utils.misc import modules_help, prefix
from utils.scripts import interact_with, interact_with_to_delete, format_exc

import time

class SDHandler:
    def __init__(self):
        self.prompt = ""
        self.chat_id = ""

sd_handler = SDHandler()

@Client.on_message(filters.command("sd", prefix) & filters.me)
async def sd(client: Client, message: Message):
    sd_handler.chat_id = message.chat.id
    if len(message.command) > 1:
        sd_handler.prompt = message.text.split(maxsplit=1)[1]
    elif message.reply_to_message:
        sd_handler.prompt = message.reply_to_message.text
    else:
        await message.edit("<b>Prompt isn't provided</b>")
        return
    try:
        await message.edit("<b>Generating...</b>")
        await client.unblock_user("@UDream_ai_bot")
        await client.send_message("@UDream_ai_bot", f"!gen {sd_handler.prompt}")
    except Exception as e:
        await message.edit(format_exc(e))
    else:
        await client.delete_messages("@UDream_ai_bot", interact_with_to_delete)
        interact_with_to_delete.clear()
        await message.delete()


@Client.on_message(filters.photo & filters.user(6988546996))
async def handle_photo(client: Client, message: Message):
    if message.caption and sd_handler.prompt in message.caption:
        await client.send_photo(chat_id=sd_handler.chat_id, photo=message.photo.file_id, caption=f"Prompt: <b>{sd_handler.prompt}</b>")


modules_help["sd"] = {
    "sd [link|reply]*": "generate a photo by stable diffusion",
}
