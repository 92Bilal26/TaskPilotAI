# Implementation Plan: Phase 2 - Full-Stack Web Application

**Branch**: `phase-2` | **Date**: 2025-12-07 | **Due**: 2025-12-14 | **Points**: 150
**Input**: Phase 2 specifications from `/specs/overview.md`, `/specs/database/schema.md`, `/specs/api/rest-endpoints.md`, `/specs/features/authentication.md`, `/specs/features/task-crud.md`

## Summary

Transform Phase 1 in-memory console app into a modern multi-user web application with persistent PostgreSQL storage, JWT-based authentication via Better Auth, and a responsive Next.js frontend with FastAPI REST API backend. All Phase 1 features (Add, Delete, Update, View, Mark Complete) reimplemented as web app with user isolation and token-based authorization.

**Key Achievement**: Full-stack web app with:
- 6 REST API endpoints with JWT authentication
- Multi-user support with task isolation per user
- Automatic token refresh (7-day access, 14-day refresh)
- Database persistence (Neon PostgreSQL)
- Responsive Next.js frontend (Vercel deployment ready)
- Better Auth integration for signup/signin

---

## Technical Context

**Language/Version**:
- Backend: Python 3.13+
- Frontend: TypeScript (Next.js 16+)

**Primary Dependencies**:
- Backend: FastAPI, SQLModel, uvicorn, python-jose (JWT), pydantic
- Frontend: Next.js 16+ (App Router), TypeScript, Tailwind CSS, Better Auth SDK, React

**Storage**: Neon Serverless PostgreSQL with SQLModel ORM

**Testing**:
- Backend: pytest with pytest-cov (≥95% coverage required)
- Frontend: Jest or Vitest with React Testing Library

**Target Platform**: Web application (Vercel frontend + FastAPI server backend)

**Project Type**: Full-stack web application (monorepo with frontend + backend separation)

**Performance Goals**:
- API response time: <200ms p95
- Frontend Lighthouse score: >90
- Database query time: <50ms p95
- Page load: <3s
- Bundled frontend: <200KB gzipped

**Constraints**:
- JWT tokens expire after 7 days (access) / 14 days (refresh)
- Automatic silent token refresh (Better Auth handles)
- No rate limiting in Phase 2 (add in Phase 4 with Kubernetes)
- Hard delete (no soft delete/audit log in Phase 2)
- Last-write-wins for concurrent edits (no versioning)
- User isolation required at database, API, and frontend levels

**Scale/Scope**:
- ~3,000 LOC backend (models, routes, middleware)
- ~2,500 LOC frontend (components, pages, services)
- ~60+ test cases (backend + frontend)
- 5 core features + authentication
- ~2,000 database queries/day (estimated)

---

## Constitution Check

**Reference**: `.specify/memory/constitution.md` (Phase 1) + Phase 2 additions

### Phase 2 Specific Gates

| Gate | Phase 1 | Phase 2 | Status |
|------|---------|---------|--------|
| **Spec-Driven** | All features specified | ✅ All Phase 2 specs created + clarified | ✅ PASS |
| **Test-First** | ≥95% coverage | ✅ Required for both backend + frontend | ✅ PASS |
| **Python/Code Quality** | PEP 8, mypy, flake8 | ✅ Backend: PEP 8, mypy, flake8 | ✅ PASS |
| **Frontend Quality** | N/A | ✅ TypeScript, ESLint, Prettier | ✅ PASS |
| **Authentication** | N/A | ✅ JWT + Better Auth (Phase 2 requirement) | ✅ PASS |
| **Database** | In-memory only | ✅ Neon PostgreSQL (Phase 2 requirement) | ✅ PASS |
| **Multi-Repo** | N/A | ✅ Frontend + Backend separation allowed | ✅ PASS |
| **External Dependencies** | None allowed | ✅ FastAPI, SQLModel, Next.js, Better Auth (required) | ✅ PASS |
| **User Isolation** | N/A | ✅ Tasks filtered by user_id (DB, API, Frontend) | ✅ PASS |

**Gate Status**: ✅ All gates pass. Phase 2 approved for implementation.

**Re-evaluation Trigger**: After backend models and API contracts are designed.

---

## Project Structure

### Documentation (Phase 2 Specs & Plans)

```
specs/
├── overview.md                    # Phase 2 overview + Hackathon verification + Clarifications ✅
├── database/
│   └── schema.md                 # PostgreSQL schema (users + tasks) ✅
├── api/
│   └── rest-endpoints.md         # 6 REST endpoints + JWT auth ✅
├── features/
│   ├── authentication.md         # Better Auth + JWT flow ✅
│   └── task-crud.md             # Task operations ✅
├── phase-2-plan.md               # This file (Phase 1 planning output)
├── research.md                    # Phase 0 output (TBD)
├── data-model.md                  # Phase 1 design output (TBD)
├── quickstart.md                  # Phase 1 design output (TBD)
└── contracts/                     # Phase 1 design output (TBD)
    ├── openapi.yaml              # OpenAPI 3.0 spec
    └── models.yaml               # Data models schema
```

