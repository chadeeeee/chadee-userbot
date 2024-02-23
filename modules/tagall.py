from time import sleep
from pyrogram import Client, filters
from pyrogram.types import Message

from utils.misc import modules_help, prefix


@Client.on_message(filters.command("tagall", prefix) & filters.me)
def tagall(client: Client, message: Message):
    message.delete()
    chat_id = message.chat.id
    string = ""
    members = client.get_chat_members(chat_id)
    for member in members:
        if member.user.username:
            string += f"@{member.user.username} "
        else:
            string += f"{member.user.mention} "
        if len(string) > 3500:
            client.send_message(chat_id, text=string)
            string = ""
    if string:
        client.send_message(chat_id, text=string)


modules_help["tagall"] = {
    "tagall": "Tag all members",
}
