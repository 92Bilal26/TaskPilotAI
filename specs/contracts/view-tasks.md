# Contract: View Tasks

**Feature**: 04-view-tasks
**Command**: `python main.py list [--status <status>] [--json]`

## Input Contract

```
Optional Arguments:
  --status TEXT             Filter by status: pending, completed, all (default: all)
  --json                    Output as JSON instead of table (optional flag)

Valid Status Values:
  - "pending"  → only incomplete tasks (completed=False)
  - "completed" → only complete tasks (completed=True)
  - "all"      → all tasks (default, can be omitted)

Exit Codes:
  0: Success (even if no tasks)
  1: Invalid status value
  2: System error
```

## Output Contract - Success (Table Format)

```
ID | Title              | Status    | Created
<task_id> | <title> | <pending|completed> | <YYYY-MM-DD>
```

**Example with tasks**:
```
ID | Title              | Status    | Created
1  | Buy groceries      | pending   | 2025-12-07
2  | Call mom           | completed | 2025-12-06
3  | Fix authentication | pending   | 2025-12-07
```

**Example empty list**:
```
No tasks
```

## Output Contract - Success (JSON Format)

```json
[
  {
    "id": 1,
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false,
    "created_at": "2025-12-07T10:30:00Z",
    "updated_at": "2025-12-07T10:30:00Z"
  },
  {
    "id": 2,
    "title": "Call mom",
    "description": "",
    "completed": true,
    "created_at": "2025-12-06T14:00:00Z",
    "updated_at": "2025-12-07T09:00:00Z"
  }
]
```

**Example empty list (JSON)**:
```json
[]
```

## Output Contract - Error

```
Error: Invalid status. Use: all, pending, completed
```

## Data Contract (Storage Query)

**Input**:
```python
{
  "status": str,  # "all", "pending", or "completed"
  "format": str   # "table" or "json"
}
```

**Output** (Filtered tasks):
```python
# For status="pending":
[task for task in storage.tasks if task["completed"] == False]

# For status="completed":
[task for task in storage.tasks if task["completed"] == True]

# For status="all":
storage.tasks  # All tasks, unchanged order
```

## State Changes

- No modifications to storage
- Read-only operation
- `updated_at` fields NOT modified

## Example Workflows

### Happy Path: View all tasks (table format)
```bash
$ python main.py list
ID | Title              | Status    | Created
1  | Buy groceries      | pending   | 2025-12-07
2  | Call mom           | completed | 2025-12-06
$ echo $?
0
```

### Happy Path: View pending tasks only
```bash
$ python main.py list --status pending
ID | Title              | Status    | Created
1  | Buy groceries      | pending   | 2025-12-07
$ echo $?
0
```

### Happy Path: View completed tasks only
```bash
$ python main.py list --status completed
ID | Title              | Status    | Created
2  | Call mom           | completed | 2025-12-06
$ echo $?
0
```

### Happy Path: View as JSON
```bash
$ python main.py list --json
[
  {"id": 1, "title": "Buy groceries", "description": "Milk, eggs, bread", "completed": false, "created_at": "2025-12-07T10:30:00Z", "updated_at": "2025-12-07T10:30:00Z"},
  {"id": 2, "title": "Call mom", "description": "", "completed": true, "created_at": "2025-12-06T14:00:00Z", "updated_at": "2025-12-07T09:00:00Z"}
]
$ echo $?
0
```

### Happy Path: View pending as JSON
```bash
$ python main.py list --status pending --json
[{"id": 1, ...}]
$ echo $?
0
```

### Happy Path: Empty list (table)
```bash
$ python main.py list
No tasks
$ echo $?
0
```

### Happy Path: Empty list (JSON)
```bash
$ python main.py list --json
[]
$ echo $?
0
```

### Error Path: Invalid status
```bash
$ python main.py list --status invalid
Error: Invalid status. Use: all, pending, completed
$ echo $?
1
```

## Display Formatting Rules

**Table Format**:
- Column separator: ` | ` (pipe with spaces)
- Header row with column names
- Date format: YYYY-MM-DD (date only, not time)
- Status: lowercase "pending" or "completed"
- Sort by ID ascending
- Proper column alignment (padding)

**JSON Format**:
- Indent: 2 spaces
- All task fields included unchanged
- Full ISO 8601 timestamps (not just date)
- Timezone info: Z suffix for UTC
- Valid JSON array (even if empty)
- UTF-8 encoding

**Empty List Handling**:
- Table: Print "No tasks" (not an error)
- JSON: Print "[]" (empty array)
- Exit code: 0 (success, not error)
