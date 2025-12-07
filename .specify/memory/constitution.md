# TaskPilotAI - Phase 1 Constitution

**The Evolution of Todo: In-Memory Python Console App**

Hackathon II - Phase 1 (Due: Dec 7, 2025) - 100 Points

A spec-driven, test-first implementation of a command-line todo application using Claude Code and Spec-Kit Plus following the exact requirements from Hackathon II documentation.

---

## Hackathon Phase 1 Overview

| Aspect | Details |
|---|---|
| **Phase Name** | Phase I: Todo In-Memory Python Console App |
| **Objective** | Build a command-line todo app that stores tasks in memory |
| **Due Date** | Sunday, Dec 7, 2025 |
| **Points** | 100 |
| **Key Constraint** | Cannot write code manually—specs must be refined until Claude Code generates correct output |

---

## Core Principles

### I. Spec-Driven Development (Non-Negotiable)
Every feature implementation must be preceded by a detailed Markdown specification. Specifications MUST define:
- User stories and acceptance criteria
- Input/output contracts
- Data models
- Error handling scenarios

**Critical Rule:** You cannot write code manually. Refine the spec until Claude Code generates the correct output. This enforces clarity of requirements and prevents assumptions.

Claude Code reads the spec first. Ambiguities are clarified before implementation begins.

### II. Test-First Development (Red-Green-Refactor Mandatory)
Strict TDD cycle:
- **Red Phase:** Write failing tests that define expected behavior
- **Green Phase:** Implement minimum code to pass tests
- **Refactor Phase:** Clean up code while maintaining all passing tests

Every feature requires tests with 95%+ coverage. No code without tests. The cycle is strictly enforced.

### III. In-Memory State Management (Phase 1 Only)
All tasks are stored in memory using Python data structures (lists, dictionaries).

**Constraints:**
- ❌ No external database
- ❌ No file persistence or caching
- ❌ No data serialization
- ✅ State is ephemeral—resets on app restart

This constraint ensures focus on core logic without infrastructure complexity.

### IV. Clean Code & Python Best Practices
All code must:
- Follow **PEP 8** style guide strictly
- Use **type hints** for all function signatures
- Include **docstrings** for all classes and public methods
- Use named constants (no magic numbers)
- Apply **Single Responsibility Principle**—one class = one job
- Be readable first, optimized second

Quality tools (mypy, flake8) enforce compliance automatically.

### V. CLI-First Interface
The application is a command-line tool with:
- **Input:** Command-line arguments or interactive menu
- **Output:** Human-readable display + optional JSON for programmatic parsing
- **Errors:** Clear, actionable messages to stderr
- **Exit Codes:** 0 for success, 1 for user error, 2 for system error

Example usage: `python main.py add --title "Buy groceries" --description "Milk, eggs"`

### VI. Minimal Viable Complexity
- Start simple; avoid over-engineering
- **Zero external runtime dependencies** (only standard library)
- No async/threading unless explicitly required
- No configuration files; hard-code sensible defaults
- If it's not in Phase 1 scope, it's out of bounds

---

## Phase 1: Basic Level Features (5 Required)

Implement **exactly these 5 features** in order:

### 1. Add Task
**User Story:** As a user, I can create a new task with a title and optional description.

**Requirements:**
- Accept task title (required, 1-200 characters)
- Accept task description (optional, max 1000 characters)
- Auto-assign unique ID (auto-increment from 1)
- Store with creation timestamp (ISO 8601)
- Return confirmation with assigned task ID

**Example:**
```
Input: add --title "Buy groceries" --description "Milk, eggs, bread"
Output: Task created with ID 1
```

### 2. Delete Task
**User Story:** As a user, I can remove a task from my list by ID.

