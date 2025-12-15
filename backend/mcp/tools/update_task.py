"""MCP Tool: Update Task

Handles modification of task title and/or description.
"""

import logging
from typing import Dict, Any, Optional
from sqlmodel import Session
from db import engine
from models import Task
from datetime import datetime

logger = logging.getLogger(__name__)


def update_task(
    user_id: str,
    task_id: str,
    title: Optional[str] = None,
    description: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Update a task's title and/or description.

    Args:
        user_id: ID of the user
        task_id: ID of the task to update
        title: New task title (optional, max 200 chars)
        description: New task description (optional, max 1000 chars)

    Returns:
        Dictionary with:
        - task_id: The task ID
        - title: Updated task title
        - description: Updated task description
        - updated_at: ISO 8601 timestamp
        - message: Human-readable confirmation message

    Raises:
        ValueError: If validation fails or user not authorized
    """
    if not task_id:
        raise ValueError("Error: Task ID is required")

    if not title and not description:
        raise ValueError(
            "Error: At least one of title or description must be provided"
        )

    try:
        with Session(engine) as session:
            # Find task
            task = session.get(Task, task_id)

            if not task:
                raise ValueError(f"Error: Task '{task_id}' not found")

            # Verify user owns the task
            if task.user_id != user_id:
                raise ValueError("Error: Not authorized to modify this task")

            # Update title if provided
            if title is not None:
                title = title.strip()
                if not title:
                    raise ValueError("Error: Title cannot be empty")
                if len(title) > 200:
                    logger.info(f"Title truncated from {len(title)} to 200 characters")
                    title = title[:200]
                task.title = title

            # Update description if provided
            if description is not None:
                description = description.strip()
                if len(description) > 1000:
                    logger.info(
                        f"Description truncated from {len(description)} to 1000 characters"
                    )
                    description = description[:1000]
                # Allow empty description
                task.description = description if description else None

            # Update timestamp
            task.updated_at = datetime.utcnow()

            session.add(task)
            session.commit()
            session.refresh(task)

            # Generate message
            updates = []
            if title is not None:
                updates.append(f"title to '{task.title}'")
            if description is not None:
                desc_display = task.description[:50] + "..." if task.description and len(task.description) > 50 else task.description or "(empty)"
                updates.append(f"description to '{desc_display}'")

            message = f"I've updated the task {' and '.join(updates)}"

            logger.info(f"Task {task_id} updated for user {user_id}")

            return {
                "task_id": task.id,
                "title": task.title,
                "description": task.description,
                "updated_at": task.updated_at.isoformat(),
                "message": message,
                "success": True,
            }

    except ValueError:
        raise
    except Exception as e:
        logger.error(f"Failed to update task: {e}")
        raise ValueError(f"Error: Failed to update task: {str(e)}")
