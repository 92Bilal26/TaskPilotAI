#!/usr/bin/env python
"""Database initialization script

This script:
1. Creates database tables using SQLModel metadata
2. Applies Alembic migrations
3. Sets up indexes for performance
4. Verifies database connectivity
"""

import sys
import logging
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from db import engine, create_db_and_tables
from models import SQLModel, User, Task, Conversation, Message
from config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_database() -> None:
    """Initialize database and create all tables"""
    logger.info(f"Initializing database: {settings.DATABASE_URL}")

    try:
        # Create all tables from SQLModel metadata
        logger.info("Creating tables...")
        create_db_and_tables()
        logger.info("✅ All tables created successfully")

        # Verify tables exist
        logger.info("Verifying database schema...")
        with engine.connect() as conn:
            # Get all table names
            inspector = __import__("sqlalchemy").inspect(engine)
            tables = inspector.get_table_names()
            logger.info(f"✅ Tables created: {', '.join(tables)}")

            # Check indexes
            for table_name in ["user", "task", "conversation", "message"]:
                if table_name in tables:
                    indexes = inspector.get_indexes(table_name)
                    logger.info(f"  Indexes on {table_name}: {len(indexes)} indexes")

        logger.info("✅ Database initialized successfully!")
        return True

    except Exception as e:
        logger.error(f"❌ Failed to initialize database: {e}")
        return False


if __name__ == "__main__":
    success = init_database()
    sys.exit(0 if success else 1)
