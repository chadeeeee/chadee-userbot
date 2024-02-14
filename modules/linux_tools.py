import os
import shutil
import asyncio

from pyrogram import Client, filters
from pyrogram.types import Message

from utils.misc import modules_help, prefix
from utils.zxc_path import _HOME_DIR_, _ROOT_DIR_


# Функція рекурсивного пошуку
def find_file_in_directory(_ROOT_DIR_, file_name):
    for dirpath, dirnames, filenames in os.walk(_ROOT_DIR_):
        if file_name in filenames:
            return os.path.join(dirpath, file_name)
    return None


programming_languages = [
    {"lang": "abap", "ext": ".abap"},
    {"lang": "actionscript", "ext": ".as"},
    {"lang": "ada", "ext": ".ada"},
    {"lang": "algol", "ext": ".algol"},
    {"lang": "apl", "ext": ".apl"},
    {"lang": "assembly", "ext": ".asm"},
    {"lang": "awk", "ext": ".awk"},
    {"lang": "bash", "ext": ".sh"},
    {"lang": "basic", "ext": ".bas"},
    {"lang": "batch", "ext": ".bat"},
    {"lang": "c", "ext": ".c"},
    {"lang": "c#", "ext": ".cs"},
    {"lang": "c++", "ext": ".cpp"},
    {"lang": "cobol", "ext": ".cobol"},
    {"lang": "cool", "ext": ".cl"},
    {"lang": "clojure", "ext": ".clj"},
    {"lang": "cool", "ext": ".cl"},
    {"lang": "crystal", "ext": ".cr"},
    {"lang": "d", "ext": ".d"},
    {"lang": "dart", "ext": ".dart"},
    {"lang": "delphi", "ext": ".dpr"},
    {"lang": "dibol", "ext": ".dibol"},
    {"lang": "dylan", "ext": ".dylan"},
    {"lang": "eiffel", "ext": ".e"},
    {"lang": "elixir", "ext": ".ex"},
    {"lang": "elm", "ext": ".elm"},
    {"lang": "emacs lisp", "ext": ".el"},
    {"lang": "erlang", "ext": ".erl"},
    {"lang": "f#", "ext": ".fs"},
    {"lang": "forth", "ext": ".forth"},
    {"lang": "fortran", "ext": ".f"},
    {"lang": "fjölnir", "ext": ".fjo"},
    {"lang": "gherkin", "ext": ".feature"},
    {"lang": "go", "ext": ".go"},
    {"lang": "gnuplot", "ext": ".gp"},
    {"lang": "groovy", "ext": ".groovy"},
    {"lang": "haskell", "ext": ".hs"},
    {"lang": "html", "ext": ".html"},
    {"lang": "idl", "ext": ".idl"},
    {"lang": "inform", "ext": ".inf"},
    {"lang": "io", "ext": ".io"},
    {"lang": "jcl", "ext": ".jcl"},
    {"lang": "jscript", "ext": ".js"},
    {"lang": "jscript.net", "ext": ".js"},
    {"lang": "jupyter notebook", "ext": ".ipynb"},
    {"lang": "kotlin", "ext": ".kt"},
    {"lang": "labview", "ext": ".vi"},
    {"lang": "ladder logic", "ext": ".ldl"},
    {"lang": "lisp", "ext": ".lisp"},
    {"lang": "lua", "ext": ".lua"},
    {"lang": "matlab", "ext": ".m"},
    {"lang": "makefile", "ext": ".mk"},
    {"lang": "mathematica", "ext": ".m"},
    {"lang": "max", "ext": ".maxpat"},
    {"lang": "mercury", "ext": ".m"},
    {"lang": "minizinc", "ext": ".mzn"},
    {"lang": "modelica", "ext": ".mo"},
    {"lang": "modula-2", "ext": ".mod"},
    {"lang": "nim", "ext": ".nim"},
    {"lang": "nu", "ext": ".nu"},
    {"lang": "nxtosek", "ext": ".c"},
    {"lang": "oberon", "ext": ".oberon"},
    {"lang": "objective-c", "ext": ".m"},
    {"lang": "opencl", "ext": ".cl"},
    {"lang": "openedge abl", "ext": ".p"},
    {"lang": "oxygene", "ext": ".oxygene"},
    {"lang": "pascal", "ext": ".pas"},
    {"lang": "perl", "ext": ".pl"},
    {"lang": "powershell", "ext": ".ps1"},
    {"lang": "pure data", "ext": ".pd"},
    {"lang": "racket", "ext": ".rkt"},
    {"lang": "rebol", "ext": ".r"},
    {"lang": "ring", "ext": ".ring"},
    {"lang": "robot", "ext": ".robot"},
    {"lang": "rpl", "ext": ".rpl"},
    {"lang": "ruby", "ext": ".rb"},
    {"lang": "rust", "ext": ".rs"},
    {"lang": "sas", "ext": ".sas"},
    {"lang": "scala", "ext": ".scala"},
    {"lang": "scheme", "ext": ".scm"},
    {"lang": "shell", "ext": ".sh"},
    {"lang": "shen", "ext": ".shen"},
    {"lang": "smalltalk", "ext": ".st"},
    {"lang": "squirrel", "ext": ".nut"},
    {"lang": "swift", "ext": ".swift"},
    {"lang": "tcl", "ext": ".tcl"},
    {"lang": "tea", "ext": ".tea"},
    {"lang": "typescript", "ext": ".ts"},
    {"lang": "vhdl", "ext": ".vhd"},
    {"lang": "verilog", "ext": ".v"},
    {"lang": "vim script", "ext": ".vim"},
    {"lang": "vim snippet", "ext": ".vimsnip"},
    {"lang": "xproc", "ext": ".xpl"},
    {"lang": "r", "ext": ".r"},
    {"lang": "prolog", "ext": ".pl"},
    {"lang": "cobol", "ext": ".cbl"},
    {"lang": "javascript", "ext": ".js"},
    {"lang": "java", "ext": ".java"},
    {"lang": "roff", "ext": ".roff"},
    {"lang": "sql", "ext": ".sql"},
    {"lang": "html", "ext": ".html"},
    {"lang": "css", "ext": ".css"},
    {"lang": "php", "ext": ".php"},
    {"lang": "coffeescript", "ext": ".coffee"},
    {"lang": "cython", "ext": ".pyx"},
    {"lang": "ruby", "ext": ".rb"},
    {"lang": "perl", "ext": ".pl"},
    {"lang": "shell", "ext": ".sh"},
    {"lang": "lua", "ext": ".lua"},
    {"lang": "groovy", "ext": ".groovy"},
    {"lang": "powershell", "ext": ".ps1"},
    {"lang": "bash", "ext": ".sh"},
    {"lang": "batch", "ext": ".bat"},
    {"lang": "python", "ext": ".py"}
]


