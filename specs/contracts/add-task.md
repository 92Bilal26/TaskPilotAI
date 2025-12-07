# Contract: Add Task

**Feature**: 01-add-task
**Command**: `python main.py add [--title <str>] [--description <str>]`

## Input Contract

```
Required Arguments:
  --title TEXT              Task title (1-200 characters, required)

Optional Arguments:
  --description TEXT        Task description (max 1000 characters, optional)

Exit Codes:
  0: Success
  1: Validation error (missing title, invalid length)
  2: System error
```

## Output Contract - Success

```
Task {id} added: {title}
```

**Example**:
```
Task 1 added: Buy groceries
Task 2 added: Call mom
```

## Output Contract - Error

```
Error: Title required (1-200 characters)
Error: Description max 1000 characters
Error: --title is required
```

## Data Contract (Storage Impact)

**Input**:
```python
{
  "title": str,              # 1-200 chars, non-empty
  "description": str | None  # optional, max 1000 chars
}
```

**Output** (Task created in storage):
```python
{
  "id": int,                           # auto-incremented from next_id
  "title": str,                        # unchanged from input
  "description": str,                  # empty string if not provided
  "completed": False,                  # always starts as pending
  "created_at": str,                   # ISO 8601 UTC (e.g., "2025-12-07T10:30:00Z")
  "updated_at": str                    # same as created_at initially
}
```

## State Changes

- `next_id` incremented by 1
- New task appended to `tasks` list
- Task ID never reused (even after deletion)

## Example Workflows

### Happy Path: Add task with title only
```bash
$ python main.py add --title "Buy groceries"
Task 1 added: Buy groceries
$ echo $?
0
```

### Happy Path: Add task with title and description
```bash
$ python main.py add --title "Buy groceries" --description "Milk, eggs, bread"
Task 2 added: Buy groceries
$ echo $?
0
```

### Error Path: Missing required title
```bash
$ python main.py add --description "Some description"
Error: --title is required
$ echo $?
1
```

### Error Path: Title too long (>200 chars)
```bash
$ python main.py add --title "$(python -c 'print("A" * 201)')"
Error: Title required (1-200 characters)
$ echo $?
1
```

### Error Path: Description too long (>1000 chars)
```bash
$ python main.py add --title "Task" --description "$(python -c 'print("A" * 1001)')"
Error: Description max 1000 characters
$ echo $?
1
```
