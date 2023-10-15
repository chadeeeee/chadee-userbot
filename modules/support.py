from pyrogram import Client, filters
from pyrogram.types import Message
import random
import datetime

from utils.misc import (
    modules_help,
    prefix,
    userbot_version,
    python_version,
    gitrepo,
)

@Client.on_message(filters.command(["support", "repo"], prefix) & filters.me)
async def support(_, message: Message):
    devs = ["@deadboizxc"]
    random.shuffle(devs)

    commands_count = float(
        len([cmd for module in modules_help for cmd in module])
    )

    await message.edit(
        f"<b>💜 zxc-userbot 💜</b>\n\n"
        "<b>GitHub:</b> <a href=https://github.com/deadboizxc/zxc-userbot>deadboizxc/zxc-userbot</a>\n"
        "<b>License:</b> <a href=https://github.com/deadboizxc/zxc-userbot/blob/master/LICENSE>MIT</a>\n\n"
        "<b>Modules repository:</b> <a href=https://github.com/deadboizxc/custom_modules>"
        "deadboizxc/custom_modules</a>\n"
        f"<b>Main developers:</b> {', '.join(devs)}\n\n"
        f"<b>Python version:<b/> {python_version}\n"
        f"<b>Modules count:</b> {len(modules_help) / 1}\n"
        f"<b>Commands count:</b> {commands_count}</b>",
        disable_web_page_preview=True,
    )


@Client.on_message(filters.command(["version", "ver"], prefix) & filters.me)
async def version(client: Client, message: Message):
    changelog = ""
    ub_version = ".".join(userbot_version.split(".")[:2])
    await message.delete()

    remote_url = list(gitrepo.remote().urls)[0]
    commit_time = (
        datetime.datetime.fromtimestamp(gitrepo.head.commit.committed_date)
        .astimezone(datetime.timezone.utc)
        .strftime("%Y-%m-%d %H:%M:%S %Z")
    )

    await message.reply(
        f"<b>💜 <a href = https://github.com/deadboizxc/zxc-userbot>zxc-userbot</a> 💜</b>\n"
        f"<b>Version: </b><code>{userbot_version}</code>\n"
        + (
            f"<b>Branch:</b> <code><a href={remote_url}/tree/{gitrepo.active_branch}>{gitrepo.active_branch}</a></code>\n"
            if gitrepo.active_branch != "master"
            else ""
        )
        + f"<b>Commit:</b> <code><a href={remote_url}/commit/{gitrepo.head.commit.hexsha}>"
        f"{gitrepo.head.commit.hexsha[:7]}</a></code> by <b>{gitrepo.head.commit.author.name}</b>\n"
        f"<b>Commit time:</b> <code>{commit_time}</code>",
    disable_web_page_preview=True)


modules_help["support"] = {
    "support": "Information about userbot",
    "version": "Check userbot version",
}
