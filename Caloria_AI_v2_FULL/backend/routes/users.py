from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.database import get_db
from backend.models import User
from backend.schemas import UserRegister
from backend.utils import calculate_daily_norms

router = APIRouter(prefix="/api/users", tags=["Users"])


@router.post("/register")
async def register_user(data: UserRegister, db: AsyncSession = Depends(get_db)):

    q = await db.execute(select(User).where(User.telegram_id == data.telegram_id))
    user = q.scalar_one_or_none()

    if user:
        return {"status": "already_registered"}

    user = User(**data.dict())

    cal, p, f, c = calculate_daily_norms(user)
    user.daily_calories = cal
    user.daily_protein = p
    user.daily_fat = f
    user.daily_carbs = c

    db.add(user)
    await db.commit()
    await db.refresh(user)

    return {"status": "ok", "user_id": user.id}
