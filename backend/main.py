"""FastAPI application entry point"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from config import settings
from db import create_db_and_tables
from routes import auth, tasks, chat, chatkit
from middleware.auth import JWTAuthMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(
    title="TaskPilotAI",
    description="Full-stack task management application with AI Chatbot",
    version="3.0.0",
    lifespan=lifespan
)

# Add CORS middleware FIRST (will execute LAST in middleware chain)
# Ensure Vercel domain is always included
cors_origins = list(settings.CORS_ORIGINS) if isinstance(settings.CORS_ORIGINS, (list, tuple)) else settings.CORS_ORIGINS.split(",")
if "https://task-pilot-ai-ashen.vercel.app" not in cors_origins:
    cors_origins.append("https://task-pilot-ai-ashen.vercel.app")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add JWT middleware SECOND (will execute after CORS in middleware chain)
app.add_middleware(JWTAuthMiddleware)

app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(chat.router)
app.include_router(chatkit.router)

@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "TaskPilotAI API is running"}
