# Implementation Plan: TaskPilotAI Phase 1

**Branch**: `phase-1` | **Date**: 2025-12-07 | **Spec**: `/specs/` | **Deadline**: Dec 7, 2025

**Input**: Phase 1 comprehensive specifications from `/specs/features/` and `/specs/data-models.md`

**Summary**: Build an in-memory Python 3.13 CLI todo application with 5 core features (add, delete, update, view, complete). All features share a unified Task data model with auto-incrementing IDs, ISO 8601 timestamps (UTC), and comprehensive validation. Implementation uses test-first (TDD) methodology with ≥95% code coverage. Zero external runtime dependencies; CLI arguments only (no interactive menu or persistence).

---

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: None (standard library only)
**Storage**: In-memory Python list (no persistence)
**Testing**: pytest + pytest-cov (≥95% coverage required)
**Type Checking**: mypy strict mode (100% compliance required)
**Linting**: flake8 (PEP 8 compliance required)
**Target Platform**: Linux/macOS/Windows (cross-platform CLI)
**Project Type**: Single Python package with CLI entry point
**Performance Goals**: Instant response (<100ms per operation)
**Constraints**: No external dependencies, no database, in-memory only
**Scale/Scope**: Phase 1 MVP with 5 basic features, max ~500 lines implementation code

---

## Constitution Check

**GATE: Must pass before Phase 1 implementation. Re-check after all features complete.**

### Gate 1: Spec-Driven Development
- ✅ All 5 feature specs written with user stories, acceptance criteria, edge cases
- ✅ Data model spec complete with validation rules and lifecycle
- ✅ No design decisions ahead of written specs

### Gate 2: Test-First (TDD) Required
- ✅ Test files created BEFORE implementation (Red phase)
- ✅ Tests based directly on spec acceptance criteria
- ✅ All tests must pass (Green phase)
- ✅ Coverage ≥95% across all 5 features

### Gate 3: In-Memory Storage Only
- ✅ Module-level `tasks: List[Dict[str, Any]]` and `next_id: int`
- ✅ No file I/O, no database, no caching to disk
- ✅ Data lost on app restart

### Gate 4: Clean Code Standards
- ✅ 100% type hints on all functions and variables
- ✅ Docstrings for all public functions and classes
- ✅ PEP 8 compliant (enforced by flake8)
- ✅ mypy strict mode passes (zero type errors)
- ✅ No unused imports, variables, or functions

### Gate 5: CLI-First (No Manual Prompts)
- ✅ All input via `python main.py <command> [--arg value]`
- ✅ No interactive menu, no stdin prompts
- ✅ No config files or environment variable configuration

### Gate 6: Error Handling & Exit Codes
- ✅ All error messages prefixed with "Error: "
- ✅ Exit code 0 on success, 1 on validation/user error, 2 on system error
- ✅ Error messages match spec exactly

### Gate 7: No External Dependencies
- ✅ pyproject.toml runtime dependencies = empty list
- ✅ Only Python standard library allowed
- ✅ Dev dependencies (pytest, mypy, flake8) okay

### Gate 8: Documentation Standards
- ✅ README.md with setup, usage, testing
- ✅ CLAUDE.md with development workflow
- ✅ Code comments only where logic is non-obvious
- ✅ Commit messages reference specs/features

**GATE STATUS**: ✅ All 8 gates established and will be verified post-implementation

---

## Clarifications Applied

Based on user feedback during clarification phase:

1. **CLI Input Method**: CLI arguments only (no interactive menu)
2. **ID Validation**: Both CLI parsing AND business logic validation (defense in depth)
3. **Timestamp Strategy**: UTC with timezone info (e.g., `2025-12-07T15:30:00Z`)

---

## Project Structure

### Documentation Structure

```text
specs/
├── plan.md                          # This file (Phase 1 overall plan)
├── overview.md                      # Project overview
├── data-models.md                   # Task entity definition
├── features/
│   ├── 01-add-task.md              # Feature spec: Add task
│   ├── 02-delete-task.md           # Feature spec: Delete task
│   ├── 03-update-task.md           # Feature spec: Update task
│   ├── 04-view-tasks.md            # Feature spec: View tasks
│   └── 05-mark-complete.md         # Feature spec: Mark complete
├── contracts/                       # API contracts (generated in Phase 1)
│   ├── add-task-contract.md
│   ├── delete-task-contract.md
│   ├── update-task-contract.md
│   ├── view-tasks-contract.md
│   └── mark-complete-contract.md
└── tasks.md                         # Phase 2 output (from /sp.tasks)
```

### Source Code Structure

