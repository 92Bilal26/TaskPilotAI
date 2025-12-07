# Data Models Specification

**Created**: 2025-12-07
**Status**: Draft
**Scope**: In-memory task storage for Phase 1

---

## Core Entity: Task

### Definition
A task represents a single todo item with a unique identifier, user-provided title and optional description, completion status, and timestamps.

### Structure

```python
Task = Dict[str, Any]

{
  "id": int,                    # Unique, auto-incremented identifier
  "title": str,                 # Required user input, 1-200 characters
  "description": str,           # Optional user input, max 1000 chars, default ""
  "completed": bool,            # Completion status, default False
  "created_at": str,            # ISO 8601 datetime when task was created
  "updated_at": str             # ISO 8601 datetime when task was last modified
}
```

### Field Details

#### id (int)
- **Type**: Integer
- **Constraints**: Positive, unique, auto-incremented
- **Behavior**:
  - Starts at 1 for first task
  - Increments by 1 for each new task
  - Never reuses deleted IDs
  - Never resets between operations
- **Example**: 1, 2, 3, ..., 100

#### title (str)
- **Type**: String
- **Constraints**: Required, 1-200 characters
- **Behavior**:
  - Cannot be empty or whitespace-only
  - Accepts any UTF-8 characters
  - Case-sensitive (preserved as-is)
  - No automatic trimming (user responsible)
- **Example**: "Buy groceries", "Fix authentication bug", "Call dentist"

#### description (str)
- **Type**: String
- **Constraints**: Optional, max 1000 characters
- **Behavior**:
  - Default value is empty string ""
  - Accepts any UTF-8 characters including newlines
  - Case-sensitive
  - If not provided by user, defaults to ""
- **Example**: "Milk, eggs, bread", "Schedule appointment for 2 PM", ""

#### completed (bool)
- **Type**: Boolean
- **Constraints**: True or False
- **Behavior**:
  - Default value is False (pending)
  - Toggled by mark-complete operation
  - Preserved on other operations (add, update, list)
- **Example**: False (pending), True (completed)

#### created_at (str)
- **Type**: String (ISO 8601 datetime)
- **Constraints**: Valid ISO 8601 format
- **Behavior**:
  - Set when task is created
  - Never modified after creation
  - Represents task creation moment
  - Format: "YYYY-MM-DDTHH:MM:SS" or with timezone
- **Example**: "2025-12-07T10:30:00", "2025-12-07T10:30:00Z"

#### updated_at (str)
- **Type**: String (ISO 8601 datetime)
- **Constraints**: Valid ISO 8601 format
- **Behavior**:
  - Set equal to created_at when task created
  - Updated to current time when task is modified
  - Reflects most recent modification (title, description, or completion)
  - Does NOT update on read operations (list, view)
- **Example**: "2025-12-07T10:30:00", "2025-12-07T10:45:00" (after update)

---

## Storage Structure

### In-Memory Storage

```python
# Module-level variables
tasks: List[Dict[str, Any]] = []  # List of all tasks
next_id: int = 1                   # Counter for auto-incrementing ID
```

### Storage Behavior

- **tasks**: Python list (array) containing task dictionaries
- **next_id**: Integer counter that increments with each new task
- **Memory**: All data lost on app restart (no persistence)
- **Thread Safety**: Not required for Phase 1 (single-threaded)

### Example Storage State

```python
tasks = [
  {
    "id": 1,
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": False,
    "created_at": "2025-12-07T10:00:00",
    "updated_at": "2025-12-07T10:00:00"
  },
  {
    "id": 2,
    "title": "Call mom",
    "description": "",
    "completed": True,
    "created_at": "2025-12-06T14:00:00",
    "updated_at": "2025-12-07T09:30:00"
  },
  {
    "id": 4,  # Note: ID 3 was deleted
    "title": "Fix authentication",
    "description": "OAuth setup",
    "completed": False,
    "created_at": "2025-12-07T11:00:00",
    "updated_at": "2025-12-07T11:00:00"
  }
]

next_id = 5  # Next task will get ID 5
```

---

## Operations & State Changes

### Add Task
```python
# Input
title: str          # 1-200 chars
description: str    # max 1000 chars (optional)

# Process
new_task = {
  "id": next_id,
  "title": title,
  "description": description if description else "",
  "completed": False,
  "created_at": datetime.now().isoformat(),
  "updated_at": datetime.now().isoformat()
}
tasks.append(new_task)
next_id += 1

# Output
new_task
```

### Delete Task
```python
# Input
task_id: int

# Process
tasks = [t for t in tasks if t["id"] != task_id]
# next_id unchanged

# Output
Success or error
```

