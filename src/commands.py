"""Command handlers for TaskPilotAI features.

Implements the 5 core operations: add, delete, update, list, complete.
"""

import json
from datetime import datetime, timezone
from typing import List, Optional

from src import storage
from src.models import Task, validate_description, validate_task_id, validate_title


def add_task(title: str, description: str = "") -> Task:
    """Add a new task to storage.

    Validates title and description, creates task with auto-incremented ID,
    sets timestamps to current UTC time, and stores in memory.

    Args:
        title: Task title (1-200 characters, required)
        description: Task description (max 1000 characters, optional)

    Returns:
        Task dict with id, title, description, completed=False, timestamps

    Raises:
        ValueError: If title or description validation fails
    """
    if not validate_title(title):
        raise ValueError("Title required (1-200 characters)")
    if not validate_description(description):
        raise ValueError("Description max 1000 characters")

    current_time = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    task: Task = {
        "id": storage.next_id,
        "title": title,
        "description": description if description else "",
        "completed": False,
        "created_at": current_time,
        "updated_at": current_time,
    }

    storage.tasks.append(task)
    storage.next_id += 1

    return task


def delete_task(task_id: int) -> bool:
    """Delete a task from storage by ID.

    Validates task exists, removes it from storage, never reuses IDs.

    Args:
        task_id: ID of task to delete

    Returns:
        True if deletion successful

    Raises:
        ValueError: If task ID not found or invalid
    """
    if task_id <= 0:
        raise ValueError("ID must be positive integer")

    if not validate_task_id(task_id, storage.tasks):
        raise ValueError(f"Task ID {task_id} not found")

    storage.tasks[:] = [t for t in storage.tasks if t["id"] != task_id]
    return True


def update_task(
    task_id: int, title: Optional[str] = None, description: Optional[str] = None
) -> Task:
    """Update a task's title and/or description.

    Validates task exists, validates new field values, updates only provided fields,
    updates timestamp to current UTC time.

    Args:
        task_id: ID of task to update
        title: New task title (1-200 characters, optional)
        description: New task description (max 1000 characters, optional)

    Returns:
        Updated Task dict

    Raises:
        ValueError: If task not found, validation fails, or no fields to update
    """
    if task_id <= 0:
        raise ValueError("ID must be positive integer")

    if not validate_task_id(task_id, storage.tasks):
        raise ValueError(f"Task ID {task_id} not found")

    if title is None and description is None:
        raise ValueError("At least one of --title or --description required")

    if title is not None and not validate_title(title):
        raise ValueError("Title required (1-200 characters)")

    if description is not None and not validate_description(description):
        raise ValueError("Description max 1000 characters")

    for task in storage.tasks:
        if task["id"] == task_id:
            if title is not None:
                task["title"] = title
            if description is not None:
                task["description"] = description
            task["updated_at"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
            return task

    raise ValueError(f"Task ID {task_id} not found")


def list_tasks(status: str = "all") -> List[Task]:
    """Get filtered list of tasks.

    Filters by completion status: pending (False), completed (True), or all.

    Args:
        status: Filter status - "pending", "completed", or "all" (default)

    Returns:
        List of Task dicts matching filter

    Raises:
        ValueError: If status value invalid
    """
    if status not in ("pending", "completed", "all"):
        raise ValueError("Invalid status. Use: all, pending, completed")

    if status == "pending":
        return [t for t in storage.tasks if not t["completed"]]
    elif status == "completed":
        return [t for t in storage.tasks if t["completed"]]
    else:
        return storage.tasks.copy()


def format_table(tasks: List[Task]) -> str:
    """Format tasks as human-readable table.

    Table format: ID | Title | Status | Created

    Args:
        tasks: List of Task dicts to format

    Returns:
        Formatted table string, or "No tasks" if empty
    """
    if not tasks:
        return "No tasks"

    # Calculate column widths
    max_id_width = max(len(str(t["id"])) for t in tasks) if tasks else 2
    max_title_width = max(len(t["title"]) for t in tasks) if tasks else 5
    max_status_width = max(len("pending"), len("completed"))

    id_width = max(max_id_width, 2)  # At least "ID"
    title_width = max(max_title_width, 5)  # At least "Title"
    status_width = max(max_status_width, 6)  # At least "Status"

    # Build header
    header = (
        f"ID{' ' * (id_width - 2)} | "
        f"Title{' ' * (title_width - 5)} | "
        f"Status{' ' * (status_width - 6)} | "
        f"Created"
    )

    # Build rows
    rows = [header]
    for task in tasks:
        status_str = "completed" if task["completed"] else "pending"
        created_date = task["created_at"].split("T")[0]  # Extract YYYY-MM-DD
        row = (
            f"{task['id']}{' ' * (id_width - len(str(task['id'])))} | "
            f"{task['title']}{' ' * (title_width - len(task['title']))} | "
            f"{status_str}{' ' * (status_width - len(status_str))} | "
            f"{created_date}"
        )
        rows.append(row)

    return "\n".join(rows)


def format_json(tasks: List[Task]) -> str:
    """Format tasks as JSON array.

    Args:
        tasks: List of Task dicts to format

    Returns:
        JSON string representation of tasks
    """
    return json.dumps(tasks, indent=2)


def mark_complete(task_id: int) -> Task:
    """Toggle task completion status (pending ↔ completed).

    Validates task exists, toggles completed status, updates timestamp.

    Args:
        task_id: ID of task to toggle

    Returns:
        Updated Task dict

    Raises:
        ValueError: If task ID not found or invalid
    """
    if task_id <= 0:
        raise ValueError("ID must be positive integer")

    if not validate_task_id(task_id, storage.tasks):
        raise ValueError(f"Task ID {task_id} not found")

    for task in storage.tasks:
        if task["id"] == task_id:
            task["completed"] = not task["completed"]
            task["updated_at"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
            return task

    raise ValueError(f"Task ID {task_id} not found")
