import subprocess
from pathlib import Path
import datetime
import sys
from pyrogram import Client
from utils.zxc_path import _BOT_DIR_
from utils.config import API_ID, API_HASH

app = Client(
    "chadee",
     api_id=API_ID,
     api_hash=API_HASH,
     hide_password=True,
)

client = Path(_BOT_DIR_, 'client.py')

def main():
    subprocess.Popen([sys.executable, client])


if __name__ == "__main__":
    app.start()
    try:
        app.send_message(
            "me",
            f"[{datetime.datetime.now()}] chadee-userbot launched! \n"
        )
    except Exception:
        pass
    app.stop()
    main()
