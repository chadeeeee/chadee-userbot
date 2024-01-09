from sys import version_info
from .db import db
from git import Repo
import random
import datetime

__all__ = [
    "modules_help",
    "requirements_list",
    "python_version",
    "prefix",
    "gitrepo",
    "userbot_version",
]

modules_help = {}
requirements_list = []
python_version = f"{version_info[0]}.{version_info[1]}.{version_info[2]}"
prefix = db.get("core.main", "prefix", ".")
gitrepo = Repo(".")

commit_time = (
        datetime.datetime.fromtimestamp(gitrepo.head.commit.committed_date)
        .astimezone(datetime.timezone.utc)
        .strftime("%Y-%m-%d")
    )

userbot_version = f"v2.3"
