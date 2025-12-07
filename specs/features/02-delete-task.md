# Feature Specification: Delete Task

**Feature Branch**: `02-delete-task`
**Created**: 2025-12-07
**Status**: Draft
**Input**: User wants to permanently remove a task from their list

## User Scenarios & Testing

### User Story 1 - Delete Existing Task (Priority: P1)

As a user, I want to remove a task from my list so I can clean up completed or unwanted items.

**Why this priority**: Core CRUD operation—essential for task management. Users must be able to remove tasks.

**Independent Test**: Can be fully tested by creating a task (with ID 1), then running `delete --id 1`, and verifying task is removed from storage.

**Acceptance Scenarios**:

1. **Given** a task with ID 1 exists, **When** user runs `delete --id 1`, **Then** system returns "Task 1 deleted successfully" and task is removed from storage

2. **Given** multiple tasks exist (IDs 1-5), **When** user deletes task 3, **Then** remaining tasks are 1, 2, 4, 5 (no reindexing)

3. **Given** task is deleted, **When** user lists tasks, **Then** deleted task doesn't appear

---

### User Story 2 - Prevent Deletion of Non-Existent Task (Priority: P1)

As a user, I want clear feedback if I try to delete a task that doesn't exist so I don't think it was removed when it wasn't.

**Why this priority**: Error handling—prevents user confusion. Users need to know if operation succeeded.

**Independent Test**: Running `delete --id 999` (non-existent ID) returns error message "Task ID 999 not found".

**Acceptance Scenarios**:

1. **Given** no task with ID 10 exists, **When** user runs `delete --id 10`, **Then** system returns error "Task ID 10 not found" with exit code 1

2. **Given** user deletes task 1, **When** user tries to delete task 1 again, **Then** error message appears (not deleted twice)

---

### User Story 3 - Maintain ID Sequence (Priority: P1)

As a system, I must ensure that task IDs remain unique and are never reused even after deletion, so future operations work correctly.

**Why this priority**: Data integrity—IDs are permanent identifiers. Reusing IDs would break references and cause confusion.

**Independent Test**: Create 3 tasks (IDs 1-3), delete task 2, create new task, verify new task gets ID 4 (not 2).

**Acceptance Scenarios**:

1. **Given** tasks 1, 2, 3 exist, **When** task 2 is deleted and new task added, **Then** new task gets ID 4

---

### Edge Cases

- What happens if task ID is invalid (non-numeric)? → Must show error "Invalid ID format"
- What happens if no --id argument provided? → Must show error "--id is required"
- What happens if task ID is 0 or negative? → Must show error "ID must be positive integer"
- What happens if user deletes all tasks then adds new task? → New task gets next sequential ID (not 1)
- What happens with concurrent deletes? → Not applicable for Phase 1 (single-threaded)

## Requirements

### Functional Requirements

- **FR-001**: System MUST accept task ID via `--id` argument (required)
- **FR-002**: System MUST validate that --id is a positive integer
- **FR-003**: System MUST remove task from in-memory storage if it exists
- **FR-004**: System MUST return success message if task was deleted
- **FR-005**: System MUST return error message if task doesn't exist
- **FR-006**: System MUST NOT reuse IDs after deletion
- **FR-007**: System MUST NOT reindex remaining tasks (maintain original IDs)
- **FR-008**: System MUST preserve the ID sequence counter (next_id)

### Key Entities

- **Task**: Identified by immutable `id` field
- **Storage**: In-memory list of tasks, maintains next_id counter

## Success Criteria

### Measurable Outcomes

- **SC-001**: `python main.py delete --id 1` removes task if it exists
- **SC-002**: `python main.py delete --id 999` returns error with exit code 1
- **SC-003**: After deleting task, retrieving deleted task ID returns "not found"
- **SC-004**: Deleted task no longer appears in list output
- **SC-005**: 100% of delete unit tests pass
- **SC-006**: Code coverage for delete-task feature is ≥95%
- **SC-007**: Next created task after deletion uses sequential ID, not reused ID

## Data Model

### Input Contract
```
Command: python main.py delete [--id <id>]

Arguments:
  --id INT   Task ID to delete (required, positive integer)

Exit Codes:
  0: Success
  1: Task not found or invalid input
  2: System error
```

### Output Contract
```
Success:
  Task {id} deleted successfully

Error:
  Error: Task ID {id} not found
  Error: --id is required
  Error: Invalid ID format. Use --id <number>
```

### Storage Impact
```python
# Before delete
tasks = [
  {"id": 1, "title": "Task 1", ...},
  {"id": 2, "title": "Task 2", ...},
  {"id": 3, "title": "Task 3", ...}
]

# After delete --id 2
tasks = [
  {"id": 1, "title": "Task 1", ...},
  {"id": 3, "title": "Task 3", ...}
]

# ID counter unchanged
next_id = 3
```

## Implementation Notes

- Parse --id argument and validate it's a positive integer
- Search task list for matching ID
- If found, remove from list and return success
- If not found, return error with exit code 1
- Do NOT reindex remaining tasks
- Do NOT decrement next_id counter (maintains sequence)

---

**Version**: 1.0
**Last Updated**: 2025-12-07
**Status**: Ready for Implementation
