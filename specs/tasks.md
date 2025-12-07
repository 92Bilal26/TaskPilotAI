# Implementation Tasks: TaskPilotAI Phase 1

**Branch**: `phase-1` | **Date**: 2025-12-07 | **Deadline**: Dec 7, 2025 (TODAY)

**Input**: Implementation plan from `/specs/plan.md` and feature specifications from `/specs/features/`

**Summary**: Actionable task breakdown for Phase 1 implementation using TDD (Test-First). Tasks organized by feature with independent test criteria. All tasks follow strict checklist format with file paths for Claude Code execution.

---

## Overview

**Total Tasks**: 31 tasks across 6 phases
**Task Phases**:
- Phase 1: Project Setup (5 tasks)
- Phase 2: Foundational Infrastructure (6 tasks)
- Phase 3: Feature 1 - Add Task (5 tasks)
- Phase 4: Feature 2 - Delete Task (4 tasks)
- Phase 5: Features 3-5 - Update, View, Complete (8 tasks + 3 polish)

**Independent Test Criteria**:
- Each feature is independently testable
- Features 2-5 depend on Feature 1 (Add Task)
- Can implement Feature 1 → Test 1 → Feature 2 → Test 2 (parallel within features)

**MVP Scope**: Features 1-5 all required for Phase 1 (no MVP reduction due to deadline criticality)

---

## Phase 1: Project Setup (5 tasks)

**Goal**: Initialize project structure and configuration for Phase 1 implementation.

- [ ] T001 Create src/ package directory structure with __init__.py in `/home/bilal/TaskPilotAI/src/`
- [ ] T002 Create tests/ package directory structure with __init__.py in `/home/bilal/TaskPilotAI/tests/`
- [ ] T003 Create conftest.py fixture file for pytest in `/home/bilal/TaskPilotAI/tests/conftest.py`
- [ ] T004 Create pytest.ini configuration file in `/home/bilal/TaskPilotAI/pytest.ini`
- [ ] T005 Create .gitignore file for Python project in `/home/bilal/TaskPilotAI/.gitignore`

---

## Phase 2: Foundational Infrastructure (6 tasks)

**Goal**: Build core modules shared by all 5 features before implementing individual features.

**Independent Test Criteria**:
- models.py: Validation functions work for all field types
- storage.py: Storage state persists correctly across calls
- conftest.py: All fixtures work without errors

- [ ] T006 Create models.py with Task TypedDict definition and all validation functions in `/home/bilal/TaskPilotAI/src/models.py`
  - Include: validate_title(), validate_description(), validate_task_id()
  - All functions typed with full type hints
  - All functions have docstrings

- [ ] T007 Create storage.py with in-memory task list and next_id counter in `/home/bilal/TaskPilotAI/src/storage.py`
  - Include: tasks: List[Dict[str, Any]] = []
  - Include: next_id: int = 1
  - Include: get_task_by_id(task_id: int) -> Optional[Task] helper
  - All functions typed with full type hints

- [ ] T008 Create conftest.py pytest fixtures for test setup/teardown in `/home/bilal/TaskPilotAI/tests/conftest.py`
  - Include: empty_storage fixture (resets storage before each test)
  - Include: sample_task fixture (creates one task)
  - Include: sample_tasks fixture (creates 3+ tasks with varied states)

- [ ] T009 Create __init__.py package initializer in `/home/bilal/TaskPilotAI/src/__init__.py`
  - Mark as type-hinted package
  - Include py.typed marker file in src/

- [ ] T010 Create main.py CLI entry point skeleton in `/home/bilal/TaskPilotAI/src/main.py`
  - Include: argument parser setup (argparse)
  - Include: main() function structure
  - Include: if __name__ == "__main__" entry point
  - All functions typed with full type hints

- [ ] T011 Create commands.py feature handlers skeleton in `/home/bilal/TaskPilotAI/src/commands.py`
  - Include: Function stubs for: add_task(), delete_task(), update_task(), list_tasks(), mark_complete()
  - All functions typed with full type hints
  - All functions have placeholder docstrings

---

## Phase 3: Feature 1 - Add Task (5 tasks)

**Feature Spec**: `/specs/features/01-add-task.md`

