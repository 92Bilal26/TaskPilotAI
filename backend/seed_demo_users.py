#!/usr/bin/env python3
"""Seed demo users for testing"""

import sys
from sqlmodel import Session, create_engine, SQLModel, select
from bcrypt import hashpw, gensalt
from models import User, Task
from config import settings
from datetime import datetime

def hash_password(password: str) -> str:
    """Hash password using bcrypt directly"""
    return hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')

def seed_demo_users():
    """Create demo users in the database"""

    # Get database URL from config
    database_url = settings.DATABASE_URL
    engine = create_engine(database_url, connect_args={"check_same_thread": False} if "sqlite" in database_url else {})

    # Create all tables
    SQLModel.metadata.create_all(engine)

    demo_users = [
        {
            "email": "demo@example.com",
            "name": "Demo User",
            "password": "demo123"
        },
        {
            "email": "test@example.com",
            "name": "Test User",
            "password": "test123"
        },
        {
            "email": "admin@example.com",
            "name": "Admin User",
            "password": "admin123"
        }
    ]

    with Session(engine) as session:
        # Check if demo users already exist
        for demo_user in demo_users:
            statement = select(User).where(User.email == demo_user["email"])
            existing_user = session.exec(statement).first()
            if not existing_user:
                user = User(
                    email=demo_user["email"],
                    name=demo_user["name"],
                    password_hash=hash_password(demo_user["password"]),
                    emailVerified=True
                )
                session.add(user)
                print(f"✓ Created user: {demo_user['email']}")
            else:
                print(f"⊘ User already exists: {demo_user['email']}")

        session.commit()

    print("\n" + "="*60)
    print("DEMO USERS CREATED SUCCESSFULLY!")
    print("="*60)
    print("\nYou can now log in with:")
    print("\n1. Email: demo@example.com")
    print("   Password: demo123")
    print("\n2. Email: test@example.com")
    print("   Password: test123")
    print("\n3. Email: admin@example.com")
    print("   Password: admin123")
    print("\n" + "="*60)

if __name__ == "__main__":
    try:
        seed_demo_users()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
