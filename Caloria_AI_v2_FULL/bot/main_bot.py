import os

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from openai import OpenAI

# Токен бота из переменных окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN env variable is not set")

# Ключ OpenAI из переменных окружения
OPENAI_KEY = os.getenv("OPENAI_KEY")
if not OPENAI_KEY:
    raise RuntimeError("OPENAI_KEY env variable is not set")

client = OpenAI(api_key=OPENAI_KEY)

bot = Bot(BOT_TOKEN)
dp = Dispatcher()


@dp.message(F.text == "/start")
async def cmd_start(message: Message):
    await message.answer(
        "Привет! Я Caloria AI бот 🧠\n"
        "Скоро буду помогать считать калории и давать советы по питанию."
    )


async def generate_tip(stats: dict) -> str:
    """
    Создаёт короткий совет по питанию на основе потребления за день.
    Используется и ботом, и backend-ом.
    """
    prompt = f"""
Ты — нутриционист Caloria AI.
Вот статистика дня:

{stats}

Дай короткую рекомендацию (1–2 предложения).
Будь простым и мотивирующим.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
    )

    return response.choices[0].message.content


async def run_telegram_bot():
    """
    Основная функция запуска Telegram-бота.
    Её импортирует main.py и запускает в фоне.
    """
    await dp.start_polling(bot)
