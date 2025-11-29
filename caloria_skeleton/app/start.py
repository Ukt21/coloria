
from aiogram import Router
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from app.keyboards.main_menu import main_menu_kb


start_router = Router()


# FSM (машина состояний) для регистрации
class Registration(StatesGroup):
    waiting_for_name = State()
    waiting_for_gender = State()
    waiting_for_age = State()
    waiting_for_height = State()
    waiting_for_weight = State()
    waiting_for_goal = State()


@start_router.message(Command("start"))
async def start_cmd(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "<b>Привет! Я — бот для подсчёта калорий 🍏</b>\n\n"
        "Чтобы начать, давай создадим твой профиль.\n\n"
        "Как тебя зовут?",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.set_state(Registration.waiting_for_name)


@start_router.message(Registration.waiting_for_name)
async def user_name_entered(message: Message, state: FSMContext):
    await state.update_data(name=message.text)

    await message.answer(
        "Отлично! Теперь выбери свой пол:",
        reply_markup=main_menu_kb.gender_keyboard()
    )
    await state.set_state(Registration.waiting_for_gender)


from aiogram.types import CallbackQuery


@start_router.callback_query(lambda c: c.data in ["gender_m", "gender_f"])
async def gender_chosen(callback: CallbackQuery, state: FSMContext):
    gender = "m" if callback.data == "gender_m" else "f"
    await state.update_data(gender=gender)

    await callback.message.edit_text("Укажи свой возраст (число в годах):")
    await state.set_state(Registration.waiting_for_age)

