"""Tests for List and Complete Task MCP Tools

Tests for:
- list_tasks: Retrieve tasks with filtering
- complete_task: Toggle task completion status
- User isolation and authorization
"""

import pytest
from sqlmodel import Session, select
from mcp.tools import list_tasks, complete_task, add_task
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
    return "test-user-list-001"


@pytest.fixture
def other_user_id():
    """Provide another test user ID"""
    return "test-user-list-002"


@pytest.fixture
def sample_tasks(test_user_id: str, db_session: Session):
    """Create sample tasks for testing"""
    tasks = []
    for i in range(5):
        result = add_task(
            user_id=test_user_id,
            title=f"Task {i+1}",
            description=f"Description for task {i+1}",
        )
        tasks.append(result)

    # Mark some as complete
    complete_task(test_user_id, tasks[0]["task_id"])
    complete_task(test_user_id, tasks[1]["task_id"])

    return tasks


class TestListTasks:
    """Tests for list_tasks MCP tool"""

    def test_list_all_tasks(self, test_user_id: str, sample_tasks: list):
        """Test: List all tasks for user"""
        # Act
        result = list_tasks(user_id=test_user_id, status="all")

        # Assert
        assert result["success"] is True
        assert len(result["tasks"]) == 5
        assert result["total"] == 5
        assert result["pending"] == 3
        assert result["completed"] == 2
        assert result["message"] == "You have 5 total task(s)"

    def test_list_pending_tasks(self, test_user_id: str, sample_tasks: list):
        """Test: List only pending tasks"""
        # Act
        result = list_tasks(user_id=test_user_id, status="pending")

        # Assert
        assert result["success"] is True
        assert len(result["tasks"]) == 3
        assert result["filtered_status"] == "pending"
        assert all(not task["completed"] for task in result["tasks"])
        assert result["message"] == "You have 3 pending task(s)"

    def test_list_completed_tasks(self, test_user_id: str, sample_tasks: list):
        """Test: List only completed tasks"""
        # Act
        result = list_tasks(user_id=test_user_id, status="completed")

        # Assert
        assert result["success"] is True
        assert len(result["tasks"]) == 2
        assert result["filtered_status"] == "completed"
        assert all(task["completed"] for task in result["tasks"])
        assert result["message"] == "You have 2 completed task(s)"

    def test_list_empty_tasks(self, other_user_id: str):
        """Test: List tasks when user has none"""
        # Act
        result = list_tasks(user_id=other_user_id, status="all")

        # Assert
        assert result["success"] is True
        assert len(result["tasks"]) == 0
        assert result["total"] == 0
        assert result["message"] == "You don't have any tasks yet. Want to create one?"

    def test_list_no_pending_tasks(self, test_user_id: str):
        """Test: No pending message when all complete"""
        # Arrange - Create task and complete it
        task_result = add_task(user_id=test_user_id, title="Complete me")
        complete_task(test_user_id, task_result["task_id"])

        # Act
        result = list_tasks(user_id=test_user_id, status="pending")

        # Assert
        assert len(result["tasks"]) == 0
        assert result["message"] == "You have no pending tasks! 🎉"

    def test_list_invalid_status(self, test_user_id: str):
        """Test: Invalid status raises error"""
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            list_tasks(user_id=test_user_id, status="invalid")

        assert "Invalid status" in str(exc_info.value)

    def test_list_tasks_user_isolation(
        self, test_user_id: str, other_user_id: str, sample_tasks: list
    ):
        """Test: User can only see their own tasks"""
        # Act
        result = list_tasks(user_id=other_user_id)

        # Assert
        assert len(result["tasks"]) == 0
        assert result["total"] == 0

    def test_list_tasks_includes_all_fields(
        self, test_user_id: str, sample_tasks: list
    ):
        """Test: Task list includes all required fields"""
        # Act
        result = list_tasks(user_id=test_user_id)

        # Assert
        task = result["tasks"][0]
        assert "id" in task
        assert "title" in task
        assert "description" in task
        assert "completed" in task
        assert "created_at" in task
        assert isinstance(task["created_at"], str)  # ISO format

    def test_list_tasks_response_structure(self, test_user_id: str):
        """Test: Response has required fields"""
        # Act
        result = list_tasks(user_id=test_user_id)

        # Assert
        assert "tasks" in result
        assert "total" in result
        assert "pending" in result
        assert "completed" in result
        assert "filtered_status" in result
        assert "message" in result
        assert "success" in result


