import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

from audio_transcription import save_voice_as_mp3
from weather import get_location_and_date, get_weather, run_conversation
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

dp = Dispatcher()
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """This handler receives messages with `/start` command"""
    await message.answer(f"Hello, {message.from_user.full_name}! Ask your question!")


@dp.message()
async def echo_handler(message: types.Message) -> None:
    await message.answer("Please wait...")

    try:
        if message.content_type == types.ContentType.VOICE:
            answer = await save_voice_as_mp3(bot, message.voice)
            await message.answer(f"Transcription of your audio message: \n\n{answer}")

        if message.content_type == types.ContentType.TEXT:
            location, date = get_location_and_date(message.text)
            data = get_weather(location, date)
            answer = run_conversation(message.text, data)
            await message.answer(answer)

    except TypeError:
        await message.answer("Nice try!")


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
