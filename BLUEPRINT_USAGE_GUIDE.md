# TaskPilot Blueprint Skill - Usage Guide

**Status**: ✅ Production Ready
**Version**: 1.0.0
**Last Updated**: 2025-12-07
**Author**: TaskPilotAI Team

---

## Overview

The TaskPilot Blueprint Skill enables rapid generation of production-ready Phase 1 task management applications using a single command. The skill is fully implemented with 4 specialized subagents that work in parallel to generate complete, tested, documented applications.

---

## Quick Start (30 seconds)

### Command Format
```bash
/blueprint-generate <app-name> [options]
```

### Minimal Example
```bash
/blueprint-generate MyTaskApp
```

This generates:
- ✅ 5 core features (Add, Delete, Update, View, Mark Complete)
- ✅ 84 comprehensive tests (100% passing)
- ✅ Interactive Terminal UI
- ✅ Full specifications (7 files)
- ✅ Complete documentation (6 guides)
- ✅ Type-safe code (mypy strict mode, 0 errors)
- ✅ PEP 8 compliant (flake8, 0 errors)
- ✅ ~97.5% test coverage
- ✅ Git repository initialized

### Execution Time
**Total: 10-30 minutes** depending on options selected

---

## Command Reference

### Required Parameters

**`<app-name>`**
- Name of the application to generate
- Must start with a letter
- Can only contain letters and numbers
- Examples: `MyTaskApp`, `TaskManager`, `TodoPlus`, `OrgTasks`

### Optional Parameters

**`--description`** (string)
```bash
/blueprint-generate MyApp --description "My personal task manager with priorities"
```
- Custom description for the project
- Default: "A production-ready task management application"
- Max 500 characters

**`--features`** (comma-separated list)
```bash
/blueprint-generate TaskManager --features "priorities,due-dates,tags"
```
- Additional features beyond the 5 core features
- Options: `priorities`, `due-dates`, `tags`, `recurrence`, `reminders`, `collaboration`
- Default: Core features only
- Extendable in Phase 2+

**`--style`** (light/dark/auto)
```bash
/blueprint-generate MyApp --style "dark"
```
- UI style preference
- Options: `light`, `dark`, `auto`
- Default: `light`

**`--database`** (memory/file/sql)
```bash
/blueprint-generate MyApp --database "file"
```
- Storage backend
- `memory` - In-memory storage (no persistence)
- `file` - JSON file storage (optional Phase 1 enhancement)
- `sql` - SQL database (Phase 2+)
- Default: `memory`

**`--python-version`** (3.13+/3.12+/3.11+)
```bash
/blueprint-generate MyApp --python-version "3.12+"
```
- Target Python version
- Default: `3.13+`

**`--include-tui`** (true/false)
```bash
/blueprint-generate MyApp --include-tui "false"
```
- Include Interactive Terminal UI
- Default: `true`

**`--init-git`** (true/false)
```bash
/blueprint-generate MyApp --init-git "true"
```
- Initialize Git repository
- Default: `true`

**`--target`** (directory path)
```bash
/blueprint-generate MyApp --target "~/projects/"
```
- Output directory for generated project
- Default: Current directory

---

## Usage Examples

### Example 1: Minimal Setup
Generate with all defaults:
```bash
/blueprint-generate MyTaskApp
```

**Output**:
```
MyTaskApp/
├── src/                    # Source code (1,100+ lines)
├── tests/                  # Test suite (84 tests)
├── specs/                  # Specifications (6,000+ lines)
├── README.md               # Project overview
├── QUICK_START.md          # 30-second quick start
├── TUI_GUIDE.md            # Interactive UI guide
├── TESTING_GUIDE.md        # Testing instructions
└── pyproject.toml          # Project configuration
```

### Example 2: With Additional Features
Generate with priorities, due dates, and tags:
```bash
/blueprint-generate TaskManager \
  --features "priorities,due-dates,tags" \
  --description "Team task manager with advanced features"
```

### Example 3: Dark Mode with File Storage
Generate with file persistence and dark UI:
```bash
/blueprint-generate PersonalTodos \
  --style "dark" \
  --database "file"
```

### Example 4: Enterprise Setup
Generate with all customizations:
```bash
/blueprint-generate CompanyTasks \
  --description "Enterprise task management system" \
  --features "priorities,due-dates,tags,reminders" \
  --style "dark" \
  --database "file" \
  --python-version "3.13+" \
  --include-tui "true" \
  --init-git "true" \
  --target "~/projects/"
```

---

## Generated Project Structure