**User Stories**:
- US1.1 (P1): Add task with title and optional description
- US1.2 (P1): Generate auto-incrementing task ID
- US1.3 (P1): Validate title length (1-200 chars)
- US1.4 (P1): Validate description length (max 1000 chars)
- US1.5 (P1): Set completion status and timestamps

**Independent Test Criteria** (all pass before moving to Feature 2):
- ✅ Task successfully added to storage with correct fields
- ✅ Next task gets incremented ID (never reused)
- ✅ Timestamps set to current UTC time with Z suffix
- ✅ Invalid titles rejected with exact error message
- ✅ Invalid descriptions rejected with exact error message
- ✅ Exit codes correct: 0 success, 1 validation error

- [ ] T012 [US1] Write comprehensive tests for add_task feature in `/home/bilal/TaskPilotAI/tests/test_add_task.py`
  - Test cases from spec acceptance criteria and edge cases (12-15 tests)
  - Include tests for: valid add, invalid title, invalid description, ID generation, timestamps
  - All tests MUST pass after implementation

- [ ] T013 [US1] Implement add_task(title: str, description: str = "") -> Task in `/home/bilal/TaskPilotAI/src/commands.py`
  - Parse and validate title (1-200 chars, non-empty)
  - Parse and validate description (max 1000 chars, default "")
  - Create Task dict with all required fields
  - Set timestamps to current UTC ISO 8601 with Z suffix
  - Append to storage.tasks list
  - Increment storage.next_id
  - Return created Task

- [ ] T014 [US1] Implement CLI add command handler in `/home/bilal/TaskPilotAI/src/main.py`
  - Parse --title (required) and --description (optional) arguments
  - Call commands.add_task()
  - Handle validation errors with exact spec messages
  - Return exit code 0 on success, 1 on error
  - Print success message: "Task {id} added: {title}"

- [ ] T015 [US1] Run tests for add_task feature and verify ≥95% coverage in `/home/bilal/TaskPilotAI/tests/test_add_task.py`
  - `pytest tests/test_add_task.py -v` passes all tests
  - `pytest tests/test_add_task.py --cov=src.commands --cov-report=term-missing` shows ≥95%
  - No coverage gaps in add_task implementation

- [ ] T016 [US1] Verify mypy and flake8 compliance for add_task code
  - `mypy src/models.py src/storage.py src/commands.py src/main.py` passes strict mode
  - `flake8 src/commands.py src/main.py` passes with no errors
  - All type hints complete, all docstrings present

---

## Phase 4: Feature 2 - Delete Task (4 tasks)

**Feature Spec**: `/specs/features/02-delete-task.md`

**Depends On**: Feature 1 (Add Task) ✅ MUST BE COMPLETE

**User Stories**:
- US2.1 (P1): Delete task by ID
- US2.2 (P1): Validate task ID exists
- US2.3 (P1): Never reuse deleted IDs
- US2.4 (P1): Handle ID validation at CLI level

**Independent Test Criteria** (all pass before moving to Feature 3):
- ✅ Task successfully deleted from storage
- ✅ next_id NOT decremented (ID never reused)
- ✅ Invalid IDs rejected with exact error message
- ✅ Non-existent task ID returns proper error
- ✅ Exit codes correct: 0 success, 1 error

- [ ] T017 [US2] Write comprehensive tests for delete_task feature in `/home/bilal/TaskPilotAI/tests/test_delete_task.py`
  - Test cases from spec acceptance criteria and edge cases (8-10 tests)
  - Include tests for: valid delete, non-existent ID, invalid ID format, ID validation
  - All tests MUST pass after implementation

- [ ] T018 [US2] Implement delete_task(task_id: int) -> bool in `/home/bilal/TaskPilotAI/src/commands.py`
  - Validate task_id is positive integer
  - Check task exists in storage
  - Remove task from storage.tasks list
  - Return True on success
  - Raise exception or return error indicator on failure

- [ ] T019 [US2] Implement CLI delete command handler in `/home/bilal/TaskPilotAI/src/main.py`
  - Parse --id (required) argument with validation
  - Validate ID is numeric and positive (CLI-level validation)
  - Call commands.delete_task()
  - Handle errors with exact spec messages
  - Return exit code 0 on success, 1 on error
  - Print success message: "Task {id} deleted"

