"""Terminal User Interface (TUI) for TaskPilotAI.

Provides an interactive menu-driven interface with a nice UI for managing tasks.
"""

import sys
from typing import Optional

from src import commands, storage


def clear_screen() -> None:
    """Clear the terminal screen."""
    import os

    os.system("clear" if os.name != "nt" else "cls")


def print_header() -> None:
    """Print application header."""
    print("\n" + "=" * 70)
    print("  " + "🎯 TASKPILOTAI - Interactive Task Manager".center(66))
    print("=" * 70 + "\n")


def print_menu() -> None:
    """Print main menu options."""
    print("📋 MAIN MENU")
    print("-" * 70)
    print("  1️⃣  Add New Task")
    print("  2️⃣  View All Tasks (Table)")
    print("  3️⃣  View All Tasks (JSON)")
    print("  4️⃣  View Pending Tasks")
    print("  5️⃣  View Completed Tasks")
    print("  6️⃣  Update Task")
    print("  7️⃣  Mark Task Complete/Pending")
    print("  8️⃣  Delete Task")
    print("  9️⃣  View Statistics")
    print("  0️⃣  Exit")
    print("-" * 70)


def get_menu_choice() -> str:
    """Get user menu choice."""
    return input("\n👉 Enter your choice (0-9): ").strip()


def display_tasks_table(tasks: list, title: str = "Tasks") -> None:
    """Display tasks in table format."""
    if not tasks:
        print(f"\n📭 {title}: No tasks found\n")
        return

    print(f"\n📌 {title}")
    print("-" * 70)

    # Header
    print(f"{'ID':<5} | {'Title':<25} | {'Status':<12} | {'Created':<15}")
    print("-" * 70)

    # Rows
    for task in tasks:
        status = "✅ Completed" if task["completed"] else "⏳ Pending"
        created_date = task["created_at"].split("T")[0]
        print(
            f"{task['id']:<5} | {task['title'][:25]:<25} | {status:<12} | "
            f"{created_date:<15}"
        )

    print("-" * 70 + "\n")


def add_task_ui() -> None:
    """Interactive UI for adding a task."""
    clear_screen()
    print_header()
    print("➕ ADD NEW TASK")
    print("-" * 70)

    try:
        title = input("📝 Enter task title (1-200 characters): ").strip()
        if not title:
            print("❌ Error: Title cannot be empty")
            input("\nPress Enter to continue...")
            return

        description = input(
            "📄 Enter task description (optional, max 1000 chars, press Enter to skip): "
        ).strip()

        task = commands.add_task(title, description)
        print("\n" + "=" * 70)
        print(f"✅ SUCCESS! Task {task['id']} added")
        print("-" * 70)
        print(f"  ID: {task['id']}")
        print(f"  Title: {task['title']}")
        print(f"  Description: {task['description'] if task['description'] else '(none)'}")
        print(f"  Status: ⏳ Pending")
        print(f"  Created: {task['created_at']}")
        print("=" * 70)

    except ValueError as e:
        print(f"\n❌ Error: {str(e)}")

    input("\nPress Enter to continue...")


def view_all_tasks_ui() -> None:
    """Interactive UI for viewing all tasks in table format."""
    clear_screen()
    print_header()

    try:
        tasks = commands.list_tasks("all")
        display_tasks_table(tasks, "📋 ALL TASKS")

    except ValueError as e:
        print(f"❌ Error: {str(e)}")

    input("Press Enter to continue...")


def view_all_tasks_json_ui() -> None:
    """Interactive UI for viewing all tasks in JSON format."""
    clear_screen()
    print_header()
    print("📋 ALL TASKS (JSON FORMAT)")
    print("-" * 70)

    try:
        tasks = commands.list_tasks("all")
        json_output = commands.format_json(tasks)
        print(json_output)

    except ValueError as e:
        print(f"❌ Error: {str(e)}")

    print("-" * 70)
    input("Press Enter to continue...")


def view_pending_tasks_ui() -> None:
    """Interactive UI for viewing pending tasks."""
    clear_screen()
    print_header()

    try:
        tasks = commands.list_tasks("pending")
        display_tasks_table(tasks, "⏳ PENDING TASKS")

    except ValueError as e:
        print(f"❌ Error: {str(e)}")

    input("Press Enter to continue...")


def view_completed_tasks_ui() -> None:
    """Interactive UI for viewing completed tasks."""
    clear_screen()
    print_header()

    try:
        tasks = commands.list_tasks("completed")
        display_tasks_table(tasks, "✅ COMPLETED TASKS")

    except ValueError as e:
        print(f"❌ Error: {str(e)}")

    input("Press Enter to continue...")