class TestCompleteTask:
    """Tests for complete_task MCP tool"""

    def test_complete_task(self, test_user_id: str):
        """Test: Mark task as complete"""
        # Arrange
        task_result = add_task(user_id=test_user_id, title="Buy groceries")
        task_id = task_result["task_id"]

        # Act
        result = complete_task(user_id=test_user_id, task_id=task_id)

        # Assert
        assert result["success"] is True
        assert result["task_id"] == task_id
        assert result["completed"] is True
        assert "I've marked 'Buy groceries' as complete!" in result["message"]

    def test_complete_already_completed_task(self, test_user_id: str):
        """Test: Toggle task from complete to pending"""
        # Arrange
        task_result = add_task(user_id=test_user_id, title="Task to toggle")
        task_id = task_result["task_id"]
        complete_task(user_id=test_user_id, task_id=task_id)

        # Act
        result = complete_task(user_id=test_user_id, task_id=task_id)

        # Assert
        assert result["success"] is True
        assert result["completed"] is False
        assert "marked 'Task to toggle' as pending again" in result["message"]

    def test_complete_nonexistent_task(self, test_user_id: str):
        """Test: Mark nonexistent task raises error"""
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            complete_task(user_id=test_user_id, task_id="nonexistent-id")

        assert "not found" in str(exc_info.value)

    def test_complete_other_user_task(
        self, test_user_id: str, other_user_id: str
    ):
        """Test: Cannot complete another user's task"""
        # Arrange
        task_result = add_task(user_id=test_user_id, title="Private task")
        task_id = task_result["task_id"]

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            complete_task(user_id=other_user_id, task_id=task_id)

        assert "Not authorized" in str(exc_info.value)

    def test_complete_updates_timestamp(self, test_user_id: str):
        """Test: Completion updates updated_at timestamp"""
        # Arrange
        task_result = add_task(user_id=test_user_id, title="Timestamp test")
        original_time = task_result["created_at"]
        task_id = task_result["task_id"]

        # Act
        result = complete_task(user_id=test_user_id, task_id=task_id)

        # Assert
        assert result["updated_at"] != original_time
        assert "T" in result["updated_at"]  # ISO format

    def test_complete_persists_to_database(
        self, test_user_id: str, db_session: Session
    ):
        """Test: Completion is persisted to database"""
        # Arrange
        task_result = add_task(user_id=test_user_id, title="DB test")
        task_id = task_result["task_id"]

        # Act
        complete_task(user_id=test_user_id, task_id=task_id)

        # Assert - Verify in database
        db_task = db_session.get(Task, task_id)
        assert db_task is not None
        assert db_task.completed is True

    def test_complete_task_missing_id(self, test_user_id: str):
        """Test: Missing task_id raises error"""
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            complete_task(user_id=test_user_id, task_id="")

        assert "Task ID is required" in str(exc_info.value)


class TestListAndCompleteIntegration:
    """Integration tests for list and complete"""

    def test_list_reflects_completion(self, test_user_id: str):
        """Test: List reflects task completion status"""
        # Arrange
        task1 = add_task(user_id=test_user_id, title="Task 1")
        task2 = add_task(user_id=test_user_id, title="Task 2")

        # Act - Complete one task
        complete_task(user_id=test_user_id, task_id=task1["task_id"])

        # Assert - List shows correct status
        pending_result = list_tasks(user_id=test_user_id, status="pending")
        completed_result = list_tasks(user_id=test_user_id, status="completed")

        assert len(pending_result["tasks"]) == 1
        assert len(completed_result["tasks"]) == 1
        assert pending_result["tasks"][0]["id"] == task2["task_id"]
        assert completed_result["tasks"][0]["id"] == task1["task_id"]

    def test_completion_updates_totals(self, test_user_id: str):
        """Test: Completion updates pending/completed counts"""
        # Arrange
        task = add_task(user_id=test_user_id, title="Counter test")

        # Act
        list_before = list_tasks(user_id=test_user_id)
        complete_task(user_id=test_user_id, task_id=task["task_id"])
        list_after = list_tasks(user_id=test_user_id)

        # Assert
        assert list_before["pending"] == 1
        assert list_before["completed"] == 0
        assert list_after["pending"] == 0
        assert list_after["completed"] == 1
