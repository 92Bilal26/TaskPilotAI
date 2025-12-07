# TaskPilotAI - Phase 1 Constitution

**The Evolution of Todo: In-Memory Python Console App**

A spec-driven, test-first implementation of a command-line todo application using Claude Code and Spec-Kit Plus.

## Core Principles

### I. Spec-Driven Development (Non-Negotiable)
Every feature implementation must be preceded by a detailed specification in Markdown. Specifications must define user stories, acceptance criteria, input/output contracts, data models, and error handling. Claude Code reads the spec first and never assumes requirements. Ambiguities are clarified before implementation begins.

### II. Test-First (Red-Green-Refactor Mandatory)
Development follows strict TDD: Write failing tests → Implement minimum code → Refactor. Every feature change requires updated tests with 95%+ coverage. No code without tests. The red-green-refactor cycle is strictly enforced.

### III. In-Memory State Management (Phase 1 Constraint)
All tasks are stored in memory using Python data structures (lists, dictionaries). No external database, file persistence, or caching. All state is ephemeral—resets on application restart. This constraint ensures focus on core logic without infrastructure complexity.

### IV. Clean Code & Python Best Practices
All code follows PEP 8 style guide strictly, uses type hints for all function signatures, includes docstrings for classes and public methods. No magic numbers; use named constants. Single Responsibility Principle: one class = one job. Code is readable first, optimized second.

### V. CLI-First Interface
The application is a command-line tool. Input via command-line arguments or interactive menu. Output in human-readable format plus optional JSON for parsing. Errors to stderr with clear, actionable messages. Example: `python main.py add --title "Buy groceries"`

### VI. Minimal Viable Complexity
Start simple; avoid over-engineering. No external runtime dependencies beyond test frameworks. No async/threading unless explicitly required. No configuration files; hard-code sensible defaults. If a feature isn't in Phase 1 requirements, it's out of scope.

## Phase 1: Basic Level Feature Scope

Implement exactly these 5 features:

1. **Add Task** – Create new items with title (required) and description (optional)
2. **Delete Task** – Remove tasks by ID
3. **Update Task** – Modify title or description
4. **View Task List** – Display all tasks with filtering option
5. **Mark as Complete** – Toggle completion status

No intermediate or advanced features. No persistence, no database, no external APIs.

## Data Model

**Task Object:**
```
id: int (auto-incremented, unique)
title: str (required, 1-200 characters)
description: str (optional, max 1000 characters)
completed: bool (default: False)
created_at: datetime (ISO 8601)
updated_at: datetime (ISO 8601)
```

**In-Memory Storage:**
```
tasks: List[Task] = []
next_id: int = 1
```

## Project Structure

```
src/
├── main.py          # CLI entry point
├── models.py        # Task data model
├── storage.py       # In-memory storage manager
└── commands.py      # Command handlers

tests/
├── test_add_task.py
├── test_delete_task.py
├── test_update_task.py
├── test_view_tasks.py
└── test_mark_complete.py

specs/
├── overview.md
└── features/
    ├── add-task.md
    ├── delete-task.md
    └── ...

pyproject.toml       # UV package config
pytest.ini           # Test discovery
CLAUDE.md            # Claude Code instructions
README.md            # Setup & usage
```

## Development Workflow

1. **Specification:** Create spec in `/specs/features/` with acceptance criteria
2. **Red:** Write failing tests based on spec
3. **Green:** Implement minimum code to pass tests
4. **Refactor:** Clean up code, maintain readability
5. **Verify:** All tests pass, coverage ≥95%
6. **Document:** Update README, docstrings, PHR

## Quality Gates (All Required)

- ✅ Specification exists and detailed
- ✅ All tests pass (`pytest -v`)
- ✅ Code coverage ≥95%
- ✅ No type errors (`mypy src/`)
- ✅ PEP 8 compliant (`flake8 src/`)
- ✅ README and CLAUDE.md updated
- ✅ No hardcoded secrets
- ✅ Runs without warnings

## Error Handling

| Error Case | Message | Exit Code |
|---|---|---|
| Task not found | `Error: Task ID X not found` | 1 |
| Invalid input | `Error: Title required (1-200 chars)` | 1 |
| Duplicate operation | `Error: Task already completed` | 1 |
| System error | `Error: Unexpected error` | 2 |

## Testing Requirements

- **Unit Tests:** Each function has ≥1 test covering normal, edge, and error cases
- **Integration Tests:** Full CLI workflows (add → view → update → delete)
- **Coverage:** Line ≥95%, Branch ≥90%, all error paths tested
- **Test Data:** Realistic examples, boundary cases, ID collision prevention

## Dependencies & Tools

**Runtime:** Python 3.13+, UV (package manager), Standard Library only

**Development:** pytest, mypy, flake8, pytest-cov

**No External Runtime Dependencies** (this is non-negotiable)

## Governance

This constitution supersedes all other guidelines. Changes require proposal, impact analysis, migration plan, and user approval. Every PR is checked against:

- All quality gates pass
- No scope creep (Phase 1 features only)
- Spec exists and is complete
- Tests cover all new/modified code

**Non-Negotiable Rules:**
- ❌ No skipping specs
- ❌ No code without tests
- ❌ No external dependencies
- ❌ No persistence/file I/O for data
- ❌ No Phase 2+ features

## Success Criteria (Phase 1 Complete When)

✅ All 5 basic features implemented and tested
✅ GitHub repo with clean structure
✅ README with setup instructions
✅ Working console app demonstrating all features
✅ 100% test pass rate, ≥95% coverage
✅ All linting checks pass
✅ Spec-driven workflow documented
✅ CLAUDE.md instructions provided

**Version**: 1.0.0 | **Ratified**: 2025-12-07 | **Last Amended**: 2025-12-07
