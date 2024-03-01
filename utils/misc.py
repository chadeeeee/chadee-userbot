from sys import version_info
from .db import db
from git import Repo
import random
import datetime

modules_help = {}
requirements_list = []

prefix = db.get("core.main", "prefix", ".")
gitrepo = Repo(".")

__python_version__ = f"{version_info[0]}.{version_info[1]}.{version_info[2]}"
__userbot_version__ = f"v2.1"
