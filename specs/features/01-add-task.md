# Feature Specification: Add Task

**Feature Branch**: `01-add-task`
**Created**: 2025-12-07
**Status**: Draft
**Input**: User wants to create a new todo item with a title and optional description

## User Scenarios & Testing

### User Story 1 - Create Task with Title Only (Priority: P1)

As a user, I want to quickly add a task with just a title so I can capture an idea without typing a description.

**Why this priority**: Core feature—essential for MVP. Users need to be able to create tasks with minimal friction.

**Independent Test**: Can be fully tested by running `python main.py add --title "Buy groceries"` and verifying task is stored with auto-assigned ID and correct title.

**Acceptance Scenarios**:

1. **Given** the app is running and task storage is empty, **When** user runs `add --title "Buy groceries"`, **Then** system returns success message with task ID 1, and task is stored with:
   - id: 1
   - title: "Buy groceries"
   - description: "" (empty)
   - completed: False
   - created_at: current ISO 8601 datetime
   - updated_at: current ISO 8601 datetime

2. **Given** one task exists with ID 1, **When** user adds another task with `add --title "Call mom"`, **Then** new task gets ID 2 (auto-increment works)

3. **Given** user adds 10 tasks, **When** checking IDs, **Then** all have unique auto-incremented IDs (1-10)

---

### User Story 2 - Create Task with Title and Description (Priority: P1)

As a user, I want to add a task with both title and description so I can provide context and details about what needs to be done.

**Why this priority**: Core feature—equally important as title-only task. Users need descriptive tasks for complex items.

**Independent Test**: Can be fully tested by running `python main.py add --title "Buy groceries" --description "Milk, eggs, bread"` and verifying both fields are stored correctly.

**Acceptance Scenarios**:

1. **Given** task storage is empty, **When** user runs `add --title "Buy groceries" --description "Milk, eggs, bread"`, **Then** system returns success and task stores:
   - title: "Buy groceries"
   - description: "Milk, eggs, bread"
   - All other fields same as Story 1

2. **Given** description is provided, **When** task is created, **Then** updated_at equals created_at (new task)

---

### User Story 3 - Return Task ID to User (Priority: P1)

As a user, I want to know the assigned task ID immediately after creating a task so I can reference it for other operations.

**Why this priority**: Essential for usability—user needs ID to update/delete/complete the task.

**Independent Test**: Output verification: running `add --title "Task"` returns "Task created with ID X" where X is an integer.

**Acceptance Scenarios**:

1. **Given** user creates a task, **When** command completes, **Then** output contains "Task created with ID 1" or similar clear message
2. **Given** user creates second task, **When** command completes, **Then** output shows correct new ID (not reused)

---

### Edge Cases

- What happens if title is empty or missing? → Must show error "Title required"
- What happens if title exceeds 200 characters? → Must show error "Title max 200 characters"
- What happens if description exceeds 1000 characters? → Must show error "Description max 1000 characters"
- What happens if user provides invalid arguments? → Must show error "Invalid arguments. Use: add --title <title> [--description <desc>]"
- What happens after 1000 tasks? → IDs continue incrementing correctly (no wraparound)
- What if title contains special characters? → Must be accepted and stored as-is

## Requirements

### Functional Requirements

- **FR-001**: System MUST accept task title (required) via `--title` argument
- **FR-002**: System MUST accept task description (optional) via `--description` argument
- **FR-003**: System MUST auto-increment task ID starting from 1, never reuse IDs
- **FR-004**: System MUST validate title: required, 1-200 characters
- **FR-005**: System MUST validate description: optional, max 1000 characters
- **FR-006**: System MUST store task with ISO 8601 creation timestamp (created_at)
- **FR-007**: System MUST set updated_at equal to created_at for new tasks
- **FR-008**: System MUST store task in in-memory data structure (no persistence)
- **FR-009**: System MUST return clear success message with assigned task ID
- **FR-010**: System MUST return error message if validation fails (title length, missing required field)

### Key Entities

- **Task**: Represents a single todo item with:
  - id (int): Auto-incremented, unique identifier
  - title (str): Required, 1-200 characters
  - description (str): Optional, max 1000 characters, default empty string
  - completed (bool): Default False
  - created_at (str): ISO 8601 datetime when created
  - updated_at (str): ISO 8601 datetime when last modified

## Success Criteria

### Measurable Outcomes

- **SC-001**: Command `python main.py add --title "Task"` executes without errors
- **SC-002**: System correctly auto-increments task IDs starting from 1
- **SC-003**: Task with title and optional description stores all fields correctly
- **SC-004**: Created_at and updated_at timestamps are valid ISO 8601 format
- **SC-005**: 100% of unit tests pass for add_task function
- **SC-006**: Code coverage for add-task feature is ≥95%
- **SC-007**: All validation errors return appropriate error messages with exit code 1
- **SC-008**: Command processes 100 sequential add operations without error

## Data Model

### Input Contract
```
Command: python main.py add [--title <title>] [--description <description>]

Arguments:
  --title TEXT        Task title (required, 1-200 chars)
  --description TEXT  Task description (optional, max 1000 chars)

Exit Codes:
  0: Success
  1: Validation error (invalid input)
  2: System error
```

### Output Contract
```
Success:
  Task created with ID {id}

Error:
  Error: Title required (1-200 characters)
  Error: Description max 1000 characters
  Error: Invalid arguments
```

### Storage Contract
```python
# New task created in memory
{
  "id": int,                    # Auto-incremented
  "title": str,                 # 1-200 chars
  "description": str,           # Optional, max 1000 chars
  "completed": bool,            # False
  "created_at": str,            # ISO 8601, e.g., "2025-12-07T10:30:00"
  "updated_at": str             # Same as created_at
}
```

## Implementation Notes

- Use Python's `datetime.datetime.now().isoformat()` for timestamps
- Store tasks in a module-level list: `tasks: List[Dict] = []`
- Maintain separate counter: `next_id: int = 1`
- Increment next_id AFTER assigning ID to task
- IDs never reset or reuse, even if tasks are deleted
- Input validation must happen before storage

---

**Version**: 1.0
**Last Updated**: 2025-12-07
**Status**: Ready for Implementation
