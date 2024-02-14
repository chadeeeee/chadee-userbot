from time import *
from pyrogram import Client, filters
from pyrogram.types import Message

from utils.misc import modules_help, prefix


@Client.on_message(filters.command("tagall", prefix) & filters.me)
def tagall(client: Client, message: Message):
    message.delete()
    chat_id = message.chat.id
    string = ""
    for member in client.get_chat_members(chat_id):
        tag = member.user.username
        string = f"@{tag}\n" if tag != None else f"{member.user.mention}\n"
        client.send_message(chat_id, text=string)
#        time.sleep(2)


modules_help["tagall"] = {
    "tagall": "Tag all members",
}
