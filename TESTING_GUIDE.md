# Phase 1 Testing Guide - Manual Command Verification

**Date**: 2025-12-07
**Status**: All 5 commands ready for testing
**Branch**: `phase-1`

---

## Quick Start (5 minutes)

### 1. Install Dependencies

```bash
cd /home/bilal/TaskPilotAI
/home/bilal/.local/bin/uv sync --all-extras
```

### 2. Verify Installation

```bash
/home/bilal/.local/bin/uv run pytest tests/ -v --tb=short
```

Expected output: `84 passed in 0.30s` ✅

---

## Testing All 5 Commands (Demo Script)

Run these commands in sequence to test all features. Each command demonstrates a specific feature.

### Command 1: ADD TASK ✅

**What it does**: Create a new task with title and optional description

```bash
/home/bilal/.local/bin/uv run python src/main.py add --title "Buy groceries" --description "Milk, eggs, bread"
```

**Expected Output**:
```
Task 1 added: Buy groceries
```

**What to verify**:
- ✅ Task ID is 1 (first task)
- ✅ Title is exactly "Buy groceries"
- ✅ Exit code is 0 (success)

**Check exit code**:
```bash
/home/bilal/.local/bin/uv run python src/main.py add --title "Buy groceries" --description "Milk, eggs, bread" && echo "Exit code: $?"
```

---

### Command 2: ADD ANOTHER TASK ✅

**What it does**: Add second task to demonstrate ID incrementing

```bash
/home/bilal/.local/bin/uv run python src/main.py add --title "Call mom"
```

**Expected Output**:
```
Task 2 added: Call mom
```

**What to verify**:
- ✅ Task ID is 2 (auto-increment works)
- ✅ Description is optional (defaults to empty)
- ✅ Exit code is 0

---

### Command 3: VIEW ALL TASKS (TABLE FORMAT) ✅

**What it does**: Display all tasks in human-readable table

```bash
/home/bilal/.local/bin/uv run python src/main.py list
```

**Expected Output**:
```
ID | Title         | Status | Created
1  | Buy groceries | pending | 2025-12-07
2  | Call mom      | pending | 2025-12-07
```

**What to verify**:
- ✅ Both tasks shown
- ✅ Table has columns: ID | Title | Status | Created
- ✅ Status is "pending" (not completed)
- ✅ Date is YYYY-MM-DD format (no time)
- ✅ Exit code is 0

---

### Command 4: VIEW AS JSON ✅

**What it does**: Display tasks in JSON format for programmatic access

```bash
/home/bilal/.local/bin/uv run python src/main.py list --json
```

**Expected Output**:
```json
[
  {
    "id": 1,
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false,
    "created_at": "2025-12-07T...:...Z",
    "updated_at": "2025-12-07T...:...Z"
  },
  {
    "id": 2,
    "title": "Call mom",
    "description": "",
    "completed": false,
    "created_at": "2025-12-07T...:...Z",
    "updated_at": "2025-12-07T...:...Z"
  }
]
```

**What to verify**:
- ✅ Valid JSON array format
- ✅ All 5 fields present: id, title, description, completed, created_at, updated_at
- ✅ Timestamps have Z suffix (UTC)
- ✅ Timestamps have T separator (ISO 8601)
- ✅ Exit code is 0

---

### Command 5: UPDATE TASK ✅

**What it does**: Modify task title and/or description

```bash
/home/bilal/.local/bin/uv run python src/main.py update --id 1 --title "Buy groceries and fruits"
```

**Expected Output**:
```
Task 1 updated
```

**What to verify**:
- ✅ Task 1 is updated (correct ID)
- ✅ Title changed to "Buy groceries and fruits"
- ✅ Exit code is 0

**Verify the update worked**:
```bash
/home/bilal/.local/bin/uv run python src/main.py list
```

Expected output shows: `Buy groceries and fruits` (updated title)

---

### Command 6: MARK TASK COMPLETE ✅

**What it does**: Toggle completion status (pending → completed)

```bash
/home/bilal/.local/bin/uv run python src/main.py complete --id 1
```