```text
src/
├── __init__.py                      # Package initialization
├── main.py                          # CLI entry point with argument parsing
├── models.py                        # Task data model definition
├── storage.py                       # In-memory storage manager (tasks list, next_id)
├── commands.py                      # Command handlers (add, delete, update, list, complete)
└── py.typed                         # Type hint marker for mypy

tests/
├── __init__.py                      # Test package initialization
├── conftest.py                      # pytest fixtures and shared utilities
├── test_add_task.py                 # Tests for add task feature
├── test_delete_task.py              # Tests for delete task feature
├── test_update_task.py              # Tests for update task feature
├── test_view_tasks.py               # Tests for view tasks feature
└── test_mark_complete.py            # Tests for mark complete feature

Root:
├── pyproject.toml                   # Project config (dependencies, pytest, mypy, flake8)
├── pytest.ini                       # pytest configuration
├── README.md                        # Setup and usage guide
├── CLAUDE.md                        # Claude Code development guide
└── .gitignore                       # Git ignore rules
```

**Structure Decision**: Single Python package with CLI entry point. All 5 features implemented in shared `commands.py` and `storage.py`, with feature-specific test files. No submodules or monorepo complexity (aligns with "basic level" Phase 1 constraint).

---

## Implementation Strategy: 5-Feature Sequential Build

### Feature Build Order (with dependencies)

**Feature 1: Add Task** (no dependencies)
- Implements: `add_task(title, description="") -> Task`
- Creates: Task ID generation, timestamp handling, validation
- Enables: All other features depend on this
- Complexity: Medium

**Feature 2: Delete Task** (depends on: Add Task)
- Implements: `delete_task(task_id) -> bool`
- Uses: ID lookup, list filtering
- Complexity: Low

**Feature 3: Update Task** (depends on: Add Task)
- Implements: `update_task(task_id, title=None, description=None) -> Task`
- Uses: ID lookup, timestamp update
- Complexity: Medium

**Feature 4: View Tasks** (depends on: Add Task)
- Implements: `list_tasks(status="all") -> List[Task]`, table/JSON formatting
- Uses: Status filtering, date extraction
- Complexity: Medium (UI formatting)

**Feature 5: Mark Complete** (depends on: Add Task)
- Implements: `mark_complete(task_id) -> Task`
- Uses: ID lookup, boolean toggle, timestamp update
- Complexity: Low

**Rationale**: Add Task first (foundation), then utilities (Delete, Update, Complete), then display (View). This order minimizes rework and enables testing of storage operations independently.

---

## Module Design & Contracts

### Module 1: models.py - Task Data Model

**Responsibility**: Define Task entity, validation rules, type definitions

**Public Interface**:
```python
from typing import TypedDict

class Task(TypedDict):
    id: int
    title: str
    description: str
    completed: bool
    created_at: str  # ISO 8601
    updated_at: str  # ISO 8601

# Validation functions
def validate_title(title: str) -> bool: ...
def validate_description(description: str) -> bool: ...
def validate_task_id(task_id: int, tasks: List[Task]) -> bool: ...
```

**Key Constraints**:
- Title: 1-200 chars, non-empty, non-whitespace-only
- Description: Optional, max 1000 chars, default ""
- ID: Positive integer, unique, never reused
- completed: Boolean, default False
- Timestamps: ISO 8601 format with UTC timezone

### Module 2: storage.py - In-Memory Storage

**Responsibility**: Manage global task list and ID counter

**Public Interface**:
```python
# Module-level storage
tasks: List[Task] = []
next_id: int = 1

# Helper function
def get_task_by_id(task_id: int) -> Optional[Task]: ...
```

**Key Behavior**:
- `tasks`: Global list holding all Task dicts
- `next_id`: Global counter for auto-incrementing IDs
- No persistence, no file I/O
- Accessed by all command handlers

### Module 3: commands.py - Feature Handlers

**Responsibility**: Implement 5 feature operations

**Public Interface**:
```python
def add_task(title: str, description: str = "") -> Task: ...
def delete_task(task_id: int) -> bool: ...
def update_task(task_id: int, title: Optional[str] = None,
                description: Optional[str] = None) -> Task: ...
def list_tasks(status: str = "all") -> List[Task]: ...
def mark_complete(task_id: int) -> Task: ...
```

**Error Handling**: Raise custom exceptions or return error tuples (TBD during implementation)

### Module 4: main.py - CLI Entry Point

**Responsibility**: Parse arguments, call handlers, format output

**Public Interface**:
```python
def main() -> int:
    # 1. Parse sys.argv[1:] with argparse
    # 2. Dispatch to appropriate command handler
    # 3. Format output (table, JSON, or message)
    # 4. Return exit code (0, 1, or 2)
    ...

if __name__ == "__main__":
    sys.exit(main())
```

**CLI Commands** (from specs):
- `python main.py add --title <str> [--description <str>]`
- `python main.py delete --id <int>`
- `python main.py update --id <int> [--title <str>] [--description <str>]`
- `python main.py list [--status pending|completed|all] [--json]`
- `python main.py complete --id <int>`

---

## Testing Strategy

### Test Pyramid

```
    ┌─────────────────┐
    │  Integration    │  Full CLI workflows (e.g., add → list → complete → delete)
    │  Tests (5-10)   │  Uses main.py entry point, verifies end-to-end behavior
    ├─────────────────┤
    │  Unit Tests     │  Individual functions: add_task, delete_task, validate_*
    │  (50-70)        │  Tests in isolation, fixtures for storage setup/teardown
    └─────────────────┘
```

