# placeholder ai
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.database import get_db
from backend.models import User, FoodEntry
from backend.ai.tips import generate_tip

router = APIRouter(prefix="/api/ai", tags=["AI"])


@router.get("/tip/{telegram_id}")
async def ai_tip(telegram_id: str, db: AsyncSession = Depends(get_db)):

    user_q = await db.execute(select(User).where(User.telegram_id == telegram_id))
    user = user_q.scalar_one_or_none()

    if not user:
        return {"error": "user_not_found"}

    entries_q = await db.execute(select(FoodEntry).where(FoodEntry.user_id == user.id))
    entries = entries_q.scalars().all()

    stats = {
        "total_calories": sum(e.calories for e in entries),
        "total_protein": sum(e.protein for e in entries),
        "total_fat": sum(e.fat for e in entries),
        "total_carbs": sum(e.carbs for e in entries),
        "goal_calories": user.daily_calories,
        "goal_protein": user.daily_protein,
        "goal_fat": user.daily_fat,
        "goal_carbs": user.daily_carbs,
    }

    tip = await generate_tip(stats)
    return {"tip": tip}
