import os
import openai

from pyrogram import Client, filters
from pyrogram.types import Message

from utils.misc import modules_help, prefix

from utils.config import OPEN_AI

openai.api_key = OPEN_AI


@Client.on_message(filters.command(["ai", "gpt",], prefix) & filters.me)
async def antispam(_, message: Message):
    prompt = message.text.replace(".gpt ", "")
    await message.edit_text("<b>Generating...</b>")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Ваше повідомлення для системи."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=4096
    )
    await message.edit_text(f"👤 <b>Питання:</b> {prompt}\n\n🧠 <b>Відповідь:</b>{response.choices[0].message['content']}")


modules_help["ai"] = {
    "ai [question]": "ask ChatGPT something",
}
