import os
import json
import requests
import pathlib
import asyncio

from asyncio import sleep
from pathlib import Path

from pyrogram import Client, filters
from pyrogram.types import Message

from utils.misc import modules_help, prefix
from utils.zxc_path import _HOME_DIR_, _BOT_DIR_, _YTDLP_DIR_

from utils.scripts import import_library
yt_dlp = import_library("yt_dlp")


class AudioFile:
    def __init__(self, link):
        self.url = link
        self.main_dir = _BOT_DIR_
        self.module_dir = _YTDLP_DIR_

    def download_file(self):
        if not os.path.exists(self.module_dir):
            os.mkdir(self.module_dir)
            os.chdir(self.module_dir)
        else:
            os.chdir(self.module_dir)

        ydl_opts = {
            'outtmpl': '%(title)s.%(ext)s',
            'writethumbnail': True,
            'format': 'bestaudio/best',
            'postprocessors':[
                {'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'},
                {'key': 'FFmpegMetadata', 'add_metadata': 'True'},
                {'key': 'EmbedThumbnail','already_have_thumbnail': False}
            ]
        }
        self.audioformat = ydl_opts['postprocessors'][0]['preferredcodec']

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(self.url, download=True)
            var1 = json.dumps(ydl.sanitize_info(info))
            data = json.loads(var1)
            self.json_name = data['id']+'.json'
            self.filename = data['title']+'.'+self.audioformat
            self.thumb_link = data['thumbnail']
            self.thumb = str(self.thumb_link.split('/')[-1])

        r = requests.get(self.thumb_link)
        with open(self.thumb, 'wb') as code:
            code.write(r.content)
        os.chdir(self.main_dir)

    def delete_files(self):
        file_list = os.listdir(_YTDLP_DIR_)
        for file_name in file_list:
            file_path = os.path.join(_YTDLP_DIR_, file_name)  # Получаем полный путь к файлу
            if os.path.isfile(file_path):  # Проверяем, что это файл, а не папка
                os.remove(file_path)

    def show_thumb(self):
        return self.thumb

    def show_path(self):
        return self.filepath

    def to_home(self):
        os.chdir(self.main_dir)


class VideoFile:
    def __init__(self, link):
        self.url = link
        self.main_dir = _BOT_DIR_
        self.module_dir = _YTDLP_DIR_

    def download_file(self):
        if not os.path.exists(self.module_dir):
            os.mkdir(self.module_dir)
            os.chdir(self.module_dir)
        else:
            os.chdir(self.module_dir)

        ydl_opts = {
            'outtmpl': '%(title)s.%(ext)s',
            'noplaylist': True,
            'quiet': True,
            'format':'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(self.url, download=True)
            var1 = json.dumps(ydl.sanitize_info(info))
            data = json.loads(var1)

            self.json_name = data['id']+'-'+data['title']+'.json'
            self.filename = data['title']+'.'+'mp4'
            self.thumb_link = data['thumbnail']
            self.thumb = str(self.thumb_link.split('/')[-1])

        r = requests.get(self.thumb_link)
        with open(self.thumb, 'wb') as code:
            code.write(r.content)
        os.chdir(self.main_dir)

    def delete_files(self):
        file_list = os.listdir(_YTDLP_DIR_)
        for file_name in file_list:
            file_path = os.path.join(_YTDLP_DIR_, file_name)  # Получаем полный путь к файлу
            if os.path.isfile(file_path):  # Проверяем, что это файл, а не папка
                os.remove(file_path)

    def show_thumb(self):
        return self.thumb

    def show_path(self):
        return self.filepath

    def to_home(self):
        os.chdir(self.main_dir)


@Client.on_message(filters.command('a', prefix) & filters.me)
async def soundcloud(client, message):
    if len(message.command) < 2:
        await message.edit('**please enter link**')
        return

    first_path = os.getcwd()
    s = message.text.split(maxsplit=1)[1]
    n1 = 'https://soundcloud.com/'
    n2 = 'https://soundcloud.app.goo.gl/'
    n3 = 'https://youtu.be/'
    n4 = 'https://www.youtube.com/'
    n5 = 'https://deezer.page.link/'
    split_text = s.split()

    for i in split_text:
        if n5 in i:
            link = None
            x = None
            await message.edit_text(text='**such links are not supported**')
            pass

        elif n1 or n2 or n3 or n4 in i:
            link = i
            x = AudioFile(link)
        else:
            await message.edit_text(text='**such links are not supported**')
            pass


    if link == i:
        await message.edit_text(text='**please wait ...**')
        x.download_file()
        thumb = x.show_thumb()

        mas_audio = []
        path = _YTDLP_DIR_
        for root, dirs, files in os.walk(_YTDLP_DIR_):
            for file in files:
                if(file.endswith('.mp3')):
                    mas_audio.append(os.path.join(file))
                elif(file.endswith('.m4a')):
                    mas_audio.append(os.path.join(file))
                else:
                    pass

        for data in mas_audio:
            link = None
            await client.send_audio(chat_id=message.chat.id, audio=f'{_YTDLP_DIR_}{data}', thumb=f'{_YTDLP_DIR_}{thumb}')
            await message.edit_text(text='**file sent successfully**')
            await asyncio.sleep(2)
            await message.delete()
            x.delete_files()
            x.to_home()
    else:
        await message.edit_text(text='**such links are not supported**')
        pass


@Client.on_message(filters.command('v', prefix) & filters.me)
async def youtube(client, message):
    if len(message.command) < 2:
        await message.edit('**please enter link**')
        return

    first_path = os.getcwd()
    s = message.text.split(maxsplit=1)[1]
    split_text = s.split()
    n = 'https://youtu.be/'
    n2 = 'https://www.youtube.com/'

    for i in split_text:
        if n or n2 in i:
            link = i
            y = VideoFile(link)
        else:
            await message.edit_text(text='**such links are not supported**')
            pass

    if link == i:
        await message.edit_text(text='**please wait ...**')
        y.download_file()
        thumb = y.show_thumb()

        mas_video = []
        path = _YTDLP_DIR_
        for root, dirs, files in os.walk(_YTDLP_DIR_):
            for file in files:
                if(file.endswith('.mp4')):
                    mas_video.append(os.path.join(file))
                else:
                    pass

        for data in mas_video:
            await client.send_audio(chat_id=message.chat.id, audio=f'{_YTDLP_DIR_}{data}', thumb=f'{_YTDLP_DIR_}{thumb}')
            await message.edit_text(text='**file sent successfully**')
            await asyncio.sleep(2)
            await message.delete()
            y.delete_files()
            y.to_home()
    else:
        await message.edit_text(text='**such links are not supported**')
        pass


modules_help['ytdlp_mod'] = {
    'a': '[link from youtube/soundcloud]',
    'v': '[link from youtube]',
}
