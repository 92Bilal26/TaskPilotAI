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
    OPENAI_API_KEY: str = "sk-test-key"  # Required for OpenAI integration
    CHATKIT_WORKFLOW_ID: str = "wf_6946b383d368819081b556e6e5fa66330d48d0c9ea4fccd8"  # OpenAI Agent Builder Workflow ID
    # ChatKit Configuration for Advanced Self-Hosted Integration
    CHATKIT_ENABLED: bool = True
    CHATKIT_SESSION_TIMEOUT: int = 3600  # 1 hour session timeout in seconds
    CHATKIT_MAX_HISTORY: int = 10  # Maximum conversation history messages to send to agent
    CHATKIT_DOMAIN_ALLOWLIST: List[str] = [
        "localhost:3000",
        "localhost:8000",
        "127.0.0.1:3000",
        "task-pilot-ai-ashen.vercel.app",
        "taskpilot-api-5l18.onrender.com"
    ]
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
