from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime

from backend.database import get_db
from backend.models import User, FoodEntry

router = APIRouter(prefix="/api/stats", tags=["Stats"])


@router.get("/today/{telegram_id}")
async def today_stats(telegram_id: str, db: AsyncSession = Depends(get_db)):

    uq = await db.execute(select(User).where(User.telegram_id == telegram_id))
    user = uq.scalar_one_or_none()
    if not user:
        return {"error": "user_not_found"}

    start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)

    fq = await db.execute(
        select(FoodEntry).where(
            FoodEntry.user_id == user.id,
            FoodEntry.created_at >= start,
        )
    )
    entries = fq.scalars().all()

    total = {
        "calories": sum(e.calories for e in entries),
        "protein": sum(e.protein for e in entries),
        "fat": sum(e.fat for e in entries),
        "carbs": sum(e.carbs for e in entries),
    }

    return {
        "entries": [
            {
                "text": e.text,
                "calories": e.calories,
                "protein": e.protein,
                "fat": e.fat,
                "carbs": e.carbs,
                "food_type": e.food_type,
            }
            for e in entries
        ],
        "total": total,
        "daily_goal_calories": user.daily_calories,
        "daily_goal_protein": user.daily_protein,
        "daily_goal_fat": user.daily_fat,
        "daily_goal_carbs": user.daily_carbs,
    }

