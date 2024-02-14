import os
import asyncio

from pyrogram import Client, filters
from pyrogram.types import Message

from utils.misc import modules_help, prefix
from utils.zxc_path import _DOWNLOADS_

@Client.on_message(filters.command("send", prefixes=prefix) & filters.me)
async def send_file(client, message):
    await message.delete()

    command_parts = message.text.split(maxsplit=2)
    if len(command_parts) < 2:
        await message.edit("No file path provided.")
        return

    file_path = command_parts[1]
    file_path = file_path if os.path.isabs(file_path) else os.path.join(os.getcwd(), file_path)

    try:
        await client.send_document(chat_id=message.chat.id, document=file_path)
    except Exception as e:
        await message.edit(f"Error sending file: {str(e)}")


@Client.on_message(filters.command("down", prefixes=prefix) & filters.me)
async def download_file(client, message):
    if message.reply_to_message.document or message.reply_to_message.audio or message.reply_to_message.video or message.reply_to_message.photo:
        if len(message.command) > 1:
            path = message.command[1]
            path = os.path.expanduser(path)
        else:
            path = os.path.expanduser(_DOWNLOADS_)

        if not os.path.exists(path):
            os.makedirs(path)

        start_path = os.getcwd()
        os.chdir(path)

        try:
            if message.reply_to_message.document:
                file = message.reply_to_message.document
            elif message.reply_to_message.audio:
                file = message.reply_to_message.audio
            elif message.reply_to_message.video:
                file = message.reply_to_message.video
            elif message.reply_to_message.photo:
                file = message.reply_to_message.photo[-1]
            else:
                file = None

            if file:
                file_name = file.file_name if file.file_name else f"file_{file.file_id}"
                file_ext = file_name.split('.')[-1]
                await client.download_media(file, file_name=file_name)
                await message.reply_text(f"Файл сохранен в: `{path}`")
        except Exception as e:
            await message.reply_text(f"Произошла ошибка при скачивании файла: {str(e)}")
        finally:
            os.chdir(start_path)

modules_help["share"] = {
    "down [/path/for/file/]": "Download file",
    "send [/path/to/file/]": "Send document in chat",
}
