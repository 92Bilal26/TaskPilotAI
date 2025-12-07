from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://localhost/taskpilot")
    JWT_SECRET: str = os.getenv("JWT_SECRET", "dev-secret")
    JWT_ALGORITHM: str = "HS256"
    CORS_ORIGINS: list = ["http://localhost:3000"]
    class Config:
        env_file = ".env"

settings = Settings()