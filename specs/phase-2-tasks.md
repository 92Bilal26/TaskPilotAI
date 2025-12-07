# Phase 2 Implementation Tasks - Full-Stack Web Application
**Date**: 2025-12-07
**Feature**: Phase 2 Full-Stack Todo Web App
**Due**: 2025-12-14
**Points**: 150

---

## Overview

Complete Phase 2 implementation tasks for transforming the Phase 1 console app into a modern multi-user web application with:
- **Backend**: FastAPI with SQLModel ORM, JWT authentication, 6 REST API endpoints
- **Frontend**: Next.js with Better Auth integration, responsive design, task CRUD UI
- **Database**: Neon PostgreSQL with user-task relationships and data isolation
- **Testing**: ≥95% backend coverage, ≥90% frontend coverage
- **Deployment**: Vercel (frontend) + FastAPI server (backend)

**Total Tasks**: 232 tasks across 7 phases
**Status**: Ready for `/sp.implement` execution

---

## Phase 1: Setup & Initialization (15 tasks)

### Goal
Initialize backend and frontend projects with required structure, configurations, and dependencies.

### Tasks

- [ ] T001 Create backend project structure in `/backend` with `main.py`, `models.py`, `db.py`, `routes/`, `middleware/`, `tests/` folders
- [ ] T002 Create `backend/requirements.txt` with: fastapi, uvicorn, sqlmodel, python-jose, pydantic, python-dotenv, pytest, pytest-cov, mypy, flake8
- [ ] T003 Create `backend/.env` with DATABASE_URL (Neon connection string), JWT_SECRET, BETTER_AUTH_SECRET placeholders
- [ ] T004 Create `backend/config.py` with environment variable loading via pydantic (Settings class)
- [ ] T005 Create `backend/db.py` with Neon PostgreSQL connection pool and SQLModel session factory
- [ ] T006 Create `backend/pytest.ini` and `backend/conftest.py` with database fixtures for testing
- [ ] T007 Create frontend project structure in `/frontend` with Next.js 16+ App Router: `app/`, `components/`, `lib/`, `types/`, `tests/` folders
- [ ] T008 Create `frontend/package.json` with: next, react, typescript, tailwind-css, @better-auth/react, jest, @testing-library/react
- [ ] T009 Create `frontend/.env.local` with NEXT_PUBLIC_API_URL placeholder
- [ ] T010 Create `frontend/tsconfig.json` with strict mode enabled
- [ ] T011 Create `frontend/tailwind.config.ts` with custom styling configuration
- [ ] T012 Create root `.env.example` documenting all environment variables for both frontend and backend
- [ ] T013 [P] Create `backend/CLAUDE.md` with FastAPI, SQLModel, JWT authentication guidelines
- [ ] T014 [P] Create `frontend/CLAUDE.md` with Next.js 16+, TypeScript, Better Auth, Tailwind CSS guidelines
- [ ] T015 Update root `/CLAUDE.md` with Phase 2 specific instructions for full-stack development

---

## Phase 2: Foundational Tasks (19 tasks)

### Goal
Create shared infrastructure and models that all user stories depend on.

### Tasks