- [ ] T020 [US2] Run tests for delete_task feature and verify coverage in `/home/bilal/TaskPilotAI/tests/test_delete_task.py`
  - `pytest tests/test_delete_task.py -v` passes all tests
  - `pytest tests/test_delete_task.py --cov=src.commands --cov-report=term-missing` shows ≥95%
  - `mypy src/` and `flake8 src/` pass strict standards

---

## Phase 5: Features 3-5 - Update, View, Complete (8 tasks)

**Goal**: Implement remaining 3 features (Update Task, View Tasks, Mark Complete) with TDD methodology.

### Feature 3: Update Task

**Feature Spec**: `/specs/features/03-update-task.md`

**Depends On**: Feature 1 (Add Task) ✅ MUST BE COMPLETE

**User Stories**:
- US3.1 (P1): Update task title
- US3.2 (P1): Update task description
- US3.3 (P1): Update both fields
- US3.4 (P1): Validate updated fields
- US3.5 (P1): Update timestamp on modification

**Independent Test Criteria** (all pass before moving to Feature 4):
- ✅ Task fields updated correctly (title and/or description)
- ✅ updated_at timestamp changed to current UTC time
- ✅ Other fields (id, created_at, completed) unchanged
- ✅ Validation same as add_task (title 1-200, description max 1000)
- ✅ Exit codes correct: 0 success, 1 error

- [ ] T021 [US3] Write comprehensive tests for update_task feature in `/home/bilal/TaskPilotAI/tests/test_update_task.py`
  - Test cases from spec acceptance criteria and edge cases (12-15 tests)
  - Include tests for: update title only, description only, both, validation, timestamp update
  - All tests MUST pass after implementation

