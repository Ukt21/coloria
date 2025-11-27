import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_KEY"))


async def transcribe_voice(path: str) -> str:
    with open(path, "rb") as audio:
        tr = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio,
        )
    return tr.text.strip()
