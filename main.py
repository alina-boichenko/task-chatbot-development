import asyncio
import datetime
import logging
import os
import sys

import dateparser
import spacy

import openai
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

openai.api_key = os.getenv("OPENAI_API_KEY")
TOKEN = os.getenv("BOT_TOKEN")
WEATHER_API_KEY = os.getenv("WEATHER_API")
nlp = spacy.load("en_core_web_sm")

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """This handler receives messages with `/start` command"""
    await message.answer(f"Hello, {message.from_user.full_name}! Ask your question!")


@dp.message()
async def echo_handler(message: types.Message) -> None:
    try:
        location, date = get_location_and_date(message.text)
        data = get_weather(location, date)
        answer = run_conversation(message.text, data)
        await message.answer(answer)
    except TypeError:
        await message.answer("Nice try!")


def get_location_and_date(message: str) -> (str, str):
    doc = nlp(message)
    location = None
    date = None

    for token in doc:
        if token.ent_type_ == "GPE":
            location = token.text
        if token.ent_type_ == "DATE":
            date = dateparser.parse(token.text)

    return location, date


def get_weather(location, date):
    """Get the weather in a given location for a specified date"""
    days = (date - datetime.datetime.today()).days
    weather_url = (
        f"https://api.weatherapi.com/v1/forecast.json?key="
        f"{WEATHER_API_KEY}&q={location}&days={days or 1}&aqi=no&alerts=no"
    )
    response = requests.get(weather_url)
    data = response.json()
    data_dict = {
        "location": data["location"],
        "current_weather": data["current"],
        "date_forecast": data["forecast"]["forecastday"][0]["date"],
        "forecast_weather": data["forecast"]["forecastday"][0]["day"],
    }
    return data_dict


def run_conversation(message: str, data: dict) -> str:
    messages = [{"role": "user", "content": f"{message} Analyze next data: {data}"}]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
    )
    return response["choices"][0]["message"]["content"]


async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