- [ ] T016 Create `backend/models.py` with SQLModel `User` model (id, email, name, emailVerified, createdAt, updatedAt) - managed by Better Auth
- [ ] T017 Create SQLModel `Task` model in `backend/models.py` (id, user_id FK, title, description, completed, created_at, updated_at)
- [ ] T018 Add SQLModel relationship between User and Task (one-to-many with cascade delete)
- [ ] T019 Create Alembic migrations folder structure in `backend/alembic/` for database schema versioning
- [ ] T020 Create initial migration script in `backend/alembic/versions/001_initial_schema.py` for users and tasks tables
- [ ] T021 Create `backend/schemas.py` with Pydantic models for request/response validation: `TaskCreate`, `TaskUpdate`, `TaskResponse`
- [ ] T022 Create `backend/middleware/auth.py` with JWT verification middleware that extracts user_id from token and validates signature
- [ ] T023 Create `backend/routes/__init__.py` to register all route blueprints
- [ ] T024 Create standardized response wrapper in `backend/main.py` for success/error JSON responses
- [ ] T025 Create `frontend/lib/api.ts` with fetch wrapper that automatically attaches JWT Bearer token to all requests
- [ ] T026 Create `frontend/lib/auth-client.ts` with Better Auth SDK initialization and session management
- [ ] T027 Create `frontend/types/index.ts` with TypeScript interfaces: Task, User, APIResponse
- [ ] T028 Create `frontend/app/globals.css` with Tailwind CSS base styles and custom components
- [ ] T029 Create `frontend/app/layout.tsx` root layout with auth guard wrapper component
- [ ] T030 Create `frontend/components/Auth/AuthGuard.tsx` wrapper that redirects unauthenticated users to login
- [ ] T031 Create `backend/tests/test_auth.py` with JWT middleware test fixtures
- [ ] T032 Create `backend/tests/test_models.py` with SQLModel validation tests
- [ ] T033 Create `frontend/jest.config.ts` with Next.js and React Testing Library configuration
- [ ] T034 Create `frontend/tests/setup.ts` with test utilities and mock API client

---

## Phase 3: User Story 1 - Authentication (47 tasks)

### Goal
Enable users to create accounts and authenticate with JWT tokens via Better Auth.

### User Story
**US1**: As a new user, I can sign up with email/password and receive a JWT token. As an existing user, I can sign in and resume my session with automatic token refresh.

### Backend Tasks

- [ ] T035 [P] [US1] Create `backend/routes/auth.py` with POST /auth/signup endpoint (email, password, name validation)
- [ ] T036 [P] [US1] Implement signup logic: hash password, create user in DB, issue JWT token with user_id claim
- [ ] T037 [P] [US1] Add email uniqueness validation in signup (return 409 if duplicate)
- [ ] T038 [P] [US1] Create POST /auth/signin endpoint (email, password validation)
- [ ] T039 [P] [US1] Implement signin logic: verify credentials, issue JWT token
- [ ] T040 [P] [US1] Add password hashing using bcrypt in signup/signin endpoints
- [ ] T041 [US1] Create POST /auth/refresh endpoint that issues new token from valid refresh token
- [ ] T042 [US1] Add JWT token blacklist or revocation mechanism for logout (store in Redis or DB)
- [ ] T043 [US1] Implement token extraction from Authorization: Bearer header in middleware
- [ ] T044 [US1] Implement JWT signature verification using BETTER_AUTH_SECRET
- [ ] T045 [US1] Extract user_id from JWT payload and attach to request context
- [ ] T046 [US1] Return 401 Unauthorized for missing/invalid tokens
- [ ] T047 [US1] Handle token expiry with 401 response (frontend will refresh)
- [ ] T048 [P] [US1] Create `backend/tests/test_auth.py` with test_signup_success (creates user, returns token with user_id)
- [ ] T049 [P] [US1] Add test_signup_duplicate_email (409 Conflict)
- [ ] T050 [P] [US1] Add test_signup_invalid_email (400 Bad Request)
- [ ] T051 [P] [US1] Add test_signup_weak_password (400 Bad Request)
- [ ] T052 [P] [US1] Add test_signin_success (returns valid JWT)
- [ ] T053 [P] [US1] Add test_signin_invalid_password (401 Unauthorized)
- [ ] T054 [P] [US1] Add test_signin_nonexistent_user (401 Unauthorized)
- [ ] T055 [US1] Add test_jwt_middleware_missing_token (401)
- [ ] T056 [US1] Add test_jwt_middleware_invalid_signature (401)
- [ ] T057 [US1] Add test_jwt_middleware_expired_token (401)

### Frontend Tasks

