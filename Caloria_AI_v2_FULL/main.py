
import os
import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from backend.database import Base, engine
from backend.routes.users import router as users_router
from backend.routes.food import router as food_router
from backend.routes.stats import router as stats_router
from backend.routes.ai import router as ai_router

from bot.main_bot import run_telegram_bot

app = FastAPI(title="Caloria AI")


# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # при желании ограничишь
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Роутеры ---
app.include_router(users_router, prefix="/api/users", tags=["users"])
app.include_router(food_router, prefix="/api/food", tags=["food"])
app.include_router(stats_router, prefix="/api/stats", tags=["stats"])
app.include_router(ai_router, prefix="/api/ai", tags=["ai"])


# --- Старт приложения: БД + бот ---
@app.on_event("startup")
async def on_startup():
    # если у тебя уже есть миграции через Alembic и таблицы созданы —
    # эту часть можно убрать
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # запускаем телеграм-бота в фоне
    asyncio.create_task(run_telegram_bot())


# --- Статический фронтенд (если есть сборка) ---
if os.path.isdir("frontend/dist"):
    app.mount("/static", StaticFiles(directory="frontend/dist/assets"), name="static")

    @app.get("/")
    async def serve_frontend():
        return FileResponse("frontend/dist/index.html")


# --- Точка входа для Render: python main.py ---
if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("main:app", host="0.0.0.0", port=port)