### Source Code (Monorepo: frontend + backend)

```
TaskPilotAI/
├── backend/
│   ├── main.py                    # FastAPI app entry point with CORS, middleware
│   ├── models.py                  # SQLModel: User (from Better Auth), Task
│   ├── db.py                      # Database connection, session management
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py               # Auth endpoints (signup/signin)
│   │   └── tasks.py              # Task CRUD endpoints (6 endpoints)
│   ├── middleware/
│   │   ├── __init__.py
│   │   └── auth.py               # JWT verification middleware
│   ├── schemas.py                 # Pydantic request/response models
│   ├── config.py                  # Environment variables
│   ├── requirements.txt           # Python dependencies
│   ├── .env                       # LOCAL ONLY: DATABASE_URL, JWT_SECRET
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py           # Pytest fixtures (database, client)
│   │   ├── test_auth.py          # JWT middleware, token validation
│   │   ├── test_tasks.py         # CRUD operations, validation
│   │   ├── test_integration.py   # End-to-end workflows
│   │   └── test_user_isolation.py # User isolation verification
│   ├── pytest.ini
│   └── CLAUDE.md                 # Backend development guidelines
│
├── frontend/
│   ├── app/
│   │   ├── page.tsx              # Home/login page
│   │   ├── signup/
│   │   │   └── page.tsx          # Signup form
│   │   ├── dashboard/
│   │   │   ├── page.tsx          # Dashboard (task list)
│   │   │   ├── layout.tsx        # Dashboard layout with nav
│   │   │   ├── tasks/
│   │   │   │   ├── [id]/
│   │   │   │   │   └── page.tsx  # Edit task page
│   │   │   │   └── new/
│   │   │   │       └── page.tsx  # Create task page
│   │   │   └── settings/
│   │   │       └── page.tsx      # User settings/logout
│   │   ├── layout.tsx            # Root layout (auth guard)
│   │   ├── globals.css           # Global styles
│   │   └── favicon.ico
│   ├── components/
│   │   ├── TaskForm.tsx          # Create/edit task form
│   │   ├── TaskList.tsx          # Display tasks with filters
│   │   ├── TaskCard.tsx          # Individual task item
│   │   ├── Auth/
│   │   │   ├── LoginForm.tsx
│   │   │   ├── SignupForm.tsx
│   │   │   └── AuthGuard.tsx    # Require auth wrapper
│   │   ├── ui/
│   │   │   ├── Button.tsx
│   │   │   ├── Input.tsx
│   │   │   └── Modal.tsx
│   │   └── Loading.tsx
│   ├── lib/
│   │   ├── auth-client.ts        # Better Auth SDK initialization
│   │   └── api.ts                # API client (fetch wrapper with token)
│   ├── types/
│   │   └── index.ts              # TypeScript types (Task, User)
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   ├── next.config.ts
│   ├── .env.local                # LOCAL ONLY: NEXT_PUBLIC_API_URL
│   ├── tests/
│   │   ├── components.test.tsx   # Component unit tests
│   │   └── integration.test.tsx  # E2E user workflows
│   ├── jest.config.ts
│   └── CLAUDE.md                 # Frontend development guidelines
│
├── .spec-kit/
│   └── config.yaml               # Spec-Kit configuration
│
├── CLAUDE.md                      # Root guide (updated with Phase 2)
└── README.md                      # Enhanced with Phase 2 sections
```

**Structure Decision**: Full-stack monorepo with separate `frontend/` and `backend/` folders. This allows:
- Parallel development (frontend team + backend team)
- Independent deployment (Vercel for frontend, separate server for backend)
- Shared specifications and CLAUDE.md guidance
- Single Claude Code context for full-stack implementation

---

## Phase 0: Research & Design Decisions (Ready for Execution)

### Research Tasks

**Task 1: Better Auth JWT Implementation**
- Investigate: How Better Auth issues JWT tokens for custom backends
- Outcome: Document token structure, refresh mechanism, shared secret setup
- File: `specs/research.md` (section: Better Auth JWT)

**Task 2: FastAPI + SQLModel + Neon Integration**
- Investigate: Connection pooling, async sessions, migration strategy
- Outcome: Setup guide for FastAPI ↔ Neon PostgreSQL via SQLModel
- File: `specs/research.md` (section: Database Integration)

**Task 3: JWT Middleware in FastAPI**
- Investigate: Token extraction, signature verification, error responses
- Outcome: Reusable middleware for all protected routes
- File: `specs/research.md` (section: JWT Middleware)