**Expected Output**:
```
Task 1 marked as completed
```

**What to verify**:
- ✅ Task 1 marked as completed
- ✅ Exit code is 0

**Verify in list**:
```bash
/home/bilal/.local/bin/uv run python src/main.py list
```

Expected output shows task 1 with status: `completed` ✅

---

### Command 7: FILTER BY STATUS ✅

**What it does**: Show only pending tasks

```bash
/home/bilal/.local/bin/uv run python src/main.py list --status pending
```

**Expected Output**:
```
ID | Title   | Status | Created
2  | Call mom | pending | 2025-12-07
```

**What to verify**:
- ✅ Only task 2 shown (task 1 is completed, hidden)
- ✅ Status is "pending"
- ✅ Exit code is 0

---

### Command 8: DELETE TASK ✅

**What it does**: Remove task by ID

```bash
/home/bilal/.local/bin/uv run python src/main.py delete --id 2
```

**Expected Output**:
```
Task 2 deleted
```

**What to verify**:
- ✅ Task 2 deleted
- ✅ Exit code is 0

**Verify deletion**:
```bash
/home/bilal/.local/bin/uv run python src/main.py list
```

Expected output: Only task 1 remains

---

### Command 9: ERROR HANDLING - INVALID ID ✅

**What it does**: Test error handling with non-existent task

```bash
/home/bilal/.local/bin/uv run python src/main.py delete --id 999
```

**Expected Output**:
```
Error: Task ID 999 not found
```

**What to verify**:
- ✅ Error message starts with "Error: "
- ✅ Message is specific: "Task ID 999 not found"
- ✅ Exit code is 1 (error code)

**Check exit code**:
```bash
/home/bilal/.local/bin/uv run python src/main.py delete --id 999 || echo "Exit code: $?"
```

---

### Command 10: ERROR HANDLING - MISSING REQUIRED ARG ✅

**What it does**: Test error when --id is missing

```bash
/home/bilal/.local/bin/uv run python src/main.py delete
```

**Expected Output**:
```
Error: --id is required
```

**What to verify**:
- ✅ Error message: "--id is required"
- ✅ Exit code is 1

---

## Complete Testing Sequence (Copy & Paste)

Run all commands in order:

```bash
#!/bin/bash
cd /home/bilal/TaskPilotAI

echo "=== TEST 1: Add first task ==="
/home/bilal/.local/bin/uv run python src/main.py add --title "Buy groceries" --description "Milk, eggs, bread"

echo ""
echo "=== TEST 2: Add second task ==="
/home/bilal/.local/bin/uv run python src/main.py add --title "Call mom"

echo ""
echo "=== TEST 3: List all tasks (table) ==="
/home/bilal/.local/bin/uv run python src/main.py list

echo ""
echo "=== TEST 4: List as JSON ==="
/home/bilal/.local/bin/uv run python src/main.py list --json

echo ""
echo "=== TEST 5: Update task 1 ==="
/home/bilal/.local/bin/uv run python src/main.py update --id 1 --title "Buy groceries and fruits"

echo ""
echo "=== TEST 6: Verify update in list ==="
/home/bilal/.local/bin/uv run python src/main.py list

echo ""
echo "=== TEST 7: Mark task 1 complete ==="
/home/bilal/.local/bin/uv run python src/main.py complete --id 1

echo ""
echo "=== TEST 8: List pending tasks only ==="
/home/bilal/.local/bin/uv run python src/main.py list --status pending

echo ""
echo "=== TEST 9: Delete task 2 ==="
/home/bilal/.local/bin/uv run python src/main.py delete --id 2

echo ""
echo "=== TEST 10: Verify deletion ==="
/home/bilal/.local/bin/uv run python src/main.py list

echo ""
echo "=== ALL TESTS COMPLETE ==="
```

---

## Quality Verification Commands

### Run All Unit Tests

```bash
/home/bilal/.local/bin/uv run pytest tests/ -v
```

Expected: `84 passed in 0.30s` ✅

### Run Tests with Coverage Report

```bash
/home/bilal/.local/bin/uv run pytest tests/ --cov=src --cov-report=term-missing
```

