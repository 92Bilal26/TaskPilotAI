"""MCP Tool: Delete Task

Handles permanent removal of tasks from the database.
"""

import logging
from typing import Dict, Any
from sqlmodel import Session
from db import engine
from models import Task

logger = logging.getLogger(__name__)


def delete_task(
    user_id: str,
    task_id: str,
) -> Dict[str, Any]:
    """
    Permanently delete a task.

    Args:
        user_id: ID of the user
        task_id: ID of the task to delete

    Returns:
        Dictionary with:
        - task_id: The deleted task ID
        - title: Title of the deleted task
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
                raise ValueError("Error: Not authorized to delete this task")

            # Store title before deletion
            task_title = task.title

            # Delete task
            session.delete(task)
            session.commit()

            message = f"I've removed '{task_title}' from your task list"

            logger.info(f"Task {task_id} deleted for user {user_id}")

            return {
                "task_id": task_id,
                "title": task_title,
                "message": message,
                "success": True,
            }

    except ValueError:
        raise
    except Exception as e:
        logger.error(f"Failed to delete task: {e}")
        raise ValueError(f"Error: Failed to delete task: {str(e)}")
