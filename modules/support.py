import random
import datetime
import platform
from git import Repo, RemoteReference

from pyrogram import Client, filters
from pyrogram.types import Message

from utils.misc import modules_help, prefix, __userbot_version__, gitrepo, __python_version__

def check_remote_branch_exists(repo, branch_name):
    try:
        repo.remotes.origin.fetch()
        remote_branch = RemoteReference(repo, f"refs/remotes/origin/{branch_name}")
        remote_branch.commit  # This will raise an exception if the branch doesn't exist
        return True
    except Exception as e:
        return False

@Client.on_message(filters.command(["support", "repo"], prefix) & filters.me)
async def support(_, message: Message):
    devs = ["@deadboizxc"]
    random.shuffle(devs)
    commands_count = float(len([cmd for module in modules_help for cmd in module]))
    remote_url = gitrepo.remote("origin").url
    if remote_url.endswith(".git"):
        remote_url = remote_url[:-4]

    branch_name = gitrepo.active_branch
    if check_remote_branch_exists(gitrepo, branch_name):
        branch_link = f"<a href={remote_url}/tree/{branch_name}>{branch_name}</a>"
    else:
        branch_link = branch_name

    await message.edit(
        f"<b>💜 zxc-userbot 💜</b>\n\n"
        f"<b>GitHub:</b> <a href={remote_url}>{remote_url}</a>\n"
        "<b>License:</b> <a href=https://github.com/deadboizxc/zxc-userbot/blob/master/LICENSE>MIT</a>\n\n"
        "<b>Modules repository:</b> <a href=https://github.com/deadboizxc/custom_modules>"
        "deadboizxc/custom_modules</a>\n"
        f"<b>Main developers:</b> {', '.join(devs)}\n\n"
        f"<b>{platform.python_implementation()}:</b> {__python_version__}\n"
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
        ub_version = f'<a href="{remote_url}/commit/{commit_sha}">{__userbot_version__}</a>'
    else:
        ub_version = __userbot_version__

    branch_name = gitrepo.active_branch
    if check_remote_branch_exists(gitrepo, branch_name):
        branch_link = f"<a href={remote_url}/tree/{branch_name}>{branch_name}</a>"
    else:
        branch_link = branch_name

    await message.edit(
        f"<b>💜 <a href={remote_url}>zxc-userbot</a> 💜</b>\n"
        f"<b>Version:</b> {ub_version}\n"
        + (f"<b>Branch:</b> {branch_link}\n" if branch_name != "master" else "")
        + f"<b>Commit:</b> <a href={remote_url}/commit/{gitrepo.head.commit.hexsha}>"
        f"{gitrepo.head.commit.hexsha[:7]}</a> by <b>{gitrepo.head.commit.author.name}</b>\n"
        f"<b>Commit time:</b> <code>{commit_time}</code>",
        disable_web_page_preview=True
    )


modules_help["support"] = {
    "support": "Information about userbot",
    "version": "Check userbot version",
}
