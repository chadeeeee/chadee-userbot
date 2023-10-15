import os
import json
import requests
import pathlib
from pathlib import Path

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

if __name__ == '__main__':
    pass

