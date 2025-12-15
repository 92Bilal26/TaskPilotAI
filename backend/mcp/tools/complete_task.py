"""MCP Tool: Complete Task

Handles toggling task completion status.
"""

import logging
from typing import Dict, Any
from sqlmodel import Session
from db import engine
from models import Task
from datetime import datetime

logger = logging.getLogger(__name__)


def complete_task(
    user_id: str,
    task_id: str,
) -> Dict[str, Any]:
    """
    Toggle task completion status (mark complete or uncomplete).

    Args:
        user_id: ID of the user
        task_id: ID of the task to complete

    Returns:
        Dictionary with:
        - task_id: The task ID
        - title: Task title
        - completed: New completion status
        - updated_at: ISO 8601 timestamp
        - message: Human-readable confirmation message

    Raises:
        ValueError: If task not found or user not authorized
    """
    if not task_id:
        raise ValueError("Error: Task ID is required")

    try:
        with Session(engine) as session:
            # Find task
            task = session.get(Task, task_id)

            if not task:
                raise ValueError(f"Error: Task '{task_id}' not found")

            # Verify user owns the task
            if task.user_id != user_id:
                raise ValueError("Error: Not authorized to modify this task")

            # Toggle completion status
            was_completed = task.completed
            task.completed = not task.completed
            task.updated_at = datetime.utcnow()

            session.add(task)
            session.commit()
            session.refresh(task)

            # Generate message
            if task.completed:
                message = f"I've marked '{task.title}' as complete! ✓"
            else:
                message = f"I've marked '{task.title}' as pending again."

            logger.info(
                f"Task {task_id} completion toggled: {was_completed} → {task.completed}"
            )

            return {
                "task_id": task.id,
                "title": task.title,
                "completed": task.completed,
                "updated_at": task.updated_at.isoformat(),
                "message": message,
                "success": True,
            }

    except ValueError:
        raise
    except Exception as e:
        logger.error(f"Failed to complete task: {e}")
        raise ValueError(f"Error: Failed to update task: {str(e)}")
