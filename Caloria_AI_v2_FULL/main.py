import os
import asyncio
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from backend.database import Base, engine
from backend.routes.users import router as users_router
from backend.routes.food import router as food_router
from backend.routes.stats import router as stats_router
from backend.routes.ai import router as ai_router

from bot.main_bot import run_telegram_bot


app = FastAPI(
    title="Caloria AI v2",
    description="AI-powered nutrition tracker",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_credentials=True,
    allow_headers=["*"],
)

app.include_router(users_router)
app.include_router(food_router)
app.include_router(stats_router)
app.include_router(ai_router)

app.mount("/webapp", StaticFiles(directory="webapp"), name="webapp")


@app.get("/")
async def root():
    return {"status": "ok", "app": "Caloria AI v2"}


@app.get("/webapp")
async def webapp_index():
    return FileResponse("webapp/index.html")


@app.on_event("startup")
async def startup():
    print("🚀 Starting Caloria AI v2...")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("📦 Database ready")

    print("🤖 Starting Telegram Bot...")
    asyncio.create_task(run_telegram_bot())
    print("🤖 Bot polling started")


def start():
    import uvicorn
    port = int(os.getenv("PORT", 10000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)


if __name__ == "__main__":
    start()

