# Feature Specification: Update Task

**Feature Branch**: `03-update-task`
**Created**: 2025-12-07
**Status**: Draft
**Input**: User wants to modify an existing task's title or description

## User Scenarios & Testing

### User Story 1 - Update Task Title (Priority: P1)

As a user, I want to change a task's title so I can correct mistakes or update it with new information.

**Why this priority**: Core CRUD operation—users must be able to modify tasks they created.

**Independent Test**: Create task (ID 1, title "Old"), run `update --id 1 --title "New"`, verify title changed and other fields preserved.

**Acceptance Scenarios**:

1. **Given** task with ID 1 has title "Buy milk", **When** user runs `update --id 1 --title "Buy milk and bread"`, **Then** task title is updated and success message shown

2. **Given** task has description and completed status, **When** title is updated, **Then** description and completed status remain unchanged

3. **Given** updated task, **When** checking updated_at field, **Then** it's newer than created_at timestamp

---

### User Story 2 - Update Task Description (Priority: P1)

As a user, I want to change a task's description so I can add details later or correct information.

**Why this priority**: Core CRUD operation—equally important as updating title.

**Independent Test**: Create task with description, run `update --id 1 --description "New details"`, verify only description changed.

**Acceptance Scenarios**:

1. **Given** task with ID 1 has description "Old", **When** user runs `update --id 1 --description "New details"`, **Then** description updated and success message shown

2. **Given** task description is updated, **When** checking task fields, **Then** id, title, completed status, and created_at remain unchanged

---

### User Story 3 - Update Both Title and Description (Priority: P2)

As a user, I want to update both title and description in one command to be efficient.

**Why this priority**: Convenience feature—allows bulk updates in single operation.

**Independent Test**: Run `update --id 1 --title "New" --description "Details"` and verify both fields changed.

**Acceptance Scenarios**:

1. **Given** task exists, **When** user provides both --title and --description, **Then** both fields are updated

---

### User Story 4 - Validate Update Input (Priority: P1)

As a user, I want validation so I don't accidentally set invalid values.

**Why this priority**: Data integrity—prevents invalid data in storage.

**Independent Test**: Run `update --id 1 --title ""` (empty) and verify error "Title required".

**Acceptance Scenarios**:

1. **Given** user tries to update with empty title, **When** command runs, **Then** error "Title required (1-200 chars)" returned

2. **Given** user tries to update with title >200 chars, **When** command runs, **Then** error "Title max 200 characters" returned

3. **Given** user provides description >1000 chars, **When** command runs, **Then** error "Description max 1000 characters" returned

---

### Edge Cases

- What happens if task ID doesn't exist? → Error "Task ID X not found"
- What happens if neither --title nor --description provided? → Error "At least one of --title or --description required"
- What happens if title provided but is empty? → Error "Title required (1-200 chars)"
- What happens if only whitespace provided for title? → Must be treated as invalid (per validation logic)
- What happens if task is completed, then title updated? → Title updates, completed status preserved

## Requirements

### Functional Requirements

- **FR-001**: System MUST accept task ID via `--id` argument (required)
- **FR-002**: System MUST accept optional `--title` argument
- **FR-003**: System MUST accept optional `--description` argument
- **FR-004**: System MUST require at least one of --title or --description
- **FR-005**: System MUST validate title if provided: 1-200 characters
- **FR-006**: System MUST validate description if provided: max 1000 characters
- **FR-007**: System MUST update only the provided fields
- **FR-008**: System MUST preserve id, created_at, and completed status
- **FR-009**: System MUST update updated_at timestamp to current time
- **FR-010**: System MUST return error if task ID doesn't exist
- **FR-011**: System MUST return success message with updated task info

### Key Entities

- **Task**: Updated task maintains all original fields except title/description and updated_at

## Success Criteria

### Measurable Outcomes

- **SC-001**: `python main.py update --id 1 --title "New"` updates title only
- **SC-002**: `python main.py update --id 1 --description "New"` updates description only
- **SC-003**: `python main.py update --id 1 --title "New" --description "Details"` updates both
- **SC-004**: Updated_at timestamp is newer than created_at after update
- **SC-005**: `python main.py update --id 999 --title "X"` returns "Task not found"
- **SC-006**: Update command without --title or --description returns error
- **SC-007**: 100% of update unit tests pass
- **SC-008**: Code coverage for update-task feature is ≥95%

## Data Model

### Input Contract
```
Command: python main.py update [--id <id>] [--title <title>] [--description <desc>]

Arguments:
  --id INT            Task ID to update (required)
  --title TEXT        New title (optional, 1-200 chars if provided)
  --description TEXT  New description (optional, max 1000 chars if provided)

Constraints:
  - At least one of --title or --description MUST be provided
  - If provided, --title must be 1-200 chars
  - If provided, --description must be max 1000 chars

Exit Codes:
  0: Success
  1: Task not found or validation error
  2: System error
```

### Output Contract
```
Success:
  Task {id} updated

Error:
  Error: Task ID {id} not found
  Error: At least one of --title or --description required
  Error: Title required (1-200 characters)
  Error: Description max 1000 characters
```

### Storage Impact
```python
# Before update
{
  "id": 1,
  "title": "Old title",
  "description": "Old desc",
  "completed": False,
  "created_at": "2025-12-07T10:00:00",
  "updated_at": "2025-12-07T10:00:00"
}

# After: update --id 1 --title "New title"
{
  "id": 1,
  "title": "New title",                    # CHANGED
  "description": "Old desc",               # UNCHANGED
  "completed": False,                      # UNCHANGED
  "created_at": "2025-12-07T10:00:00",    # UNCHANGED
  "updated_at": "2025-12-07T10:30:00"     # CHANGED (newer)
}
```

## Implementation Notes

- Parse --id, --title, --description arguments
- Validate that at least one update field is provided
- Find task by ID, return error if not found
- Validate title (1-200 chars) and description (max 1000 chars) if provided
- Only update fields that were explicitly provided
- Update the updated_at field to current time
- Preserve all other fields (id, created_at, completed)
- Return success message

---

**Version**: 1.0
**Last Updated**: 2025-12-07
**Status**: Ready for Implementation