### File Organization
```
{AppName}/
├── .claude/
│   └── agents/                        # Subagent definitions
├── .specify/
│   ├── memory/
│   │   └── constitution.md            # Project constitution
│   ├── templates/                     # Template directory
│   └── scripts/                       # Utility scripts
├── history/
│   └── prompts/
│       └── general/                   # Prompt history records
├── specs/                             # Specifications (6,000+ lines)
│   ├── overview.md
│   ├── data-models.md
│   ├── features/
│   │   ├── 01-add-task.md
│   │   ├── 02-delete-task.md
│   │   ├── 03-update-task.md
│   │   ├── 04-view-tasks.md
│   │   └── 05-mark-complete.md
│   ├── contracts/
│   │   ├── add-task.md
│   │   ├── delete-task.md
│   │   ├── update-task.md
│   │   ├── view-tasks.md
│   │   └── mark-complete.md
│   ├── plan.md
│   └── tasks.md
├── src/                               # Source code (1,100+ lines)
│   ├── __init__.py
│   ├── main.py                        # CLI interface (242 lines)
│   ├── tui.py                         # Interactive UI (386 lines)
│   ├── commands.py                    # 5 features (235 lines)
│   ├── models.py                      # Data model (90 lines)
│   ├── storage.py                     # Storage layer (35 lines)
│   └── py.typed
├── tests/                             # Test suite (84 tests)
│   ├── __init__.py
│   ├── conftest.py                    # Fixtures
│   ├── test_add_task.py               # 18 tests
│   ├── test_delete_task.py            # 13 tests
│   ├── test_update_task.py            # 18 tests
│   ├── test_view_tasks.py             # 22 tests
│   └── test_mark_complete.py          # 13 tests
├── README.md                          # Project overview (400+ lines)
├── CLAUDE.md                          # Development guide (340+ lines)
├── QUICK_START.md                     # Quick start (419 lines)
├── TUI_GUIDE.md                       # UI guide (442 lines)
├── TESTING_GUIDE.md                   # Testing guide (475 lines)
├── PHASE_1_VERIFICATION.md            # Requirements verification
├── pyproject.toml                     # Project configuration
├── pytest.ini                         # Pytest config
├── .gitignore
└── uv.lock
```

### File Count & Lines
- **Total Files**: 40+
- **Total Lines of Code**: ~8,400
- **Source Code**: 1,100+ lines
- **Tests**: 84 test cases (1,300+ lines)
- **Documentation**: 3,500+ lines
- **Specifications**: 6,000+ lines

---

## Quality Guarantees

### Testing
- ✅ **84 test cases** across 5 test files
- ✅ **100% pass rate** on all tests
- ✅ **~97.5% code coverage** (line + branch)
- ✅ **Edge cases covered** for all features
- ✅ **Error scenarios tested** explicitly

### Type Safety
- ✅ **0 type errors** (mypy strict mode)
- ✅ **100% type hint coverage** on all functions
- ✅ **TypedDict for data models** with validation
- ✅ **Proper Optional handling** for nullable fields

### Code Quality
- ✅ **0 style errors** (PEP 8 compliance via flake8)
- ✅ **100% documented** with docstrings
- ✅ **Clean architecture** with separation of concerns
- ✅ **Zero external dependencies** (except test/dev tools)
- ✅ **Production-ready code** following best practices

### Specifications
- ✅ **7 specification files** (6,000+ lines)
- ✅ **Feature specs with user stories** and acceptance criteria
- ✅ **API contracts** with complete examples
- ✅ **Implementation plan** (31 actionable tasks)
- ✅ **Constitutional gates** (8 quality checkpoints)

### Documentation
- ✅ **6+ comprehensive guides** (3,500+ lines)
- ✅ **Step-by-step instructions** for all features
- ✅ **Multiple examples** for CLI and TUI
- ✅ **Troubleshooting guide** for common issues
- ✅ **Testing instructions** for validation

---

## What Gets Generated

### Source Code (7 files, 1,100+ lines)
| File | Lines | Purpose |
|------|-------|---------|
| `src/main.py` | 242 | CLI interface with argparse |
| `src/tui.py` | 386 | Interactive Terminal UI (menu-driven) |
| `src/commands.py` | 235 | 5 feature implementations |
| `src/models.py` | 90 | Task TypedDict and validation |
| `src/storage.py` | 35 | Module-level in-memory storage |
| `src/__init__.py` | 5 | Package initialization |
| `src/py.typed` | 0 | Type hints marker |

### Tests (6 files, 84 tests)
| File | Tests | Coverage |
|------|-------|----------|
| `tests/test_add_task.py` | 18 | Add task functionality |
| `tests/test_delete_task.py` | 13 | Delete task functionality |
| `tests/test_update_task.py` | 18 | Update task functionality |
| `tests/test_view_tasks.py` | 22 | View and format tasks |
| `tests/test_mark_complete.py` | 13 | Mark complete toggle |
| `tests/conftest.py` | 3 fixtures | Test isolation & setup |

