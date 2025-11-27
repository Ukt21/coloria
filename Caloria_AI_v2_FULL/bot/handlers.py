# placeholder handlers
import os
import uuid
from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from bot.states import RegisterStates
from bot.keyboards import (
    gender_kb, activity_kb, goal_kb,
    nutrition_kb, main_menu
)
from bot.api_client import (
    register_user, add_text_food,
    add_photo_food, add_voice_food,
    get_stats, get_ai_tip
)

router = Router()


def register_handlers(dp):
    dp.include_router(router)


# ------------------ START ------------------
@router.message(CommandStart())
async def start(msg: types.Message, state: FSMContext):
    await msg.answer(
        "<b>Добро пожаловать в Caloria AI 🎯</b>\n"
        "Давайте создадим ваш профиль.\n\n"
        "Выберите пол:",
        reply_markup=gender_kb()
    )
    await state.set_state(RegisterStates.gender)


# ------------------ REGISTRATION ------------------
@router.callback_query(RegisterStates.gender)
async def reg_gender(cb: types.CallbackQuery, state: FSMContext):
    gender = "male" if cb.data.endswith("male") else "female"
    await state.update_data(gender=gender)
    await cb.message.edit_text("Введите возраст:")
    await state.set_state(RegisterStates.age)


@router.message(RegisterStates.age)
async def reg_age(msg: types.Message, state: FSMContext):
    await state.update_data(age=int(msg.text))
    await msg.answer("Введите вес (кг):")
    await state.set_state(RegisterStates.weight)


@router.message(RegisterStates.weight)
async def reg_weight(msg: types.Message, state: FSMContext):
    await state.update_data(weight=float(msg.text))
    await msg.answer("Введите рост (см):")
    await state.set_state(RegisterStates.height)


@router.message(RegisterStates.height)
async def reg_height(msg: types.Message, state: FSMContext):
    await state.update_data(height=float(msg.text))
    await msg.answer("Уровень активности:", reply_markup=activity_kb())
    await state.set_state(RegisterStates.activity)


@router.callback_query(RegisterStates.activity)
async def reg_activity(cb: types.CallbackQuery, state: FSMContext):
    level = cb.data.split("_")[1]
    await state.update_data(activity_level=level)
    await cb.message.edit_text("Цель:", reply_markup=goal_kb())
    await state.set_state(RegisterStates.goal)


@router.callback_query(RegisterStates.goal)
async def reg_goal(cb: types.CallbackQuery, state: FSMContext):
    goal = cb.data.split("_")[1]
    await state.update_data(goal=goal)
    await cb.message.edit_text("Тип питания:", reply_markup=nutrition_kb())
    await state.set_state(RegisterStates.nutrition)


@router.callback_query(RegisterStates.nutrition)
async def reg_nutrition(cb: types.CallbackQuery, state: FSMContext):
    nutr = cb.data.split("_")[1]
    await state.update_data(nutrition_type=nutr)
    await cb.message.edit_text("Есть ли аллергии?")
    await state.set_state(RegisterStates.allergies)


@router.message(RegisterStates.allergies)
async def reg_allergies(msg: types.Message, state: FSMContext):
    await state.update_data(allergies=msg.text)

    data = await state.get_data()
    data["telegram_id"] = msg.from_user.id

    await register_user(data)
    await state.clear()

    await msg.answer("🎉 Профиль создан!", reply_markup=main_menu())


# ------------------ ADD FOOD ------------------
@router.callback_query(F.data == "add_food")
async def add_food_menu(cb: types.CallbackQuery):
    await cb.message.answer("Отправьте текст, фото или голосовое, чтобы добавить еду 🍽")
    await cb.answer()


@router.message(F.text)
async def text_food(msg: types.Message):
    await msg.answer("Анализирую… ⏳")

    await add_text_food(msg.from_user.id, msg.text)

    await msg.answer("Готово! ✔", reply_markup=main_menu())


@router.message(F.photo)
async def photo_food(msg: types.Message):
    await msg.answer("Обрабатываю фото… 📸")

    file_id = msg.photo[-1].file_id
    file = await msg.bot.get_file(file_id)

    temp = f"/tmp/{uuid.uuid4()}.jpg"
    await msg.bot.download(file.file_path, temp)

    await add_photo_food(msg.from_user.id, temp)
    os.remove(temp)

    await msg.answer("Добавлено! ✔", reply_markup=main_menu())


@router.message(F.voice)
async def voice_food(msg: types.Message):
    await msg.answer("Расшифровываю голос… 🎧")

    file_id = msg.voice.file_id
    file = await msg.bot.get_file(file_id)

    temp = f"/tmp/{uuid.uuid4()}.ogg"
    await msg.bot.download(file.file_path, temp)

    await add_voice_food(msg.from_user.id, temp)
    os.remove(temp)

    await msg.answer("Добавлено! ✔", reply_markup=main_menu())


# ------------------ AI TIP ------------------
@router.callback_query(F.data == "ai_tip")
async def ai_tip_handler(cb: types.CallbackQuery):
    tip = await get_ai_tip(cb.from_user.id)
    await cb.message.answer(f"💡 Совет от ИИ:\n\n{tip['tip']}")
    await cb.answer()


# ------------------ WEBAPP ------------------
@router.callback_query(F.data == "webapp")
async def webapp_handler(cb: types.CallbackQuery):

    url = os.getenv("BACKEND_URL") + "/webapp"

    await cb.message.answer(
        "Открываю статистику 📊",
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="📊 Открыть WebApp",
                    web_app=types.WebAppInfo(url=url)
                )
            ]
        ])
    )

    await cb.answer()
