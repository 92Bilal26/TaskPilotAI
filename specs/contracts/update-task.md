# Contract: Update Task

**Feature**: 03-update-task
**Command**: `python main.py update --id <int> [--title <str>] [--description <str>]`

## Input Contract

```
Required Arguments:
  --id INT                  Task ID to update (positive integer, required)

Optional Arguments:
  --title TEXT              New task title (1-200 characters, optional)
  --description TEXT        New task description (max 1000 characters, optional)

Constraints:
  - At least one of --title or --description must be provided
  - Cannot update both fields to empty/missing

Exit Codes:
  0: Success
  1: Task not found, invalid ID, or validation error
  2: System error
```

## Output Contract - Success

```
Task {id} updated
```

**Example**:
```
Task 1 updated
Task 3 updated
```

## Output Contract - Error

```
Error: Task ID {id} not found
Error: --id is required
Error: Invalid ID format. Use --id <number>
Error: ID must be positive integer
Error: Title required (1-200 characters)
Error: Description max 1000 characters
Error: At least one of --title or --description required
```

## Data Contract (Storage Impact)

**Input**:
```python
{
  "task_id": int,                    # positive integer, must exist
  "title": str | None,               # optional, 1-200 chars if provided
  "description": str | None          # optional, max 1000 chars if provided
}
```

**Output** (Task modified in storage):
```python
{
  "id": int,                         # UNCHANGED
  "title": str,                      # CHANGED if --title provided, else unchanged
  "description": str,                # CHANGED if --description provided, else unchanged
  "completed": bool,                 # UNCHANGED
  "created_at": str,                 # UNCHANGED
  "updated_at": str                  # CHANGED to current UTC time
}
```

## State Changes

- Task fields updated (title and/or description)
- `updated_at` set to current ISO 8601 UTC timestamp
- `created_at`, `id`, `completed` never modified
- Other tasks unaffected

## Example Workflows

### Happy Path: Update title only
```bash
$ python main.py update --id 1 --title "Buy groceries and fruits"
Task 1 updated
$ echo $?
0
```

### Happy Path: Update description only
```bash
$ python main.py update --id 1 --description "New description here"
Task 1 updated
$ echo $?
0
```

### Happy Path: Update both title and description
```bash
$ python main.py update --id 1 --title "New Title" --description "New Description"
Task 1 updated
$ echo $?
0
```

### Error Path: Missing task ID
```bash
$ python main.py update --title "New Title"
Error: --id is required
$ echo $?
1
```

### Error Path: Non-existent task ID
```bash
$ python main.py update --id 999 --title "New Title"
Error: Task ID 999 not found
$ echo $?
1
```

### Error Path: Invalid title (too long)
```bash
$ python main.py update --id 1 --title "$(python -c 'print("A" * 201)')"
Error: Title required (1-200 characters)
$ echo $?
1
```

### Error Path: Invalid description (too long)
```bash
$ python main.py update --id 1 --description "$(python -c 'print("A" * 1001)')"
Error: Description max 1000 characters
$ echo $?
1
```

### Error Path: No fields to update
```bash
$ python main.py update --id 1
Error: At least one of --title or --description required
$ echo $?
1
```

### Error Path: Negative ID
```bash
$ python main.py update --id -1 --title "New"
Error: ID must be positive integer
$ echo $?
1
```

## Timestamp Guarantee

When task is updated, `updated_at` is set to current time (never updated on read operations like list).