**Task 4: Next.js API Client with Token Refresh**
- Investigate: Fetch wrapper, automatic token attachment, error handling
- Outcome: API client implementation pattern
- File: `specs/research.md` (section: Frontend API Client)

**Task 5: User Isolation in REST API**
- Investigate: Query filtering patterns, 403 Forbidden responses
- Outcome: Middleware for enforcing user_id from JWT
- File: `specs/research.md` (section: User Isolation)

---

## Phase 1: Design & Contracts (Ready for Execution)

### 1. Data Model Design

**Entities**:
- **User** (managed by Better Auth)
  - id: UUID (primary key)
  - email: string (unique)
  - name: string (optional)
  - emailVerified: boolean (default false)
  - createdAt: timestamp
  - updatedAt: timestamp

- **Task** (owned by User)
  - id: integer (auto-increment primary key)
  - user_id: UUID (foreign key → users.id, NOT NULL)
  - title: string (NOT NULL, 1-200 chars)
  - description: text (nullable, max 1000 chars)
  - completed: boolean (default false)
  - created_at: timestamp (UTC, NOT NULL)
  - updated_at: timestamp (UTC, NOT NULL)

**Relationships**:
- User (1) ← has many → (Many) Task
- Foreign key: tasks.user_id → users.id
- Cascade delete: delete user → delete all tasks
- Indexes: (user_id), (user_id, completed), (created_at)

**Validation Rules** (enforced at API level + database level):
- title: required, 1-200 characters, whitespace trimmed
- description: optional, max 1000 characters
- completed: boolean only
- user_id: must match JWT token user_id
- timestamps: ISO 8601 UTC format

**Output**: `specs/data-model.md` (TBD)

### 2. API Contracts

**6 Endpoints** (all require JWT):

| Method | Endpoint | Purpose | Auth |
|--------|----------|---------|------|
| POST | /api/tasks | Create task | Required |
| GET | /api/tasks?status={all\|pending\|completed} | List user's tasks | Required |
| GET | /api/tasks/{id} | Get single task | Required |
| PUT | /api/tasks/{id} | Update task | Required |
| DELETE | /api/tasks/{id} | Delete task | Required |
| PATCH | /api/tasks/{id}/complete | Toggle completion | Required |

**Response Format** (standardized):
```json
{
  "status": "success",
  "data": { ... }
}
```

**Error Format**:
```json
{
  "status": "error",
  "message": "...",
  "code": "ERROR_CODE"
}
```

**HTTP Status Codes**:
- 200: Success (GET, PUT, PATCH, DELETE)
- 201: Created (POST)
- 400: Validation error
- 401: Unauthorized (missing/invalid token)
- 403: Forbidden (wrong user)
- 404: Not found
- 500: Server error

**Output**: `specs/contracts/openapi.yaml` (OpenAPI 3.0) (TBD)

### 3. Quick Start Implementation

**Prerequisites**:
- Python 3.13+, Node.js 18+, PostgreSQL/Neon account

