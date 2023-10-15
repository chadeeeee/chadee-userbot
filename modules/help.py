from pyrogram import Client, filters
from pyrogram.types import Message

from utils.misc import modules_help, prefix
from utils.scripts import format_module_help


@Client.on_message(filters.command(["help", "h"], prefix) & filters.me)
async def help_cmd(_, message: Message):
    if len(message.command) == 1:
        msg_edited = False
        text = (
            "<b>Help for <a href=https://t.me/deadboizxc>deadboizxc</a>\n"
            f"For more help on how to use a command, type <code>{prefix}help [module]</code>\n\n"
            "Available Modules:\n"
        )

        for module_name, module_commands in sorted(
            modules_help.items(), key=lambda x: x[0]
        ):
            text += "★ {}: {}\n".format(
                module_name.title(),
                " ".join(
                    [
                        f"<code>{prefix + cmd_name.split()[0]}</code>"
                        for cmd_name in module_commands.keys()
                    ]
                ),
            )
            if len(text) >= 2048:
                text += "</b>"
                if msg_edited:
                    await message.reply(text, disable_web_page_preview=True)
                else:
                    await message.edit(text, disable_web_page_preview=True)
                    msg_edited = True
                text = "<b>"

        text += f"\nThe number of modules in the userbot: {len(modules_help) / 1}</b>"

        if msg_edited:
            await message.reply(text, disable_web_page_preview=True)
        else:
            await message.edit(text, disable_web_page_preview=True)
    elif message.command[1].lower() in modules_help:
        await message.edit(format_module_help(message.command[1].lower()))
    else:
        # No, this cringe won't be refactored
        command_name = message.command[1].lower()
        for name, commands in modules_help.items():
            for command in commands.keys():
                if command.split()[0] == command_name:
                    cmd = command.split(maxsplit=1)
                    cmd_desc = commands[command]
                    return await message.edit(
                        f"<b>Help for command <code>{prefix}{command_name}</code>\n"
                        f"Module: {name} (<code>{prefix}help {name}</code>)</b>\n\n"
                        f"<code>{prefix}{cmd[0]}</code>"
                        f"{' <code>' + cmd[1] + '</code>' if len(cmd) > 1 else ''}"
                        f" — <i>{cmd_desc}</i>"
                    )
        await message.edit(f"<b>Module {command_name} not found</b>")


modules_help["help"] = {
    "help [module/command name]": "Get common/module/command help"
}