# Обробник команди /ls
@Client.on_message(filters.command('ls', prefixes=prefix) & filters.me)
async def list_file(client, message):
    if len(message.command) == 1:
        path = os.getcwd()
    else:
        path = " ".join(message.command[1:])

    if os.path.exists(path):
        file_list = os.listdir(path)
        file_list_formatted = ""
        for item in file_list:
            if os.path.isdir(os.path.join(path, item)):
                file_list_formatted += "\n"
                file_list_formatted += f"`{item}/`"
            else:
                file_list_formatted += "\n"
                file_list_formatted += f"`{item}`"
    await message.edit_text(
        f"**File list for: {path}**\n{file_list_formatted}"
    )

# Обробник команди /pwd
@Client.on_message(filters.command('pwd', prefixes=prefix) & filters.me)
async def pwd_to_file(client, message):
    path = os.getcwd()
    await message.edit_text(f"`{path}`")

# Обробник команди /cd
@Client.on_message(filters.command('cd', prefixes=prefix) & filters.me)
async def cd_to_folder(client, message):
    if len(message.command) == 1:
        os.chdir("..")
    else:
        path = " ".join(message.command[1:])
        if os.path.exists(path):
            os.chdir(os.path.expanduser(path))

    current_path = os.getcwd()
    await message.edit_text(f"**Current directory:** `{current_path}`")

# Обробник команди /home
@Client.on_message(filters.command('home', prefixes=prefix) & filters.me)
async def cd_to_home(client, message):
    os.chdir(os.path.expanduser(f"{_HOME_DIR_}"))
    path = os.getcwd()

    if os.path.exists(_HOME_DIR_):
        file_list = os.listdir()
        file_list_formatted = ""
        for item in file_list:
            if os.path.isdir(os.path.join(_HOME_DIR_, item)):
                file_list_formatted += "\n"
                file_list_formatted += f"`{item}/`"
            else:
                file_list_formatted += "\n"
                file_list_formatted += f"`{item}`"

    await message.edit_text(
        f"**File list for: {path}**\n{file_list_formatted}"
    )

# Обробник команди /home0
@Client.on_message(filters.command('home0', prefixes=prefix) & filters.me)
async def cd_to_home_zero(client, message):
    HOME_ZERO= "/storage/emulated/0/"
    os.chdir(os.path.expanduser(f"{HOME_ZERO}"))
    path = os.getcwd()

    if os.path.exists(HOME_ZERO):
        file_list = os.listdir()
        file_list_formatted = ""
        for item in file_list:
            if os.path.isdir(os.path.join(HOME_ZERO, item)):
                file_list_formatted += "\n"
                file_list_formatted += f"`{item}/`"
            else:
                file_list_formatted += "\n"
                file_list_formatted += f"`{item}`"

    await message.edit_text(
        f"**File list for: {path}**\n{file_list_formatted}"
    )

