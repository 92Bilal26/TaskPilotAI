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

---

# TaskPilotAI - Phase 2 Constitution

**The Evolution of Todo: Full-Stack Web Application**

Hackathon II - Phase 2 (Due: Dec 14, 2025) - 150 Points

A spec-driven, test-first implementation of a multi-user web application transforming the Phase 1 console app into a modern full-stack system using Claude Code and Spec-Kit Plus.

---

## Phase 2 Overview

| Aspect | Details |
|---|---|
| **Phase Name** | Phase II: Todo Full-Stack Web Application |
| **Objective** | Transform console app into modern multi-user web application with persistent storage |
| **Due Date** | Sunday, Dec 14, 2025 |
| **Points** | 150 |
| **Key Constraint** | Spec-driven development; no manual code writing—Claude Code generates from specs |

---

## Phase 2 Core Principles (Extends Phase 1)

### I. Spec-Driven Development (Maintained from Phase 1)
Every feature must be defined in detailed Markdown specifications covering:
- User stories and acceptance criteria
- API contracts and endpoints
- Data models and schema
- Error handling and validation rules

**Critical Rule:** Refine the spec until Claude Code generates correct implementation.

### II. Test-First Development (Maintained from Phase 1)
- Strict TDD: Red → Green → Refactor
- ≥95% code coverage required
- All error paths tested

### III. Multi-User Architecture (NEW - Phase 2)
Core principle: **Data isolation per user**

**Enforcement at 3 levels:**
1. **Database Level:** Foreign key constraints (tasks.user_id → users.id)
2. **API Level:** JWT token validation on every request
3. **Frontend Level:** Token attachment to all API calls

**Rules:**
- ❌ No shared data between users
- ❌ No user can access another user's tasks
- ✅ Each operation filters by authenticated user_id
- ✅ Hard delete (permanent, no recovery)
- ✅ Last-write-wins for concurrent edits (no locking)

### IV. JWT Token-Based Authentication (NEW - Phase 2)
**Token Lifecycle:**
- **Issued by:** Better Auth (JavaScript library on frontend)
- **Format:** JWT with user_id, email, exp claims
- **Storage:** HTTP-only secure cookies on frontend
- **Validation:** FastAPI middleware verifies signature
- **Refresh:** Automatic silent refresh (7-day access, 14-day refresh)

**Rules:**
- ❌ No hardcoded tokens
- ❌ Tokens never exposed in URLs
- ✅ All API requests include Bearer token
- ✅ Backend extracts user_id from token
- ✅ Data filtered by extracted user_id

### V. Persistent Storage (NEW - Phase 2)
**Database:** Neon Serverless PostgreSQL

**Schema Requirements:**
- **Users table:** Managed by Better Auth (id, email, name, createdAt, updatedAt)
- **Tasks table:** Application data (id, user_id, title, description, completed, created_at, updated_at)
- **Foreign Keys:** CASCADE DELETE on user removal
- **Indexes:** user_id, completed, user_id+completed for query performance

**Rules:**
- ❌ No in-memory storage
- ❌ No file-based persistence
- ✅ All data persists across restarts
- ✅ Migrations tracked in version control
- ✅ Connection via environment variables

### VI. RESTful API Design (NEW - Phase 2)
**6 Required Endpoints:**
1. `GET /api/tasks` – List with status filter
2. `POST /api/tasks` – Create new task
3. `GET /api/tasks/{id}` – Get single task
4. `PUT /api/tasks/{id}` – Update task
5. `DELETE /api/tasks/{id}` – Hard delete task
6. `PATCH /api/tasks/{id}/complete` – Toggle completion

**Standardized Response Format:**
```json
{
  "status": "success|error",
  "data": {},
  "message": "error description"
}
```

**HTTP Status Codes:**
- 200: OK (GET, PUT, PATCH)
- 201: Created (POST)
- 400: Bad Request (validation)
- 401: Unauthorized (missing/invalid token)
- 403: Forbidden (user isolation violation)
- 404: Not Found
- 500: Server Error

---

## Phase 2: Full-Stack Web Application Features

### All 5 Phase 1 Features (Maintained)
Implemented as web application with persistent storage:
- [x] Add Task (create with title, optional description)
- [x] Delete Task (hard delete, permanent)
- [x] Update Task (partial updates allowed)
- [x] View Task List (with status filtering)
- [x] Mark as Complete (toggle status)

