from time import sleep
import random
import asyncio

from pyrogram import Client, filters
from pyrogram.types import Message

from pyrogram.errors import FloodWait
from pyrogram.types import ChatPermissions

from utils.misc import modules_help, prefix


@Client.on_message(filters.command('hack', prefixes=prefix) & filters.me)
async def hack(client, message):
        perc = 0
        while(perc < 100):
                try:
                        text = "👮 Взлом сікрітарші в процессе ..." + str(perc) + "%"
                        await message.edit_text(text)
                        perc += random.randint(1, 3)
                        sleep(0.1)
                except FloodWait as e:
                        sleep(e.x)
        await message.edit_text("🟢 Сікрітарші успішно взломана!")
        sleep(3)
        message.edit("🕶 Тиримо її окуляри ...")
        perc = 0

        while(perc < 100):
                try:
                        text = "🕶 Тиримо її окуляри ..." + str(perc) + "%"
                        await message.edit_text(text)
                        perc += random.randint(1, 5)
                        sleep(0.15)
                except FloodWait as e:
                        sleep(e.x)
        await message.edit_text("🕶 Окуляри були успішно зтирені!")

modules_help["hack"] = {
    "hack sik": "hack sikritarsha",
    "hack bog": "hack bogdan",
    "hack misha": "hack misha"
}
