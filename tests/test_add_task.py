"""Tests for add_task feature."""

import pytest

from src import commands, storage


class TestAddTask:
    """Test cases for add_task command."""

    def test_add_task_with_title_only(self, empty_storage):
        """Test adding task with title only."""
        task = commands.add_task("Buy groceries")
        assert task["id"] == 1
        assert task["title"] == "Buy groceries"
        assert task["description"] == ""
        assert task["completed"] is False
        assert "created_at" in task
        assert "updated_at" in task
        assert task["created_at"] == task["updated_at"]
        assert len(storage.tasks) == 1
        assert storage.next_id == 2

    def test_add_task_with_title_and_description(self, empty_storage):
        """Test adding task with both title and description."""
        task = commands.add_task("Buy groceries", "Milk, eggs, bread")
        assert task["id"] == 1
        assert task["title"] == "Buy groceries"
        assert task["description"] == "Milk, eggs, bread"
        assert task["completed"] is False
        assert len(storage.tasks) == 1
        assert storage.next_id == 2

    def test_add_multiple_tasks_increments_id(self, empty_storage):
        """Test that IDs increment correctly for multiple tasks."""
        task1 = commands.add_task("Task 1")
        task2 = commands.add_task("Task 2")
        task3 = commands.add_task("Task 3")

        assert task1["id"] == 1
        assert task2["id"] == 2
        assert task3["id"] == 3
        assert storage.next_id == 4
        assert len(storage.tasks) == 3

    def test_add_task_never_reuses_ids_after_delete(self, empty_storage):
        """Test that deleted task IDs are never reused."""
        task1 = commands.add_task("Task 1")
        task2 = commands.add_task("Task 2")
        task3 = commands.add_task("Task 3")

        assert task1["id"] == 1
        assert task2["id"] == 2
        assert task3["id"] == 3

        # Delete task 2
        commands.delete_task(2)
        assert len(storage.tasks) == 2

        # Add new task - should get ID 4, not 2
        task4 = commands.add_task("Task 4")
        assert task4["id"] == 4
        assert storage.next_id == 5

    def test_add_task_with_empty_description_defaults_to_empty_string(self, empty_storage):
        """Test that empty description defaults to empty string."""
        task = commands.add_task("Task", "")
        assert task["description"] == ""

    def test_add_task_timestamps_format(self, empty_storage):
        """Test that timestamps are in ISO 8601 UTC format with Z suffix."""
        task = commands.add_task("Task")
        # Should be ISO 8601 format with Z suffix
        assert "T" in task["created_at"]
        assert "Z" in task["created_at"]
        assert task["created_at"].endswith("Z")
        assert task["updated_at"].endswith("Z")

    def test_add_task_title_min_length_valid(self, empty_storage):
        """Test adding task with minimum valid title length (1 char)."""
        task = commands.add_task("A")
        assert task["id"] == 1
        assert task["title"] == "A"

    def test_add_task_title_max_length_valid(self, empty_storage):
        """Test adding task with maximum valid title length (200 chars)."""
        title = "A" * 200
        task = commands.add_task(title)
        assert task["title"] == title

    def test_add_task_title_too_long_raises_error(self, empty_storage):
        """Test that title > 200 chars raises ValueError."""
        title = "A" * 201
        with pytest.raises(ValueError, match="Title required \\(1-200 characters\\)"):
            commands.add_task(title)

    def test_add_task_empty_title_raises_error(self, empty_storage):
        """Test that empty title raises ValueError."""
        with pytest.raises(ValueError, match="Title required \\(1-200 characters\\)"):
            commands.add_task("")

    def test_add_task_whitespace_only_title_raises_error(self, empty_storage):
        """Test that whitespace-only title raises ValueError."""
        with pytest.raises(ValueError, match="Title required \\(1-200 characters\\)"):
            commands.add_task("   ")

    def test_add_task_description_max_length_valid(self, empty_storage):
        """Test adding task with maximum valid description length (1000 chars)."""
        description = "A" * 1000
        task = commands.add_task("Task", description)
        assert task["description"] == description

    def test_add_task_description_too_long_raises_error(self, empty_storage):
        """Test that description > 1000 chars raises ValueError."""
        description = "A" * 1001
        with pytest.raises(ValueError, match="Description max 1000 characters"):
            commands.add_task("Task", description)

    def test_add_task_special_characters_in_title(self, empty_storage):
        """Test adding task with special characters in title."""
        title = "Buy 🛒 groceries! & veggies (fresh)"
        task = commands.add_task(title)
        assert task["title"] == title

    def test_add_task_special_characters_in_description(self, empty_storage):
        """Test adding task with special characters in description."""
        description = "Items: 🥛 🥚 🍞 & 🥬\nDue: 2025-12-07"
        task = commands.add_task("Task", description)
        assert task["description"] == description

    def test_add_task_with_newlines_in_description(self, empty_storage):
        """Test adding task with newlines in description."""
        description = "Line 1\nLine 2\nLine 3"
        task = commands.add_task("Task", description)
        assert task["description"] == description

    def test_add_task_is_stored_in_tasks_list(self, empty_storage):
        """Test that added task is actually stored in storage.tasks list."""
        task = commands.add_task("Task 1")
        assert len(storage.tasks) == 1
        assert storage.tasks[0]["id"] == task["id"]
        assert storage.tasks[0]["title"] == task["title"]

    def test_add_task_completed_always_false_initially(self, empty_storage):
        """Test that newly added tasks always have completed=False."""
        task = commands.add_task("Task")
        assert task["completed"] is False
