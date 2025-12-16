"""MCP Tool: Find Task by Name

Handles task lookup by title or partial title match.
"""

import logging
from typing import Dict, Any, Optional
from sqlmodel import Session, select
from db import engine
from models import Task

logger = logging.getLogger(__name__)


def find_task_by_name(
    user_id: str,
    name: str,
) -> Dict[str, Any]:
    """
    Find a task by its title (exact or partial match).

    Args:
        user_id: ID of the user
        name: Task title or partial title to search for

    Returns:
        Dictionary with:
        - task_id: ID of the found task
        - title: Title of the task
        - description: Task description if available
        - completed: Completion status
        - message: Human-readable result message

    Raises:
        ValueError: If task not found
    """
    if not name or not name.strip():
        raise ValueError("Error: Task name is required")

    name = name.strip().lower()

    try:
        with Session(engine) as session:
            # Query all tasks for the user
            query = select(Task).where(Task.user_id == user_id)
            tasks = session.exec(query).all()

            # Try exact match first
            for task in tasks:
                if task.title.lower() == name:
                    logger.info(f"Found exact task match for user {user_id}: {task.id}")
                    return {
                        "task_id": task.id,
                        "title": task.title,
                        "description": task.description,
                        "completed": task.completed,
                        "message": f"Found task: '{task.title}'",
                        "success": True,
                    }

            # Try partial match
            matching_tasks = [
                t for t in tasks
                if name in t.title.lower()
            ]

            if len(matching_tasks) == 1:
                task = matching_tasks[0]
                logger.info(f"Found partial task match for user {user_id}: {task.id}")
                return {
                    "task_id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "message": f"Found task: '{task.title}'",
                    "success": True,
                }
            elif len(matching_tasks) > 1:
                # Multiple matches found
                task_list = "\n".join([f"- {t.title}" for t in matching_tasks])
                raise ValueError(
                    f"Error: Found {len(matching_tasks)} tasks matching '{name}':\n{task_list}\n"
                    f"Please be more specific."
                )
            else:
                # No match found
                raise ValueError(f"Error: Task '{name}' not found. Check the task list.")

    except ValueError:
        raise
    except Exception as e:
        logger.error(f"Failed to find task: {e}")
        raise ValueError(f"Error: Failed to find task: {str(e)}")
