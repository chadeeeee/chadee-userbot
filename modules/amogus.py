from io import BytesIO
from random import randint

from pyrogram import Client, filters
from pyrogram.types import Message

from utils.misc import modules_help, prefix
from utils.scripts import import_library

PIL = import_library("PIL", "pillow")
requests = import_library("requests")
textwrap = import_library("textwrap")

from PIL import Image, ImageFont, ImageDraw
from requests import get
from textwrap import wrap

@Client.on_message(filters.command("amogus", prefix) & filters.me)
async def amogus(client: Client, message: Message):
    text = " ".join(message.command[1:])

    await message.edit("<b>amgus, tun tun tun tun tun tun tun tudududn tun tun...</b>")

    clr = randint(1, 12)

    url = "https://raw.githubusercontent.com/KeyZenD/AmongUs/master/"
    font = ImageFont.truetype(BytesIO(get(url + "bold.ttf").content), 60)
    imposter = Image.open(BytesIO(get(f"{url}{clr}.png").content))

    text_ = "\n".join(["\n".join(wrap(part, 30)) for part in text.split("\n")])

    bbox = ImageDraw.Draw(Image.new("RGB", (1, 1))).multiline_textbbox(
        (0, 0, 1, 1), text_, font, spacing=4, stroke_width=2
    )
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]

    text_img = Image.new("RGBA", (w + 30, h + 30))
    ImageDraw.Draw(text_img).multiline_text(
        (15, 15), text_, "#FFF", font, stroke_width=2, stroke_fill="#000"
    )
    w = imposter.width + text_img.width + 10
    h = max(imposter.height, text_img.height)

    image = Image.new("RGBA", (w, h))
    image.paste(imposter, (0, h - imposter.height), imposter)
    image.paste(text_img, (w - text_img.width, 0), text_img)
    image.thumbnail((512, 512))

    output = BytesIO()
    output.name = "imposter.webp"
    image.save(output)
    output.seek(0)

    await message.delete()
    await client.send_sticker(message.chat.id, output)

modules_help["amogus"] = {
    "amogus [text]": "amgus, tun tun tun tun tun tun tun tudududn tun tun"
}