### Phase 2 New Features
- [x] User Authentication (Signup/Signin with Better Auth)
- [x] Multi-user Support (tasks isolated per user)
- [x] REST API Endpoints (6 endpoints as specified)
- [x] Persistent Database (Neon PostgreSQL)
- [x] Responsive Web UI (Next.js with Tailwind CSS)
- [x] JWT Authorization (token-based access control)

---

## Technology Stack (Phase 2)

### Frontend
| Component | Technology | Version |
|---|---|---|
| **Framework** | Next.js | 16+ (App Router) |
| **Language** | TypeScript | Latest |
| **Styling** | Tailwind CSS | Latest |
| **Authentication** | Better Auth | Latest |
| **HTTP Client** | fetch/axios | Built-in |
| **State Management** | React Context | Built-in |

### Backend
| Component | Technology | Version |
|---|---|---|
| **Framework** | FastAPI | Latest |
| **Language** | Python | 3.13+ |
| **ORM** | SQLModel | Latest |
| **Server** | uvicorn | Latest |
| **Validation** | Pydantic | v2 |
| **JWT** | python-jose | Latest |

### Database & Infrastructure
| Component | Technology | Notes |
|---|---|---|
| **Database** | Neon PostgreSQL | Serverless, free tier |
| **Frontend Deployment** | Vercel | Free tier |
| **Backend** | FastAPI server | Local or hosted |
| **Authentication** | Better Auth + JWT | Token-based |

---

## Project Structure (Phase 2)

```
TaskPilotAI/
├── .specify/                           # Spec-Kit Plus
│   ├── memory/
│   │   └── constitution.md             # This file
│   ├── scripts/bash/
│   └── templates/
│
├── specs/                              # Specifications
│   ├── overview.md                     # Phase 2 overview
│   ├── phase-2-plan.md                 # Implementation plan
│   ├── database/
│   │   └── schema.md                   # PostgreSQL schema
│   ├── api/
│   │   └── rest-endpoints.md           # 6 API endpoints
│   ├── features/
│   │   ├── task-crud.md                # Task operations
│   │   └── authentication.md           # Auth flow
│   └── tasks.md                        # Implementation tasks
│
├── frontend/                           # Next.js Application
│   ├── app/                            # App Router pages
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── signup/page.tsx
│   │   ├── signin/page.tsx
│   │   ├── dashboard/page.tsx
│   │   └── globals.css
│   ├── components/                     # React components
│   │   ├── TaskForm.tsx
│   │   ├── TaskList.tsx
│   │   ├── TaskCard.tsx
│   │   └── Auth/
│   ├── lib/                            # Utilities
│   │   ├── auth-client.ts
│   │   └── api.ts
│   ├── types/                          # TypeScript types
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   ├── .env.local                      # Environment variables
│   ├── tests/                          # Component tests
│   └── CLAUDE.md                       # Frontend guidelines
│
├── backend/                            # FastAPI Application
│   ├── main.py                         # Entry point
│   ├── models.py                       # SQLModel models
│   ├── db.py                           # Database connection
│   ├── schemas.py                      # Pydantic schemas
│   ├── config.py                       # Configuration
│   ├── routes/                         # API routes
│   │   ├── auth.py
│   │   └── tasks.py
│   ├── middleware/                     # Middleware
│   │   └── auth.py                     # JWT verification
│   ├── requirements.txt                # Dependencies
│   ├── .env                            # Environment variables
│   ├── tests/                          # Test suite
│   │   ├── conftest.py
│   │   ├── test_auth.py
│   │   ├── test_tasks.py
│   │   └── test_integration.py
│   └── CLAUDE.md                       # Backend guidelines
│
├── README.md                           # Setup instructions
├── CLAUDE.md                           # Root guidelines
└── history/prompts/                    # Prompt History Records
    └── phase-2/
```

---

## Quality Gates (ALL REQUIRED for Phase 2)

### Specification Gates
- ✅ All feature specs complete and detailed
- ✅ API endpoints fully documented with examples
- ✅ Database schema validated
- ✅ Authentication flow documented
- ✅ Error scenarios defined

### Code Quality Gates
- ✅ Backend: mypy (0 errors), flake8 (0 errors)
- ✅ Frontend: ESLint (0 errors), TypeScript (0 errors)
- ✅ Code coverage: ≥95% (backend), ≥90% (frontend)
- ✅ PEP 8 compliance (Python)
- ✅ No hardcoded secrets or credentials

### Functional Gates
- ✅ All tests passing (100%)
- ✅ All 5 Phase 1 features working in web UI
- ✅ Authentication workflow complete (signup/signin)
- ✅ All 6 API endpoints functional
- ✅ Data isolation verified (user can't access other users' tasks)
- ✅ JWT tokens properly refreshed
- ✅ Error handling for all edge cases

