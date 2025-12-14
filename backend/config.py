"""Configuration management"""
from pydantic_settings import BaseSettings
from typing import List
import os
import json

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./taskpilot.db"
    JWT_SECRET: str = "dev-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRY_SECONDS: int = 604800
    JWT_REFRESH_EXPIRY_SECONDS: int = 1209600
    BETTER_AUTH_SECRET: str = "dev-secret-key"
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "https://task-pilot-ai-ashen.vercel.app",
        "https://taskpilot-api-5l18.onrender.com"
    ]
    ENVIRONMENT: str = "development"

    class Config:
        env_file = ".env"
        case_sensitive = False

    def __init__(self, **data):
        super().__init__(**data)
        # Parse CORS_ORIGINS if it's a JSON string
        if isinstance(self.CORS_ORIGINS, str):
            try:
                self.CORS_ORIGINS = json.loads(self.CORS_ORIGINS)
            except json.JSONDecodeError:
                self.CORS_ORIGINS = [self.CORS_ORIGINS]

settings = Settings()
