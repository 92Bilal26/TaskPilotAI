"""Tests for SQLModel models"""

import pytest
from models import User, Task


def test_user_creation():
    """Test creating a user"""
    user = User(email="test@example.com", name="Test User")
    assert user.email == "test@example.com"
    assert user.name == "Test User"
    assert user.emailVerified == False


def test_task_creation():
    """Test creating a task"""
    user = User(id="user123", email="test@example.com", name="Test User")
    task = Task(user_id="user123", title="Test Task")
    assert task.title == "Test Task"
    assert task.user_id == "user123"
    assert task.completed == False
