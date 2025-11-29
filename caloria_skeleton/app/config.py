
from pydantic import BaseSettings

class Settings(BaseSettings):
    BOT_TOKEN: str
    DATABASE_URL: str
    OPENAI_API_KEY: str = ""
    ADMINS: str = ""

    class Config:
        env_file = ".env"

settings = Settings()
