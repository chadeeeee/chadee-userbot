import os
import carbon
import asyncio

from pyrogram import Client, filters
from pyrogram.types import Message

from utils.misc import modules_help, prefix
from utils.scripts import interact_with, interact_with_to_delete, format_exc


@Client.on_message(filters.command("code", prefix) & filters.me)
async def rayso(client: Client, message: Message):
    _, lang, code = message.text.split(maxsplit=2)

    try:
        await message.edit(f"<b>Creating...</b>")

        cb = carbon.Carbon()
        opts = carbon.CarbonOptions(code=code,
                                    show_line_numbers=True,
                                    first_line_number=1,
                                    font_family='JetBrains Mono',
                                    font_size_px=20,
                                    language='python',
                                    background_color=(18, 33, 44))
        image = await cb.generate(opts)
        await image.save('pretty_code')
        await message.delete()
        await client.send_photo(message.chat.id, 'pretty_code.png')
        os.remove('pretty_code.png')
    except Exception as e:
        await message.edit(format_exc(e))


modules_help["code"] = {
    "code [lang] [title] [code]": "create a photo of code in pretty format",
}