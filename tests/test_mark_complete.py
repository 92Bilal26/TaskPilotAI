"""Tests for mark_complete feature."""

import pytest

from src import commands, storage


class TestMarkComplete:
    """Test cases for mark_complete command."""

    def test_mark_pending_task_as_completed(self, sample_task):
        """Test marking pending task as completed."""
        assert storage.tasks[0]["completed"] is False
        task = commands.mark_complete(1)
        assert task["completed"] is True
        assert storage.tasks[0]["completed"] is True

    def test_mark_completed_task_as_pending(self, empty_storage):
        """Test marking completed task back to pending."""
        commands.add_task("Task")
        commands.mark_complete(1)
        assert storage.tasks[0]["completed"] is True

        task2 = commands.mark_complete(1)
        assert task2["completed"] is False
        assert storage.tasks[0]["completed"] is False

    def test_mark_complete_updates_timestamp(self, sample_task):
        """Test that marking complete updates the timestamp."""
        original_updated = storage.tasks[0]["updated_at"]
        task = commands.mark_complete(1)
        assert task["updated_at"] != original_updated

    def test_mark_complete_does_not_modify_id(self, sample_task):
        """Test that marking complete does not change ID."""
        task = commands.mark_complete(1)
        assert task["id"] == 1

    def test_mark_complete_does_not_modify_title(self, sample_task):
        """Test that marking complete does not change title."""
        original_title = storage.tasks[0]["title"]
        commands.mark_complete(1)
        assert storage.tasks[0]["title"] == original_title

    def test_mark_complete_does_not_modify_description(self, sample_task):
        """Test that marking complete does not change description."""
        original_desc = storage.tasks[0]["description"]
        commands.mark_complete(1)
        assert storage.tasks[0]["description"] == original_desc

    def test_mark_complete_does_not_modify_created_at(self, sample_task):
        """Test that marking complete does not change created_at."""
        original_created = storage.tasks[0]["created_at"]
        commands.mark_complete(1)
        assert storage.tasks[0]["created_at"] == original_created

    def test_mark_complete_toggle_multiple_times(self, sample_task):
        """Test toggling completion status multiple times."""
        assert storage.tasks[0]["completed"] is False

        commands.mark_complete(1)
        assert storage.tasks[0]["completed"] is True

        commands.mark_complete(1)
        assert storage.tasks[0]["completed"] is False

        commands.mark_complete(1)
        assert storage.tasks[0]["completed"] is True

    def test_mark_complete_nonexistent_task_raises_error(self, sample_task):
        """Test that marking non-existent task raises error."""
        with pytest.raises(ValueError, match="Task ID 999 not found"):
            commands.mark_complete(999)

    def test_mark_complete_zero_id_raises_error(self, sample_task):
        """Test that task ID 0 raises error."""
        with pytest.raises(ValueError, match="ID must be positive integer"):
            commands.mark_complete(0)

    def test_mark_complete_negative_id_raises_error(self, sample_task):
        """Test that negative task ID raises error."""
        with pytest.raises(ValueError, match="ID must be positive integer"):
            commands.mark_complete(-1)

    def test_mark_complete_with_different_tasks(self, sample_tasks):
        """Test marking different tasks complete independently."""
        # Mark task 1 complete
        commands.mark_complete(1)
        assert storage.tasks[0]["completed"] is True
        # Task 2 should still be completed (was already)
        assert storage.tasks[1]["completed"] is True
        # Task 3 should still be pending
        assert storage.tasks[2]["completed"] is False

        # Mark task 3 complete
        commands.mark_complete(3)
        assert storage.tasks[2]["completed"] is True

        # Now all are completed
        assert all(t["completed"] for t in storage.tasks)

    def test_mark_complete_already_completed_task(self, empty_storage):
        """Test that marking already completed task toggles it."""
        commands.add_task("Task")
        commands.mark_complete(1)
        assert storage.tasks[0]["completed"] is True

        # Marking again should toggle to False
        task2 = commands.mark_complete(1)
        assert task2["completed"] is False

    def test_mark_complete_timestamp_increments(self, sample_task):
        """Test that each toggle increments the timestamp."""
        task1 = commands.mark_complete(1)
        timestamp1 = task1["updated_at"]

        task2 = commands.mark_complete(1)
        timestamp2 = task2["updated_at"]

        assert timestamp1 != timestamp2
        assert timestamp2 > timestamp1