def update_task_ui() -> None:
    """Interactive UI for updating a task."""
    clear_screen()
    print_header()
    print("✏️  UPDATE TASK")
    print("-" * 70)

    try:
        # Show current tasks
        tasks = commands.list_tasks("all")
        if not tasks:
            print("❌ No tasks available to update")
            input("\nPress Enter to continue...")
            return

        display_tasks_table(tasks, "Current Tasks")

        task_id_str = input("🔢 Enter task ID to update: ").strip()
        task_id = int(task_id_str)

        new_title = input(
            "📝 Enter new title (press Enter to keep current): "
        ).strip()
        new_description = input(
            "📄 Enter new description (press Enter to keep current): "
        ).strip()

        if not new_title and not new_description:
            print("❌ Error: Please provide at least title or description")
            input("\nPress Enter to continue...")
            return

        updated_task = commands.update_task(
            task_id, new_title if new_title else None,
            new_description if new_description else None
        )

        print("\n" + "=" * 70)
        print(f"✅ SUCCESS! Task {task_id} updated")
        print("-" * 70)
        print(f"  ID: {updated_task['id']}")
        print(f"  Title: {updated_task['title']}")
        print(f"  Description: {updated_task['description'] if updated_task['description'] else '(none)'}")
        print(f"  Updated: {updated_task['updated_at']}")
        print("=" * 70)

    except ValueError as e:
        print(f"\n❌ Error: {str(e)}")
    except (ValueError, IndexError):
        print("❌ Error: Invalid task ID")

    input("\nPress Enter to continue...")


def mark_complete_ui() -> None:
    """Interactive UI for marking task complete/pending."""
    clear_screen()
    print_header()
    print("🎯 TOGGLE TASK STATUS")
    print("-" * 70)

    try:
        tasks = commands.list_tasks("all")
        if not tasks:
            print("❌ No tasks available")
            input("\nPress Enter to continue...")
            return

        display_tasks_table(tasks, "Current Tasks")

        task_id_str = input("🔢 Enter task ID to toggle: ").strip()
        task_id = int(task_id_str)

        updated_task = commands.mark_complete(task_id)
        new_status = "✅ Completed" if updated_task["completed"] else "⏳ Pending"

        print("\n" + "=" * 70)
        print(f"✅ SUCCESS! Task {task_id} status changed")
        print("-" * 70)
        print(f"  ID: {updated_task['id']}")
        print(f"  Title: {updated_task['title']}")
        print(f"  New Status: {new_status}")
        print(f"  Updated: {updated_task['updated_at']}")
        print("=" * 70)

    except ValueError as e:
        print(f"\n❌ Error: {str(e)}")

    input("\nPress Enter to continue...")


def delete_task_ui() -> None:
    """Interactive UI for deleting a task."""
    clear_screen()
    print_header()
    print("🗑️  DELETE TASK")
    print("-" * 70)

    try:
        tasks = commands.list_tasks("all")
        if not tasks:
            print("❌ No tasks available to delete")
            input("\nPress Enter to continue...")
            return

        display_tasks_table(tasks, "Current Tasks")

        task_id_str = input("🔢 Enter task ID to delete: ").strip()
        task_id = int(task_id_str)

        confirm = input(
            f"⚠️  Are you sure you want to delete task {task_id}? (yes/no): "
        ).strip().lower()

        if confirm != "yes":
            print("❌ Deletion cancelled")
            input("\nPress Enter to continue...")
            return

        commands.delete_task(task_id)

        print("\n" + "=" * 70)
        print(f"✅ SUCCESS! Task {task_id} deleted")
        print("=" * 70)

    except ValueError as e:
        print(f"\n❌ Error: {str(e)}")

    input("\nPress Enter to continue...")


def view_statistics_ui() -> None:
    """Interactive UI for viewing task statistics."""
    clear_screen()
    print_header()
    print("📊 TASK STATISTICS")
    print("-" * 70)

    try:
        all_tasks = commands.list_tasks("all")
        pending_tasks = commands.list_tasks("pending")
        completed_tasks = commands.list_tasks("completed")

        total = len(all_tasks)
        pending = len(pending_tasks)
        completed = len(completed_tasks)

        if total == 0:
            print("📭 No tasks yet")
        else:
            completion_percent = (completed / total * 100) if total > 0 else 0

            print(f"\n📈 Task Summary:")
            print(f"  Total Tasks:      {total}")
            print(f"  ⏳ Pending:       {pending}")
            print(f"  ✅ Completed:     {completed}")
            print(f"  Progress:         {completion_percent:.1f}% complete")

            # Progress bar
            filled = int(completion_percent / 10)
            bar = "█" * filled + "░" * (10 - filled)
            print(f"  [{bar}] {completion_percent:.0f}%")

            if pending_tasks:
                print(f"\n⏳ Pending Tasks:")
                for task in pending_tasks:
                    print(f"  • Task {task['id']}: {task['title']}")

    except ValueError as e:
        print(f"❌ Error: {str(e)}")

    print("-" * 70)
    input("\nPress Enter to continue...")


def main() -> int:
    """Main TUI loop."""
    while True:
        clear_screen()
        print_header()
        print_menu()

        choice = get_menu_choice()

        if choice == "1":
            add_task_ui()
        elif choice == "2":
            view_all_tasks_ui()
        elif choice == "3":
            view_all_tasks_json_ui()
        elif choice == "4":
            view_pending_tasks_ui()
        elif choice == "5":
            view_completed_tasks_ui()
        elif choice == "6":
            update_task_ui()
        elif choice == "7":
            mark_complete_ui()
        elif choice == "8":
            delete_task_ui()
        elif choice == "9":
            view_statistics_ui()
        elif choice == "0":
            clear_screen()
            print("\n" + "=" * 70)
            print("  " + "Thank you for using TaskPilotAI! 👋".center(66))
            print("=" * 70 + "\n")
            return 0
        else:
            print("❌ Invalid choice. Please enter 0-9")
            input("\nPress Enter to continue...")


if __name__ == "__main__":
    sys.exit(main())