- [ ] T058 [P] [US1] Create `frontend/app/page.tsx` (home/login page with signup/signin redirect)
- [ ] T059 [P] [US1] Create `frontend/app/signup/page.tsx` with signup form component
- [ ] T060 [P] [US1] Create `frontend/app/signin/page.tsx` with signin form component
- [ ] T061 [P] [US1] Create `frontend/components/Auth/SignupForm.tsx` with email/password inputs and validation
- [ ] T062 [P] [US1] Create `frontend/components/Auth/LoginForm.tsx` (signin) with email/password inputs
- [ ] T063 [US1] Implement Better Auth SDK integration in signup form (call signUp.email)
- [ ] T064 [US1] Implement Better Auth SDK integration in signin form (call signIn.email)
- [ ] T065 [US1] Handle signup/signin success: store JWT token, redirect to dashboard
- [ ] T066 [US1] Handle signup/signin errors: display error message to user
- [ ] T067 [US1] Implement automatic JWT token storage in httpOnly cookies via Better Auth
- [ ] T068 [US1] Implement automatic token refresh interceptor in API client (`frontend/lib/api.ts`)
- [ ] T069 [US1] Refresh token before expiry (check expiration time, refresh at 6.5 days for 7-day token)
- [ ] T070 [US1] Handle refresh failure: redirect to signin page
- [ ] T071 [P] [US1] Create `frontend/components/Auth/AuthGuard.tsx` that checks session before rendering protected pages
- [ ] T072 [P] [US1] Create loading state component while checking authentication status
- [ ] T073 [US1] Create error message component for auth errors (wrong password, email exists, etc.)
- [ ] T074 [P] [US1] Create `frontend/tests/auth.test.tsx` with test_signup_form_renders
- [ ] T075 [P] [US1] Add test_signup_form_submission (calls Better Auth SDK)
- [ ] T076 [P] [US1] Add test_signin_form_renders
- [ ] T077 [P] [US1] Add test_signin_form_submission
- [ ] T078 [US1] Add test_auth_guard_redirects_unauthenticated_users
- [ ] T079 [US1] Add test_token_refresh_interceptor_attaches_bearer_token

---

## Phase 4: User Story 2 - Task CRUD (65 tasks)

### Goal
Implement all task operations (Create, Read, Update, Delete) with proper user isolation and validation.

### User Story
**US2**: As an authenticated user, I can create tasks with title and optional description, view all my tasks, update task details, and delete tasks. All operations are isolated to my tasks only.

### Backend Tasks

