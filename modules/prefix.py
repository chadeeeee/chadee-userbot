from pyrogram import Client, filters
from pyrogram.types import Message

from utils.db import db
from utils.scripts import restart
from utils.misc import modules_help, prefix


@Client.on_message(
    filters.command(["sp", "setprefix", "setprefix_zxc"], prefix)
    & filters.me
)
async def setprefix(_, message: Message):
    if len(message.command) > 1:
        pref = message.command[1]
        db.set("core.main", "prefix", pref)
        await message.edit(f"<b>Prefix [ <code>{pref}</code> ] is set!</b>")
        restart()
    else:
        await message.edit("<b>The prefix must not be empty!</b>")


modules_help["prefix"] = {
    "setprefix [prefix]": "Set custom prefix",
    "setprefix_zxc [prefix]": "Set custom prefix",
}
