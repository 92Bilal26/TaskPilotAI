"""Tests for view_tasks (list_tasks) feature."""

import json

import pytest

from src import commands


class TestListTasks:
    """Test cases for list_tasks command."""

    def test_list_all_tasks(self, sample_tasks):
        """Test listing all tasks."""
        tasks = commands.list_tasks("all")
        assert len(tasks) == 3
        assert any(t["id"] == 1 for t in tasks)
        assert any(t["id"] == 2 for t in tasks)
        assert any(t["id"] == 3 for t in tasks)

    def test_list_default_status_is_all(self, sample_tasks):
        """Test that default status is 'all'."""
        tasks_default = commands.list_tasks()
        tasks_all = commands.list_tasks("all")
        assert tasks_default == tasks_all
        assert len(tasks_default) == 3

    def test_list_pending_tasks_only(self, sample_tasks):
        """Test listing only pending tasks."""
        tasks = commands.list_tasks("pending")
        assert len(tasks) == 2
        assert all(not t["completed"] for t in tasks)
        task_ids = [t["id"] for t in tasks]
        assert 1 in task_ids
        assert 3 in task_ids

    def test_list_completed_tasks_only(self, sample_tasks):
        """Test listing only completed tasks."""
        tasks = commands.list_tasks("completed")
        assert len(tasks) == 1
        assert all(t["completed"] for t in tasks)
        assert tasks[0]["id"] == 2

    def test_list_empty_tasks_returns_empty_list(self, empty_storage):
        """Test listing tasks when storage is empty."""
        tasks = commands.list_tasks()
        assert tasks == []

    def test_list_invalid_status_raises_error(self, sample_tasks):
        """Test that invalid status raises error."""
        with pytest.raises(ValueError, match="Invalid status. Use: all, pending, completed"):
            commands.list_tasks("invalid")

    def test_list_pending_when_all_completed(self, empty_storage):
        """Test listing pending tasks when all are completed."""
        commands.add_task("Task 1")
        task = commands.add_task("Task 2")
        commands.mark_complete(task["id"])
        commands.mark_complete(1)

        pending = commands.list_tasks("pending")
        assert len(pending) == 0

    def test_list_completed_when_all_pending(self, empty_storage):
        """Test listing completed tasks when all are pending."""
        commands.add_task("Task 1")
        commands.add_task("Task 2")

        completed = commands.list_tasks("completed")
        assert len(completed) == 0

    def test_list_does_not_modify_storage(self, sample_tasks):
        """Test that listing tasks does not modify storage."""
        original_count = len(commands.list_tasks())
        commands.list_tasks("pending")
        commands.list_tasks("completed")
        final_count = len(commands.list_tasks())
        assert original_count == final_count


class TestFormatTable:
    """Test cases for format_table function."""

    def test_format_empty_table(self, empty_storage):
        """Test formatting empty task list."""
        output = commands.format_table([])
        assert output == "No tasks"

    def test_format_table_single_task(self, sample_task):
        """Test formatting single task as table."""
        from src import storage

        output = commands.format_table(storage.tasks)
        assert "ID" in output
        assert "Title" in output
        assert "Status" in output
        assert "Created" in output
        assert "Test Task" in output
        assert "pending" in output

    def test_format_table_multiple_tasks(self, sample_tasks):
        """Test formatting multiple tasks as table."""
        from src import storage

        output = commands.format_table(storage.tasks)
        assert "Buy groceries" in output
        assert "Call mom" in output
        assert "Fix authentication" in output
        assert "completed" in output
        assert output.count("pending") == 2
        assert output.count("completed") == 1

    def test_format_table_shows_date_only(self, sample_tasks):
        """Test that table shows date only (not full timestamp)."""
        from src import storage

        output = commands.format_table(storage.tasks)
        # Should show YYYY-MM-DD format
        assert "2025-12-07" in output or "2025-12-06" in output
        # Should not show time portion (HH:MM:SS)
        lines = output.split("\n")
        for line in lines[1:]:  # Skip header
            if "2025" in line:
                date_part = line.split("|")[-1].strip()
                assert ":" not in date_part  # No time portion

    def test_format_table_alignment(self, sample_tasks):
        """Test that table has proper column alignment."""
        from src import storage

        output = commands.format_table(storage.tasks)
        lines = output.split("\n")
        # All lines should have consistent pipe separators
        pipe_counts = [line.count("|") for line in lines]
        assert len(set(pipe_counts)) == 1  # All lines have same number of pipes


class TestFormatJson:
    """Test cases for format_json function."""

    def test_format_empty_json(self, empty_storage):
        """Test formatting empty task list as JSON."""
        output = commands.format_json([])
        assert output == "[]"
        # Verify it's valid JSON
        parsed = json.loads(output)
        assert parsed == []

    def test_format_json_single_task(self, sample_task):
        """Test formatting single task as JSON."""
        from src import storage

        output = commands.format_json(storage.tasks)
        parsed = json.loads(output)
        assert len(parsed) == 1
        assert parsed[0]["id"] == 1
        assert parsed[0]["title"] == "Test Task"

    def test_format_json_multiple_tasks(self, sample_tasks):
        """Test formatting multiple tasks as JSON."""
        from src import storage

        output = commands.format_json(storage.tasks)
        parsed = json.loads(output)
        assert len(parsed) == 3
        assert parsed[0]["id"] == 1
        assert parsed[1]["id"] == 2
        assert parsed[2]["id"] == 3

    def test_format_json_includes_all_fields(self, sample_task):
        """Test that JSON includes all task fields."""
        from src import storage

        output = commands.format_json(storage.tasks)
        parsed = json.loads(output)
        task = parsed[0]
        assert "id" in task
        assert "title" in task
        assert "description" in task
        assert "completed" in task
        assert "created_at" in task
        assert "updated_at" in task

    def test_format_json_preserves_full_timestamps(self, sample_task):
        """Test that JSON preserves full ISO 8601 timestamps."""
        from src import storage

        output = commands.format_json(storage.tasks)
        parsed = json.loads(output)
        task = parsed[0]
        # Should include Z suffix for UTC
        assert task["created_at"].endswith("Z")
        assert task["updated_at"].endswith("Z")
        # Should include T for ISO format
        assert "T" in task["created_at"]
        assert "T" in task["updated_at"]

    def test_format_json_valid_json(self, sample_tasks):
        """Test that JSON output is always valid JSON."""
        from src import storage

        output = commands.format_json(storage.tasks)
        # Should not raise exception
        parsed = json.loads(output)
        assert isinstance(parsed, list)
        assert len(parsed) == 3
