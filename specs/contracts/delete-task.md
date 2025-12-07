# Contract: Delete Task

**Feature**: 02-delete-task
**Command**: `python main.py delete --id <int>`

## Input Contract

```
Required Arguments:
  --id INT                  Task ID to delete (positive integer, required)

Exit Codes:
  0: Success
  1: Task not found or invalid ID
  2: System error
```

## Output Contract - Success

```
Task {id} deleted
```

**Example**:
```
Task 1 deleted
Task 3 deleted
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

**Output** (Task removed from storage):
```python
# Task removed from tasks list
# next_id unchanged (never reset or decremented)
# Remaining tasks: unchanged
```

## State Changes

- Task with matching ID removed from `tasks` list
- `next_id` unchanged (IDs never reused)
- Other tasks unaffected

## Example Workflows

### Happy Path: Delete existing task
```bash
$ python main.py delete --id 1
Task 1 deleted
$ echo $?
0
```

### Happy Path: Delete non-first task
```bash
$ python main.py delete --id 3
Task 3 deleted
$ echo $?
0
```

### Error Path: Missing required ID
```bash
$ python main.py delete
Error: --id is required
$ echo $?
1
```

### Error Path: Non-existent task ID
```bash
$ python main.py delete --id 999
Error: Task ID 999 not found
$ echo $?
1
```

### Error Path: Negative ID
```bash
$ python main.py delete --id -1
Error: ID must be positive integer
$ echo $?
1
```

### Error Path: Invalid ID format (non-numeric)
```bash
$ python main.py delete --id "abc"
Error: Invalid ID format. Use --id <number>
$ echo $?
1
```

### Error Path: Zero ID
```bash
$ python main.py delete --id 0
Error: ID must be positive integer
$ echo $?
1
```

## ID Sequence Guarantee

After deleting task ID 2 from [1, 2, 3], storage is [1, 3]. Next add creates task 4 (not 2). IDs are never reused.
