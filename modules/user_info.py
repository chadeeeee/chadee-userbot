from pyrogram import Client, filters
from pyrogram.raw import functions
from pyrogram.types import Message

from utils.misc import modules_help, prefix
from utils.scripts import format_exc, interact_with, interact_with_to_delete


@Client.on_message(filters.command("inf", prefix) & filters.me)
async def get_user_inf(client: Client, message: Message):
    if len(message.command) >= 2:
        peer = await client.resolve_peer(message.command[1])
    elif message.reply_to_message and message.reply_to_message.from_user:
        peer = await client.resolve_peer(message.reply_to_message.from_user.id)
    else:
        peer = await client.resolve_peer("me")

    response = await client.invoke(functions.users.GetFullUser(id=peer))

    user = response.users[0]
    full_user = response.full_user

    if user.username is None:
        username = "None"
    else:
        username = f"@{user.username}"
    about = "None" if full_user.about is None else full_user.about

    user_info = f"""|=<b>Username: {username}
|-Id: <code>{user.id}</code>
|-Bot: <code>{user.bot}</code>
|-Scam: <code>{user.scam}</code>
|-Name: <code>{user.first_name}</code>
|-Deleted: <code>{user.deleted}</code>
|-BIO: <code>{about}</code>
</b>"""
    await message.edit(user_info)


@Client.on_message(filters.command("inffull", prefix) & filters.me)
async def get_full_user_inf(client: Client, message: Message):
    await message.edit("<b>Receiving the information...</b>")

    try:
        if len(message.command) >= 2:
            peer = await client.resolve_peer(message.command[1])
        elif message.reply_to_message and message.reply_to_message.from_user:
            peer = await client.resolve_peer(
                message.reply_to_message.from_user.id
            )
        else:
            peer = await client.resolve_peer("me")

        response = await client.invoke(functions.users.GetFullUser(id=peer))

        user = response.users[0]
        full_user = response.full_user

        if user.username is None:
            username = "None"
        else:
            username = f"@{user.username}"
        about = "None" if full_user.about is None else full_user.about
        user_info = f"""|=<b>Username: {username}
|-Id: <code>{user.id}</code>
|-Bot: <code>{user.bot}</code>
|-Scam: <code>{user.scam}</code>
|-Name: <code>{user.first_name}</code>
|-Deleted: <code>{user.deleted}</code>
|-BIO: <code>{about}</code>
|-Contact: <code>{user.contact}</code>
|-Can pin message: <code>{full_user.can_pin_message}</code>
|-Mutual contact: <code>{user.mutual_contact}</code>
|-Access hash: <code>{user.access_hash}</code>
|-Restricted: <code>{user.restricted}</code>
|-Verified: <code>{user.verified}</code>
|-Phone calls available: <code>{full_user.phone_calls_available}</code>
|-Phone calls private: <code>{full_user.phone_calls_private}</code>
|-Blocked: <code>{full_user.blocked}</code></b>"""
        await message.edit(user_info)
    except Exception as e:
        await message.edit(format_exc(e))


modules_help["user_info"] = {
    "inf [reply|id|username]": "Get brief information about user",
    "inffull [reply|id|username": "Get full information about user",
}
