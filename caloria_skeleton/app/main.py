import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from app.config import settings
from app.handlers.start import start_router


async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=settings.BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()

    # Регистрация роутеров
    dp.include_router(start_router)

    print("Bot started...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
