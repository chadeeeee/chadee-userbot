import textwrap

from pyrogram import Client, filters
from pyrogram.types import Message, Document

from utils.misc import modules_help, prefix
from utils.scripts import import_library, format_exc
from utils.db import db

pylast = import_library("pylast")
requests = import_library("requests")

import pylast
import requests


def auth_required(function):
    async def wrapped(client: Client, message: Message):
        if db.get("custom.lastfm", "session_key", None) is None:
            await message.edit(
                f"<b>⚠️To use this module auth is required\n"
                f"ℹ️Run <code>{prefix}lfauth</code> to authorize.</b>"
            )
        else:
            return await function(client, message)

    return wrapped


@Client.on_message(filters.command("lfauth", prefix) & filters.me)
async def lfauth(client: Client, message: Message):
    sg = pylast.SessionKeyGenerator(
        pylast.LastFMNetwork(
            api_key="077cc8b034fe314509f292ef2ff5b98f",
            api_secret="6087563066c158c5b991a29f36569b93",
        )
    )
    url = sg.get_web_auth_url()
    token = sg.web_auth_tokens[url]
    await message.edit(
        f"<b>ℹ️Go to {url} and grant access.\n"
        f"After this, run <code>{prefix}lfconfirm</code> command</b>",
        disable_web_page_preview=True,
    )
    db.set("custom.lastfm", "request_url", url)
    db.set("custom.lastfm", "request_token", token)


@Client.on_message(filters.command("lfconfirm", prefix) & filters.me)
async def lfconfirmauth(client: Client, message: Message):
    sg = pylast.SessionKeyGenerator(
        pylast.LastFMNetwork(
            api_key="077cc8b034fe314509f292ef2ff5b98f",
            api_secret="6087563066c158c5b991a29f36569b93",
        )
    )
    try:
        session_key, username = sg.get_web_auth_session_key_username(
            db.get("custom.lastfm", "request_url", "null"),
            db.get("custom.lastfm", "request_token", "null"),
        )
        db.set("custom.lastfm", "session_key", session_key)
        db.set("custom.lastfm", "username", username)
        db.remove("custom.lastfm", "request_url")
        db.remove("custom.lastfm", "request_token")
    except Exception as e:
        await message.edit(
            "<b>⚠️Something went wrong.\nInfo about error: </b>"
            f"<code>{format_exc(e)}</code></b>"
        )
        return
    await message.edit("<b>✅Authorized.</b>")


@Client.on_message(filters.command("lfnow", prefix) & filters.me)
@auth_required
async def example_edit(client: Client, message: Message):
    nw = pylast.LastFMNetwork(
        api_key="077cc8b034fe314509f292ef2ff5b98f",
        api_secret="6087563066c158c5b991a29f36569b93",
        session_key=db.get("custom.lastfm", "session_key"),
        username=db.get("custom.lastfm", "username"),
    )
    if len(message.text.split()) > 1:
        try:
            track = nw.get_user(message.text.split()[1]).get_now_playing()
        except:
            await message.edit(f"<b>User not found.</b>")
            return
        if track is None:
            try:
                track = (
                    nw.get_user(message.text.split()[1]).get_recent_tracks(1)[0].track
                )
            except:
                await message.edit(f"<b>Nothing is playing.</b>")
                return
    else:
        track = nw.get_user(db.get("custom.lastfm", "username")).get_now_playing()
        if track is None:
            try:
                track = (
                    nw.get_user(db.get("custom.lastfm", "username"))
                    .get_recent_tracks(1)[0]
                    .track
                )
            except:
                await message.edit(f"<b>Nothing is playing.</b>")
                return
    try:
        link = f"https://song.link/i/{requests.get(f'https://itunes.apple.com/search?term={track}&country=RU&entity=song&limit=1').json()['results'][0]['trackId']}"
    except Exception:
        link = "#"

    res = textwrap.dedent(
        f"""
            <b>🎶 Now playing: <i><a href="{link}">{track}</a></i></b>
        """
    )
    await message.edit(res, disable_web_page_preview=True)


modules_help["lastfm"] = {
    "lfnow [username]": "Show now playing track using last.fm",
    "lfauth": "Auth last.fm account",
}
