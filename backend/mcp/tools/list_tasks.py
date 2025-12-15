"""MCP Tool: List Tasks

Handles retrieval of tasks with optional filtering by status.
"""

import logging
from typing import Optional, Dict, Any, List
from sqlmodel import Session, select
from db import engine
from models import Task

logger = logging.getLogger(__name__)


def list_tasks(
    user_id: str,
    status: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Retrieve tasks for a user with optional filtering.

    Args:
        user_id: ID of the user
        status: Filter by status ('all', 'pending', 'completed')
                Default is 'all'

    Returns:
        Dictionary with:
        - tasks: List of task objects
        - total: Total number of tasks
        - pending: Count of pending tasks
        - completed: Count of completed tasks
        - message: Human-readable summary message
    """
    # Normalize status filter
    if status:
        status = status.lower().strip()
    if status not in ('all', 'pending', 'completed', None):
        raise ValueError(
            f"Error: Invalid status '{status}'. Must be 'all', 'pending', or 'completed'"
        )

    default_status = 'all' if not status else status

    try:
        # Query tasks for user
        with Session(engine) as session:
            query = select(Task).where(Task.user_id == user_id)

            if default_status == 'pending':
                query = query.where(Task.completed == False)
            elif default_status == 'completed':
                query = query.where(Task.completed == True)

            # Order by creation date (newest first)
            query = query.order_by(Task.created_at.desc())

            tasks = session.exec(query).all()

        # Count totals
        all_tasks = session.exec(
            select(Task).where(Task.user_id == user_id)
        ).all()
        total = len(all_tasks)
        pending_count = len([t for t in all_tasks if not t.completed])
        completed_count = len([t for t in all_tasks if t.completed])

        # Format response
        task_list = [
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "created_at": task.created_at.isoformat(),
            }
            for task in tasks
        ]

        # Generate message based on status
        if len(task_list) == 0:
            if default_status == 'pending':
                message = "You have no pending tasks! 🎉"
            elif default_status == 'completed':
                message = "You have no completed tasks yet."
            else:
                message = "You don't have any tasks yet. Want to create one?"
        else:
            status_label = default_status if default_status != 'all' else 'total'
            message = f"You have {len(task_list)} {status_label} task(s)"

        logger.info(
            f"Retrieved {len(task_list)} tasks for user {user_id} "
            f"(status={default_status})"
        )

        return {
            "tasks": task_list,
            "total": total,
            "pending": pending_count,
            "completed": completed_count,
            "filtered_status": default_status,
            "message": message,
            "success": True,
        }

    except ValueError:
        raise
    except Exception as e:
        logger.error(f"Failed to list tasks: {e}")
        raise ValueError(f"Error: Failed to retrieve tasks: {str(e)}")
