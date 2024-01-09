from pyrogram import Client, filters
from pyrogram.types import Message

import random
import datetime

from utils.misc import modules_help, prefix, userbot_version, python_version, gitrepo

@Client.on_message(filters.command(["support", "repo"], prefix) & filters.me)
async def support(_, message: Message):
    devs = ["@deadboizxc"]
    random.shuffle(devs)
    commands_count = float(len([cmd for module in modules_help for cmd in module]))

    remote_url = gitrepo.remote("origin").url
    if remote_url.endswith(".git"):
        remote_url = remote_url[:-4]

    branch_link = f"<a href={remote_url}/tree/{gitrepo.active_branch}>{gitrepo.active_branch}</a>"

    await message.edit(
        f"<b>💜 zxc-userbot 💜</b>\n\n"
        f"<b>GitHub:</b> <a href={remote_url}>{remote_url}</a>\n"
        "<b>License:</b> <a href=https://github.com/deadboizxc/zxc-userbot/blob/master/LICENSE>MIT</a>\n\n"
        "<b>Modules repository:</b> <a href=https://github.com/deadboizxc/custom_modules>"
        "deadboizxc/custom_modules</a>\n"
        f"<b>Main developers:</b> {', '.join(devs)}\n\n"
        f"<b>Python version:</b> {python_version}\n"
        f"<b>Modules count:</b> {len(modules_help) / 1}\n"
        f"<b>Commands count:</b> {commands_count}\n"
        f"<b>Branch:</b> {branch_link}",
        disable_web_page_preview=True,
    )

@Client.on_message(filters.command(["version", "ver"], prefix) & filters.me)
async def version(client: Client, message: Message):
    changelog = ""

    remote_url = gitrepo.remote("origin").url
    if remote_url.endswith(".git"):
        remote_url = remote_url[:-4]

    commit_time = (
        datetime.datetime.fromtimestamp(gitrepo.head.commit.committed_date)
        .astimezone(datetime.timezone.utc)
        .strftime("%Y-%m-%d %H:%M:%S %Z")
    )

    update_version_commit = None
    for commit in gitrepo.iter_commits():
        if any(keyword in commit.message.lower() for keyword in ["update version", "update ver", "upd ver"]):
            update_version_commit = commit
            break

    if update_version_commit:
        commit_sha = update_version_commit.hexsha
        ub_version = f'<a href="{remote_url}/commit/{commit_sha}">{userbot_version}</a>'
    else:
        ub_version = userbot_version

    branch_link = f"<a href={remote_url}/tree/{gitrepo.active_branch}>{gitrepo.active_branch}</a>"

    await message.edit(
        f"<b>💜 <a href={remote_url}>zxc-userbot</a> 💜</b>\n"
        f"<b>Version:</b> {ub_version}\n"
        + (f"<b>Branch:</b> {branch_link}\n" if gitrepo.active_branch != "master" else "")
        + f"<b>Commit:</b> <a href={remote_url}/commit/{gitrepo.head.commit.hexsha}>"
        f"{gitrepo.head.commit.hexsha[:7]}</a> by <b>{gitrepo.head.commit.author.name}</b>\n"
        f"<b>Commit time:</b> <code>{commit_time}</code>",
        disable_web_page_preview=True
    )

modules_help["support"] = {
    "support": "Information about userbot",
    "version": "Check userbot version",
}
