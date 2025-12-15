"""Tests for Delete and Update Task MCP Tools

Tests for:
- delete_task: Permanent removal of tasks
- update_task: Modification of task title and/or description
- User isolation and authorization
"""

import pytest
from sqlmodel import Session, select
from mcp.tools import add_task, delete_task, update_task, list_tasks
from models import Task
from db import engine


@pytest.fixture
def db_session():
    """Provide database session"""
    from db import Session
    session = Session(engine)
    yield session
    session.close()


@pytest.fixture
def test_user_id():
    """Provide test user ID"""
    return "test-user-delete-update-001"


@pytest.fixture
def other_user_id():
    """Provide another test user ID"""
    return "test-user-delete-update-002"


class TestDeleteTask:
    """Tests for delete_task MCP tool"""

    def test_delete_task(self, test_user_id: str, db_session: Session):
        """Test: Delete a task"""
        # Arrange
        task_result = add_task(user_id=test_user_id, title="Task to delete")
        task_id = task_result["task_id"]

        # Act
        result = delete_task(user_id=test_user_id, task_id=task_id)

        # Assert
        assert result["success"] is True
        assert result["task_id"] == task_id
        assert result["title"] == "Task to delete"
        assert "I've removed 'Task to delete' from your task list" in result["message"]

        # Verify deleted from database
        db_task = db_session.get(Task, task_id)
        assert db_task is None

    def test_delete_nonexistent_task(self, test_user_id: str):
        """Test: Delete nonexistent task raises error"""
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            delete_task(user_id=test_user_id, task_id="nonexistent-id")

        assert "not found" in str(exc_info.value)

    def test_delete_other_user_task(self, test_user_id: str, other_user_id: str):
        """Test: Cannot delete another user's task"""
        # Arrange
        task_result = add_task(user_id=test_user_id, title="Private task")
        task_id = task_result["task_id"]

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            delete_task(user_id=other_user_id, task_id=task_id)

        assert "Not authorized" in str(exc_info.value)

    def test_delete_task_missing_id(self, test_user_id: str):
        """Test: Missing task_id raises error"""
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            delete_task(user_id=test_user_id, task_id="")

        assert "Task ID is required" in str(exc_info.value)

    def test_delete_task_removes_from_list(self, test_user_id: str):
        """Test: Deleted task doesn't appear in list"""
        # Arrange
        task1 = add_task(user_id=test_user_id, title="Task 1")
        task2 = add_task(user_id=test_user_id, title="Task 2")

        # Act
        delete_task(user_id=test_user_id, task_id=task1["task_id"])

        # Assert
        result = list_tasks(user_id=test_user_id)
        assert len(result["tasks"]) == 1
        assert result["tasks"][0]["title"] == "Task 2"

    def test_delete_multiple_tasks(self, test_user_id: str):
        """Test: Can delete multiple tasks"""
        # Arrange
        tasks = [
            add_task(user_id=test_user_id, title=f"Task {i}")
            for i in range(3)
        ]

        # Act
        for task in tasks:
            delete_task(user_id=test_user_id, task_id=task["task_id"])

        # Assert
        result = list_tasks(user_id=test_user_id)
        assert len(result["tasks"]) == 0


