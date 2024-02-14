import io
from textwrap import wrap

from pyrogram import Client, filters
from pyrogram.types import Message
from utils.misc import modules_help, prefix
from utils.scripts import import_library

PIL = import_library("PIL", "pillow")
requests = import_library("requests")

from PIL import Image, ImageFont, ImageDraw
import requests


@Client.on_message(filters.command(["j", "jac"], prefix) & filters.me)
async def jac(client: Client, message: Message):
    if message.command[1:]:
        text = " ".join(message.command[1:])
    elif message.reply_to_message:
        text = message.reply_to_message.text
    else:
        text = " "
    await message.delete()

    # Получение фото из ссылки
    photo_url = "https://raw.githubusercontent.com/deadboizxc/zxc-userbot-files/master/jac.jpg"
    photo_response = requests.get(photo_url)
    photo_response.raise_for_status()
    photo_data = photo_response.content

    # Создание объекта изображения
    img = Image.open(io.BytesIO(photo_data)).convert("RGB")

    # Добавление текста
    font_url = "https://github.com/deadboizxc/zxc-userbot-files/blob/master/CascadiaCodePL.ttf?raw=true"
    font_response = requests.get(font_url)
    font_response.raise_for_status()
    font_data = font_response.content

    text = "\n".join(wrap(text, 19))
    t = text + "\n"

    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(io.BytesIO(font_data), 32, encoding="UTF-8")

    lines = text.split("\n")
    max_line_width = max(draw.textbbox((10, 10), line, font=font)[2] for line in lines)

    y = 10
    for line in lines:
        draw.text((10, y), line, font=font, fill=(0, 0, 0))
        y += draw.textbbox((10, y), line, font=font)[3]

    # Сохранение изображения в памяти
    output_data = io.BytesIO()
    img.save(output_data, format='JPEG')
    output_data.seek(0)

    # Отправка изображения
    if message.reply_to_message:
        await client.send_photo(
            message.chat.id,
            photo=output_data,
            reply_to_message_id=message.reply_to_message.id,
        )
    else:
        await client.send_photo(message.chat.id, photo=output_data)

modules_help["jac"] = {
    "jac [text]/[reply]*": "generate Jacque Fresco quote"
}
