# TaskPilotAI - Phase 1

**The Evolution of Todo: In-Memory Python Console App**

Hackathon II Phase 1 (Due: Dec 7, 2025) - 100 Points

A spec-driven, test-first command-line todo application built using Claude Code and Spec-Kit Plus.

---

## ✨ Features

Phase 1 implements 5 basic level features:

1. **Add Task** – Create new todo items with title and optional description
2. **Delete Task** – Remove tasks from your list
3. **Update Task** – Modify task title or description
4. **View Task List** – Display tasks in table or JSON format with filtering
5. **Mark as Complete** – Toggle task completion status (pending ↔ completed)

---

## 🚀 Quick Start

### ⚡ Ultra Quick Start (30 seconds)

**Launch the interactive UI immediately:**

```bash
cd /home/bilal/TaskPilotAI
uv run python -m src.tui
```

**Menu appears with options 1-9. Try these:**
- Press `1` → Add a task
- Press `2` → View all tasks in table
- Press `7` → Mark a task complete
- Press `0` → Exit

Done! 🎉

---

### Prerequisites

- **Python**: 3.13 or higher
- **UV**: Package manager for Python

### Installation

```bash
# Clone the repository
git clone https://github.com/92Bilal26/TaskPilotAI.git
cd TaskPilotAI

# Install dependencies using UV
uv sync --all-extras
```

---

### 🎮 Two Ways to Use

#### Option 1: Interactive UI (Recommended)

**Beautiful menu-driven interface with tables, formatting, and statistics:**

```bash
uv run python -m src.tui
```

**Menu Options:**
```
1️⃣  Add New Task           → Create new task with title & description
2️⃣  View All Tasks         → Display all tasks in beautiful table format
3️⃣  View All Tasks (JSON)  → Display tasks in JSON format
4️⃣  View Pending Tasks     → Show only incomplete tasks
5️⃣  View Completed Tasks   → Show only completed tasks
6️⃣  Update Task           → Modify task title or description
7️⃣  Mark Task Complete    → Toggle task completion status
8️⃣  Delete Task           → Remove task from list
9️⃣  View Statistics       → See progress and task statistics
0️⃣  Exit                  → Close application
```

**Example Walkthrough:**
1. Press `1` → Enter title "Buy groceries" → Enter description "Milk, eggs, bread" → ✅ Task created
2. Press `2` → See beautiful table with all tasks
3. Press `7` → Enter ID `1` → Task marked complete ✅
4. Press `9` → See statistics showing 1/1 tasks completed

#### Option 2: Command Line (For Automation/Scripts)

```bash
# Add a task
uv run python src/main.py add --title "Buy groceries" --description "Milk, eggs, bread"

# List all tasks
uv run python src/main.py list

# List pending tasks only
uv run python src/main.py list --status pending

# List tasks as JSON
uv run python src/main.py list --json

# Update a task
uv run python src/main.py update --id 1 --title "Buy groceries and fruits"

# Mark task as complete
uv run python src/main.py complete --id 1

# Delete a task
uv run python src/main.py delete --id 1
```

---

### 📚 Comprehensive Guides

This project includes detailed guides for all aspects:

