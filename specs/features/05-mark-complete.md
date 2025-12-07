# Feature Specification: Mark Task as Complete

**Feature Branch**: `05-mark-complete`
**Created**: 2025-12-07
**Status**: Draft
**Input**: User wants to toggle a task's completion status (pending ↔ completed)

## User Scenarios & Testing

### User Story 1 - Mark Pending Task as Completed (Priority: P1)

As a user, I want to mark a task as complete when I finish doing it so I can track my progress.

**Why this priority**: Core feature—essential for task management workflow. Users need to mark tasks done.

**Independent Test**: Create task with completed=False, run `complete --id 1`, verify completed=True and success message shown.

**Acceptance Scenarios**:

1. **Given** task with ID 1 has completed=False, **When** user runs `complete --id 1`, **Then** system returns "Task 1 marked as completed" and task.completed is now True

2. **Given** multiple pending tasks, **When** one is marked complete, **Then** only that task's completed status changes

3. **Given** task is marked complete, **When** checking updated_at field, **Then** it's updated to current time

---

### User Story 2 - Mark Completed Task as Pending (Priority: P1)

As a user, I want to unmark a completed task if I need to redo it, so I can manage changes.

**Why this priority**: Usability—users make mistakes or need to revisit tasks. Toggling is essential.

**Independent Test**: Mark task as complete, then run `complete --id 1` again, verify completed=False.

**Acceptance Scenarios**:

1. **Given** task with ID 1 has completed=True, **When** user runs `complete --id 1`, **Then** system returns "Task 1 marked as pending" and task.completed is now False

2. **Given** task toggled from completed to pending, **When** checking task fields, **Then** all other fields remain unchanged except updated_at

---

### User Story 3 - Prevent Completing Non-Existent Task (Priority: P1)

As a user, I want error feedback if I try to complete a task that doesn't exist so I know the operation failed.

**Why this priority**: Error handling—prevents silent failures and user confusion.

**Independent Test**: Run `complete --id 999` (doesn't exist), verify error "Task ID 999 not found" returned.

**Acceptance Scenarios**:

1. **Given** no task with ID 10 exists, **When** user runs `complete --id 10`, **Then** system returns error "Task ID 10 not found" with exit code 1

2. **Given** task is deleted, **When** user tries to mark it complete, **Then** error "Task not found" returned

---

### User Story 4 - Update Timestamp on Completion (Priority: P2)

As a system, I must track when tasks are last modified, including completion status changes.

**Why this priority**: Data integrity—updated_at reflects actual changes to task state.

**Independent Test**: Mark task complete, verify updated_at timestamp is newer than before.

**Acceptance Scenarios**:

1. **Given** task created at 10:00, **When** marked complete at 10:30, **Then** updated_at reflects 10:30

---

### Edge Cases

- What happens if --id not provided? → Error "--id is required"
- What happens if --id is non-numeric? → Error "Invalid ID format. Use --id <number>"
- What happens if --id is 0 or negative? → Error "ID must be positive integer"
- What happens if marking already completed task as complete again? → Should toggle to pending (not error)
- What happens if task is the only one? → Mark complete works same as with multiple tasks

## Requirements

### Functional Requirements

- **FR-001**: System MUST accept task ID via `--id` argument (required)
- **FR-002**: System MUST validate --id is a positive integer
- **FR-003**: System MUST toggle completed status: False → True or True → False
- **FR-004**: System MUST update updated_at timestamp when completion status changes
- **FR-005**: System MUST preserve all other task fields (id, title, description, created_at)
- **FR-006**: System MUST return error if task ID doesn't exist
- **FR-007**: System MUST return success message indicating new status (completed or pending)
- **FR-008**: System MUST handle toggle both directions (pending→completed and completed→pending)

### Key Entities

- **Task**: Completion status toggles between False (pending) and True (completed)

## Success Criteria

### Measurable Outcomes

- **SC-001**: `python main.py complete --id 1` toggles completion status
- **SC-002**: Pending task marked complete shows completed status
- **SC-003**: Completed task marked again becomes pending
- **SC-004**: `python main.py complete --id 999` returns "Task not found" error
- **SC-005**: Updated_at timestamp is newer after marking complete
- **SC-006**: Other task fields (title, description) unchanged by completion status change
- **SC-007**: 100% of complete unit tests pass
- **SC-008**: Code coverage for mark-complete feature is ≥95%

## Data Model

### Input Contract
```
Command: python main.py complete [--id <id>]

Arguments:
  --id INT   Task ID to toggle completion (required, positive integer)

Exit Codes:
  0: Success
  1: Task not found or invalid input
  2: System error
```

### Output Contract
```
Success (was pending):
  Task {id} marked as completed

Success (was completed):
  Task {id} marked as pending

Error:
  Error: Task ID {id} not found
  Error: --id is required
  Error: Invalid ID format. Use --id <number>
```

### Storage Impact
```python
# Before: complete --id 1 (task is pending)
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs",
  "completed": False,                    # WILL CHANGE
  "created_at": "2025-12-07T10:00:00",
  "updated_at": "2025-12-07T10:00:00"   # WILL UPDATE
}

# After: complete --id 1
{
  "id": 1,
  "title": "Buy groceries",              # UNCHANGED
  "description": "Milk, eggs",           # UNCHANGED
  "completed": True,                     # CHANGED (toggle)
  "created_at": "2025-12-07T10:00:00",  # UNCHANGED
  "updated_at": "2025-12-07T10:30:00"   # CHANGED (updated)
}

# If toggled again: complete --id 1
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs",
  "completed": False,                    # CHANGED back (toggle)
  "created_at": "2025-12-07T10:00:00",
  "updated_at": "2025-12-07T10:45:00"   # CHANGED again
}
```

## Implementation Notes

- Parse --id argument and validate it's a positive integer
- Find task by ID, return error if not found
- Toggle completed status: `task["completed"] = not task["completed"]`
- Update updated_at to current ISO 8601 datetime
- Determine new status (pending or completed)
- Return appropriate success message with new status
- Exit with code 0 on success, 1 on error

---

**Version**: 1.0
**Last Updated**: 2025-12-07
**Status**: Ready for Implementation
