# Contract: Mark Task as Complete

**Feature**: 05-mark-complete
**Command**: `python main.py complete --id <int>`

## Input Contract

```
Required Arguments:
  --id INT                  Task ID to toggle completion (positive integer, required)

Exit Codes:
  0: Success
  1: Task not found or invalid ID
  2: System error
```

## Output Contract - Success

```
Task {id} marked as completed

OR

Task {id} marked as pending
```

**Example**:
```
Task 1 marked as completed
Task 1 marked as pending
```

## Output Contract - Error

```
Error: Task ID {id} not found
Error: --id is required
Error: Invalid ID format. Use --id <number>
Error: ID must be positive integer
```

## Data Contract (Storage Impact)

**Input**:
```python
{
  "task_id": int  # positive integer, must exist in storage
}
```

**Output** (Task modified in storage):
```python
{
  "id": int,                           # UNCHANGED
  "title": str,                        # UNCHANGED
  "description": str,                  # UNCHANGED
  "completed": bool,                   # CHANGED (toggled: True→False or False→True)
  "created_at": str,                   # UNCHANGED
  "updated_at": str                    # CHANGED to current UTC time
}
```

## State Changes

- `completed` toggled: False → True or True → False
- `updated_at` set to current ISO 8601 UTC timestamp
- All other fields unchanged
- Other tasks unaffected

## Example Workflows

### Happy Path: Mark pending task as completed
```bash
$ python main.py complete --id 1
Task 1 marked as completed
$ echo $?
0
```

### Happy Path: Mark completed task as pending (toggle back)
```bash
$ python main.py complete --id 1
Task 1 marked as pending
$ echo $?
0
```

### Happy Path: Toggle multiple times
```bash
$ python main.py complete --id 1
Task 1 marked as completed
$ python main.py complete --id 1
Task 1 marked as pending
$ python main.py complete --id 1
Task 1 marked as completed
$ echo $?
0
```

### Error Path: Missing required ID
```bash
$ python main.py complete
Error: --id is required
$ echo $?
1
```

### Error Path: Non-existent task ID
```bash
$ python main.py complete --id 999
Error: Task ID 999 not found
$ echo $?
1
```

### Error Path: Negative ID
```bash
$ python main.py complete --id -1
Error: ID must be positive integer
$ echo $?
1
```

### Error Path: Zero ID
```bash
$ python main.py complete --id 0
Error: ID must be positive integer
$ echo $?
1
```

### Error Path: Invalid ID format (non-numeric)
```bash
$ python main.py complete --id "abc"
Error: Invalid ID format. Use --id <number>
$ echo $?
1
```

## Timestamp Guarantee

When task completion status is toggled, `updated_at` is set to current time. Other fields remain identical.

## Toggle Behavior

- **First toggle**: pending (False) → completed (True)
  - Message: "Task {id} marked as completed"
- **Second toggle**: completed (True) → pending (False)
  - Message: "Task {id} marked as pending"
- **Repeatable**: Can toggle unlimited times in either direction
