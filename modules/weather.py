import requests
import datetime

from pyrogram import Client, filters

from utils.db import db
from utils.scripts import format_exc
from utils.misc import modules_help, prefix
from utils.config import OPEN_WEATHER_TOKEN

async def weather_city(data, city):
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    time = datetime.datetime.now().strftime('%H:%M:%S')
    weather = data['weather'][0]['main']
    description = data['weather'][0]['description']
    temp = round(data['main']['temp'])
    feels_like = round(data['main']['feels_like'])
    humidity = data['main']['humidity']
    wind = data['wind']['speed']
    clouds = data['clouds']['all']
    sunrise = datetime.datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M:%S')
    sunset = datetime.datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M:%S')

    if weather == 'Thunderstorm':
        emoji = '⛈'
    elif weather == 'Drizzle' or weather == 'Rain':
        emoji = '🌧'
    elif weather == 'Snow':
        emoji = '❄️'
    elif weather == 'Clear':
        emoji = '☀️'
    elif weather == 'Tornado':
        emoji = '🌪'
    else:
        emoji = '☁️'

    sign_temp = '+' if temp > 0 else ''
    sign_feels_like = '+' if feels_like > 0 else ''

    info_weather = (
        f'🌍 <b>City</b>: <code>{city}\n'
        f'🗓 <b>Date</b>: <code>{date}\n'
        f'⏱ <b>Time</b>: <code>{time}\n\n'
        f'{emoji} <b>Weather</b>: <code>{weather}</code> - <code>{description}\n</code>'
        f'🌡️ <b>**Average Temperature</b>: <code>{sign_temp}{temp}°C\n</code>'
        f'🌡️ <b>**Feels Like</b>: <code>{sign_feels_like}{feels_like}°C\n</code>'
        f'💧 <b>**Humidity</b>: <code>{humidity}%\n</code>'
        f'💨 <b>**Wind</b>: <code>{wind}m/s\n</code>'
        f'☁️ <b>**Clouds</b>: <code>{clouds}%\n</code>'
        f'🌅 <b>**Sunrise</b>: <code>{sunrise}\n</code>'
        f'🌇 <b>**Sunset</b>: <code>{sunset}</code>'
    )

    return info_weather

async def get_weather(city):
    try:
        # Getting weather data from OpenWeatherMap API
        r = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPEN_WEATHER_TOKEN}&units=metric')
        r.raise_for_status()
        data = r.json()
        info_weather = await weather_city(data, city)
        return info_weather
    except Exception as e:
        return format_exc(e)

@Client.on_message(filters.command(["weather", "w"], prefixes=prefix) & filters.me)
async def weather_command(_, message):
    if len(message.command) == 1:
        city = db.get("custom.weather", "city", "Kiev")
    else:
        city = message.command[1]

    await message.edit(f"<b>Processing city {city}...</b>")

    info_weather = await get_weather(city)

    await message.edit(info_weather)

@Client.on_message(filters.command(["set_weather_city", "swcity"], prefixes=prefix) & filters.me)
async def set_weather_city(_, message):
    if len(message.command) == 1:
        return await message.edit("<b>City name isn't provided</b>")

    db.set("custom.weather", "city", message.command[1])
    await message.edit(f"<b>City {message.command[1]} set!</b>")

modules_help["weather"] = {
        "weather [city]**": "Get weather for the selected city.",
        "set_weather_city [city]**": "Set the default city for the weather command."
}
