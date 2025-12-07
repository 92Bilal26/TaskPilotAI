"""Configuration management"""
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/taskpilot"
    JWT_SECRET: str = "your-secret-key"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRY_SECONDS: int = 604800
    JWT_REFRESH_EXPIRY_SECONDS: int = 1209600
    BETTER_AUTH_SECRET: str = "auth-secret"
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    ENVIRONMENT: str = "development"

    class Config:
        env_file = ".env"

settings = Settings()