- [ ] T080 [P] [US2] Create `backend/routes/tasks.py` with POST /api/tasks endpoint (create task)
- [ ] T081 [P] [US2] Implement create task: validate title (1-200 chars), extract user_id from JWT, store in DB, return 201
- [ ] T082 [P] [US2] Create GET /api/tasks endpoint (list user's tasks with optional status filter)
- [ ] T083 [P] [US2] Implement list tasks: query tasks WHERE user_id = current_user_id, support ?status=pending|completed|all filter
- [ ] T084 [P] [US2] Add pagination support to GET /api/tasks (?page=1&limit=50)
- [ ] T085 [P] [US2] Create GET /api/tasks/{id} endpoint (get single task)
- [ ] T086 [P] [US2] Implement get task: verify task.user_id == current_user_id, return 200 on success, 404 if not found, 403 if unauthorized
- [ ] T087 [P] [US2] Create PUT /api/tasks/{id} endpoint (update task)
- [ ] T088 [P] [US2] Implement update task: allow partial updates (title and/or description), preserve created_at, update updated_at
- [ ] T089 [P] [US2] Implement update validation: verify user ownership (403 if not owner), verify title constraints (400 if invalid)
- [ ] T090 [P] [US2] Create DELETE /api/tasks/{id} endpoint (hard delete)
- [ ] T091 [P] [US2] Implement delete: verify ownership (403), delete task (hard delete, no soft delete), return 200 on success
- [ ] T092 [US2] Implement concurrency handling: use last-write-wins (no row locking), updated_at reflects latest change
- [ ] T093 [US2] Add user_id extraction from JWT token to all task routes (dependency injection via Depends)
- [ ] T094 [US2] Implement ownership check in all routes: filter queries by user_id, return 403 if user tries to access another's tasks
- [ ] T095 [US2] Create helper function in `backend/models.py` for user isolation checks
- [ ] T096 [P] [US2] Add title length validation: min 1, max 200 characters (strip whitespace)
- [ ] T097 [P] [US2] Add description length validation: max 1000 characters (optional field)
- [ ] T098 [P] [US2] Add timestamp format validation: ISO 8601 UTC in created_at and updated_at
- [ ] T099 [P] [US2] Add response schema in `backend/schemas.py`: TaskResponse with id, user_id, title, description, completed, created_at, updated_at
- [ ] T100 [P] [US2] Create `backend/tests/test_tasks.py` with test_create_task_success
- [ ] T101 [P] [US2] Add test_create_task_invalid_title_too_long (400)
- [ ] T102 [P] [US2] Add test_create_task_missing_title (400)
- [ ] T103 [P] [US2] Add test_create_task_unauthorized (401 - no token)
- [ ] T104 [P] [US2] Add test_list_tasks_empty (returns [])
- [ ] T105 [P] [US2] Add test_list_tasks_returns_only_user_tasks (multiple users scenario)
- [ ] T106 [P] [US2] Add test_list_tasks_filter_by_status (status=pending, completed, all)
- [ ] T107 [P] [US2] Add test_get_task_success
- [ ] T108 [P] [US2] Add test_get_task_not_found (404)
- [ ] T109 [P] [US2] Add test_get_task_forbidden (403 - trying to get another user's task)
- [ ] T110 [P] [US2] Add test_update_task_success
- [ ] T111 [P] [US2] Add test_update_task_partial (only title, only description)
- [ ] T112 [P] [US2] Add test_update_task_preserves_created_at
- [ ] T113 [P] [US2] Add test_update_task_forbidden (403)
- [ ] T114 [P] [US2] Add test_delete_task_success (204 or 200)
- [ ] T115 [P] [US2] Add test_delete_task_not_found (404)
- [ ] T116 [P] [US2] Add test_delete_task_forbidden (403)
- [ ] T117 [US2] Add test_user_isolation (user A cannot see user B's tasks)

### Frontend Tasks

- [ ] T118 [P] [US2] Create `frontend/app/dashboard/page.tsx` (main dashboard with task list)
- [ ] T119 [P] [US2] Create `frontend/app/dashboard/tasks/new/page.tsx` (create task form)
- [ ] T120 [P] [US2] Create `frontend/app/dashboard/tasks/[id]/page.tsx` (edit task form)
- [ ] T121 [P] [US2] Create `frontend/components/TaskList.tsx` (displays all user tasks with filters)
- [ ] T122 [P] [US2] Create `frontend/components/TaskCard.tsx` (individual task item with action buttons)
- [ ] T123 [P] [US2] Create `frontend/components/TaskForm.tsx` (reusable form for create/edit)
- [ ] T124 [P] [US2] Create `frontend/components/TaskActions.tsx` (buttons for edit, delete, complete)
- [ ] T125 [US2] Implement createTask() in API client (POST /api/tasks) with error handling
- [ ] T126 [US2] Implement listTasks() in API client (GET /api/tasks) with status filter support
- [ ] T127 [US2] Implement getTask() in API client (GET /api/tasks/{id})
- [ ] T128 [US2] Implement updateTask() in API client (PUT /api/tasks/{id})
- [ ] T129 [US2] Implement deleteTask() in API client (DELETE /api/tasks/{id})
- [ ] T130 [US2] Add loading states to task operations (show spinner during request)
- [ ] T131 [US2] Add error handling: display error messages for 400, 404, 403 responses
- [ ] T132 [US2] Implement form validation on frontend (title required, max lengths)
- [ ] T133 [P] [US2] Create `frontend/components/ui/Button.tsx` reusable button component
- [ ] T134 [P] [US2] Create `frontend/components/ui/Input.tsx` reusable input component
- [ ] T135 [P] [US2] Create `frontend/components/Loading.tsx` loading spinner component
- [ ] T136 [US2] Create `frontend/components/ErrorMessage.tsx` error display component
- [ ] T137 [P] [US2] Create `frontend/tests/task-list.test.tsx` with test_task_list_renders
- [ ] T138 [P] [US2] Add test_task_list_fetches_tasks (calls API)
- [ ] T139 [P] [US2] Add test_task_card_renders_task_details
- [ ] T140 [P] [US2] Add test_task_card_shows_action_buttons
- [ ] T141 [P] [US2] Add test_task_form_create_new_task
- [ ] T142 [P] [US2] Add test_task_form_edit_existing_task
- [ ] T143 [US2] Add test_delete_task_confirmation (shows confirmation dialog)
- [ ] T144 [US2] Add test_error_handling_displays_message_on_api_failure

---

## Phase 5: User Story 3 - Task Filtering & Completion (23 tasks)

### Goal
Enable users to filter tasks by status and toggle task completion status.

### User Story
**US3**: As an authenticated user, I can view tasks filtered by status (pending, completed, all) and mark tasks as complete or incomplete.

### Backend Tasks

- [ ] T145 [P] [US3] Create PATCH /api/tasks/{id}/complete endpoint in `backend/routes/tasks.py`
- [ ] T146 [P] [US3] Implement toggle completion: read completed from request body, update task.completed, update updated_at
- [ ] T147 [P] [US3] Add ownership verification in completion endpoint (403 if not owner)
- [ ] T148 [P] [US3] Verify status filter in list endpoint works with database queries (WHERE completed = true/false)
- [ ] T149 [P] [US3] Create tests for PATCH /api/tasks/{id}/complete in test_tasks.py
- [ ] T150 [P] [US3] Add test_complete_task_success (toggles false → true)
- [ ] T151 [P] [US3] Add test_complete_task_toggle_back (true → false)
- [ ] T152 [P] [US3] Add test_complete_task_updates_timestamp
- [ ] T153 [US3] Add test_list_tasks_filter_pending
- [ ] T154 [US3] Add test_list_tasks_filter_completed
- [ ] T155 [US3] Add test_list_tasks_filter_all

### Frontend Tasks

- [ ] T156 [P] [US3] Add status filter tabs to `frontend/components/TaskList.tsx` (All, Pending, Completed)
- [ ] T157 [P] [US3] Implement filter logic: call listTasks() with ?status parameter
- [ ] T158 [P] [US3] Add visual indicator for completed tasks (strikethrough, opacity, checkbox state)
- [ ] T159 [P] [US3] Create `frontend/components/TaskStatusBadge.tsx` component showing task status
- [ ] T160 [US3] Implement toggleCompletion() in TaskCard component
- [ ] T161 [US3] Call API PATCH /api/tasks/{id}/complete on checkbox toggle
- [ ] T162 [US3] Update UI immediately (optimistic update) before API response
- [ ] T163 [US3] Handle API errors: revert UI state if API fails
- [ ] T164 [P] [US3] Add test_task_list_filter_tabs_render to test file
- [ ] T165 [P] [US3] Add test_task_list_filter_by_pending (calls API with ?status=pending)
- [ ] T166 [P] [US3] Add test_task_card_toggle_completion_updates_ui
- [ ] T167 [US3] Add test_error_handling_reverts_optimistic_update_on_failure

---

## Phase 6: Integration & Deployment (38 tasks)

### Goal
Ensure complete end-to-end functionality and deploy to Vercel + backend server.

### Backend Tasks

- [ ] T168 Create Neon PostgreSQL database and get CONNECTION_URL
- [ ] T169 Run Alembic migrations: `alembic upgrade head` to create schema
- [ ] T170 [P] Verify database tables exist: users, tasks with correct columns
- [ ] T171 [P] Test database connection with sample query in test suite
- [ ] T172 [P] Add CORS middleware to FastAPI app for frontend URL (http://localhost:3000 + Vercel domain)
- [ ] T173 [P] Test all 6 endpoints work together: create task → list → get → update → complete → delete
- [ ] T174 [P] Verify JWT middleware applies to all protected routes
- [ ] T175 [P] Test user isolation: create tasks as User A, verify User B cannot access them
- [ ] T176 Run full test suite: `pytest -v` (expect ≥95% coverage)
- [ ] T177 Run type checker: `mypy src/` (expect 0 errors)
- [ ] T178 Run linter: `flake8 src/` (expect 0 errors)
- [ ] T179 [P] Fix any test failures, type errors, linting issues
- [ ] T180 [P] Create `backend/Procfile` for server deployment (e.g., Heroku or Railway)
- [ ] T181 [P] Test backend locally: `uvicorn main:app --reload --port 8000`
- [ ] T182 Deploy backend to server (Heroku, Railway, or other)
- [ ] T183 Test backend deployment: make API calls to deployed backend

### Frontend Tasks

- [ ] T184 [P] Install dependencies: `npm install` in frontend folder
- [ ] T185 [P] Set NEXT_PUBLIC_API_URL to backend URL (.env.local)
- [ ] T186 [P] Test locally: `npm run dev` (visit http://localhost:3000)
- [ ] T187 [P] Run end-to-end flow: signup → create task → view → update → delete
- [ ] T188 Run TypeScript compiler: `tsc --noEmit` (expect 0 errors)
- [ ] T189 Run ESLint: `npx eslint .` (expect 0 errors)
- [ ] T190 Run test suite: `npm test` (expect ≥90% coverage)
- [ ] T191 [P] Fix any TypeScript errors, ESLint warnings, or test failures
- [ ] T192 [P] Build frontend: `npm run build` (expect no errors)
- [ ] T193 [P] Connect GitHub repo to Vercel (Settings → Deployments)
- [ ] T194 [P] Configure environment variables in Vercel: NEXT_PUBLIC_API_URL
- [ ] T195 [P] Deploy frontend to Vercel: `vercel --prod`
- [ ] T196 Test Vercel deployment: make API calls from deployed frontend to backend

### Integration Tests

- [ ] T197 [P] Create `backend/tests/test_integration.py` with complete signup → create task → list flow
- [ ] T198 [P] Add test_e2e_user_isolation (User A creates task, User B cannot access it)
- [ ] T199 [P] Add test_e2e_complete_task_workflow (create → update → complete → delete)
- [ ] T200 [US2] Create `frontend/tests/integration.test.tsx` with end-to-end component tests
- [ ] T201 Test with real backend (not mocked): sign up, create task, verify in list, delete
- [ ] T202 [P] Test CORS: requests from frontend domain to backend succeed
- [ ] T203 [P] Test missing authentication: requests without JWT token return 401
- [ ] T204 [P] Test user isolation: token from User A doesn't grant access to User B's tasks
- [ ] T205 [P] Test token expiry: requests with expired token return 401

---

## Phase 7: Polish & Testing (25 tasks)

### Goal
Improve code quality, add missing tests, and ensure production readiness.

### Tasks

- [ ] T206 Audit test coverage: run pytest with --cov (backend ≥95%)
- [ ] T207 Audit test coverage: run jest with --coverage (frontend ≥90%)
- [ ] T208 Add tests for error edge cases (malformed JSON, missing fields, large payloads)
- [ ] T209 [P] Add performance tests: verify API response time <200ms p95
- [ ] T210 Add docstrings to all backend functions/classes
- [ ] T211 Add JSDoc comments to all frontend components/utilities
- [ ] T212 Update `backend/CLAUDE.md` with examples and troubleshooting
- [ ] T213 Update `frontend/CLAUDE.md` with examples and troubleshooting
- [ ] T214 Update root `CLAUDE.md` with Phase 2 deployment instructions
- [ ] T215 Update `README.md` with Phase 2 features, architecture diagram, setup guide
- [ ] T216 [P] Verify no secrets in code (check for hardcoded tokens, passwords)
- [ ] T217 [P] Test input validation: SQL injection, XSS, command injection attempts
- [ ] T218 [P] Verify password hashing (bcrypt with proper salt rounds)
- [ ] T219 [P] Test HTTPS enforcement on Vercel
- [ ] T220 Test secure cookie settings (httpOnly, Secure, SameSite)
- [ ] T221 [P] Optimize frontend bundle size (target <200KB gzipped)
- [ ] T222 [P] Test Lighthouse score on Vercel deployment (target >90)
- [ ] T223 [P] Verify loading states show during API calls
- [ ] T224 [P] Verify error messages are user-friendly and actionable
- [ ] T225 [P] Test responsive design on mobile, tablet, desktop
- [ ] T226 Verify all specifications in `/specs/` are updated with implementation notes
- [ ] T227 Create summary document: what was implemented, what remains for Phase 3+
- [ ] T228 Test complete Phase 2 workflow one final time (signup → full CRUD → delete account flow)
- [ ] T229 [P] Commit all changes to `phase-2` branch with clear commit messages
- [ ] T230 Create GitHub PR from `phase-2` to `main` (ready for review)

---

## Task Summary

| Phase | Task Range | Count | Status |
|-------|-----------|-------|--------|
| **Phase 1: Setup** | T001-T015 | 15 | Ready |
| **Phase 2: Foundational** | T016-T034 | 19 | Ready |
| **Phase 3: Auth (US1)** | T035-T079 | 45 | Ready |
| **Phase 4: CRUD (US2)** | T080-T144 | 65 | Ready |
| **Phase 5: Filtering (US3)** | T145-T167 | 23 | Ready |
| **Phase 6: Integration** | T168-T205 | 38 | Ready |
| **Phase 7: Polish** | T206-T230 | 25 | Ready |
| **TOTAL** | T001-T230 | **230 tasks** | Ready for `/sp.implement` |

---

## Execution Strategy

### Recommended Parallelization
- **Backend Routes** (T035-T091): Can run in parallel on different route files
- **Frontend Pages** (T058-T120): Can run in parallel on different page/component files
- **Tests** (T048-T167): Can run in parallel on different test files
- **Code Quality** (T176-T205): Can run in parallel on different machines

### MVP Scope
For fastest Phase 2 delivery:
1. Phase 1: Setup (T001-T015)
2. Phase 2: Foundational (T016-T034)
3. Phase 3: Auth (T035-T079)
4. Phase 4: CRUD (T080-T144) - focus on core routes
5. Phase 6: Integration (T168-T205)

**MVP Total**: ~190 tasks (skip Phase 5 filtering, Phase 7 polish initially)

---

## Success Metrics

**Phase 2 Complete When**:
- ✅ All 230 tasks marked complete (or MVP 190 tasks for faster delivery)
- ✅ All tests passing (100%)
- ✅ Code coverage ≥95% (backend), ≥90% (frontend)
- ✅ No type errors or linting errors
- ✅ Frontend deployed to Vercel
- ✅ Backend running and accessible
- ✅ Full signup → CRUD → delete workflow verified
- ✅ User isolation tested and working
- ✅ Verified against Hackathon II Phase 2 requirements

---

**Generated**: 2025-12-07
**Ready for**: `/sp.implement` execution
**Next**: Execute tasks Phase 1 → Phase 2 → ... → Phase 7