**Requirements:**
- Accept task ID (required)
- Remove task from in-memory storage
- Return success confirmation or error if not found
- Maintain ID sequence (don't reuse IDs)

**Example:**
```
Input: delete --id 1
Output: Task 1 deleted successfully
Output (error): Error: Task ID 5 not found
```

### 3. Update Task
**User Story:** As a user, I can modify a task's title or description.

**Requirements:**
- Accept task ID (required)
- Accept new title or description (at least one required)
- Update in-memory storage while preserving ID and timestamps
- Update `updated_at` timestamp
- Return updated task or error if not found

**Example:**
```
Input: update --id 1 --title "Buy groceries and fruits"
Output: Task 1 updated
```

### 4. View Task List
**User Story:** As a user, I can see all my tasks with their status.

**Requirements:**
- Display all tasks in a formatted table/list
- Show: ID, Title, Status (pending/completed), Created date
- Support optional filtering by status (pending, completed, all)
- Support JSON output with `--json` flag
- Support sorting (optional: by date, by status)

**Example:**
```
Input: list
Output:
  ID | Title              | Status    | Created
  1  | Buy groceries      | pending   | 2025-12-07
  2  | Call mom           | completed | 2025-12-06

Input: list --status pending
Output: [filtered list]

Input: list --json
Output: [{"id": 1, "title": "...", "completed": false, ...}]
```

### 5. Mark as Complete
**User Story:** As a user, I can mark a task as complete or incomplete.

**Requirements:**
- Accept task ID (required)
- Toggle completion status (pending ↔ completed)
- Preserve all other task data
- Update `updated_at` timestamp
- Return confirmation or error if not found

**Example:**
```
Input: complete --id 1
Output: Task 1 marked as completed

Input: complete --id 1
Output: Task 1 marked as pending
```

---

## Data Model

### Task Object (in memory)
```python
{
  "id": int,                    # Auto-incremented, never reused
  "title": str,                 # Required, 1-200 chars
  "description": str,           # Optional, max 1000 chars, default ""
  "completed": bool,            # Default: False
  "created_at": str,            # ISO 8601 datetime
  "updated_at": str             # ISO 8601 datetime
}
```

### In-Memory Storage Structure
```python
tasks: List[Dict] = []          # All tasks stored here
next_id: int = 1                # Auto-increment counter
```

---

## Project Structure (Required Deliverables)

```
TaskPilotAI/
├── .specify/                           # Spec-Kit Plus
│   ├── memory/
│   │   └── constitution.md             # This file
│   ├── scripts/bash/                   # Helper scripts
│   └── templates/                      # Spec templates
│
├── specs/                              # REQUIRED: Specifications
│   ├── overview.md                     # Project overview
│   ├── features/                       # Feature specifications
│   │   ├── 01-add-task.md
│   │   ├── 02-delete-task.md
│   │   ├── 03-update-task.md
│   │   ├── 04-view-tasks.md
│   │   └── 05-mark-complete.md
│   └── data-models.md                  # Data schema
│
├── src/                                # REQUIRED: Source code
│   ├── __init__.py
│   ├── main.py                         # CLI entry point
│   ├── models.py                       # Task data model
│   ├── storage.py                      # In-memory storage
│   └── commands.py                     # Command handlers
│
├── tests/                              # REQUIRED: Test files
│   ├── __init__.py
│   ├── conftest.py                     # Pytest fixtures
│   ├── test_add_task.py
│   ├── test_delete_task.py
│   ├── test_update_task.py
│   ├── test_view_tasks.py
│   └── test_mark_complete.py
│
├── pyproject.toml                      # REQUIRED: UV config
├── pytest.ini                          # Test configuration
├── README.md                           # REQUIRED: Setup instructions
├── CLAUDE.md                           # REQUIRED: Claude Code guide
├── .gitignore
└── history/prompts/                    # Prompt History Records
    └── phase-1/
```

---

## Technology Stack

| Component | Technology | Version |
|---|---|---|
| **Language** | Python | 3.13+ |
| **Package Manager** | UV | Latest |
| **Testing Framework** | pytest | Latest |
| **Type Checking** | mypy | Latest |
| **Style Checker** | flake8 | Latest |
| **Coverage** | pytest-cov | Latest |

### Runtime Dependencies
✅ **Zero external dependencies**—only Python standard library

### Development Dependencies
- pytest
- pytest-cov
- mypy
- flake8

---

## Development Workflow

### 1. Specification Phase
1. Create detailed spec in `/specs/features/` (use template)
2. Define acceptance criteria with examples
3. Include user stories, input/output contracts
4. Get clarity before any coding

### 2. Test Phase (Red)
1. Create test file in `/tests/`
2. Write failing tests based on spec
3. Run `pytest` → all tests fail
4. Tests define the expected behavior

### 3. Implementation Phase (Green)
1. Implement minimum code to pass tests
2. Follow Python best practices
3. Use type hints and docstrings
4. Run `pytest` → all tests pass

### 4. Refactor & Review
1. Clean up code for readability
2. Verify all tests still pass
3. Check PEP 8 compliance
4. No changes to passing tests

### 5. Quality Verification
1. Run full test suite: `pytest -v`
2. Check coverage: `pytest --cov=src`
3. Type check: `mypy src/`
4. Lint: `flake8 src/`
5. All gates must pass

### 6. Documentation
1. Update README.md if user-facing behavior changed
2. Update docstrings and comments
3. Create Prompt History Record (PHR) in `/history/prompts/phase-1/`

---

## Quality Gates (ALL REQUIRED)

Every feature must pass all gates before moving to the next feature:

- ✅ Specification exists and is detailed
- ✅ All tests pass (`pytest -v`)
- ✅ Code coverage ≥95% (`pytest --cov=src`)
- ✅ No type errors (`mypy src/`)
- ✅ PEP 8 compliant (`flake8 src/`)
- ✅ README and CLAUDE.md updated
- ✅ No hardcoded secrets or credentials
- ✅ Application runs without warnings

**Failure on any gate blocks submission.**

---

## Error Handling Standards

Every operation must gracefully handle errors:

| Error Case | Message | Exit Code |
|---|---|---|
| Task not found | `Error: Task ID X not found` | 1 |
| Invalid title length | `Error: Title required (1-200 characters)` | 1 |
| Invalid description length | `Error: Description max 1000 characters` | 1 |
| Duplicate completion | `Error: Task X already completed` | 1 |
| Missing required argument | `Error: --id is required` | 1 |
| Invalid input format | `Error: Invalid ID format. Use --id <number>` | 1 |
| System error | `Error: Unexpected error occurred` | 2 |

**Rules:**
- Errors always go to stderr
- User errors = exit code 1
- System errors = exit code 2
- Messages are clear and actionable
- Never expose stack traces to users

---

## Testing Requirements

### Unit Tests
- Each function has ≥1 test
- Test normal cases, edge cases, error cases
- Use fixtures in conftest.py for common setup
- Isolated tests (no side effects)

### Integration Tests
- Full CLI workflows (add → view → update → complete → delete)
- JSON output valid and parseable
- CLI argument parsing works correctly

### Coverage Targets
- **Line coverage:** ≥95%
- **Branch coverage:** ≥90%
- **All error paths tested**

### Test Data
- Realistic task examples
- Boundary cases: empty strings, max-length strings, special characters
- ID edge cases: consecutive IDs, large IDs
- State transitions: pending → completed → pending

---

## Governance

### Constitution Authority
This constitution is the source of truth. It supersedes all other guidelines. Conflicts are resolved in favor of this document.

### Amendment Process
Changes to the constitution require:
1. Proposal with clear rationale
2. Impact analysis (which features affected)
3. Migration plan for existing code
4. User approval before implementation

### Compliance Verification
Every commit is checked:
- All quality gates pass
- No scope creep (Phase 1 features only)
- Spec exists and is complete
- Tests cover all new/modified code
- No external dependencies added

### Non-Negotiable Rules
- ❌ Cannot skip specification phase
- ❌ Cannot write code without tests
- ❌ Cannot add external dependencies
- ❌ Cannot add persistence/file I/O for data
- ❌ Cannot implement Phase 2+ features
- ❌ Cannot modify constitution without approval

---

## Success Criteria (Phase 1 Complete When)

All of the following must be true:

✅ All 5 basic features implemented and working
✅ 100% of tests passing (`pytest -v`)
✅ Code coverage ≥95% (`pytest --cov=src`)
✅ All type checks pass (`mypy src/`)
✅ All linting passes (`flake8 src/`)
✅ GitHub repository with clean structure
✅ README.md with complete setup instructions
✅ CLAUDE.md with Claude Code workflow instructions
✅ Working console application demonstrating:
  - Adding tasks with title and description
  - Listing all tasks with status indicators
  - Updating task details
  - Deleting tasks by ID
  - Marking tasks as complete/incomplete
✅ All specifications in `/specs/features/`
✅ Prompt History Records created for significant work
✅ Zero warnings or errors on any quality tool

---

## Architectural Decisions

### Decision: In-Memory Storage
- **Chosen:** Python lists/dicts in memory
- **Rationale:** Simple, focuses on core logic without infrastructure
- **Trade-off:** Data lost on restart, but acceptable for Phase 1 MVP
- **Phase 2+:** Will migrate to persistent database (PostgreSQL)

### Decision: No External Dependencies
- **Chosen:** Standard library only
- **Rationale:** Forces clear architecture, teaches fundamentals
- **Phase 2+:** Will add frameworks (FastAPI, SQLModel) as needed

### Decision: Test-First Mandatory
- **Chosen:** Strict TDD with red-green-refactor
- **Rationale:** Ensures correctness, enables safe refactoring, documents behavior

### Decision: Spec-Driven Only
- **Chosen:** Cannot write code manually
- **Rationale:** Clarifies requirements, prevents assumptions, aligns with AI-native development

---

## Submission Checklist

Before submitting to Hackathon II, verify:

- [ ] All 5 features fully implemented
- [ ] All tests passing (100%)
- [ ] Coverage ≥95%
- [ ] All linting checks pass
- [ ] README.md complete and clear
- [ ] CLAUDE.md guidelines provided
- [ ] /specs directory with all feature specs
- [ ] /src directory with clean Python code
- [ ] /tests directory with comprehensive tests
- [ ] GitHub repository is public
- [ ] Branch structure: main + phase-1
- [ ] Working console app demo ready
- [ ] No hardcoded secrets or credentials

---

## Timeline

| Date | Milestone | Status |
|---|---|---|
| Dec 1, 2025 | Hackathon starts | Reference point |
| Dec 7, 2025 | Phase 1 Due | **TARGET** |
| Dec 14, 2025 | Phase 2 Due | Next phase |
| Dec 21, 2025 | Phase 3 Due | Next phase |

---

## Resources

- **Hackathon Doc:** `/home/bilal/TaskPilotAI/hakcathon_2_doc.md`
- **Spec Template:** `.specify/templates/spec-template.md`
- **PHR Template:** `.specify/templates/phr-template.prompt.md`
- **Python 3.13 Docs:** https://docs.python.org/3.13/
- **pytest Docs:** https://docs.pytest.org/

---

**Version**: 1.1.0
**Ratified**: 2025-12-07
**Last Amended**: 2025-12-07
**Status**: Active for Phase 1
**Next Review**: Post Phase 1 Completion
