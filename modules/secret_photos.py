from pyrogram import Client, filters
from pyrogram.types import Message
import datetime

def _secret_media(_, __, message: Message) -> bool:
    media = message.photo or message.video
    return media and media.ttl_seconds

secret_media = filters.create(_secret_media)


@Client.on_message(filters.private & ~filters.me & secret_media)
async def secret_media(client: Client, message: Message):
    full_name = (
        f"{message.chat.first_name} {message.chat.last_name} | {message.chat.username}"
        if message.chat.last_name
        else message.chat.first_name
    )
    caption = f"Secret {message.media.value} from {full_name}"
    media = await message.download(in_memory=True)
    await client.send_document(
        chat_id="me",
        document=media,
        caption=caption,
        force_document=True,
    )
