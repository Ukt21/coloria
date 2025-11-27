from aiogram.fsm.state import State, StatesGroup


class RegisterStates(StatesGroup):
    gender = State()
    age = State()
    weight = State()
    height = State()
    activity = State()
    goal = State()
    nutrition = State()
    allergies = State()
