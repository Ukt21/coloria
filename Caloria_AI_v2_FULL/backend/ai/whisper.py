# placeholder ai whisper
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_KEY"))


async def transcribe_voice(path: str):
    """
    Whisper-1 переводит голосовое сообщение в текст.
    """

    with open(path, "rb") as audio:
        result = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio
        )

    return result.text
