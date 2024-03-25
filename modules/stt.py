from pyrogram import Client, filters
from pyrogram.types import Message

from utils.misc import modules_help, prefix
from utils.scripts import interact_with, interact_with_to_delete, format_exc

import speech_recognition as sr
from pydub import AudioSegment

import os

recognizer = sr.Recognizer()


def recognize_speech(audio_file, language="uk-UA"):
    with sr.AudioFile(audio_file) as source:
        try:
            return recognizer.recognize_google(recognizer.record(source), language=language)
        except sr.UnknownValueError:
            return "Unable to recognize language"
        except sr.RequestError as e:
            return f"Language recognition service error: {str(e)}"


@Client.on_message(filters.command("stt", prefix) & filters.me)
async def stt(_, message: Message):
    try:
        if (r := message.reply_to_message) and r.voice:
            await message.edit("<b>Processing...</b>")
            lang = message.text.split(maxsplit=1)[-1]
            if lang == "ua":
                language = "uk-UA"
            elif lang == "ru":
                language = "ru-RU"
            elif lang == "en":
                language = "en-US"
            else:
                language = "uk-UA"
            v, w = await r.download(), "converted_audio.wav"
            AudioSegment.from_file(v).export(w, format="wav")
            t = recognize_speech(w, language)
            os.remove(v)
            os.remove(w)
            await message.edit(f"<b>Text</b>: {t}")
    except Exception as e:
        await message.edit(str(e))


modules_help["stt"] = {
    "stt [reply]*": "get text from voice message",
}