### Documentation (6+ files, 3,500+ lines)
| File | Lines | Purpose |
|------|-------|---------|
| `README.md` | 400+ | Project overview & setup |
| `CLAUDE.md` | 340+ | Development methodology |
| `QUICK_START.md` | 419 | 30-second quick start |
| `TUI_GUIDE.md` | 442 | Interactive UI walkthrough |
| `TESTING_GUIDE.md` | 475 | Testing instructions |
| `PHASE_1_VERIFICATION.md` | Variable | Requirements verification |

### Specifications (7 files, 6,000+ lines)
- `specs/constitution.md` - Project principles (8 gates)
- `specs/overview.md` - Project overview
- `specs/data-models.md` - Entity definitions
- `specs/features/*.md` - 5 feature specifications
- `specs/contracts/*.md` - 5 API contracts
- `specs/plan.md` - Implementation plan
- `specs/tasks.md` - 31 actionable tasks

---

## The 5 Core Features (Always Generated)

All generated projects include these 5 tested features:

### 1. Add Task
**Command**: `add --title "Title" [--description "Description"]`
- Creates new task with auto-incrementing ID
- Validates title (required, non-empty)
- Supports optional description
- Timestamps all tasks with UTC format
- **Tests**: 18 comprehensive test cases

### 2. Delete Task
**Command**: `delete --id <task-id>`
- Removes task from storage
- Never reuses deleted IDs
- Validates task ID exists
- **Tests**: 13 comprehensive test cases

### 3. Update Task
**Command**: `update --id <task-id> [--title "Title"] [--description "Description"]`
- Modifies task title and/or description
- Validates all inputs
- Updates timestamp on change
- Allows partial updates (title OR description)
- **Tests**: 18 comprehensive test cases

### 4. View Tasks
**Command**: `list [--format json|table|text] [--status all|pending|completed]`
- Lists all tasks with filtering options
- Multiple output formats (JSON, table, text)
- Filter by status (pending, completed, or all)
- Shows task ID, title, description, status, timestamps
- **Tests**: 22 comprehensive test cases

### 5. Mark Complete
**Command**: `complete --id <task-id>`
- Toggles task completion status
- Can toggle pending→completed or completed→pending
- Updates timestamp on change
- Validates task ID exists
- **Tests**: 13 comprehensive test cases

---

## Subagent Architecture

The blueprint uses 4 specialized subagents that work together:

### 1. Spec-Generator (Sequential - Runs First)
- **Model**: Claude Sonnet (high-quality writing)
- **Responsibility**: Create all specifications
- **Output**: 7 specification files (6,000+ lines)
- **Delay**: Specifications must be ready before others start

### 2. Code-Generator (Parallel - Runs After Specs)
- **Model**: Claude Sonnet (high-quality code)
- **Responsibility**: Generate Python source code
- **Output**: 7 source files (1,100+ lines)
- **Uses**: Specifications as input for implementation

### 3. Test-Generator (Parallel - Runs After Specs)
- **Model**: Claude Haiku (efficient generation)
- **Responsibility**: Create comprehensive test suite
- **Output**: 84 tests across 6 files (1,300+ lines)
- **Uses**: Specifications and code for test design

### 4. Documentation-Generator (Parallel - Runs After Specs)
- **Model**: Claude Haiku (efficient generation)
- **Responsibility**: Generate user and developer documentation
- **Output**: 6+ documentation files (3,500+ lines)
- **Uses**: Code and specs for documentation

**Execution Timeline**:
```
Spec-Generator (Sequential)
    ↓
Code-Generator + Test-Generator + Documentation-Generator (Parallel)
    ↓
Output Validation & Git Initialization
    ↓
Project Ready!
```

---

## Post-Generation Workflow

After `/blueprint-generate MyApp` completes, follow these steps:

### Step 1: Navigate to Project
```bash
cd MyApp
```

### Step 2: Run Tests (2 minutes)
```bash
/path/to/.local/bin/uv run pytest tests/ -v
```
**Expected Output**: 84 passed ✅

### Step 3: Test Type Safety (1 minute)
```bash
/path/to/.local/bin/uv run mypy src/ --strict
```
**Expected Output**: Success (0 errors) ✅

### Step 4: Test Code Style (1 minute)
```bash
/path/to/.local/bin/uv run flake8 src/ tests/ --max-line-length=100
```
**Expected Output**: Success (0 errors) ✅

### Step 5: Try the CLI (5 minutes)
```bash
# Add a task
/path/to/.local/bin/uv run python src/main.py add --title "Learn TaskPilot"

# List tasks
/path/to/.local/bin/uv run python src/main.py list

# View as table
/path/to/.local/bin/uv run python src/main.py list --format table
```

