"""Data models and validation for TaskPilotAI.

Defines the Task entity and validation rules for all fields.
"""

from typing import List, Optional, TypedDict


class Task(TypedDict):
    """Task entity representing a todo item.

    Attributes:
        id: Auto-incremented unique identifier (starts at 1, never reused)
        title: Task title (1-200 characters, required)
        description: Task description (max 1000 characters, optional, default "")
        completed: Completion status (False=pending, True=completed)
        created_at: ISO 8601 UTC timestamp when task was created
        updated_at: ISO 8601 UTC timestamp when task was last modified
    """

    id: int
    title: str
    description: str
    completed: bool
    created_at: str
    updated_at: str


def validate_title(title: str) -> bool:
    """Validate task title.

    Title must be:
    - Non-empty and non-whitespace
    - Between 1 and 200 characters
    - Any UTF-8 characters allowed

    Args:
        title: Task title to validate

    Returns:
        True if valid, False otherwise
    """
    if not title or not title.strip():
        return False
    if len(title) < 1 or len(title) > 200:
        return False
    return True


def validate_description(description: Optional[str]) -> bool:
    """Validate task description.

    Description must be:
    - Optional (None or empty string allowed)
    - Max 1000 characters if provided
    - Any UTF-8 characters allowed

    Args:
        description: Task description to validate

    Returns:
        True if valid, False otherwise
    """
    if description is None:
        return True
    if len(description) <= 1000:
        return True
    return False


def validate_task_id(task_id: int, tasks: List[Task]) -> bool:
    """Validate task ID.

    ID must be:
    - Positive integer
    - Exist in current tasks list

    Args:
        task_id: Task ID to validate
        tasks: List of current tasks

    Returns:
        True if valid, False otherwise
    """
    if task_id <= 0:
        return False
    if not any(t["id"] == task_id for t in tasks):
        return False
    return True
