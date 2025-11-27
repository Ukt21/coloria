# placeholder models
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(String, unique=True)

    gender = Column(String)
    age = Column(Integer)
    weight = Column(Float)
    height = Column(Float)

    activity_level = Column(String)
    goal = Column(String)
    nutrition_type = Column(String)
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
    food_type = Column(String)
    ai_source = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="food_entries")
