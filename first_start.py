import subprocess
from pathlib import Path
import datetime
import sys
from pyrogram import Client
from utils.zxc_path import _BOT_DIR_
from utils.config import API_ID_1, API_HASH_1

app = Client(
    "my_account_1",
     api_id=API_ID_1,
     api_hash=API_HASH_1,
     hide_password=True,
)

client_1 = Path(_BOT_DIR_, 'client1.py')

def main():
    subprocess.Popen([sys.executable, client_1])


if __name__ == "__main__":
    app.start()
    try:
        app.send_message(
            "me",
            f"[{datetime.datetime.now()}] zxc-userbot launched! \n"
        )
    except Exception:
        pass
    app.stop()
    main()