### Update Task
```python
# Input
task_id: int
title: str (optional)       # 1-200 chars
description: str (optional) # max 1000 chars

# Process
for task in tasks:
  if task["id"] == task_id:
    if title is not None:
      task["title"] = title
    if description is not None:
      task["description"] = description
    task["updated_at"] = datetime.now().isoformat()
    return task

# Output
Updated task or error
```

### Mark Complete
```python
# Input
task_id: int

# Process
for task in tasks:
  if task["id"] == task_id:
    task["completed"] = not task["completed"]
    task["updated_at"] = datetime.now().isoformat()
    return task

# Output
Updated task or error
```

### View Tasks
```python
# Input
status: str (optional)  # "pending", "completed", or "all"
output_format: str      # "table" or "json"

# Process
if status == "pending":
  filtered = [t for t in tasks if t["completed"] == False]
elif status == "completed":
  filtered = [t for t in tasks if t["completed"] == True]
else:  # "all"
  filtered = tasks

# Output
formatted_output(filtered, output_format)
```

---

## Data Validation Rules

### Title Validation
```python
def validate_title(title: str) -> bool:
    """
    Title must be:
    - Non-empty and non-whitespace
    - Between 1 and 200 characters
    - Any UTF-8 characters allowed
    """
    if not title or not title.strip():
        return False
    if len(title) < 1 or len(title) > 200:
        return False
    return True
```

### Description Validation
```python
def validate_description(description: str) -> bool:
    """
    Description must be:
    - Optional (can be empty string)
    - Max 1000 characters if provided
    - Any UTF-8 characters allowed
    """
    if description is None:
        return True  # Optional field
    if len(description) <= 1000:
        return True
    return False
```

### ID Validation
```python
def validate_task_id(task_id: int, tasks: List[Dict]) -> bool:
    """
    ID must be:
    - Positive integer
    - Exist in current tasks list
    """
    if task_id <= 0:
        return False
    if not any(t["id"] == task_id for t in tasks):
        return False
    return True
```

---

## Timestamp Format

### ISO 8601 Format
- **Standard Format**: `YYYY-MM-DDTHH:MM:SS`
- **With Timezone**: `YYYY-MM-DDTHH:MM:SS+00:00` or `YYYY-MM-DDTHH:MM:SSZ`
- **Python Generation**: `datetime.datetime.now().isoformat()`
- **Example**: `2025-12-07T10:30:00` or `2025-12-07T10:30:00Z`

### Display Format
- **User Display**: `YYYY-MM-DD` (date only) for created_at in tables
- **Full Format**: Full ISO 8601 in JSON output

---

## Storage Constraints

### Phase 1 (Current)
- ❌ No persistence to disk
- ❌ No database
- ❌ No file I/O
- ❌ No caching
- ✅ In-memory Python data structures only
- ✅ Data lost on restart

### Phase 2+ (Future)
- Will migrate to PostgreSQL (Neon)
- Will add persistence
- Will support multi-user with authentication

---

## Type Hints (Python)

```python
from typing import Dict, List, Any
from datetime import datetime

# Task type definition
Task = Dict[str, Any]

# Storage type
TaskList = List[Task]

# Function signatures
def add_task(title: str, description: str = "") -> Task:
    pass

def delete_task(task_id: int) -> bool:
    pass

def update_task(task_id: int, title: str = None, description: str = None) -> Task:
    pass

def get_task(task_id: int) -> Task:
    pass

def list_tasks(status: str = "all") -> TaskList:
    pass

def mark_complete(task_id: int) -> Task:
    pass
```

---

## Example Complete Lifecycle

```python
# 1. Start with empty storage
tasks = []
next_id = 1

# 2. Add task
ADD: --title "Buy groceries" --description "Milk, eggs"
→ next_id = 2
→ tasks = [{id: 1, title: "Buy groceries", description: "Milk, eggs", completed: False, created_at: "10:00", updated_at: "10:00"}]

# 3. Add another task
ADD: --title "Call mom"
→ next_id = 3
→ tasks = [..., {id: 2, title: "Call mom", description: "", completed: False, created_at: "10:05", updated_at: "10:05"}]

# 4. Update first task
UPDATE: --id 1 --title "Buy groceries and fruits"
→ tasks[0].title = "Buy groceries and fruits"
→ tasks[0].updated_at = "10:30" (newer)

# 5. Mark first task complete
COMPLETE: --id 1
→ tasks[0].completed = True
→ tasks[0].updated_at = "10:35" (newer)

# 6. Delete second task
DELETE: --id 2
→ tasks = [tasks[0]] (id 2 removed)
→ next_id = 3 (unchanged)

# 7. Add another task
ADD: --title "New task"
→ next_id = 4
→ tasks = [..., {id: 3, ...}]

# Result: IDs are 1, 3 (2 was deleted, 4 is next)
```

---

**Version**: 1.0
**Last Updated**: 2025-12-07
**Status**: Ready for Implementation
