from utils.misc import modules_help, prefix
from utils.config import DETECT
from pyrogram import Client, filters

from deep_translator import GoogleTranslator
import detectlanguage

detectlanguage.configuration.api_key = DETECT



@Client.on_message(filters.command(["tr", "trans"], prefix) & filters.me)
async def translate(_client, message):
    await message.edit_text("<b>Translating text...</b>")
    if message.reply_to_message and (
        message.reply_to_message.text or message.reply_to_message.caption
    ):
        if len(message.text.split()) == 1:
            await message.edit(
                f"<b>Usage: Reply to a message, then <code>{prefix}tr [lang]*</code></b>"
            )
            return
        target = message.text.split()[1]
        if message.reply_to_message.text:
            text = message.reply_to_message.text
        else:
            text = message.reply_to_message.caption
        detectlang = detectlanguage.simple_detect(text)
        try:
            translated = GoogleTranslator(source=detectlang, target=target).translate(text=text)
        except ValueError as err:
            await message.edit("Error: <code>{}</code>".format(str(err)))
            return
        await message.edit(
            f"<b>Translated from <code>{detectlang}</code> to <code>{target}</code></b>:\n\n<code>{translated}</code>"
        )
    else:
        if len(message.text.split()) <= 2:
            await message.edit(f"<b>Usage: <code>{prefix}tr [lang]* [text]*</code></b>")
            return
        target = message.text.split(None, 2)[1]
        text = message.text.split(None, 2)[2]
        detectlang = detectlanguage.simple_detect(text)
        try:
            translated = GoogleTranslator(source=detectlang, target=target).translate(text=text)
        except ValueError as err:
            await message.edit("Error: <code>{}</code>".format(str(err)))
            return
        await message.edit(
            f"<b>Translated from <code>{detectlang}</code> to <code>{target}</code></b>:\n\n<code>{translated}</code>"
        )


@Client.on_message(filters.command(["transdl", "trdl"], prefix) & filters.me)
async def translatedl(_client, message):
    target = message.text.split(None, 2)[1]
    text = message.text.split(None, 2)[2]
    try:
        translated = GoogleTranslator(source=detectlang, target=target).translate(text=text)
    except ValueError as err:
        await message.edit("Error: <code>{}</code>".format(str(err)))
        return
    await message.edit(f"{translated}")


modules_help["translator"] = {
    "tr": "[lang]* [text/reply]* translate message",
    "trdl": f"[lang]* [your text]* short variant of {prefix}tr",
}