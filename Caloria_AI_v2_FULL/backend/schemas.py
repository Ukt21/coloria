# placeholder schemas
from pydantic import BaseModel


class UserRegister(BaseModel):
    telegram_id: str
    gender: str
    age: int
    weight: float
    height: float
    activity_level: str
    goal: str
    nutrition_type: str
    allergies: str
