"""Database configuration"""
from sqlalchemy.pool import QueuePool
from sqlmodel import SQLModel, create_engine, Session
from contextlib import contextmanager
from config import settings

engine = create_engine(
    settings.DATABASE_URL,
    echo=False,
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

@contextmanager
def get_db_session():
    with Session(engine) as session:
        yield session
