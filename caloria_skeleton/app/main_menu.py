# app/keyboards/main_menu.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class main_menu_kb:

    @staticmethod
    def gender_keyboard():
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="👨 Мужчина", callback_data="gender_m"),
                    InlineKeyboardButton(text="👩 Женщина", callback_data="gender_f"),
                ]
            ]
        )
