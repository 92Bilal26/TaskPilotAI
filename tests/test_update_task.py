"""Tests for update_task feature."""

import pytest

from src import commands, storage


class TestUpdateTask:
    """Test cases for update_task command."""

    def test_update_task_title_only(self, sample_task):
        """Test updating only task title."""
        task = commands.update_task(1, title="New Title")
        assert task["id"] == 1
        assert task["title"] == "New Title"
        assert task["description"] == ""
        assert task["completed"] is False
        assert task["updated_at"] != task["created_at"]

    def test_update_task_description_only(self, sample_task):
        """Test updating only task description."""
        task = commands.update_task(1, description="New Description")
        assert task["id"] == 1
        assert task["title"] == "Test Task"
        assert task["description"] == "New Description"
        assert task["completed"] is False
        assert task["updated_at"] != task["created_at"]

    def test_update_task_both_title_and_description(self, sample_task):
        """Test updating both title and description."""
        task = commands.update_task(1, title="New Title", description="New Desc")
        assert task["title"] == "New Title"
        assert task["description"] == "New Desc"

    def test_update_task_does_not_modify_id(self, sample_task):
        """Test that update does not change task ID."""
        original_id = 1
        task = commands.update_task(1, title="Updated")
        assert task["id"] == original_id

    def test_update_task_does_not_modify_completed(self, sample_task):
        """Test that update does not change completed status."""
        task = commands.update_task(1, title="Updated")
        assert task["completed"] is False

    def test_update_task_does_not_modify_created_at(self, sample_task):
        """Test that update does not change created_at timestamp."""
        original_created = storage.tasks[0]["created_at"]
        commands.update_task(1, title="Updated")
        assert storage.tasks[0]["created_at"] == original_created

    def test_update_task_updates_timestamp(self, sample_task):
        """Test that update changes updated_at timestamp."""
        original_updated = storage.tasks[0]["updated_at"]
        task = commands.update_task(1, title="Updated")
        assert task["updated_at"] != original_updated

    def test_update_nonexistent_task_raises_error(self, sample_task):
        """Test that updating non-existent task raises error."""
        with pytest.raises(ValueError, match="Task ID 999 not found"):
            commands.update_task(999, title="New Title")

    def test_update_task_zero_id_raises_error(self, sample_task):
        """Test that task ID 0 raises error."""
        with pytest.raises(ValueError, match="ID must be positive integer"):
            commands.update_task(0, title="New")

    def test_update_task_negative_id_raises_error(self, sample_task):
        """Test that negative task ID raises error."""
        with pytest.raises(ValueError, match="ID must be positive integer"):
            commands.update_task(-1, title="New")

    def test_update_task_no_fields_raises_error(self, sample_task):
        """Test that update with no fields raises error."""
        with pytest.raises(ValueError, match="At least one of --title or --description required"):
            commands.update_task(1)

    def test_update_task_title_too_long_raises_error(self, sample_task):
        """Test that title > 200 chars raises error."""
        long_title = "A" * 201
        with pytest.raises(ValueError, match="Title required \\(1-200 characters\\)"):
            commands.update_task(1, title=long_title)

    def test_update_task_title_empty_raises_error(self, sample_task):
        """Test that empty title raises error."""
        with pytest.raises(ValueError, match="Title required \\(1-200 characters\\)"):
            commands.update_task(1, title="")

    def test_update_task_title_whitespace_only_raises_error(self, sample_task):
        """Test that whitespace-only title raises error."""
        with pytest.raises(ValueError, match="Title required \\(1-200 characters\\)"):
            commands.update_task(1, title="   ")

    def test_update_task_description_too_long_raises_error(self, sample_task):
        """Test that description > 1000 chars raises error."""
        long_desc = "A" * 1001
        with pytest.raises(ValueError, match="Description max 1000 characters"):
            commands.update_task(1, description=long_desc)

    def test_update_task_with_special_characters(self, sample_task):
        """Test updating task with special characters."""
        task = commands.update_task(1, title="Buy 🛒 groceries!", description="🥛 🥚 🍞")
        assert task["title"] == "Buy 🛒 groceries!"
        assert task["description"] == "🥛 🥚 🍞"

    def test_update_task_with_newlines_in_description(self, sample_task):
        """Test updating task with newlines in description."""
        desc = "Line 1\nLine 2\nLine 3"
        task = commands.update_task(1, description=desc)
        assert task["description"] == desc

    def test_update_task_clears_description(self, empty_storage):
        """Test updating task to clear description."""
        task1 = commands.add_task("Task", "Original description")
        assert task1["description"] == "Original description"

        task2 = commands.update_task(1, description="")
        assert task2["description"] == ""

    def test_update_multiple_times_increments_timestamp(self, sample_task):
        """Test that multiple updates increment timestamp each time."""
        update1 = commands.update_task(1, title="Update 1")
        timestamp1 = update1["updated_at"]

        update2 = commands.update_task(1, title="Update 2")
        timestamp2 = update2["updated_at"]

        assert timestamp1 != timestamp2
        assert timestamp2 > timestamp1
