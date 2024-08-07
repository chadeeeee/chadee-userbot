import os
import requests

from pyrogram import Client, filters
from pyrogram.types import Message

from utils.misc import modules_help, prefix
from utils.scripts import format_exc


@Client.on_message(filters.command("short", prefix) & filters.me)
async def short(_, message: Message):
    if len(message.command) > 1:
        link = message.text.split(maxsplit=1)[1]
    elif message.reply_to_message:
        link = message.reply_to_message.text
    else:
        await message.edit(f"<b>Usage: </b><code>{prefix}short [url to short]</code>")
        return

    try:
        # Using the TinyURL API to shorten the URL
        response = requests.post("http://tinyurl.com/api-create.php?url=" + link)
        response.raise_for_status()

        shortlink = response.text
        await message.edit(shortlink, disable_web_page_preview=True)
    except requests.exceptions.RequestException as ex:
        await message.edit(f"<b>Error: {ex}</b>")
        print(f"An unexpected error occurred: {ex}")



@Client.on_message(filters.command("urldl", prefix) & filters.me)
async def urldl(client: Client, message: Message):
    if len(message.command) > 1:
        link = message.text.split(maxsplit=1)[1]
    elif message.reply_to_message:
        link = message.reply_to_message.text
    else:
        await message.edit(
            f"<b>Usage: </b><code>{prefix}urldl [url to download]</code>"
        )
        return

    await message.edit("<b>Downloading...</b>")
    file_name = "downloads/" + link.split("/")[-1]

    try:
        resp = requests.get(link)
        resp.raise_for_status()

        with open(file_name, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)

        await message.edit("<b>Uploading...</b>")
        await client.send_document(message.chat.id, file_name)
        await message.delete()
    except Exception as e:
        await message.edit(format_exc(e))
    finally:
        os.remove(file_name)

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
        # Extract the URL from the HTML response
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
    "short [url]*": "short url",
    "urldl [url]*": "download url content",
    "upload [file|reply]*": "upload file to internet",
}
