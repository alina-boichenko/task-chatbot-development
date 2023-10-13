import io

from pydub import AudioSegment

import whisper
from aiogram import Bot
from aiogram.types import Voice

model = whisper.load_model("base")


async def save_voice_as_mp3(bot: Bot, voice: Voice) -> str:
    voice_file_info = await bot.get_file(voice.file_id)
    voice_ogg = io.BytesIO()
    await bot.download_file(voice_file_info.file_path, voice_ogg)
    path = f"voices/voice-{voice.file_unique_id}.mp3"
    AudioSegment.from_file(voice_ogg, format="ogg").export(path, format="mp3")
    text = await process_voice_message(path)
    return text


async def process_voice_message(path: str):
    result = model.transcribe(path, fp16=False)
    return result["text"]
