"""Tests for delete_task feature."""

import pytest

from src import commands, storage


class TestDeleteTask:
    """Test cases for delete_task command."""

    def test_delete_existing_task(self, sample_tasks):
        """Test deleting an existing task."""
        assert len(storage.tasks) == 3
        result = commands.delete_task(1)
        assert result is True
        assert len(storage.tasks) == 2
        assert not any(t["id"] == 1 for t in storage.tasks)

    def test_delete_task_removes_correct_task(self, sample_tasks):
        """Test that delete removes the correct task."""
        assert any(t["id"] == 2 for t in storage.tasks)
        commands.delete_task(2)
        assert not any(t["id"] == 2 for t in storage.tasks)
        assert any(t["id"] == 1 for t in storage.tasks)
        assert any(t["id"] == 3 for t in storage.tasks)

    def test_delete_task_does_not_modify_next_id(self, sample_tasks):
        """Test that deleting a task does not decrement next_id."""
        next_id_before = storage.next_id
        commands.delete_task(1)
        assert storage.next_id == next_id_before

    def test_delete_task_ids_never_reused(self, sample_tasks):
        """Test that deleted IDs are never reused when adding new task."""
        commands.delete_task(1)
        commands.delete_task(2)
        new_task = commands.add_task("New Task")
        # Should get next available ID (4), not reuse 1 or 2
        assert new_task["id"] == 4

    def test_delete_nonexistent_task_raises_error(self, sample_tasks):
        """Test that deleting non-existent task raises ValueError."""
        with pytest.raises(ValueError, match="Task ID 999 not found"):
            commands.delete_task(999)

    def test_delete_task_zero_id_raises_error(self, sample_tasks):
        """Test that task ID 0 raises ValueError."""
        with pytest.raises(ValueError, match="ID must be positive integer"):
            commands.delete_task(0)

    def test_delete_task_negative_id_raises_error(self, sample_tasks):
        """Test that negative task ID raises ValueError."""
        with pytest.raises(ValueError, match="ID must be positive integer"):
            commands.delete_task(-1)

    def test_delete_first_task_in_list(self, sample_tasks):
        """Test deleting the first task in the list."""
        assert storage.tasks[0]["id"] == 1
        commands.delete_task(1)
        assert storage.tasks[0]["id"] == 2

    def test_delete_last_task_in_list(self, sample_tasks):
        """Test deleting the last task in the list."""
        assert storage.tasks[-1]["id"] == 3
        commands.delete_task(3)
        assert storage.tasks[-1]["id"] == 2

    def test_delete_middle_task_in_list(self, sample_tasks):
        """Test deleting a task in the middle of the list."""
        commands.delete_task(2)
        remaining_ids = [t["id"] for t in storage.tasks]
        assert remaining_ids == [1, 3]

    def test_delete_already_deleted_task_raises_error(self, sample_tasks):
        """Test that deleting already deleted task raises error."""
        commands.delete_task(1)
        with pytest.raises(ValueError, match="Task ID 1 not found"):
            commands.delete_task(1)

    def test_delete_only_task(self, empty_storage):
        """Test deleting the only task in storage."""
        commands.add_task("Only Task")
        assert len(storage.tasks) == 1
        commands.delete_task(1)
        assert len(storage.tasks) == 0

    def test_delete_from_multiple_tasks_list_integrity(self, sample_tasks):
        """Test that deleting maintains list integrity with multiple tasks."""
        commands.delete_task(2)
        remaining_titles = [t["title"] for t in storage.tasks]
        assert "Call mom" not in remaining_titles
        assert "Buy groceries" in remaining_titles
        assert "Fix authentication" in remaining_titles
