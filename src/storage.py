"""In-memory storage for TaskPilotAI tasks.

Provides module-level storage with auto-incrementing ID counter.
All data is lost on application restart (no persistence).
"""

from typing import List, Optional

from src.models import Task

# In-memory storage
tasks: List[Task] = []
next_id: int = 1


def get_task_by_id(task_id: int) -> Optional[Task]:
    """Get a task by its ID.

    Args:
        task_id: ID of the task to retrieve

    Returns:
        Task dict if found, None otherwise
    """
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None


def reset_storage() -> None:
    """Reset storage to empty state.

    Used for testing - clears all tasks and resets next_id.
    """
    global tasks, next_id
    tasks = []
    next_id = 1
