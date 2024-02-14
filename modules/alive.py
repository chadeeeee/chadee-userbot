import asyncio
import time
import platform
from datetime import datetime
from sys import version_info

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram import __version__ as __pyro_version__

from utils.misc import modules_help, requirements_list, prefix, __python_version__

StartTime = time.time()
def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time

@Client.on_message(filters.command("alive", prefix) & filters.me)
async def alive(client, message):
    start_time = time.time()
    uptime = get_readable_time((time.time() - StartTime))
    reply_msg = f"<b>💜 <a href=https://github.com/deadboizxc/zxc-userbot>zxc-userbot</a> 💜</b>\n"
    reply_msg += f"<b>{platform.python_implementation()}: </b> <code>{__python_version__}</code>\n"
    reply_msg += f"<b>Pyrogram Version: </b> <code>{__pyro_version__}</code>\n"
    end_time = time.time()
    reply_msg += f"\nUptime: <code>{uptime}</code>"
    await message.edit(reply_msg, disable_web_page_preview=True)

modules_help["alive"] = {
    "alive": " check bot alive status",
}