# Обробник команди /touch
@Client.on_message(filters.command('touch', prefixes=prefix) & filters.me)
async def create_file(client, message):
    if len(message.command) == 1:
        await message.edit('Please enter a file name.')
        return

    filename = " ".join(message.command[1:])
    with open(filename, 'w') as f:
        pass
    await message.edit_text(
        f"**Created new file: `{filename}`**"
    )

# Обробник команди /rm
@Client.on_message(filters.command('rm', prefixes=prefix) & filters.me)
async def removed_file(client, message):
    if len(message.command) == 1:
        await message.edit('Please specify a file or directory to remove.')
        return

    target = " ".join(message.command[1:])
    if os.path.exists(target):
        if os.path.isdir(target):
            shutil.rmtree(target, ignore_errors=True)
            await message.edit_text(f"**Directory '{target}' removed**")
        else:
            os.remove(target)
            await message.edit_text(f"**File '{target}' removed**")
    else:
        await message.edit_text(f"**'{target}' does not exist**")

# Обробник команди /echo
@Client.on_message(filters.command('echo', prefixes=prefix) & filters.me)
async def echo_file(client, message):
    if len(message.command) < 3:
        await message.edit('Please provide a file name and content to write.')
        return

    filename = message.command[1]
    filedata = message.command[2:]

    data = " ".join(filedata)

    with open(filename, 'w') as f:
        f.write(data)
    await message.edit_text(f"**File '{filename}' edited**")

# Обробник команди /cat
@Client.on_message(filters.command('cat', prefixes=prefix) & filters.me)
async def show_file(client, message):
    if len(message.command) == 1:
        await message.edit('Please specify a file to display.')
        return

    filename = message.command[1]
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            data = f.read()
        await message.edit_text(
            f"**File {filename}:\n**{data}"
        )

# Обробник команди /mkdir
@Client.on_message(filters.command('mkdir', prefixes=prefix) & filters.me)
async def create_dir(client, message):
    if len(message.command) == 1:
        await message.edit('Please specify a directory name to create.')
        return

    dirname = " ".join(message.command[1:])
    if not os.path.isdir(dirname):
        os.makedirs(dirname)
    await message.edit_text(
        f"**Create new dir: `{dirname}`**"
    )

# Обробник команди /codef
@Client.on_message(filters.command("codef", prefix) & filters.me)
async def send_formatted_code(client, message):
    # Отримання мови програмування із повідомлення
    lang_name = message.command[1]

    # Отримання коду для форматування
    code = " ".join(message.command[2:])

    # Пошук розширення файла в списку мов програмування
    file_extension = None
    for lang_info in programming_languages:
        if lang_info["lang"] == lang_name:
            file_extension = lang_info["ext"]
            break

    if file_extension is None:
        await client.send_message(message.chat.id, "Не вдалось знайти МП по імені.")
        return

    # Редагування тексту
    text = f"```{lang_name}\n{code}```"

    # Відправка повідомлення
    await message.edit(text)


@Client.on_message(filters.command("filef", prefix) & filters.me)
async def send_formatted_code_from_file(client, message):
    # Отримання мови програмування із повідомлення
    file_name = message.command[1]

    # Пробуємо спочатку знайти файл у поточній папці
    current_dir = os.getcwd()
    current_file_path = os.path.join(current_dir, file_name)

    if os.path.isfile(current_file_path):
        file_path = current_file_path
    else:
        # Якщо файл не знайдено у поточній папці, шукаємо рекурсивно від _ROOT_DIR_
        file_path = find_file_in_directory(_ROOT_DIR_, file_name)

    if file_path is None:
        await client.send_message(message.chat.id, "Файл не знайден")
        return

    # Отримання розширення файлу
    file_extension = os.path.splitext(file_path)[1]

    # Отримання імені МП на основі розширення файла
    lang_name = None
    for lang_info in programming_languages:
        if lang_info["ext"] == file_extension:
            lang_name = lang_info["lang"]
            break

    if lang_name is None:
        await client.send_message(message.chat.id, "Не вдалось оприділити МП за розширенням файлу.")
        return

    try:
        # Читання коду із файлу
        with open(file_path, "r") as file:
            code = file.read()
    except FileNotFoundError:
        await client.send_message(message.chat.id, "Файл не знайден")
        return

    # Редагування тексту
    text = f"```{lang_name}\n{code}```"

    # Відправка повідомлення
    await message.edit(text)


modules_help["linux_tools"] = {
    "ls": "[path] show contents in folder ",
    "pwd": "show path to dir",
    "cd": "[path] change dir",
    "home": "change dir to home directory",
    "home0": "change dir to .../storage/emulated/0/",
    "touch": "[file name] create empty file",
    "rm": "[file/dir name] remove file/dir",
    "echo": "[file name] edit file",
    "cat": "[file name] print file",
    "mkdir": "[dir name] make dir",
    "codef": "[lang name]* [code]*",
    "filef": "[file path]*"
}