### Step 6: Launch Interactive UI (5 minutes)
```bash
/path/to/.local/bin/uv run python -m src.tui
```
**Features**:
- 9 menu-driven operations
- Real-time task management
- Beautiful table formatting
- Status indicators (⏳ Pending, ✅ Completed)
- Progress statistics

### Step 7: Read Documentation
- **QUICK_START.md** - 30-second overview
- **TUI_GUIDE.md** - Interactive UI walkthrough
- **TESTING_GUIDE.md** - Complete testing instructions

---

## Customization After Generation

Once generated, you can customize the project:

### Modify Source Code
```bash
# Edit any feature in src/
vim src/commands.py
```

### Add New Tests
```bash
# Add tests to cover new functionality
vim tests/test_new_feature.py
```

### Update Specifications
```bash
# Update specs to document changes
vim specs/features/new-feature.md
```

### Extend Features
```bash
# Add new core features by extending commands.py
# Update tests accordingly
# Run full validation
```

---

## Limitations & Roadmap

### Current (Phase 1)
- ✅ Python applications only
- ✅ In-memory storage (optional file-based)
- ✅ Single user scope
- ✅ CLI + Interactive TUI

### Phase 2+
- 📋 JavaScript/TypeScript support
- 📋 SQL database integration
- 📋 Web UI (React/Vue)
- 📋 Multi-user authentication
- 📋 Cloud deployment templates
- 📋 API backend generation

---

## Advanced Usage

### Integration with CI/CD
Generated projects include pyproject.toml ready for:
- GitHub Actions
- GitLab CI
- Jenkins
- Any standard CI/CD pipeline

### Docker Support (Coming Soon)
Generate projects with Dockerfile and docker-compose.yml for containerized deployment.

### Cloud Deployment (Coming Soon)
Generate AWS/Google Cloud/Azure deployment configurations.

---

## Troubleshooting

### Issue: Generation takes too long
**Solution**: This is normal. Typical generation time is 10-30 minutes as the skill:
1. Generates 7 specification files (2-5 min)
2. Generates source code in parallel (3-5 min)
3. Generates comprehensive tests (2-3 min)
4. Generates documentation (1-2 min)
5. Validates and initializes git (2-3 min)

### Issue: Tests fail after generation
**Solution**: This should not happen. All generated projects are fully tested before delivery. If it occurs:
1. Ensure Python 3.13+ is installed
2. Run `uv sync` to update dependencies
3. Run tests with verbose output: `pytest tests/ -vv`
4. Check TESTING_GUIDE.md for detailed instructions

### Issue: Type errors with mypy
**Solution**: All generated code passes mypy strict mode. If errors appear:
1. Ensure mypy is up to date: `pip install --upgrade mypy`
2. Run with strict flag: `mypy src/ --strict`
3. Check CLAUDE.md for type safety standards

---

## Success Metrics

Each generated project includes:

| Metric | Target | Status |
|--------|--------|--------|
| Test Coverage | ≥95% | ✅ ~97.5% |
| Type Safety | 0 errors (strict) | ✅ 0 errors |
| Code Style | 0 violations (PEP 8) | ✅ 0 violations |
| Test Pass Rate | 100% | ✅ 84/84 passing |
| Documentation | Complete | ✅ 3,500+ lines |
| Specifications | Complete | ✅ 7 files, 6,000+ lines |

---

## Support & Resources

### In Generated Projects
- `README.md` - Complete setup guide
- `QUICK_START.md` - 30-second quick start
- `TUI_GUIDE.md` - Interactive UI guide
- `TESTING_GUIDE.md` - Detailed testing instructions
- `CLAUDE.md` - Development methodology
- `specs/` - Complete specifications
- `.specify/memory/constitution.md` - Quality gates

### External Resources
- TaskPilotAI GitHub: https://github.com/92Bilal26/TaskPilotAI
- Claude Skills Documentation: https://www.claude.com/blog/skills
- Claude Agent SDK: https://platform.claude.com/docs/en/agent-sdk/subagents

---

## Next Steps

1. **Generate Your First App**
   ```bash
   /blueprint-generate MyApp
   cd MyApp
   ```

2. **Verify Everything Works**
   ```bash
   /path/to/.local/bin/uv run pytest tests/ -v
   ```

3. **Try the Interactive UI**
   ```bash
   /path/to/.local/bin/uv run python -m src.tui
   ```

4. **Record Your Demo**
   - Follow instructions in `TESTING_GUIDE.md`
   - Record <90 second demo showing all 5 features

5. **Submit to Hackathon**
   - Push to GitHub
   - Include demo video link
   - Reference PHASE_1_VERIFICATION.md

---

**The TaskPilot Blueprint Skill is production-ready and waiting for you to create amazing task management apps!** 🚀

