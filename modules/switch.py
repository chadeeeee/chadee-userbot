from pyrogram import Client, filters
from pyrogram.types import Message

from utils.misc import modules_help, prefix

ua_keys = (
    """йцукенгшщзхїфівапролджєячсмитьбю.₴"№;%:?ЙЦУКЕНГШЩЗХЇФІВАПРОЛДЖЄ/ЯЧСМИТЬБЮ,"""
)
en_keys = (
    """`qwertyuiop[]asdfghjkl;'zxcvbnm,./~@#$%^&QWERTYUIOP{}ASDFGHJKL:"|ZXCVBNM<>?"""
)
table = str.maketrans(ua_keys + en_keys, en_keys + ua_keys)


@Client.on_message(filters.command(["switch", "sw"], prefix) & filters.me)
async def switch(client: Client, message: Message):
    if len(message.command) == 1:
        if message.reply_to_message:
            text = message.reply_to_message.text
        else:
            history = await client.get_history(message.chat.id, limit=2)
            if history and history[1].from_user.is_self and history[1].text:
                text = history[1].text
            else:
                await message.edit("<b>Text to switch not found</b>")
                return
    else:
        text = message.text.split(maxsplit=1)[1]

    await message.edit(str.translate(text, table))


modules_help["switch"] = {
    "sw [reply/text for switch]*": "Useful when tou forgot to change the keyboard layout",
}