### Integration Gates
- ✅ Frontend and backend properly connected
- ✅ Neon database configured and connected
- ✅ Better Auth integrated
- ✅ CORS configured correctly
- ✅ Environment variables properly set

### Deployment Gates
- ✅ Frontend deployable to Vercel
- ✅ Backend runnable locally or hosted
- ✅ Database migrations in place
- ✅ README with complete setup instructions
- ✅ CLAUDE.md with deployment guidelines

---

## Key Decisions (Phase 2)

### Decision 1: Authenticated Users Only
- **Chosen:** No guest/anonymous access
- **Rule:** All users must signup and signin
- **Rationale:** Simplifies data isolation, aligns with "multi-user" requirement
- **No Alternative:** This is locked

### Decision 2: Automatic Token Refresh
- **Chosen:** Silent automatic refresh
- **Implementation:** Backend issues refresh tokens; frontend refreshes before expiry
- **Tokens:** 7-day access, 14-day refresh
- **Rationale:** Better UX, prevents login interruptions
- **No Alternative:** This is locked

### Decision 3: Concurrent Edit Conflict Resolution
- **Chosen:** Last-write-wins
- **Implementation:** Later update overwrites earlier update
- **No Locking:** Simplest approach for Phase 2
- **Rationale:** MVP acceptable; versioning deferred to Phase 3+
- **No Alternative:** This is locked

### Decision 4: Task Deletion Strategy
- **Chosen:** Hard delete (permanent)
- **Implementation:** Tasks permanently removed from database
- **No Recovery:** Once deleted, task is gone
- **Rationale:** Simplifies implementation, meets MVP requirements
- **No Alternative:** This is locked

### Decision 5: Rate Limiting
- **Chosen:** No rate limiting in Phase 2
- **Implementation:** All authenticated users unlimited requests
- **Deferred:** Add in Phase 4/5 with Kubernetes and API gateway
- **Rationale:** MVP scope, add later for production
- **No Alternative:** This is locked

---

## Data Isolation Verification

Every implementation must enforce user isolation at 3 levels:

### 1. Database Level
```sql
-- Foreign key constraint
ALTER TABLE tasks ADD CONSTRAINT fk_tasks_user_id
FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;

-- Index for performance
CREATE INDEX idx_tasks_user_id ON tasks(user_id);

-- Cascading delete on user removal
```

### 2. API Level
```python
# Middleware extracts user_id from JWT token
async def get_current_user(token: str) -> str:
    payload = jwt.decode(token, SECRET_KEY)
    return payload["user_id"]

# All queries filtered by user
@router.get("/api/tasks")
async def get_tasks(user_id: str = Depends(get_current_user)):
    # MUST filter: WHERE tasks.user_id = user_id
    tasks = db.query(Task).filter(Task.user_id == user_id).all()
    return tasks
```

### 3. Frontend Level
```typescript
// Attach token to every API call
const response = await fetch(`/api/tasks`, {
  headers: {
    'Authorization': `Bearer ${token}`
  }
});
```

---

## Error Handling Standards (Extended)

| Error Case | Message | HTTP | User Error? |
|---|---|---|---|
| Missing JWT token | Invalid or missing authentication token | 401 | No |
| Invalid JWT token | Invalid token signature | 401 | No |
| Token expired | Token expired. Please login again | 401 | No |
| Access denied | You do not have permission to access this task | 403 | No |
| Task not found | Task not found | 404 | Yes |
| Invalid title length | Title required (1-200 characters) | 400 | Yes |
| Validation error | [Specific field error message] | 400 | Yes |
| Concurrent edit | Task was modified. Please refresh | 409 | Yes |
| Duplicate email | Email already registered | 409 | Yes |

---

## Testing Requirements (Phase 2)

### Backend Tests
- **Unit Tests:** Models, database operations, validation
- **Integration Tests:** API endpoints with JWT auth, user isolation
- **User Isolation Tests:** Verify task ownership enforcement
- **Auth Tests:** Signup, signin, token refresh, token expiry
- **Coverage Target:** ≥95%

### Frontend Tests
- **Component Tests:** Forms, task list, auth pages
- **Integration Tests:** API client, token refresh, error handling
- **E2E Tests:** Full signup → create task → view → delete flow
- **Responsive Design:** Desktop, tablet, mobile

---

## Non-Negotiable Rules (Phase 2)

