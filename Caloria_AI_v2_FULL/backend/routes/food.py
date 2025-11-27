# placeholder food
from fastapi import APIRouter, Depends, Form, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.database import get_db
from backend.models import User, FoodEntry
from backend.ai.text import analyze_food_text
from backend.ai.vision import analyze_food_photo
from backend.ai.whisper import transcribe_voice

import os, shutil, uuid

router = APIRouter(prefix="/api/food", tags=["Food"])


async def get_user(db, telegram_id):
    q = await db.execute(select(User).where(User.telegram_id == str(telegram_id)))
    return q.scalar_one_or_none()


@router.post("/add/text")
async def add_text_food(
    telegram_id: str = Form(...),
    text: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    user = await get_user(db, telegram_id)
    if not user:
        return {"error": "user_not_found"}

    ai = await analyze_food_text(text)

    entry = FoodEntry(
        user_id=user.id,
        text=text,
        calories=ai["calories"],
        protein=ai["protein"],
        fat=ai["fat"],
        carbs=ai["carbs"],
        food_type=ai["food_type"],
        ai_source="text"
    )

    db.add(entry)
    await db.commit()

    return {"status": "ok"}
