"""FastAPI main application for TaskPilotAI Phase 2"""

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from config import settings
from db import create_db_and_tables, get_session
from middleware.auth import JWTAuthMiddleware

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager"""
    create_db_and_tables()
    logger.info("Application started")
    yield
    logger.info("Application shutdown")


app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(JWTAuthMiddleware)


class APIResponse:
    """Standardized API response"""

    @staticmethod
    def success(data=None, message="Success"):
        return {"success": True, "data": data, "message": message}

    @staticmethod
    def error(message="Error", status_code=400):
        return {"success": False, "error": message, "status_code": status_code}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
