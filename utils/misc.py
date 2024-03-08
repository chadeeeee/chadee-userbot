from sys import version_info
from git import Repo
import random
import datetime

from sys import version_info
import random
import datetime

__all__ = [
    "modules_help",
    "requirements_list",
    "__python_version__",
    "prefix",
    "__userbot_version__",
]

modules_help = {}
requirements_list = []
__python_version__ = f"{version_info[0]}.{version_info[1]}.{version_info[2]}"
prefix = "."

__userbot_version__ = f"v2.2"
