"""CLI entry point for TaskPilotAI.

Handles argument parsing and command dispatch for all 5 features:
- add: Create new task
- delete: Remove task by ID
- update: Modify task title and/or description
- list: Display tasks (filtered by status, table or JSON)
- complete: Toggle task completion status
"""

import argparse
import sys
from typing import Optional

from src import commands


def parse_args(args: list[str]) -> argparse.Namespace:
    """Parse command-line arguments.

    Args:
        args: Command-line arguments (typically sys.argv[1:])

    Returns:
        Parsed arguments as Namespace
    """
    parser = argparse.ArgumentParser(description="TaskPilotAI - In-memory todo app")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("--title", required=True, help="Task title (required)")
    add_parser.add_argument(
        "--description", default="", help="Task description (optional)"
    )

    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("--id", type=int, required=True, help="Task ID")

    # Update command
    update_parser = subparsers.add_parser("update", help="Update a task")
    update_parser.add_argument("--id", type=int, required=True, help="Task ID")
    update_parser.add_argument("--title", help="New task title (optional)")
    update_parser.add_argument("--description", help="New task description (optional)")

    # List command
    list_parser = subparsers.add_parser("list", help="List all tasks")
    list_parser.add_argument(
        "--status",
        default="all",
        choices=["pending", "completed", "all"],
        help="Filter by status (optional, default: all)",
    )
    list_parser.add_argument(
        "--json", action="store_true", help="Output as JSON (optional)"
    )

    # Complete command
    complete_parser = subparsers.add_parser("complete", help="Toggle task completion")
    complete_parser.add_argument("--id", type=int, required=True, help="Task ID")

    return parser.parse_args(args)


def handle_add(args: argparse.Namespace) -> int:
    """Handle 'add' command.

    Args:
        args: Parsed arguments with title and description

    Returns:
        Exit code (0 success, 1 error)
    """
    try:
        title: str = args.title
        description: str = args.description if hasattr(args, "description") else ""

        task = commands.add_task(title, description)
        print(f"Task {task['id']} added: {task['title']}")
        return 0
    except ValueError as e:
        print(f"Error: {str(e)}")
        return 1
    except Exception:
        print("Error: Unexpected error occurred")
        return 2


def handle_delete(args: argparse.Namespace) -> int:
    """Handle 'delete' command.

    Args:
        args: Parsed arguments with task ID

    Returns:
        Exit code (0 success, 1 error)
    """
    try:
        task_id: int = args.id
        if task_id <= 0:
            print("Error: ID must be positive integer")
            return 1

        commands.delete_task(task_id)
        print(f"Task {task_id} deleted")
        return 0
    except ValueError as e:
        print(f"Error: {str(e)}")
        return 1
    except Exception:
        print("Error: Unexpected error occurred")
        return 2


def handle_update(args: argparse.Namespace) -> int:
    """Handle 'update' command.

    Args:
        args: Parsed arguments with task ID, title, description

    Returns:
        Exit code (0 success, 1 error)
    """
    try:
        task_id: int = args.id
        if task_id <= 0:
            print("Error: ID must be positive integer")
            return 1

        title: Optional[str] = getattr(args, "title", None)
        description: Optional[str] = getattr(args, "description", None)

        commands.update_task(task_id, title, description)
        print(f"Task {task_id} updated")
        return 0
    except ValueError as e:
        print(f"Error: {str(e)}")
        return 1
    except Exception:
        print("Error: Unexpected error occurred")
        return 2


def handle_list(args: argparse.Namespace) -> int:
    """Handle 'list' command.

    Args:
        args: Parsed arguments with status and json flags

    Returns:
        Exit code (0 success even if empty, 1 error)
    """
    try:
        status: str = getattr(args, "status", "all")
        output_json: bool = getattr(args, "json", False)

        tasks = commands.list_tasks(status)

        if output_json:
            print(commands.format_json(tasks))
        else:
            print(commands.format_table(tasks))

        return 0
    except ValueError as e:
        print(f"Error: {str(e)}")
        return 1
    except Exception:
        print("Error: Unexpected error occurred")
        return 2


def handle_complete(args: argparse.Namespace) -> int:
    """Handle 'complete' command.

    Args:
        args: Parsed arguments with task ID

    Returns:
        Exit code (0 success, 1 error)
    """
    try:
        task_id: int = args.id
        if task_id <= 0:
            print("Error: ID must be positive integer")
            return 1

        task = commands.mark_complete(task_id)
        status_str = "completed" if task["completed"] else "pending"
        print(f"Task {task_id} marked as {status_str}")
        return 0
    except ValueError as e:
        print(f"Error: {str(e)}")
        return 1
    except Exception:
        print("Error: Unexpected error occurred")
        return 2


def main(args: Optional[list[str]] = None) -> int:
    """Main entry point for TaskPilotAI CLI.

    Args:
        args: Command-line arguments (default: sys.argv[1:])

    Returns:
        Exit code (0 success, 1 error, 2 system error)
    """
    if args is None:
        args = sys.argv[1:]

    if not args:
        print("Usage: python -m src.main <command> [options]")
        print("Commands: add, delete, update, list, complete")
        return 1

    try:
        parsed_args = parse_args(args)
    except SystemExit:
        return 1

    if not hasattr(parsed_args, "command") or parsed_args.command is None:
        print("Usage: python -m src.main <command> [options]")
        print("Commands: add, delete, update, list, complete")
        return 1

    command = parsed_args.command

    if command == "add":
        return handle_add(parsed_args)
    elif command == "delete":
        return handle_delete(parsed_args)
    elif command == "update":
        return handle_update(parsed_args)
    elif command == "list":
        return handle_list(parsed_args)
    elif command == "complete":
        return handle_complete(parsed_args)
    else:
        print(f"Error: Unknown command '{command}'")
        return 1


if __name__ == "__main__":
    sys.exit(main())
