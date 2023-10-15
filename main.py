import subprocess
import sys
from pathlib import Path

from utils.zxc_path import _BOT_DIR_

client_1 = Path(_BOT_DIR_, 'client1.py')

def main():
    subprocess.Popen([sys.executable, client_1])

if __name__ == '__main__':
    main()
