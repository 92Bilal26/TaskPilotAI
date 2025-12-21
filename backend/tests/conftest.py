"""Pytest configuration and fixtures"""
import pytest
from sqlmodel import SQLModel
from db import engine, create_db_and_tables

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Create fresh database tables for testing"""
    # Drop all existing tables and recreate them
    SQLModel.metadata.drop_all(engine)
    create_db_and_tables()
    yield
    # Cleanup after tests
    SQLModel.metadata.drop_all(engine)