| Guide | Purpose | Best For |
|-------|---------|----------|
| **QUICK_START.md** | 30-second setup + 2-minute demo | Getting started quickly |
| **TUI_GUIDE.md** | Complete interactive menu guide | Understanding all UI features |
| **TESTING_GUIDE.md** | Testing instructions + 10 scenarios | Verifying everything works |
| **CLAUDE.md** | Development methodology & architecture | Understanding the codebase |
| **/specs/** | Detailed feature specifications | Deep technical understanding |

---

## 🏗️ Project Structure

```
TaskPilotAI/
├── specs/                              # Specifications (Spec-Kit Plus)
│   ├── overview.md                     # Project overview
│   ├── data-models.md                  # Data model definitions
│   └── features/                       # Feature specifications
│       ├── 01-add-task.md
│       ├── 02-delete-task.md
│       ├── 03-update-task.md
│       ├── 04-view-tasks.md
│       └── 05-mark-complete.md
│
├── src/                                # Source code
│   ├── __init__.py                     # Package initialization
│   ├── main.py                         # CLI entry point
│   ├── models.py                       # Task data model
│   ├── storage.py                      # In-memory storage manager
│   └── commands.py                     # Command handlers
│
├── tests/                              # Test suite
│   ├── __init__.py
│   ├── conftest.py                     # Pytest fixtures
│   ├── test_add_task.py                # Add task tests
│   ├── test_delete_task.py             # Delete task tests
│   ├── test_update_task.py             # Update task tests
│   ├── test_view_tasks.py              # View tasks tests
│   └── test_mark_complete.py           # Mark complete tests
│
├── .specify/                           # Spec-Kit Plus config
│   ├── memory/
│   │   └── constitution.md             # Project constitution
│   ├── scripts/bash/                   # Helper scripts
│   └── templates/                      # Spec templates
│
├── .claude/commands/                   # Claude Code commands
├── history/prompts/                    # Prompt History Records
├── pyproject.toml                      # Project configuration (UV)
├── pytest.ini                          # Pytest configuration
├── CLAUDE.md                           # Claude Code guidelines
├── README.md                           # This file
└── .gitignore                          # Git ignore rules
```

---

## 🧪 Testing

### Run All Tests

```bash
# Run all tests with verbose output
pytest -v

# Run tests with coverage report
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_add_task.py -v

# Run tests matching a pattern
pytest -k "test_add" -v
```

### Test Coverage

Phase 1 aims for **≥95% code coverage**. After running tests with coverage:

```bash
# View coverage report in terminal
pytest --cov=src --cov-report=term-missing

# Generate HTML coverage report
pytest --cov=src --cov-report=html
open htmlcov/index.html
```

---

## 🔍 Code Quality

### Type Checking

```bash
# Run mypy for type checking
mypy src/

# Check with strict mode
mypy --strict src/
```

### Linting

```bash
# Run flake8 for style checking
flake8 src/ tests/

# Check with specific rules
flake8 src/ --show-source --statistics
```

### Format Code (Optional)

```bash
# Format code with black
black src/ tests/

# Check formatting without changes
black --check src/ tests/
```

### Quality Gates (All Required)

```bash
# Run all quality checks
pytest -v --cov=src
mypy src/
flake8 src/ tests/
```

All quality gates must pass before submission.

---

## 📝 Development Workflow

This project follows **Spec-Driven Development** with strict **Test-First (TDD)** methodology:

### 1. Specification Phase
- Read feature specification in `/specs/features/`
- Understand requirements, acceptance criteria, and data model
- Clarify any ambiguities

### 2. Test Phase (Red)
- Write failing tests based on specification
- Tests define expected behavior
- Run `pytest` → all tests fail initially

### 3. Implementation Phase (Green)
- Write minimum code to pass all tests
- Follow Python best practices (PEP 8, type hints, docstrings)
- Run `pytest` → all tests pass

### 4. Refactor Phase
- Clean up code for readability and maintainability
- Ensure all tests still pass
- No behavioral changes

### 5. Quality Verification
```bash
pytest -v --cov=src      # Tests & coverage
mypy src/                # Type checking
flake8 src/              # Code style
```

### 6. Document
- Update docstrings and comments
- Create Prompt History Record (PHR)
- Update README if user-facing behavior changed

---

## 📊 Data Model

### Task Object

```python
{
  "id": int,                    # Auto-incremented, unique
  "title": str,                 # Required, 1-200 characters
  "description": str,           # Optional, max 1000 characters
  "completed": bool,            # False (pending) or True (completed)
  "created_at": str,            # ISO 8601 datetime
  "updated_at": str             # ISO 8601 datetime
}
```

### Example Task

```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2025-12-07T10:30:00",
  "updated_at": "2025-12-07T10:30:00"
}
```

---

## ⚠️ Error Handling

The application provides clear, actionable error messages:

| Error | Message | Exit Code |
|---|---|---|
| Task not found | `Error: Task ID X not found` | 1 |
| Invalid title | `Error: Title required (1-200 characters)` | 1 |
| Invalid description | `Error: Description max 1000 characters` | 1 |
| Missing argument | `Error: --id is required` | 1 |
| System error | `Error: Unexpected error occurred` | 2 |

---

## 📖 CLI Commands Reference

### Add Task
```bash
python src/main.py add --title "Task title" [--description "Optional description"]

# Examples
python src/main.py add --title "Buy groceries"
python src/main.py add --title "Buy groceries" --description "Milk, eggs, bread"
```

### Delete Task
```bash
python src/main.py delete --id <task_id>

# Example
python src/main.py delete --id 1
```

### Update Task
```bash
python src/main.py update --id <task_id> [--title "New title"] [--description "New description"]

# Examples
python src/main.py update --id 1 --title "New title"
python src/main.py update --id 1 --description "New description"
python src/main.py update --id 1 --title "New" --description "New desc"
```

### List Tasks
```bash
python src/main.py list [--status <status>] [--json]

# Examples
python src/main.py list                          # Show all tasks
python src/main.py list --status pending        # Show pending only
python src/main.py list --status completed      # Show completed only
python src/main.py list --json                  # JSON output
```

### Mark Task as Complete
```bash
python src/main.py complete --id <task_id>

# Example
python src/main.py complete --id 1
```

---

## 🔧 Technology Stack

| Component | Technology | Purpose |
|---|---|---|
| **Language** | Python 3.13+ | Implementation |
| **Package Manager** | UV | Dependency management |
| **Testing** | pytest | Test framework |
| **Type Checking** | mypy | Static type verification |
| **Linting** | flake8 | Code style enforcement |
| **Coverage** | pytest-cov | Coverage measurement |

### Runtime Dependencies
✅ **Zero external dependencies** – Only Python standard library

### Development Dependencies
- pytest
- pytest-cov
- mypy
- flake8

---

## 🎯 Quality Standards

### Code Quality
- **Style**: PEP 8 compliant (enforced by flake8)
- **Type Hints**: 100% type hints on all functions
- **Documentation**: Docstrings for all classes and public methods
- **Coverage**: ≥95% code coverage (enforced by pytest-cov)
- **Type Safety**: 100% mypy compliance (strict mode)

### Testing
- **Unit Tests**: Each function has ≥1 test
- **Integration Tests**: Full CLI workflows tested
- **Edge Cases**: Boundary conditions and error cases tested
- **Data Integrity**: ID sequences, state transitions verified

### Documentation
- **README.md**: Setup and usage instructions
- **CLAUDE.md**: Claude Code development guidelines
- **Specs**: Detailed feature specifications in `/specs/`
- **Code Comments**: Self-documenting code, minimal comments

---

## 📚 Phase 1 Constitution

This project follows a strict **Constitution** defined in `.specify/memory/constitution.md`. The constitution establishes:

- **Core Principles**: Spec-driven development, test-first TDD, in-memory storage
- **Quality Gates**: All 8 gates must pass before submission
- **Error Standards**: Consistent error messages and exit codes
- **Non-Negotiable Rules**: Cannot skip specs, cannot code without tests, zero external dependencies

**Key Constraint**: Cannot write code manually. Specs must be refined until Claude Code generates correct output.

---

## 🚀 Next Steps (Phase 2+)

Phase 1 focuses on core logic. Future phases will add:

- **Phase 2**: Full-stack web application (Next.js + FastAPI + PostgreSQL)
- **Phase 3**: AI chatbot with natural language interface
- **Phase 4**: Kubernetes deployment (Minikube)
- **Phase 5**: Cloud deployment (DigitalOcean DOKS) + Kafka + Dapr

---

## 📝 Contributing

This is a hackathon project following strict spec-driven development. All contributions must:

1. Start with a specification in `/specs/`
2. Include comprehensive tests (TDD)
3. Pass all quality gates (pytest, mypy, flake8)
4. Follow the constitution principles

---

## 📄 License

MIT License - See LICENSE file for details

---

## 👤 Author

**92Bilal26** (Bilal Ahmed)
- Email: talibebaqi@gmail.com
- GitHub: https://github.com/92Bilal26

---

## 🔗 Resources

- **Project Repository**: https://github.com/92Bilal26/TaskPilotAI
- **Phase 1 Branch**: https://github.com/92Bilal26/TaskPilotAI/tree/phase-1
- **Hackathon Info**: Evolution of Todo - Hackathon II
- **Constitution**: `.specify/memory/constitution.md`
- **Specifications**: `/specs/` directory

---

## 📞 Support

For questions or issues:

1. Check the specification files in `/specs/`
2. Review the constitution in `.specify/memory/constitution.md`
3. Check existing tests in `/tests/` for examples
4. Open an issue on GitHub

---

**Last Updated**: 2025-12-07
**Status**: Phase 1 Implementation
**Next Milestone**: Dec 7, 2025 (Phase 1 Deadline)