class TestUpdateTask:
    """Tests for update_task MCP tool"""

    def test_update_task_title(self, test_user_id: str):
        """Test: Update task title"""
        # Arrange
        task_result = add_task(user_id=test_user_id, title="Old title")
        task_id = task_result["task_id"]

        # Act
        result = update_task(
            user_id=test_user_id,
            task_id=task_id,
            title="New title",
        )

        # Assert
        assert result["success"] is True
        assert result["title"] == "New title"
        assert result["description"] is None
        assert "I've updated the task" in result["message"]

    def test_update_task_description(self, test_user_id: str):
        """Test: Update task description"""
        # Arrange
        task_result = add_task(user_id=test_user_id, title="Task")
        task_id = task_result["task_id"]

        # Act
        result = update_task(
            user_id=test_user_id,
            task_id=task_id,
            description="New description",
        )

        # Assert
        assert result["success"] is True
        assert result["title"] == "Task"
        assert result["description"] == "New description"

    def test_update_both_title_and_description(self, test_user_id: str):
        """Test: Update both title and description"""
        # Arrange
        task_result = add_task(
            user_id=test_user_id,
            title="Old title",
            description="Old description",
        )
        task_id = task_result["task_id"]

        # Act
        result = update_task(
            user_id=test_user_id,
            task_id=task_id,
            title="New title",
            description="New description",
        )

        # Assert
        assert result["success"] is True
        assert result["title"] == "New title"
        assert result["description"] == "New description"
        assert "title to 'New title'" in result["message"]
        assert "description to 'New description'" in result["message"]

    def test_update_task_truncates_long_title(self, test_user_id: str):
        """Test: Long title is truncated to 200 chars"""
        # Arrange
        task_result = add_task(user_id=test_user_id, title="Task")
        task_id = task_result["task_id"]
        long_title = "x" * 250

        # Act
        result = update_task(
            user_id=test_user_id,
            task_id=task_id,
            title=long_title,
        )

        # Assert
        assert len(result["title"]) == 200
        assert result["title"] == "x" * 200

    def test_update_task_truncates_long_description(self, test_user_id: str):
        """Test: Long description is truncated to 1000 chars"""
        # Arrange
        task_result = add_task(user_id=test_user_id, title="Task")
        task_id = task_result["task_id"]
        long_desc = "y" * 1200

        # Act
        result = update_task(
            user_id=test_user_id,
            task_id=task_id,
            description=long_desc,
        )

        # Assert
        assert len(result["description"]) == 1000
        assert result["description"] == "y" * 1000

    def test_update_task_strips_whitespace(self, test_user_id: str):
        """Test: Whitespace is stripped from title and description"""
        # Arrange
        task_result = add_task(user_id=test_user_id, title="Task")
        task_id = task_result["task_id"]

        # Act
        result = update_task(
            user_id=test_user_id,
            task_id=task_id,
            title="  New title  ",
            description="  New description  ",
        )

        # Assert
        assert result["title"] == "New title"
        assert result["description"] == "New description"

    def test_update_empty_title_raises_error(self, test_user_id: str):
        """Test: Empty title raises error"""
        # Arrange
        task_result = add_task(user_id=test_user_id, title="Task")
        task_id = task_result["task_id"]

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            update_task(user_id=test_user_id, task_id=task_id, title="")

        assert "Title cannot be empty" in str(exc_info.value)

    def test_update_task_requires_at_least_one_field(self, test_user_id: str):
        """Test: At least one field must be provided"""
        # Arrange
        task_result = add_task(user_id=test_user_id, title="Task")
        task_id = task_result["task_id"]

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            update_task(user_id=test_user_id, task_id=task_id)

        assert "At least one of title or description must be provided" in str(
            exc_info.value
        )

    def test_update_nonexistent_task(self, test_user_id: str):
        """Test: Update nonexistent task raises error"""
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            update_task(
                user_id=test_user_id,
                task_id="nonexistent-id",
                title="New title",
            )

        assert "not found" in str(exc_info.value)

    def test_update_other_user_task(self, test_user_id: str, other_user_id: str):
        """Test: Cannot update another user's task"""
        # Arrange
        task_result = add_task(user_id=test_user_id, title="Private task")
        task_id = task_result["task_id"]

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            update_task(
                user_id=other_user_id,
                task_id=task_id,
                title="Hacked title",
            )

        assert "Not authorized" in str(exc_info.value)

    def test_update_task_updates_timestamp(self, test_user_id: str):
        """Test: Update changes the updated_at timestamp"""
        # Arrange
        task_result = add_task(user_id=test_user_id, title="Task")
        original_time = task_result["created_at"]
        task_id = task_result["task_id"]

        # Act
        result = update_task(
            user_id=test_user_id,
            task_id=task_id,
            title="Updated",
        )

        # Assert
        assert result["updated_at"] != original_time

    def test_update_task_persists_to_database(
        self, test_user_id: str, db_session: Session
    ):
        """Test: Update is persisted to database"""
        # Arrange
        task_result = add_task(user_id=test_user_id, title="Original")
        task_id = task_result["task_id"]

        # Act
        update_task(
            user_id=test_user_id,
            task_id=task_id,
            title="Updated",
            description="New desc",
        )

        # Assert
        db_task = db_session.get(Task, task_id)
        assert db_task.title == "Updated"
        assert db_task.description == "New desc"

    def test_update_clear_description(self, test_user_id: str):
        """Test: Description can be cleared by setting to empty string"""
        # Arrange
        task_result = add_task(
            user_id=test_user_id,
            title="Task",
            description="Original description",
        )
        task_id = task_result["task_id"]

        # Act
        result = update_task(
            user_id=test_user_id,
            task_id=task_id,
            description="",
        )

        # Assert
        assert result["description"] is None


class TestDeleteAndUpdateIntegration:
    """Integration tests for delete and update"""

    def test_delete_after_update(self, test_user_id: str):
        """Test: Can delete a task that was updated"""
        # Arrange
        task_result = add_task(user_id=test_user_id, title="Task")
        task_id = task_result["task_id"]

        # Act - Update then delete
        update_task(user_id=test_user_id, task_id=task_id, title="Updated")
        result = delete_task(user_id=test_user_id, task_id=task_id)

        # Assert
        assert result["success"] is True
        assert result["title"] == "Updated"

    def test_update_reflects_in_list(self, test_user_id: str):
        """Test: Updated task shows new values in list"""
        # Arrange
        task_result = add_task(user_id=test_user_id, title="Original")
        task_id = task_result["task_id"]

        # Act
        update_task(
            user_id=test_user_id,
            task_id=task_id,
            title="Updated title",
            description="Updated description",
        )

        # Assert
        result = list_tasks(user_id=test_user_id)
        assert result["tasks"][0]["title"] == "Updated title"
        assert result["tasks"][0]["description"] == "Updated description"

    def test_multiple_updates(self, test_user_id: str):
        """Test: Can update a task multiple times"""
        # Arrange
        task_result = add_task(user_id=test_user_id, title="Task 1")
        task_id = task_result["task_id"]

        # Act - Update multiple times
        result1 = update_task(user_id=test_user_id, task_id=task_id, title="Task 2")
        result2 = update_task(user_id=test_user_id, task_id=task_id, title="Task 3")

        # Assert
        assert result1["title"] == "Task 2"
        assert result2["title"] == "Task 3"

        # Verify in list
        list_result = list_tasks(user_id=test_user_id)
        assert list_result["tasks"][0]["title"] == "Task 3"
