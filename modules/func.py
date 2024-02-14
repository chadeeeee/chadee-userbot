import subprocess
import time
from time import sleep
import random
import asyncio

from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import Message, ChatPermissions

from utils.misc import prefix
from utils.scripts import import_library

bs4 = import_library("bs4")

from bs4 import BeautifulSoup

# Команда type
@Client.on_message(filters.command("type", prefixes=prefix) & filters.me)
async def type(_, msg):
    orig_text = msg.text.split(".type ", maxsplit=1)[1]
    text = orig_text
    tbp = "" # to be printed
    typing_symbol = "▒"
    while(tbp != orig_text):
        try:
            await msg.edit(tbp + typing_symbol)
            sleep(0.1) # 50 ms

            tbp = tbp + text[0]
            text = text[1:]

            await msg.edit(tbp)
            sleep(0.1)

        except FloodWait as e:
            sleep(e.x)

R = "❤️"
W = "🤍"

heart_list = [
    W * 9,
    W * 2 + R * 2 + W + R * 2 + W * 2,
    W + R * 7 + W,
    W + R * 7 + W,
    W + R * 7 + W,
    W * 2 + R * 5 + W * 2,
    W * 3 + R * 3 + W * 3,
    W * 4 + R + W * 4,
    W * 9,
]
joined_heart = "\n".join(heart_list)

heartlet_len = joined_heart.count(R)

SLEEP = 0.1


@Client.on_message(filters.command("cm", prefixes=prefix) & filters.me)
async def commands(_, msg):
    to_send = msg.text.split(None, 1)
    result = subprocess.run(to_send[1], shell = True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            stdin=subprocess.PIPE,
                            encoding='utf-8')
    if result.returncode == 0:
        try:
            await msg.edit(f"`{result.stdout}`", parse_mode="MARKDOWN")
        except:
            await msg.edit(f"`Команда завершена удачно`", parse_mode="MARKDOWN")
    else:
        await msg.edit(f"`Я не могу выполнить эту команду`", parse_mode="MARKDOWN")


@Client.on_message(filters.command("site", prefixes=prefix) & filters.me)
async def screenshot_site(client, msg):
    to_send = msg.text.split(maxsplit=1)[1]
    await msg.delete()
    await asyncio.sleep(3)
    await client.send_photo(chat_id=msg.chat.id, photo="https://mini.s-shot.ru/920x768/JPEG/1024/Z100/?" + to_send)


@Client.on_message(filters.command("search", prefixes=prefix) & filters.me)
async def search_google(_, msg):
    user_agent = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) clientleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }

    to_send = msg.text.split(None, 1) #Запрашиваем у юзера, что он хочет найти
    url = requests.get('https://www.google.com/search?q=' + to_send[1], headers=user_agent) #Делаем запрос
    soup = BeautifulSoup(url.text, features="lxml") #Получаем запрос
    r = soup.find_all("div", class_="yuRUbf") #Выводи весь тег div class="r"
    rs = soup.find_all("div", class_="IsZvec")
    results_news = []
    for s, sr in zip(r, rs):
        link = s.find('a').get('href') #Ищем ссылки по тегу <a href="example.com"
        title = s.find("h3") #Ищем описание ссылки по тегу <h3 class="LC20lb DKV0Md"
        opisanie = sr.get_text()
        title = title.get_text()
        results = f'<a href="{link}">{title}</a>\n<code>{opisanie}</code>'
        results_news.clientend(results)
        result = "\n\n".join(results_news)

    await msg.edit(f'Результаты по запросу: `"{to_send[1]}"`\n\n{result}', parse_mode="HTML", disable_web_page_preview = True)

