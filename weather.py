import datetime
import os

import dateparser
import openai
import requests
import spacy

nlp = spacy.load("en_core_web_sm")

openai.api_key = os.getenv("OPENAI_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API")


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