Expected: Coverage ~97.5% for commands.py ✅

### Type Checking (mypy)

```bash
/home/bilal/.local/bin/uv run mypy src/
```

Expected: `Success: no issues found in 5 source files` ✅

### Code Style Checking (flake8)

```bash
/home/bilal/.local/bin/uv run flake8 src/ tests/ --max-line-length=100
```

Expected: No output (all checks pass) ✅

---

## Creating Demo Video

When recording your demo video (<90 seconds), follow this script:

### Video Script (90 seconds)

**Opening (5 sec)**:
- Show the terminal with `/home/bilal/TaskPilotAI` as working directory
- Say: "I'm demonstrating TaskPilotAI Phase 1 with all 5 features"

**Feature 1: Add Task (15 sec)**:
```bash
/home/bilal/.local/bin/uv run python src/main.py add --title "Buy groceries" --description "Milk, eggs, bread"
/home/bilal/.local/bin/uv run python src/main.py add --title "Call dentist"
```
- Narrate: "Creating two tasks. Each gets an auto-incrementing ID."

**Feature 4: View Tasks (10 sec)**:
```bash
/home/bilal/.local/bin/uv run python src/main.py list
```
- Narrate: "Listing all tasks in table format. ID, title, status, and creation date."

**Feature 5: Mark Complete (10 sec)**:
```bash
/home/bilal/.local/bin/uv run python src/main.py complete --id 1
/home/bilal/.local/bin/uv run python src/main.py list
```
- Narrate: "Marking task 1 complete. Status changed from pending to completed."

**Feature 3: Update Task (10 sec)**:
```bash
/home/bilal/.local/bin/uv run python src/main.py update --id 2 --title "Call dentist and check teeth"
/home/bilal/.local/bin/uv run python src/main.py list
```
- Narrate: "Updating task title. Timestamp is updated automatically."

**Feature 2: Delete Task (10 sec)**:
```bash
/home/bilal/.local/bin/uv run python src/main.py delete --id 2
/home/bilal/.local/bin/uv run python src/main.py list
```
- Narrate: "Deleting task 2. IDs are never reused."

**Feature 4 Bonus: JSON Output (10 sec)**:
```bash
/home/bilal/.local/bin/uv run python src/main.py list --json
```
- Narrate: "JSON output for programmatic access. Full timestamps in ISO 8601 format."

**Closing (10 sec)**:
- Show: `git log --oneline -5`
- Say: "All code is version controlled with meaningful commits. Ready for submission."

**Total: ~90 seconds** ✅

---

## Testing Checklist for Video

- [ ] Feature 1 (Add): Creates tasks with auto-incrementing IDs
- [ ] Feature 2 (Delete): Removes tasks, IDs never reused
- [ ] Feature 3 (Update): Modifies title/description, updates timestamps
- [ ] Feature 4 (View): Table and JSON output, status filtering
- [ ] Feature 5 (Mark Complete): Toggles completion status
- [ ] Error Handling: Shows "Error: " messages with exit code 1
- [ ] Exit Codes: 0 for success, 1 for errors
- [ ] Timestamps: UTC format with Z suffix
- [ ] Data Persistence: Changes survive within session

---

## Submit to Hackathon

**URL**: https://forms.gle/KMKEKaFUD6ZX4UtY8

**Required Info**:
1. **GitHub Repo**: https://github.com/92Bilal26/TaskPilotAI
2. **Branch**: `phase-1`
3. **Demo Video**: Upload <90 second video
4. **WhatsApp**: Your contact number

---

## Quality Assurance Checklist

- [x] All 5 commands work correctly
- [x] 84/84 tests pass
- [x] mypy: 0 type errors
- [x] flake8: 0 style errors
- [x] Code coverage: 97.5%
- [x] Error messages match spec
- [x] Exit codes correct (0, 1, 2)
- [x] UTC timestamps with Z suffix
- [x] No external dependencies
- [x] All 8 constitution gates pass

---

**Status**: ✅ Ready for submission

**Last Updated**: 2025-12-07
**Next Step**: Record demo video and submit form
