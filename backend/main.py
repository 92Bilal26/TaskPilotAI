"""FastAPI application entry point"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from config import settings
from db import create_db_and_tables
from routes import auth, tasks
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

# Add JWT middleware FIRST (will execute SECOND - after CORS)
app.add_middleware(JWTAuthMiddleware)

# Add CORS middleware LAST (will execute FIRST - before JWT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(tasks.router)
# Chat route will be added in Phase 2 (T028)

@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "TaskPilotAI API is running"}
