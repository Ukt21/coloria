# placeholder keyboards
from aiogram.utils.keyboard import InlineKeyboardBuilder


def gender_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text="Мужчина", callback_data="gender_male")
    kb.button(text="Женщина", callback_data="gender_female")
    kb.adjust(2)
    return kb.as_markup()


def activity_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text="Низкая", callback_data="act_low")
    kb.button(text="Средняя", callback_data="act_medium")
    kb.button(text="Высокая", callback_data="act_high")
    kb.adjust(1)
    return kb.as_markup()


def goal_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text="Похудение", callback_data="goal_lose")
    kb.button(text="Поддержание", callback_data="goal_maintain")
    kb.button(text="Набор массы", callback_data="goal_gain")
    kb.adjust(1)
    return kb.as_markup()


def nutrition_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text="Обычное питание", callback_data="nut_standard")
    kb.button(text="Спортивное", callback_data="nut_sport")
    kb.button(text="Халяль", callback_data="nut_halal")
    kb.button(text="Веган", callback_data="nut_vegan")
    kb.adjust(1)
    return kb.as_markup()


def main_menu():
    kb = InlineKeyboardBuilder()
    kb.button(text="📊 Моя статистика", callback_data="webapp")
    kb.button(text="➕ Добавить еду", callback_data="add_food")
    kb.button(text="💡 Совет от ИИ", callback_data="ai_tip")
    kb.adjust(1)
    return kb.as_markup()
