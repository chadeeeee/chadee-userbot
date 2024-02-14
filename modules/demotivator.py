import random
from io import BytesIO

from pyrogram import Client, filters
from pyrogram.types import Message

from utils.misc import modules_help, prefix
from utils.scripts import import_library

requests = import_library("requests")
PIL = import_library("PIL", "pillow")

from PIL import Image, ImageDraw, ImageFont

@Client.on_message(filters.command(["dem"], prefix) & filters.me)
async def demotivator(client: Client, message: Message):
    await message.edit("<code>Process of demotivation...</code>")
    font = requests.get("https://github.com/deadboizxc/zxc-userbot-files/blob/master/Times%20New%20Roman.ttf?raw=true").content
    template_dem = requests.get("https://raw.githubusercontent.com/deadboizxc/zxc-userbot-files/master/demotivator.png").content

    if message.reply_to_message:
        words = ["random", "text", "typing", "fuck"]
        if message.reply_to_message.photo:
            downloads = await client.download_media(message.reply_to_message.photo.file_id)
            photo = Image.open(f"{downloads}")
            resize_photo = photo.resize((469, 312))
            text = (
                message.text.split(" ", maxsplit=1)[1]
                if len(message.text.split()) > 1
                else random.choice(words)
            )
            im = Image.open(BytesIO(template_dem))
            im.paste(resize_photo, (65, 48))
            text_font = ImageFont.truetype(BytesIO(font), 22)
            text_draw = ImageDraw.Draw(im)
            text_draw.multiline_text(
                (299, 412), text, font=text_font, fill=(255, 255, 255), anchor="ms"
            )
            with BytesIO() as bio:
                im.save(bio, "PNG")
                bio.seek(0)
                await message.reply_to_message.reply_photo(bio)
            await message.delete()
        elif message.reply_to_message.sticker:
            if not message.reply_to_message.sticker.is_animated:
                downloads = await client.download_media(message.reply_to_message.sticker.file_id)
                photo = Image.open(f"{downloads}")
                resize_photo = photo.resize((469, 312))
                text = (
                    message.text.split(" ", maxsplit=1)[1]
                    if len(message.text.split()) > 1
                    else random.choice(words)
                )
                im = Image.open(BytesIO(template_dem))
                im.paste(resize_photo, (65, 48))
                text_font = ImageFont.truetype(BytesIO(font), 22)
                text_draw = ImageDraw.Draw(im)
                text_draw.multiline_text(
                    (299, 412), text, font=text_font, fill=(255, 255, 255), anchor="ms"
                )
                with BytesIO() as bio:
                    im.save(bio, "PNG")
                    bio.seek(0)
                    await message.reply_to_message.reply_photo(bio)
                await message.delete()
            else:
                await message.edit("<b>Animated stickers are not supported</b>")
        else:
            await message.edit("<b>Need to reply to a photo/sticker</b>")
    else:
        await message.edit("<b>Need to reply to a photo/sticker</b>")


modules_help["demotivator"] = {
    "dem [text]*": "Reply to a picture to create a demotivator out of it"
}
