import os
import sys
import logging
import asyncio
import datetime
import subprocess

from time import sleep
from colorlog import ColoredFormatter

from utils.config import (
    API_ID_1,
    API_HASH_1,
)
from utils.misc import prefix
from utils.misc import __userbot_version__

from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import ChatPermissions

logger = logging.getLogger()
logger.setLevel(logging.INFO)

formatter = ColoredFormatter(
    "%(log_color)s%(levelname)-8s%(reset)s %(blue)s%(message)s",
    datefmt=None,
    reset=True,
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    }
)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

app = Client("my_account_1",
              api_id=API_ID_1,
              api_hash=API_HASH_1,
              plugins=dict(root="modules")
             )

async def start():
    await app.start()
    data = datetime.datetime.now().strftime("%Y-%m-%d" + " " + "%H:%M:%S")
    await app.send_message("me", f"**<b>[{data}]</b> zxc-userbot launched!** \n")

async def stop():
    await app.send_message("me", "**zxc-userbot stopping...**")
    await app.stop()

@app.on_message(filters.command("stop", prefix) & filters.me)
async def stop_command(_, message):
    loop.create_task(stop())

if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(start())
        loop.run_forever()
    except KeyboardInterrupt:
        loop.run_until_complete(stop())
    finally:
        loop.close()
