"""Pytest configuration and shared fixtures for TaskPilotAI tests."""

import pytest

from src import storage
from src.models import Task


@pytest.fixture
def empty_storage() -> None:
    """Reset storage to empty state before each test.

    Ensures test isolation - each test starts with clean storage.

    Yields:
        None
    """
    storage.reset_storage()
    yield
    storage.reset_storage()


@pytest.fixture
def sample_task(empty_storage) -> Task:
    """Create a single sample task for testing.

    Uses empty_storage fixture to ensure clean state.

    Returns:
        Task dict with id=1, title="Test Task", description="", completed=False
    """
    from datetime import datetime, timezone

    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    task: Task = {
        "id": 1,
        "title": "Test Task",
        "description": "",
        "completed": False,
        "created_at": now,
        "updated_at": now,
    }
    storage.tasks.append(task)
    storage.next_id = 2
    return task


@pytest.fixture
def sample_tasks(empty_storage) -> list[Task]:
    """Create multiple sample tasks with varied states for testing.

    Uses empty_storage fixture to ensure clean state.
    Creates 3 tasks with different statuses and properties.

    Returns:
        List of 3 Task dicts with varied properties
    """
    from datetime import datetime, timezone

    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    earlier = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    tasks_list: list[Task] = [
        {
            "id": 1,
            "title": "Buy groceries",
            "description": "Milk, eggs, bread",
            "completed": False,
            "created_at": now,
            "updated_at": now,
        },
        {
            "id": 2,
            "title": "Call mom",
            "description": "",
            "completed": True,
            "created_at": earlier,
            "updated_at": earlier,
        },
        {
            "id": 3,
            "title": "Fix authentication",
            "description": "OAuth setup and testing",
            "completed": False,
            "created_at": now,
            "updated_at": now,
        },
    ]
    storage.tasks.extend(tasks_list)
    storage.next_id = 4
    return tasks_list
