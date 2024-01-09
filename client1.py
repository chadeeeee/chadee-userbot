import subprocess
import os
import sys
from pathlib import Path
from importlib import import_module
import logging
import platform
import asyncio
import datetime
from time import sleep
from colorlog import ColoredFormatter

from utils.config import (
    API_ID_1,
    API_HASH_1,
)
from utils.misc import prefix
from utils.db import db
from utils.misc import userbot_version
from utils.scripts import restart

from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import ChatPermissions

# Инициализация colorlog
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Создаем форматтер с поддержкой цветов
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

# Создаем обработчик консольного вывода
console_handler = logging.StreamHandler()

# Устанавливаем форматтер для обработчика
console_handler.setFormatter(formatter)

# Добавляем обработчик в логгер
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
