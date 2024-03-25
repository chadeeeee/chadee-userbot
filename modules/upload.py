import os
import requests

from pyrogram import Client, filters
from pyrogram.types import Message

from utils.misc import modules_help, prefix
from utils.scripts import format_exc


@Client.on_message(filters.command("upload", prefix) & filters.me)
async def upload_cmd(_, message: Message):
    max_size = 512 * 1024 * 1024
    max_size_mb = 512

    min_file_age = 31
    max_file_age = 180

    await message.edit("<b>Downloading...</b>")

    try:
        file_name = await message.download()
    except ValueError:
        try:
            file_name = await message.reply_to_message.download()
        except ValueError:
            await message.edit("<b>File to upload not found</b>")
            return

    if os.path.getsize(file_name) > max_size:
        await message.edit(f"<b>Files longer than {max_size_mb}MB aren't supported</b>")
        os.remove(file_name)
        return

    await message.edit("<b>Uploading...</b>")
    with open(file_name, "rb") as f:
        response = requests.post(
            "https://x0.at",
            files={"file": f},
        )

    if response.ok:
        url = response.text.split('value="', 1)[-1].split('"', 1)[0]
        file_size_mb = os.path.getsize(file_name) / 1024 / 1024
        file_age = int(
            min_file_age
            + (max_file_age - min_file_age) * ((1 - (file_size_mb / max_size_mb)) ** 2)
        )
        await message.edit(
            f"<b>Your URL: {url}\nYour file will live {file_age} days</b>",
            disable_web_page_preview=True,
        )
    else:
        await message.edit(f"<b>API returned an error!\n" f"{response.text}</b>")

    os.remove(file_name)


modules_help["url"] = {
    "upload [file|reply]*": "upload file to internet",
}
