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
from colorama import init, Fore, Back, Style

from utils.config import (
    API_ID,
    API_HASH,
)
from utils.misc import prefix
from utils.db import db
from utils.misc import __userbot_version__
from utils.scripts import restart

from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import ChatPermissions
from git import Repo

gitrepo = Repo(".")

# Добавьте этот блок в начало вашего кода
init(autoreset=True)

# Замените ваш текущий блок logging.basicConfig на следующий код
logging.basicConfig(level=logging.INFO,
                    format=f"{Style.BRIGHT}{Fore.CYAN}%(levelname)s{Fore.RESET} {Fore.MAGENTA}%(message)s{Fore.RESET}",
                    handlers=[logging.StreamHandler()])

# Добавьте цвета для каждого уровня логирования
logging.addLevelName(logging.DEBUG, f"{Style.BRIGHT}{Fore.CYAN}{logging.getLevelName(logging.DEBUG)}{Fore.RESET}{Style.RESET_ALL}")
logging.addLevelName(logging.INFO, f"{Style.BRIGHT}{Fore.MAGENTA}{logging.getLevelName(logging.INFO)}{Fore.RESET}{Style.RESET_ALL}")
logging.addLevelName(logging.WARNING, f"{Style.BRIGHT}{Fore.YELLOW}{logging.getLevelName(logging.WARNING)}{Fore.RESET}{Style.RESET_ALL}")
logging.addLevelName(logging.ERROR, f"{Style.BRIGHT}{Fore.RED}{logging.getLevelName(logging.ERROR)}{Fore.RESET}{Style.RESET_ALL}")
logging.addLevelName(logging.CRITICAL, f"{Style.BRIGHT}{Fore.RED}{Back.WHITE}{logging.getLevelName(logging.CRITICAL)}{Back.RESET}{Fore.RESET}{Style.RESET_ALL}")

app = Client("chadee",
              api_id=API_ID,
              api_hash=API_HASH,
              plugins=dict(root="modules")
             )

async def start():
    await app.start()
    data = datetime.datetime.now().strftime("%Y-%m-%d" + " " + "%H:%M:%S")
    await app.send_message("me", f"**<b>[{data}]</b> chadee-userbot launched!** \n")

async def stop():
    await app.send_message("me", "**chadee-userbot stopping...**")
    await app.stop()

@app.on_message(filters.command("stop", prefix) & filters.me)
async def stop_command(_, message):
    await loop.create_task(stop())

if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(start())
        loop.run_forever()
    except KeyboardInterrupt:
        loop.run_until_complete(stop())
    finally:
        loop.close()
