from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(String, unique=True, index=True)

    gender = Column(String)
    age = Column(Integer)
    weight = Column(Float)
    height = Column(Float)

    activity_level = Column(String)  # low / medium / high
    goal = Column(String)            # lose / maintain / gain
    nutrition_type = Column(String)  # standard / sport / halal / vegan
    allergies = Column(Text)

    daily_calories = Column(Float)
    daily_protein = Column(Float)
    daily_fat = Column(Float)
    daily_carbs = Column(Float)

    created_at = Column(DateTime, default=datetime.utcnow)

    food_entries = relationship("FoodEntry", back_populates="user")


class FoodEntry(Base):
    __tablename__ = "food_entries"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    text = Column(Text)
    calories = Column(Float)
    protein = Column(Float)
    fat = Column(Float)
    carbs = Column(Float)
    food_type = Column(String)   # breakfast / lunch / dinner / snack
    ai_source = Column(String)   # text / photo / voice

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="food_entries")
