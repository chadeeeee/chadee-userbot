import subprocess
import os
import sys
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import ChatPermissions
from time import sleep
from utils.config import (
    API_ID_1,
    API_HASH_1,
    TOKEN_1,
    channel_id
)
from utils.misc import prefix
from pathlib import Path
from importlib import import_module
import logging
import platform
import asyncio
import datetime
import time
from utils.db import db
from utils.misc import userbot_version
from utils.scripts import restart

logging.basicConfig(level=logging.INFO)

app = Client("my_account_1",
              api_id=API_ID_1,
              api_hash=API_HASH_1,
              bot_token=TOKEN_1,
              plugins=dict(root="modules")
             )

logging.info("zxc-userbot started!")
data = datetime.datetime.now().strftime("%Y-%m-%d"+" "+"%H:%M:%S")

app.start()
app.send_message("me", f"**<b>[{data}]</b> zxc-userbot launched!** \n")
app.stop()
app.run()