- [ ] T022 [US3] Implement update_task(task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> Task in `/home/bilal/TaskPilotAI/src/commands.py`
  - Validate task_id exists
  - Validate title (if provided): 1-200 chars
  - Validate description (if provided): max 1000 chars
  - Require at least one field to update
  - Update matching fields in task
  - Set updated_at to current UTC time
  - Return updated Task

- [ ] T023 [US3] Implement CLI update command handler in `/home/bilal/TaskPilotAI/src/main.py`
  - Parse --id (required), --title (optional), --description (optional) arguments
  - Validate --id is numeric and positive (CLI-level)
  - Require at least one of --title or --description
  - Call commands.update_task()
  - Handle errors with exact spec messages
  - Return exit code 0 on success, 1 on error
  - Print success message: "Task {id} updated"

- [ ] T024 [US3] Run tests for update_task feature and verify coverage in `/home/bilal/TaskPilotAI/tests/test_update_task.py`
  - `pytest tests/test_update_task.py -v` passes all tests
  - `pytest tests/test_update_task.py --cov=src.commands --cov-report=term-missing` shows ≥95%
  - `mypy src/` and `flake8 src/` pass strict standards

### Feature 4: View Tasks

**Feature Spec**: `/specs/features/04-view-tasks.md`

**User Stories**:
- US4.1 (P1): Display all tasks in table format
- US4.2 (P1): Filter tasks by status (pending/completed)
- US4.3 (P2): Display tasks as JSON
- US4.4 (P1): Handle empty task list gracefully

**Independent Test Criteria** (all pass before moving to Feature 5):
- ✅ Table format displays all tasks with proper columns (ID, Title, Status, Created)
- ✅ Status filter works (pending, completed, all)
- ✅ JSON output is valid JSON array
- ✅ Empty list returns "No tasks" (not error)
- ✅ Exit codes correct: 0 success even if empty, 1 on invalid args

- [ ] T025 [US4] Write comprehensive tests for view_tasks feature in `/home/bilal/TaskPilotAI/tests/test_view_tasks.py`
  - Test cases from spec acceptance criteria and edge cases (12-15 tests)
  - Include tests for: display all, filter pending, filter completed, JSON output, empty list
  - All tests MUST pass after implementation

- [ ] T026 [US4] Implement list_tasks(status: str = "all") -> List[Task] and formatting functions in `/home/bilal/TaskPilotAI/src/commands.py`
  - Filter tasks by status (pending=False, completed=True, all=both)
  - Return filtered task list
  - Create format_table(tasks: List[Task]) -> str function for table display
  - Create format_json(tasks: List[Task]) -> str function for JSON output
  - Handle empty list case

- [ ] T027 [US4] Implement CLI list command handler in `/home/bilal/TaskPilotAI/src/main.py`
  - Parse --status (optional, default "all") and --json (optional flag) arguments
  - Validate --status value (pending, completed, all)
  - Call commands.list_tasks()
  - Format output as table (default) or JSON (--json flag)
  - Print "No tasks" if list empty (not error)
  - Return exit code 0 always (even if empty)

- [ ] T028 [US4] Run tests for view_tasks feature and verify coverage in `/home/bilal/TaskPilotAI/tests/test_view_tasks.py`
  - `pytest tests/test_view_tasks.py -v` passes all tests
  - `pytest tests/test_view_tasks.py --cov=src.commands --cov-report=term-missing` shows ≥95%
  - `mypy src/` and `flake8 src/` pass strict standards

### Feature 5: Mark Complete

**Feature Spec**: `/specs/features/05-mark-complete.md`

**User Stories**:
- US5.1 (P1): Toggle task completion status (pending → completed)
- US5.2 (P1): Toggle task back to pending
- US5.3 (P1): Validate task ID exists
- US5.4 (P2): Update timestamp on toggle

**Independent Test Criteria** (all pass):
- ✅ Task completion status toggled correctly
- ✅ Success message reflects new status (completed or pending)
- ✅ updated_at timestamp changed
- ✅ Other fields unchanged
- ✅ Exit codes correct: 0 success, 1 error

- [ ] T029 [US5] Write comprehensive tests for mark_complete feature in `/home/bilal/TaskPilotAI/tests/test_mark_complete.py`
  - Test cases from spec acceptance criteria and edge cases (10-12 tests)
  - Include tests for: pending→completed, completed→pending, validation, timestamp
  - All tests MUST pass after implementation

- [ ] T030 [US5] Implement mark_complete(task_id: int) -> Task in `/home/bilal/TaskPilotAI/src/commands.py`
  - Validate task_id exists
  - Toggle completed status: True → False or False → True
  - Set updated_at to current UTC time
  - Return updated Task

- [ ] T031 [US5] Implement CLI complete command handler in `/home/bilal/TaskPilotAI/src/main.py`
  - Parse --id (required) argument with validation
  - Validate --id is numeric and positive (CLI-level)
  - Call commands.mark_complete()
  - Determine new status (completed or pending)
  - Print appropriate success message
  - Return exit code 0 on success, 1 on error

---

## Phase 6: Quality Verification & Polish (3 tasks)

**Goal**: Verify all features pass quality gates and prepare for submission.

**Independent Test Criteria** (all must pass):
- ✅ All 5 features have ≥95% code coverage
- ✅ mypy strict mode passes with zero type errors
- ✅ flake8 PEP 8 linting passes
- ✅ All error messages match spec exactly
- ✅ All exit codes correct (0, 1, 2)

- [ ] T032 Run full test suite with coverage report for all features
  - `pytest -v --cov=src --cov-report=html` from repo root
  - Verify ≥95% overall coverage
  - Identify any coverage gaps and fill them
  - Generate and verify htmlcov/index.html

- [ ] T033 Run mypy strict type checking on all source files
  - `mypy src/` passes with zero errors
  - Verify all functions have complete type hints
  - Verify no "Any" types without justification

- [ ] T034 Run flake8 PEP 8 linting on all source and test files
  - `flake8 src/ tests/` passes with no errors
  - Verify line length (max 100 chars)
  - Verify no unused imports or variables

- [ ] T035 [Final] Create PHR (Prompt History Record) documenting implementation phase
  - Log all implementation decisions
  - Document any modifications to specs during implementation
  - List all files created and modified
  - Include test coverage results

- [ ] T036 [Final] Create demo video (<90 seconds) showing all 5 commands in action
  - Run: `python src/main.py add --title "Test Task"`
  - Run: `python src/main.py list`
  - Run: `python src/main.py complete --id 1`
  - Run: `python src/main.py update --id 1 --title "Updated"`
  - Run: `python src/main.py delete --id 1`
  - Show exit codes and output clearly

- [ ] T037 [Final] Push code to GitHub and submit Phase 1 form
  - Commit all changes with clear messages
  - Push to `phase-1` branch
  - Submit GitHub repo URL to: https://forms.gle/KMKEKaFUD6ZX4UtY8
  - Include demo video link and contact info

---

## Execution Strategy

### Recommended Parallel Execution (Within Features)

After Phase 2 (Foundational) complete:

**Option 1: Feature-by-Feature (RECOMMENDED for deadline)**
1. Feature 1 (Add): T012-T016 sequential
2. Feature 2 (Delete): T017-T020 sequential (after Feature 1 ✅)
3. Feature 3 (Update): T021-T024 sequential (after Feature 1 ✅)
4. Feature 4 (View): T025-T028 sequential (independent)
5. Feature 5 (Complete): T029-T031 sequential (independent)
6. Quality: T032-T037 sequential (after all features)

**Parallelization Opportunities**:
- ✅ Feature 4 (View) can start in parallel with Feature 2 (Delete) - no dependencies
- ✅ Feature 5 (Complete) can start in parallel with Feature 3 (Update) - no dependencies
- ❌ Cannot parallelize Feature 1 - all others depend on it

### Estimated Time Breakdown

| Phase | Tasks | Est. Time | Notes |
|-------|-------|-----------|-------|
| Phase 1 (Setup) | T001-T005 | 15 min | Quick directory structure |
| Phase 2 (Foundation) | T006-T011 | 30 min | Shared models, storage, fixtures |
| Phase 3 (Add Task) | T012-T016 | 60 min | First complete feature with tests |
| Phase 4 (Delete Task) | T017-T020 | 40 min | Shorter, depends on Phase 3 |
| Phase 5a (Update) | T021-T024 | 50 min | Similar complexity to Add |
| Phase 5b (View) | T025-T028 | 55 min | UI formatting adds complexity |
| Phase 5c (Complete) | T029-T031 | 40 min | Simple toggle operation |
| Phase 6 (Quality) | T032-T037 | 30 min | Testing and finalization |
| **TOTAL** | **31 tasks** | **~5 hours** | **Deadline-critical** |

**Deadline**: Today (Dec 7, 2025) - approximately 8 hours remaining
**Status**: On track if execution maintains pace

---

## Task Dependencies Graph

```
T001-T005 (Setup)
    ↓
T006-T011 (Foundation: models, storage, fixtures)
    ↓
T012-T016 (Feature 1: Add Task) ← CRITICAL PATH
    ↓
    ├→ T017-T020 (Feature 2: Delete Task)
    ├→ T021-T024 (Feature 3: Update Task)
    │
    ├→ [PARALLEL] T025-T028 (Feature 4: View Tasks)
    └→ [PARALLEL] T029-T031 (Feature 5: Mark Complete)
    ↓
T032-T037 (Quality & Submission)
```

---

## Success Criteria (Post-Implementation)

### Functional Success
- [ ] All 5 commands execute correctly: `add`, `delete`, `update`, `list`, `complete`
- [ ] All user stories from specs have working implementations
- [ ] All acceptance criteria from specs pass
- [ ] All error cases handled with exact spec messages
- [ ] All exit codes correct (0, 1, 2)

### Quality Success
- [ ] Test coverage ≥95% across all modules
- [ ] mypy strict mode: 0 type errors
- [ ] flake8: 0 linting errors
- [ ] All docstrings present and accurate
- [ ] All type hints complete

### Documentation Success
- [ ] README.md complete and accurate
- [ ] CLAUDE.md complete with development guide
- [ ] specs/ directory fully detailed
- [ ] contracts/ fully specified
- [ ] Git history clean with meaningful commits

### Submission Success
- [ ] Code pushed to `phase-1` branch on GitHub
- [ ] Form submitted with all required fields
- [ ] Demo video created (<90 seconds)
- [ ] All quality gates passed before submission

---

**Version**: 1.0
**Last Updated**: 2025-12-07
**Status**: Ready for Implementation
**Next Command**: `/sp.implement` (execute tasks sequentially with TDD)
