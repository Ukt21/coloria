import os
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from bot.handlers import register_handlers

bot = Bot(token=os.getenv("BOT_TOKEN"), parse_mode=ParseMode.HTML)
dp = Dispatcher()


def run_telegram_bot():
    register_handlers(dp)
    asyncio.create_task(dp.start_polling(bot))

