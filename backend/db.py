from sqlmodel import create_engine, Session, SQLModel
from sqlalchemy.pool import QueuePool
from .config import settings
import logging

logger = logging.getLogger(__name__)

engine = create_engine(
    settings.DATABASE_URL,
    echo=False,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    logger.info("Database tables initialized")

def get_session():
    with Session(engine) as session:
        yield session