- ❌ Cannot skip specification phase
- ❌ Cannot hardcode user IDs or secrets
- ❌ Cannot write code without tests
- ❌ Cannot violate user data isolation
- ❌ Cannot use in-memory storage for production data
- ❌ Cannot add Phase 3+ features (chatbot, K8s, etc.)
- ❌ Cannot modify constitution without approval
- ❌ Cannot deploy without all quality gates passing

---

## Success Criteria (Phase 2 Complete When)

### Specification Requirements
- ✅ /specs/overview.md complete with Phase 2 details
- ✅ /specs/database/schema.md with PostgreSQL design
- ✅ /specs/api/rest-endpoints.md with 6 endpoints
- ✅ /specs/features/task-crud.md with Phase 2 requirements
- ✅ /specs/features/authentication.md with Better Auth flow
- ✅ /specs/phase-2-plan.md with implementation roadmap

### Implementation Requirements
- ✅ Backend (FastAPI):
  - Main app with 6 endpoints
  - SQLModel models for users and tasks
  - JWT middleware for authentication
  - Database connection to Neon
  - Error handling for all scenarios
  - ≥95% test coverage

- ✅ Frontend (Next.js):
  - Signup page with Better Auth
  - Signin page with Better Auth
  - Dashboard with task CRUD operations
  - Responsive design (Tailwind CSS)
  - API client with JWT token handling
  - Automatic token refresh
  - ≥90% test coverage

### Quality Requirements
- ✅ All tests passing (100%)
- ✅ Code coverage ≥95% (backend), ≥90% (frontend)
- ✅ No type errors (TypeScript, mypy)
- ✅ No linting errors (ESLint, flake8)
- ✅ All 5 Phase 1 features working in web UI
- ✅ User isolation verified and tested
- ✅ JWT tokens properly refreshed

### Functional Requirements
- ✅ User can signup with email
- ✅ User can signin and get JWT token
- ✅ User can create task (stored in database)
- ✅ User can view their tasks (filtered by user_id)
- ✅ User can update task (partial updates allowed)
- ✅ User can delete task (hard delete)
- ✅ User can mark task complete/pending
- ✅ User can filter tasks by status
- ✅ Task ownership enforced at all levels
- ✅ Data isolation verified (user A can't see user B's tasks)

### Deployment Requirements
- ✅ GitHub repository with clean monorepo structure
- ✅ Frontend deployable to Vercel
- ✅ Backend runnable locally or on a server
- ✅ Neon database configured and connected
- ✅ Environment variables documented
- ✅ README.md with complete setup instructions
- ✅ CLAUDE.md with Claude Code guidelines
- ✅ Database migrations tracked in version control

---

## Constitutional Amendments (Phase 2 Changes)

### Changes from Phase 1
1. **Storage:** In-memory → Persistent PostgreSQL database
2. **Architecture:** Single-user CLI → Multi-user web app
3. **Authentication:** None → JWT with Better Auth
4. **API:** CLI commands → 6 RESTful endpoints
5. **Frontend:** Terminal UI → Next.js web interface
6. **Scope:** Console app → Full-stack application

### Maintained from Phase 1
1. **Spec-Driven Development:** Still non-negotiable
2. **Test-First (TDD):** Still mandatory, ≥95% coverage
3. **Clean Code:** PEP 8, type hints, docstrings
4. **Quality Gates:** All 7 gates must pass

---

## Governance (Phase 2)

### Constitution Authority
This Phase 2 constitution extends Phase 1 and is the source of truth for Phase 2 development.

### Amendment Process
Changes to Phase 2 constitution require:
1. Proposal with clear rationale
2. Impact analysis
3. User approval before implementation

### Compliance Verification
Every Phase 2 commit is checked:
- Specifications exist and are complete
- All quality gates pass
- No scope creep (Phase 2 features only)
- Tests cover all new code
- Data isolation enforced
- No hardcoded secrets

---

## Timeline

| Date | Milestone | Status |
|---|---|---|
| Dec 7, 2025 | Phase 1 Complete | ✅ Complete |
| Dec 14, 2025 | Phase 2 Due | ⏳ In Progress |
| Dec 21, 2025 | Phase 3 Due | Future |
| Jan 4, 2026 | Phase 4 Due | Future |
| Jan 18, 2026 | Phase 5 Due | Future |

---

**Version**: 2.0.0
**Ratified**: 2025-12-07
**Last Amended**: 2025-12-07
**Status**: Active for Phase 1 & Phase 2
**Next Review**: Post Phase 2 Completion
