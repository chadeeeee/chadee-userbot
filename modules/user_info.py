from pyrogram import Client, filters
from pyrogram.raw import functions
from pyrogram.types import Message

from utils.misc import modules_help, prefix
from utils.scripts import format_exc, interact_with, interact_with_to_delete


@Client.on_message(filters.command("inf", prefix) & filters.me)
async def get_user_inf(client: Client, message: Message):
    await message.edit("<b>Receiving user information...</b>")
    if len(message.command) >= 2:
        peer = await client.resolve_peer(message.command[1])
    elif message.reply_to_message and message.reply_to_message.from_user:
        peer = await client.resolve_peer(message.reply_to_message.from_user.id)
    else:
        peer = await client.resolve_peer("me")

    response = await client.invoke(functions.users.GetFullUser(id=peer))

    user = response.users[0]
    print(user)
    full_user = response.full_user
    async for photo in client.get_chat_photos(user.id, limit=1):
        await client.download_media(photo.file_id, "name.jpg")

    if user.username is None:
        username = "None"
    else:
        username = f"@{user.username}"
    bio = "None" if full_user.about is None else full_user.about
    common = await client.get_common_chats(user.id)

    user_info = f"""<b>USER INFORMATION:</b>

🆔 <b>User ID:</b> <code>{user.id}</code>
👤 <b>First Name:</b> {user.first_name}
🗣️ <b>Last Name:</b> {user.last_name}
🌐 <b>Username:</b> {user.username}
📱 <b>Phone number:</b> +{user.phone}
🤖 <b>Is Bot:</b> <code>{user.bot}</code>
🚷 <b>Is Scam:</b> <code>{user.scam}</code>
🚫 <b>Restricted:</b> <code>{user.restricted}</code>
✅ <b>Verified:</b> <code>{user.verified}</code>
⭐ <b>Premium:</b> <code>{user.premium}</code>
📝 <b>User Bio:</b> {bio}

👀 <b>Same groups seen:</b> {len(common)}
🔗 <b>User permanent link:</b> <a href='tg://user?id={user.id}'>{user.username}</a>
"""
    async for photo in client.get_chat_photos(user.id, limit=1):
        await message.delete()
        await client.send_photo(message.chat.id, photo.file_id, caption=f"{user_info}")


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
        bio = "None" if full_user.about is None else full_user.about
        user_info = f"""🌐 <b>Username</b>: {username}
🆔 <b>User ID:</b> <code>{user.id}</code>
👤 <b>First Name:</b> {user.first_name}
🗣️ <b>Last Name:</b> {user.last_name}
🌐 <b>Username:</b> {user.username}
📱 <b>Phone number:</b> +{user.phone}
🤖 <b>Is Bot:</b> <code>{user.bot}</code>
🚷 <b>Is Scam:</b> <code>{user.scam}</code>
🚫 <b>Restricted:</b> <code>{user.restricted}</code>
✅ <b>Verified:</b> <code>{user.verified}</code>
⭐ <b>Premium:</b> <code>{user.premium}</code>
📝 <b>User Bio:</b> {bio}
📞 <b>Contact:</b> <code>{user.contact}</code>
📌 <b>Can pin message:</b> <code>{full_user.can_pin_message}</code>
💬 <b>Mutual contact:</b> <code>{user.mutual_contact}</code>
🔒 <b>Access hash:</b> <code>{user.access_hash}</code>
📲 <b>Phone calls available</b>: <code>{full_user.phone_calls_available}</code>
🔕 <b>Phone calls private:</b> <code>{full_user.phone_calls_private}</code>
❌ <b>Blocked:</b> <code>{full_user.blocked}</code></b>"""
        async for photo in client.get_chat_photos(user.id, limit=1):
            await message.delete()
            await client.send_photo(message.chat.id, photo.file_id, caption=f"{user_info}")
    except Exception as e:
        await message.edit(format_exc(e))


modules_help["user_info"] = {
    "inf [reply|id|username]": "Get brief information about user",
    "inffull [reply|id|username]": "Get full information about user",
}