### Test Files Organization

| File | Responsibility | Test Count | Coverage |
|------|---|---|---|
| `test_add_task.py` | Add feature: valid/invalid titles, descriptions, ID generation, timestamps | 12-15 | ≥95% |
| `test_delete_task.py` | Delete feature: success, not found, ID validation, list modification | 8-10 | ≥95% |
| `test_update_task.py` | Update feature: title only, description only, both, validation, timestamps | 12-15 | ≥95% |
| `test_view_tasks.py` | View feature: all/pending/completed filters, table format, JSON output, empty list | 12-15 | ≥95% |
| `test_mark_complete.py` | Mark complete: toggle pending→completed, toggle completed→pending, validation, timestamps | 10-12 | ≥95% |

**Total Expected**: 54-67 tests with ≥95% coverage across all modules

### conftest.py - Shared Fixtures

```python
@pytest.fixture
def empty_storage():
    """Reset storage to empty state before each test"""
    # Clear tasks and reset next_id
    # Yield control to test
    # Restore original state after test

@pytest.fixture
def sample_task():
    """Create a sample task for testing"""
    # Add task to storage, yield task dict, clean up after

@pytest.fixture
def sample_tasks():
    """Create multiple tasks with varied states"""
    # Add 3-5 tasks with different titles, descriptions, completion states
    # Yield list, clean up after
```

---

## Red-Green-Refactor Workflow per Feature

### For Each Feature (1-5):

**RED Phase** (Test First)
1. Write all test cases based on spec acceptance criteria
2. Write test fixtures in conftest.py
3. Run tests → all fail (RED)

**GREEN Phase** (Implementation)
1. Implement function bodies to pass RED tests
2. Focus on minimal code, no extra features
3. Run tests → all pass (GREEN)

**REFACTOR Phase**
1. Clean up code: remove duplication, improve clarity
2. Ensure all tests still pass
3. Verify type hints, docstrings complete
4. Run full quality gates: pytest, mypy, flake8

**Quality Verification**
```bash
pytest -v --cov=src --cov-report=html  # ≥95% coverage
mypy src/                                # Zero type errors (strict)
flake8 src/ tests/                       # PEP 8 compliance
```

---

## Validation & Gates (Pre-Submission)

### Pre-Submission Checklist

- [ ] All 5 features implemented and passing tests
- [ ] pytest coverage ≥95% (`pytest --cov=src`)
- [ ] mypy strict mode passes (`mypy src/`)
- [ ] flake8 style passes (`flake8 src/ tests/`)
- [ ] All error messages match spec format ("Error: ...")
- [ ] Exit codes correct (0, 1, 2)
- [ ] Timestamps in UTC with timezone info (Z suffix)
- [ ] ID validation at CLI AND business logic levels
- [ ] README.md complete with setup/usage examples
- [ ] CLAUDE.md complete with development guide
- [ ] Git history clean (meaningful commits per feature)
- [ ] No uncommitted changes

### Submission Artifacts

1. GitHub repository: https://github.com/92Bilal26/TaskPilotAI
2. Branch: `phase-1` (all changes)
3. Demo video: <90 seconds showing all 5 commands
4. Form submission: https://forms.gle/KMKEKaFUD6ZX4UtY8

---

## Risk Analysis & Mitigation

### Top 3 Risks

**Risk 1: Timestamp Handling Complexity**
- **Impact**: Medium (affects all features with updated_at)
- **Probability**: Medium (timezone-aware UTC adds complexity)
- **Mitigation**: Use `datetime.now(datetime.timezone.utc).isoformat()` consistently; validate with tests

**Risk 2: Tight Deadline (Due Today)**
- **Impact**: High (Phase 1 due Dec 7, 2025 = TODAY)
- **Probability**: High (only ~8 hours remaining)
- **Mitigation**: Parallel implementation of features after core modules; leverage clear specs; keep refactoring minimal

**Risk 3: ID Validation at Two Levels**
- **Impact**: Low (edge case handling)
- **Probability**: Low (specs are clear)
- **Mitigation**: Write comprehensive validation tests; document validation rules in docstrings

---

## Next Steps

1. ✅ **Clarification Phase**: Complete (3 questions answered)
2. ✅ **Plan Phase**: Complete (this document)
3. **Task Generation Phase**: Run `/sp.tasks` to create granular task list from plan
4. **Implementation Phase**: Run `/sp.implement` to execute tasks with TDD workflow
5. **Quality Verification**: Run quality gates (pytest, mypy, flake8)
6. **Submission**: Push to GitHub and submit form

**Estimated Time to Complete**:
- Task Generation: 30 min
- Implementation (TDD): 3-4 hours
- Quality Verification: 30 min
- **Total: 4-5 hours** (deadline-critical)

---

**Version**: 1.0
**Last Updated**: 2025-12-07
**Status**: Ready for Task Generation
