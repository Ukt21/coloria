# placeholder api client
import aiohttp
import os

BACKEND = os.getenv("BACKEND_URL")


async def register_user(data: dict):
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{BACKEND}/api/users/register", json=data) as r:
            return await r.json()


async def add_text_food(telegram_id, text):
    async with aiohttp.ClientSession() as session:
        form = {"telegram_id": str(telegram_id), "text": text}
        async with session.post(f"{BACKEND}/api/food/add/text", data=form) as r:
            return await r.json()


async def add_photo_food(telegram_id, path):
    async with aiohttp.ClientSession() as session:
        form = aiohttp.FormData()
        form.add_field("telegram_id", str(telegram_id))
        form.add_field("file", open(path, "rb"), filename="photo.jpg")

        async with session.post(f"{BACKEND}/api/food/add/photo", data=form) as r:
            return await r.json()


async def add_voice_food(telegram_id, path):
    async with aiohttp.ClientSession() as session:
        form = aiohttp.FormData()
        form.add_field("telegram_id", str(telegram_id))
        form.add_field("file", open(path, "rb"), filename="voice.ogg")

        async with session.post(f"{BACKEND}/api/food/add/voice", data=form) as r:
            return await r.json()


async def get_stats(telegram_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BACKEND}/api/stats/today/{telegram_id}") as r:
            return await r.json()


async def get_ai_tip(telegram_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BACKEND}/api/ai/tip/{telegram_id}") as r:
            return await r.json()
