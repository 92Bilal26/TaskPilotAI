"""MCP Tool: Add Task

Handles creation of new tasks with validation and database persistence.
"""

import logging
from typing import Optional, Dict, Any
from sqlmodel import Session
from db import engine
from models import Task
import uuid
from datetime import datetime

logger = logging.getLogger(__name__)


def add_task(
    user_id: str,
    title: str,
    description: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Create a new task with the given title and optional description.

    Args:
        user_id: ID of the user creating the task
        title: Task title (required, 1-200 characters)
        description: Optional task description (max 1000 characters)

    Returns:
        Dictionary with:
        - task_id: Auto-assigned task ID
        - title: Task title (may be truncated if >200 chars)
        - description: Task description
        - completed: Task completion status (false by default)
        - created_at: ISO 8601 timestamp
        - message: Human-readable confirmation message

    Raises:
        ValueError: If validation fails
    """
    # Validate input
    if not title or not isinstance(title, str):
        raise ValueError("Error: Title is required and must be a string")

    title = title.strip()
    if not title:
        raise ValueError("Error: Title cannot be empty or whitespace only")

    if len(title) > 200:
        logger.info(f"Title truncated from {len(title)} to 200 characters")
        title = title[:200]

    if description:
        description = description.strip()
        if len(description) > 1000:
            logger.info(f"Description truncated from {len(description)} to 1000 characters")
            description = description[:1000]
    else:
        description = None

    try:
        # Create task object
        task = Task(
            id=str(uuid.uuid4()),
            user_id=user_id,
            title=title,
            description=description,
            completed=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        # Persist to database
        with Session(engine) as session:
            session.add(task)
            session.commit()
            session.refresh(task)

        logger.info(f"Task created: {task.id} for user {user_id}")

        return {
            "task_id": task.id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "created_at": task.created_at.isoformat(),
            "message": f"I've added '{task.title}' to your task list",
            "success": True,
        }

    except Exception as e:
        logger.error(f"Failed to create task: {e}")
        raise ValueError(f"Error: Failed to create task: {str(e)}")