**Backend Setup**:
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Set DATABASE_URL in .env
uvicorn main:app --reload --port 8000
```

**Frontend Setup**:
```bash
cd frontend
npm install
# Set NEXT_PUBLIC_API_URL in .env.local
npm run dev
# Visit http://localhost:3000
```

**Example Flow**:
1. User visits localhost:3000
2. Clicks signup, fills form
3. Better Auth creates account, issues JWT
4. Redirected to dashboard
5. Creates task via form
6. Frontend POSTs to /api/tasks with JWT
7. Backend verifies token, extracts user_id
8. Task saved to database
9. User sees task in list (filtered by user_id)

**Output**: `specs/quickstart.md` (TBD)

### 4. Agent Context Files

Run: `.specify/scripts/bash/update-agent-context.sh claude`

**Output**:
- `CLAUDE.md` (updated with Phase 2 tech)
- `frontend/CLAUDE.md` (new - Next.js, TypeScript, Better Auth)
- `backend/CLAUDE.md` (new - FastAPI, SQLModel, JWT)

---

## Implementation Phases

### Phase 0: Planning ✅ (This document)
- Specifications created + clarified
- Hackathon requirements verified
- Technical decisions documented

### Phase 1: Design (In Progress via /sp.plan)
- Data model finalized
- API contracts (OpenAPI)
- Research findings consolidated
- Agent context updated

### Phase 2: Implementation (Via /sp.tasks → /sp.implement)
1. Backend setup & tests
   - FastAPI app structure
   - Database models
   - Authentication middleware
   - CRUD routes
   - Test suite

2. Frontend setup & tests
   - Next.js project
   - Better Auth integration
   - Pages and components
   - API client
   - Test suite

3. Integration & deployment
   - E2E testing
   - Vercel deployment
   - Backend server
   - Production readiness

---

## Risk Analysis

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|-----------|
| JWT token refresh complexity | Medium | High | Use Better Auth SDK (handles refresh) |
| Cross-Origin (CORS) issues | Medium | Medium | FastAPI CORS middleware for frontend URL |
| User isolation bugs | Medium | Critical | Extensive testing; verify user_id filtering |
| Database connection issues | Low | High | Connection pooling; environment variable validation |
| Type mismatches (TS/Pydantic) | Medium | Medium | Strict TypeScript + mypy; test contract compliance |
| Token expiry during long operations | Low | Medium | Automatic refresh tokens (14-day refresh token) |
| Concurrent edits | Low | Low | Last-write-wins strategy (acceptable for Phase 2) |
| Deployment differences | Medium | Medium | Environment parity; test locally first |

---

## Success Criteria (Definition of Done)

### Backend Complete When:
- ✅ FastAPI app with all 6 endpoints
- ✅ SQLModel models for Task + User
- ✅ Neon PostgreSQL connection
- ✅ JWT middleware verification
- ✅ User isolation enforced (queries filtered by user_id)
- ✅ Error handling with correct HTTP status codes
- ✅ ≥95% test coverage
- ✅ mypy: 0 errors (strict mode)
- ✅ flake8: 0 errors (PEP 8)
- ✅ All 5 Phase 1 features working as REST endpoints

### Frontend Complete When:
- ✅ Next.js app with App Router
- ✅ Better Auth signup/signin pages
- ✅ Dashboard with task list
- ✅ Create/edit/delete task forms
- ✅ API client with automatic token attachment
- ✅ Automatic token refresh (no interruption)
- ✅ Error handling (401, 403, 404 responses)
- ✅ Loading states and error messages
- ✅ Responsive design (mobile-friendly)
- ✅ Unit + integration tests
- ✅ TypeScript: 0 errors
- ✅ ESLint: 0 errors

### Integration Complete When:
- ✅ End-to-end signup/login flow works
- ✅ Create/read/update/delete tasks fully functional
- ✅ User isolation verified (users can't see each other's tasks)
- ✅ Token refresh automatic (no re-login interruption)
- ✅ Frontend deployed to Vercel
- ✅ Backend running on server
- ✅ Database connected (Neon)
- ✅ All tests passing (100%)
- ✅ Code coverage ≥95%
- ✅ No warnings or errors

### Phase 2 Complete When:
1. ✅ All 5 Phase 1 features work in web UI
2. ✅ User signup/signin functional via Better Auth
3. ✅ JWT authentication on all API endpoints
4. ✅ Multi-user support with task isolation
5. ✅ All 6 REST API endpoints functional
6. ✅ Database schema properly designed and normalized
7. ✅ Automatic token refresh (7-day access, 14-day refresh)
8. ✅ Frontend deployed to Vercel
9. ✅ Backend running and accessible
10. ✅ 100% test pass rate
11. ✅ ≥95% code coverage
12. ✅ All type/lint checks pass
13. ✅ **Verified against Hackathon II Phase 2 requirements**

---

## Complexity Tracking

**Justification**: No complexity violations expected.

**Reasoning**: Phase 2 specifications explicitly require web-stack components (frontend, REST API, database). Monorepo structure allows Claude Code to edit both frontend and backend efficiently. All technology choices align with hackathon requirements.

---

## Timeline

| Milestone | Target Date | Status |
|-----------|-------------|--------|
| **Specifications** | 2025-12-07 | ✅ Complete |
| **Clarifications** | 2025-12-07 | ✅ Complete |
| **Hackathon Verification** | 2025-12-07 | ✅ Complete |
| **Implementation Plan** | 2025-12-07 | ✅ Complete (this doc) |
| **Research & Design** | 2025-12-08 | ⏳ Via /sp.plan |
| **Backend Implementation** | 2025-12-10 | ⏳ Via /sp.tasks + /sp.implement |
| **Frontend Implementation** | 2025-12-10 | ⏳ Via /sp.tasks + /sp.implement |
| **Integration & Testing** | 2025-12-12 | ⏳ Manual |
| **Deployment** | 2025-12-13 | ⏳ Manual |
| **Phase 2 Due** | 2025-12-14 | ⏳ Submission deadline |

---

## Next Command

**Ready to execute**: `/sp.tasks`

This will generate `specs/tasks.md` with actionable implementation tasks, breaking down:
- Backend setup tasks (main.py, models, routes, middleware, tests)
- Frontend setup tasks (pages, components, API client, tests)
- Integration and deployment tasks
- Testing and quality gate tasks

Each task will be concrete, testable, and assigned in order of execution.

---

**Status**: Phase 1 Planning Complete ✅
**Next**: `/sp.tasks` (Task Breakdown)
**Timeline**: 1 week to complete (due Dec 14, 2025)
**Points**: 150

*Created: 2025-12-07*
*Branch: phase-2*
*Duration: 7 days*
