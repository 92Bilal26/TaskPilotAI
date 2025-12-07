# Feature Specification: View Task List

**Feature Branch**: `04-view-tasks`
**Created**: 2025-12-07
**Status**: Draft
**Input**: User wants to see their tasks in a readable format with optional filtering

## User Scenarios & Testing

### User Story 1 - View All Tasks in Human-Readable Format (Priority: P1)

As a user, I want to see all my tasks in a nicely formatted table so I can see what I need to do.

**Why this priority**: Core feature—users must see their tasks. Foundation for task management.

**Independent Test**: Create 3 tasks, run `list`, verify all 3 tasks displayed in table with ID, Title, Status, Created columns.

**Acceptance Scenarios**:

1. **Given** 3 tasks exist with various titles, **When** user runs `list`, **Then** output shows table with all tasks:
   ```
   ID | Title          | Status    | Created
   1  | Buy groceries  | pending   | 2025-12-07
   2  | Call mom       | completed | 2025-12-06
   3  | Fix bug        | pending   | 2025-12-07
   ```

2. **Given** task storage is empty, **When** user runs `list`, **Then** output shows "No tasks" or empty table

3. **Given** tasks have various completion statuses, **When** list is displayed, **Then** status shows "pending" or "completed"

---

### User Story 2 - Filter Tasks by Status (Priority: P1)

As a user, I want to filter tasks by status so I can focus on pending work or see what I've completed.

**Why this priority**: Essential usability—users need to see pending vs completed separately.

**Independent Test**: Create 2 pending and 1 completed task, run `list --status pending`, verify only 2 pending shown.

**Acceptance Scenarios**:

1. **Given** 2 pending and 1 completed task exist, **When** user runs `list --status pending`, **Then** only pending tasks shown

2. **Given** multiple tasks, **When** user runs `list --status completed`, **Then** only completed tasks shown with "completed" status

3. **Given** no tasks with filter status, **When** user runs `list --status pending`, **Then** output shows "No tasks" or empty result

---

### User Story 3 - View Tasks as JSON (Priority: P2)

As a developer/API consumer, I want JSON output so I can parse tasks programmatically.

**Why this priority**: Convenience—enables automation and integration. Nice-to-have for Phase 1.

**Independent Test**: Run `list --json`, verify output is valid JSON array of task objects.

**Acceptance Scenarios**:

1. **Given** tasks exist, **When** user runs `list --json`, **Then** output is valid JSON array:
   ```json
   [
     {"id": 1, "title": "Task 1", "description": "Desc 1", "completed": false, "created_at": "...", "updated_at": "..."},
     {"id": 2, "title": "Task 2", "description": "", "completed": true, "created_at": "...", "updated_at": "..."}
   ]
   ```

2. **Given** JSON output requested, **When** command runs, **Then** output is parseable by JSON parser (no formatting issues)

---

### User Story 4 - View No Tasks Gracefully (Priority: P1)

As a user, I want a clear message when I have no tasks so I know the app is working correctly.

**Why this priority**: User experience—prevents confusion about whether app is working.

**Independent Test**: Run `list` with empty storage, verify message like "No tasks" appears.

**Acceptance Scenarios**:

1. **Given** task storage is empty, **When** user runs `list`, **Then** output shows "No tasks" or similar message (not error)

---

### Edge Cases

- What happens if --status has invalid value? → Error "Invalid status. Use: all, pending, completed"
- What happens with very long task titles? → Truncate in table display or wrap lines, but preserve full data
- What happens with many tasks (100+)? → Display all, consider pagination (not required for Phase 1)
- What happens with special characters in titles? → Display as-is without escaping

## Requirements

### Functional Requirements

- **FR-001**: System MUST display all tasks in human-readable table format
- **FR-002**: System MUST show columns: ID, Title, Status (pending/completed), Created date
- **FR-003**: System MUST support optional `--status` filter (pending, completed, all)
- **FR-004**: System MUST support `--json` flag for JSON output
- **FR-005**: System MUST show task creation date in readable format (YYYY-MM-DD or similar)
- **FR-006**: System MUST handle empty task list gracefully with "No tasks" message
- **FR-007**: System MUST sort tasks by ID (ascending)
- **FR-008**: System MUST return error for invalid --status values
- **FR-009**: System MUST output JSON as valid, parseable array when --json used
- **FR-010**: System MUST exit with code 0 even if no tasks (list is valid result)

### Key Entities

- **Task**: Read-only display of stored task data
- **Status Values**: "pending" (completed=False), "completed" (completed=True), "all" (both)

## Success Criteria

### Measurable Outcomes

- **SC-001**: `python main.py list` shows all tasks in table format
- **SC-002**: `python main.py list --status pending` shows only pending tasks
- **SC-003**: `python main.py list --status completed` shows only completed tasks
- **SC-004**: `python main.py list --json` returns valid JSON array
- **SC-005**: Empty list returns "No tasks" message, exit code 0
- **SC-006**: Table has proper column alignment and headers
- **SC-007**: 100% of list unit tests pass
- **SC-008**: Code coverage for view-tasks feature is ≥95%
- **SC-009**: JSON output contains all task fields unchanged

## Data Model

### Input Contract
```
Command: python main.py list [--status <status>] [--json]

Arguments:
  --status TEXT  Filter by status: pending, completed, all (optional, default: all)
  --json         Output as JSON instead of table (optional flag)

Exit Codes:
  0: Success (even if no tasks)
  1: Invalid arguments or filter value
  2: System error
```

### Output Contract - Table Format
```
ID | Title              | Status    | Created
1  | Buy groceries      | pending   | 2025-12-07
2  | Call mom           | completed | 2025-12-06

OR (if no tasks):
No tasks

OR (if invalid status):
Error: Invalid status. Use: all, pending, completed
```

### Output Contract - JSON Format
```json
[
  {
    "id": 1,
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false,
    "created_at": "2025-12-07T10:30:00",
    "updated_at": "2025-12-07T10:30:00"
  },
  {
    "id": 2,
    "title": "Call mom",
    "description": "",
    "completed": true,
    "created_at": "2025-12-06T14:00:00",
    "updated_at": "2025-12-07T09:00:00"
  }
]

OR (if no tasks):
[]
```

### Storage Query
```python
# Get all tasks (no filter)
tasks = [task for task in storage.tasks]

# Get pending tasks only
pending = [task for task in storage.tasks if task["completed"] == False]

# Get completed tasks only
completed = [task for task in storage.tasks if task["completed"] == True]
```

## Implementation Notes

- Parse command arguments: --status, --json
- Validate --status value (pending, completed, all)
- Filter task list based on --status
- If --json flag present, output as JSON array
- If --json not present, output as formatted table
- Extract date portion from created_at (YYYY-MM-DD format)
- Sort tasks by ID ascending
- Return "No tasks" message if list is empty (not an error)
- Use proper column alignment and headers for table

## Display Format Recommendations

### Table Format
```
ID | Title              | Status    | Created
---+--------------------+-----------+----------
1  | Buy groceries      | pending   | 2025-12-07
2  | Call mom           | completed | 2025-12-06
3  | Fix authentication | pending   | 2025-12-07
```

### JSON Format
Indent 2 spaces, include all task fields, valid UTF-8

---

**Version**: 1.0
**Last Updated**: 2025-12-07
**Status**: Ready for Implementation
