# Phase 3 Implementation Tasks: AI-Powered Todo Chatbot

**Feature**: AI-Powered Todo Chatbot with ChatKit, Agents SDK, and MCP
**Branch**: `phase-3`
**Created**: 2025-12-15
**Status**: Ready for Implementation
**Total Tasks**: 67 tasks across 10 phases
**Deadline**: December 21, 2025

---

## Executive Summary

This document contains 67 actionable implementation tasks for Phase 3, organized by implementation phase and user story. Tasks are sequenced to enable independent testing and parallel execution where possible.

### Key Metrics

| Metric | Value |
|--------|-------|
| Total Tasks | 67 |
| Setup Phase Tasks | 8 |
| Foundational Phase Tasks | 12 |
| User Story 1 (P1) | 14 tasks |
| User Story 2 (P1) | 12 tasks |
| User Story 3 (P1) | 11 tasks |
| User Story 4 (P2) | 8 tasks |
| User Story 5 (P2) | 7 tasks |
| Quality & Deployment | 15 tasks |

### MVP Scope (Recommended)

**Minimum Viable Product**: User Stories 1-3 (all P1 stories)
- Create task via natural language
- View tasks via natural language
- Mark task complete via chat
- Basic multi-turn conversation
- Basic error handling

**Estimated MVP Time**: 5-6 days
**Full Implementation Time**: 8-12 days

### Parallel Execution Opportunities

1. **Backend & Frontend Setup** (T001-T008): Fully parallelizable
2. **Database & Infrastructure** (T009-T020): Fully parallelizable after database setup
3. **MCP Tools** (T026, T047, T061, T068, T076): Can be developed in parallel
4. **Frontend Components** (T034, T050, T088): Can be developed in parallel
5. **User Story Tests**: Each story's tests are independent

---

## Phase 1: Setup & Infrastructure

**Duration**: 1 day | **Critical Path**: YES

### Goal
Set up project structure, initialize backend and frontend applications, configure environment variables.

### Independent Test Criteria
- FastAPI server starts on port 8000 without errors
- Next.js server starts on port 3000 without errors
- Database connection credentials work
- Both servers accessible via localhost

### Tasks

- [ ] T001 Create backend directory structure per plan: `mkdir -p backend/{alembic,mcp/tools,agents,routes,middleware,tests}`
- [ ] T002 Create frontend directory structure per plan: `mkdir -p frontend/{app/chatbot,components/Chat,lib,hooks,types,tests}`
- [ ] T003 [P] Create backend `pyproject.toml` with dependencies (fastapi, uvicorn, sqlmodel, openai, modelcontextprotocol) in `backend/pyproject.toml`
- [ ] T004 [P] Create frontend `package.json` with dependencies (next, react, typescript, @openai/chatkit-react, tailwind) in `frontend/package.json`
- [ ] T005 [P] Create backend `.env.example` with DATABASE_URL, OPENAI_API_KEY, JWT_SECRET in `backend/.env.example`
- [ ] T006 [P] Create frontend `.env.example` with NEXT_PUBLIC_API_URL in `frontend/.env.example`
- [ ] T007 Create backend `main.py` FastAPI entry point with app() factory and CORS in `backend/main.py`
- [ ] T008 Create frontend `app/layout.tsx` root layout with auth provider in `frontend/app/layout.tsx`

---

## Phase 2: Foundational Infrastructure

**Duration**: 1-2 days | **Critical Path**: YES | **Blocks**: All user stories

### Goal
Establish database schema, authentication, MCP server, Agents SDK, and chat endpoint foundation.

### Independent Test Criteria
- All database tables created (conversations, messages, tasks, users)
- JWT middleware validates tokens correctly
- MCP server initializes without errors
- Agents SDK creates agent instance successfully
- Chat endpoint responds to POST requests
- All SQLModel models can be imported

### Tasks

- [ ] T009 Set up Neon PostgreSQL database and save connection string
- [ ] T010 [P] Initialize Alembic migrations: `alembic init backend/alembic` in `backend/alembic/`
- [ ] T011 [P] Create Conversation model in `backend/models.py`: id, user_id, title, created_at, updated_at, archived
- [ ] T012 [P] Create Message model in `backend/models.py`: id, conversation_id, user_id, role, content, tool_calls, created_at
- [ ] T013 [P] Create User model in `backend/models.py`: id, email, name (reference from Phase 2)
- [ ] T014 [P] Extend Task model in `backend/models.py`: ensure id, user_id, title, description, completed, created_at, updated_at
- [ ] T015 [P] Create database migration with indexes: conversation(user_id), message(conversation_id, created_at), task(user_id, completed)
- [ ] T016 Create database connection module in `backend/db.py` with SessionLocal and engine setup
- [ ] T017 Apply migrations: `cd backend && alembic upgrade head`
- [ ] T018 Create JWT authentication middleware in `backend/middleware.py` to extract user_id from token
- [ ] T019 [P] Create MCP server initialization in `backend/mcp/server.py` with Official SDK
- [ ] T020 [P] Create Agents SDK setup in `backend/agents/task_agent.py` with agent instance (no tools yet)

---

## Phase 3: User Story 1 - Create Task via Natural Language (P1)

**Duration**: 2 days | **Critical Path**: YES | **Depends On**: Phase 2 | **Enables**: Phase 4, 5

### User Story Goal
Users can create new tasks by typing natural language messages like "add a task to buy groceries" and receive confirmation.

### Acceptance Scenarios
1. User types "add a task to buy groceries" → chatbot creates task → responds "I've added 'Buy groceries' to your task list"
2. User types "create a reminder: call mom tonight" → chatbot creates task with title "Call mom" and description "tonight"
3. User types ambiguous "add stuff" → chatbot asks for clarification "What would you like to add?"
4. User types task title >200 chars → chatbot truncates → responds "Task title limited to 200 characters"

### Independent Test Criteria (US1)
- POST /api/{user_id}/chat accepts message, creates conversation
- add_task MCP tool validates inputs (title 1-200 chars, description max 1000)
- Task persists to database with auto-assigned ID
- Chatbot responds with confirmation containing task title
- Tool result included in response JSON

### Test Tasks

- [ ] T021 [US1] Write test: add_task with valid title in `backend/tests/test_mcp_tools.py`
- [ ] T022 [US1] Write test: add_task with title and description in `backend/tests/test_mcp_tools.py`
- [ ] T023 [US1] Write test: add_task title validation (length, empty) in `backend/tests/test_mcp_tools.py`
- [ ] T024 [US1] Write test: conversation creation and persistence in `backend/tests/test_chat_endpoint.py`
- [ ] T025 [US1] Write test: chat endpoint returns tool_calls array in `backend/tests/test_chat_endpoint.py`

### Implementation Tasks

- [ ] T026 [US1] Implement add_task MCP tool in `backend/mcp/tools/add_task.py` with validation, DB insert, return task_id
- [ ] T027 [US1] Register add_task with MCP server in `backend/mcp/server.py`
- [ ] T028 [US1] Create chat endpoint POST /api/{user_id}/chat in `backend/routes/chat.py`
- [ ] T029 [US1] Implement conversation creation logic in `backend/routes/chat.py`
- [ ] T030 [US1] Implement user message persistence in `backend/routes/chat.py`
- [ ] T031 [US1] Integrate Agents SDK with add_task tool in `backend/agents/task_agent.py`
- [ ] T032 [US1] Implement agent invocation in chat endpoint in `backend/routes/chat.py`
- [ ] T033 [US1] Implement assistant message storage with tool_calls in `backend/routes/chat.py`
- [ ] T034 [US1] Create ChatWindow component wrapping ChatKit in `frontend/components/Chat/ChatWindow.tsx`
- [ ] T035 [US1] Create chatbot page at `/chatbot` in `frontend/app/chatbot/page.tsx`
- [ ] T036 [US1] Create chat API client in `frontend/lib/chat-client.ts` with POST request
- [ ] T037 [US1] Create useChat hook for state management in `frontend/hooks/useChat.ts`
- [ ] T038 [US1] Integrate ChatWindow into chatbot page in `frontend/app/chatbot/page.tsx`
- [ ] T039 [US1] Run acceptance test 1: user types "add task to buy groceries" → verify creation
- [ ] T040 [US1] Run acceptance test 2: user types with description → verify both fields stored

---

## Phase 4: User Story 2 - View Tasks via Conversational Query (P1)

**Duration**: 1 day | **Depends On**: Phase 2 | **Parallel**: Phase 5 (US3)

### User Story Goal
Users can ask natural language questions like "show me my pending tasks" and receive a formatted list.

### Acceptance Scenarios
1. User has 5 tasks (3 pending, 2 completed) → asks "show me pending tasks" → chatbot displays 3 pending tasks
2. User asks "what do I need to do?" → chatbot shows all pending tasks
3. User asks "list all my tasks" → chatbot shows both pending and completed
4. User has no tasks → asks to see tasks → chatbot responds "You have no tasks yet. Would you like to create one?"

### Independent Test Criteria (US2)
- list_tasks MCP tool accepts user_id and status filter (all/pending/completed)
- Tool returns correct array of tasks matching filter
- Empty result returns empty array (not error)
- Tool respects user isolation (returns only user's tasks)

### Test Tasks

- [ ] T041 [P] [US2] Write test: list_tasks with "pending" status in `backend/tests/test_mcp_tools.py`
- [ ] T042 [P] [US2] Write test: list_tasks with "completed" status in `backend/tests/test_mcp_tools.py`
- [ ] T043 [P] [US2] Write test: list_tasks empty result in `backend/tests/test_mcp_tools.py`
- [ ] T044 [P] [US2] Write test: user isolation in list_tasks in `backend/tests/test_user_isolation.py`
- [ ] T045 [P] [US2] Write test: list_tasks returns correct field format in `backend/tests/test_mcp_tools.py`

### Implementation Tasks

- [ ] T046 [US2] Implement list_tasks MCP tool in `backend/mcp/tools/list_tasks.py` with status filter, user isolation
- [ ] T047 [US2] Register list_tasks with MCP server in `backend/mcp/server.py`
- [ ] T048 [US2] Integrate list_tasks with Agents SDK in `backend/agents/task_agent.py`
- [ ] T049 [US2] Create ToolVisualization component in `frontend/components/Chat/ToolVisualization.tsx`
- [ ] T050 [US2] Update ChatWindow to display tool visualizations in `frontend/components/Chat/ChatWindow.tsx`
- [ ] T051 [US2] Test acceptance 1: user has 5 tasks, asks "pending tasks" → verify 3 displayed
- [ ] T052 [US2] Test acceptance 4: user has no tasks, asks to see → verify helpful message
- [ ] T053 [US2] Verify user isolation: User A cannot see User B's tasks

---

## Phase 5: User Story 3 - Mark Task Complete via Chat (P1)

**Duration**: 1 day | **Depends On**: Phase 2 | **Parallel**: Phase 4 (US2)

### User Story Goal
Users can mark tasks as complete by saying "mark task 3 as done" and receive confirmation.

### Acceptance Scenarios
1. User has task "Buy groceries" → says "mark buy groceries as complete" → chatbot completes and confirms
2. User has 3 tasks → says "mark task 2 as done" → chatbot completes second task
3. Task is already complete → user says "mark it as done again" → chatbot suggests toggling to pending
4. User references non-existent task → chatbot responds "I can't find task 99" with task list

### Independent Test Criteria (US3)
- complete_task MCP tool accepts user_id, task_id
- Tool toggles completion (pending → completed, completed → pending)
- Tool updates updated_at timestamp
- Tool validates task exists and user owns task
- Tool respects user isolation

### Test Tasks

- [ ] T054 [US3] Write test: complete_task toggle pending→completed in `backend/tests/test_mcp_tools.py`
- [ ] T055 [US3] Write test: complete_task toggle completed→pending in `backend/tests/test_mcp_tools.py`
- [ ] T056 [US3] Write test: complete_task with non-existent task in `backend/tests/test_mcp_tools.py`
- [ ] T057 [US3] Write test: user isolation in complete_task in `backend/tests/test_user_isolation.py`
- [ ] T058 [US3] Write test: complete_task updates updated_at timestamp in `backend/tests/test_mcp_tools.py`

### Implementation Tasks

- [ ] T059 [US3] Implement complete_task MCP tool in `backend/mcp/tools/complete_task.py` with toggle logic, user isolation
- [ ] T060 [US3] Register complete_task with MCP server in `backend/mcp/server.py`
- [ ] T061 [US3] Integrate complete_task with Agents SDK in `backend/agents/task_agent.py`
- [ ] T062 [US3] Test acceptance 1: user says "mark buy groceries as complete" → verify completion
- [ ] T063 [US3] Test acceptance 2: user says "mark task 2 as done" → verify second task marked
- [ ] T064 [US3] Test acceptance 3: already complete task → verify toggle to pending suggestion
- [ ] T065 [US3] Verify user isolation: User A cannot complete User B's tasks
- [ ] T066 [US3] Test acceptance 4: reference non-existent task → verify helpful message
- [ ] T067 [US3] Verify task appears pending/complete in list_tasks after completion

---

## Phase 6: User Story 4 - Update Task Details (P2)

**Duration**: 1 day | **Depends On**: Phase 3 (US1 for testing)

### User Story Goal
Users can update task title and description by saying "change task 1 to 'Buy groceries and fruits'".

### Acceptance Scenarios
1. Task "Buy groceries" exists → user says "update task 1 title to 'Buy groceries and fruits'" → chatbot updates and confirms
2. Task has no description → user says "add description: organic items only" → chatbot adds description
3. User requests unsupported feature (due date) → chatbot responds "Due dates aren't supported. Would you like to update the description instead?"

### Independent Test Criteria (US4)
- update_task MCP tool accepts user_id, task_id, optional title/description
- Tool validates inputs (title 1-200 chars, description max 1000)
- created_at remains unchanged, updated_at refreshed
- Tool respects user isolation

### Test Tasks

- [ ] T068 [P] [US4] Write test: update_task title only in `backend/tests/test_mcp_tools.py`
- [ ] T069 [P] [US4] Write test: update_task description only in `backend/tests/test_mcp_tools.py`
- [ ] T070 [P] [US4] Write test: update_task both title and description in `backend/tests/test_mcp_tools.py`
- [ ] T071 [P] [US4] Write test: update_task timestamp preservation in `backend/tests/test_mcp_tools.py`
- [ ] T072 [P] [US4] Write test: user isolation in update_task in `backend/tests/test_user_isolation.py`

### Implementation Tasks

- [ ] T073 [US4] Implement update_task MCP tool in `backend/mcp/tools/update_task.py` with validation, timestamp handling
- [ ] T074 [US4] Register update_task with MCP server in `backend/mcp/server.py`
- [ ] T075 [US4] Integrate update_task with Agents SDK in `backend/agents/task_agent.py`
- [ ] T076 [US4] Test acceptance 1: user updates title → verify created_at unchanged
- [ ] T077 [US4] Test acceptance 2: user adds description → verify update successful

---

## Phase 7: User Story 5 - Delete Task Conversationally (P2)

**Duration**: 1 day | **Depends On**: Phase 3 (US1 for testing)

### User Story Goal
Users can delete tasks by saying "delete the groceries task" or "remove task 5".

### Acceptance Scenarios
1. User has "Buy groceries" task → says "delete the groceries task" → chatbot removes and confirms
2. User says "delete task 5" → chatbot removes task and asks "Are you sure?" before deletion
3. User references non-existent task → chatbot responds "Task not found"

### Independent Test Criteria (US5)
- delete_task MCP tool accepts user_id, task_id
- Tool removes task from database permanently
- Tool validates task exists and user owns task
- Tool respects user isolation

### Test Tasks

- [ ] T078 [P] [US5] Write test: delete_task success in `backend/tests/test_mcp_tools.py`
- [ ] T079 [P] [US5] Write test: delete_task non-existent task in `backend/tests/test_mcp_tools.py`
- [ ] T080 [P] [US5] Write test: user isolation in delete_task in `backend/tests/test_user_isolation.py`
- [ ] T081 [P] [US5] Write test: deleted task doesn't appear in list_tasks in `backend/tests/test_mcp_tools.py`

### Implementation Tasks

- [ ] T082 [US5] Implement delete_task MCP tool in `backend/mcp/tools/delete_task.py` with validation, user isolation
- [ ] T083 [US5] Register delete_task with MCP server in `backend/mcp/server.py`
- [ ] T084 [US5] Integrate delete_task with Agents SDK in `backend/agents/task_agent.py`
- [ ] T085 [US5] Test acceptance 1: user deletes "Buy groceries" task → verify removed
- [ ] T086 [US5] Test acceptance 3: reference non-existent task → verify error message
- [ ] T087 [US5] Verify deleted task doesn't appear in subsequent list queries
- [ ] T088 [US5] Verify user isolation: User A cannot delete User B's tasks

---

## Phase 8: Supporting Features & Cross-Cutting

**Duration**: 1-2 days | **Parallel**: Can run with US4/US5

### Goal
Implement conversation history, message summarization, error handling, multi-turn context, and streaming.

### Tasks

- [ ] T089 [P] Implement conversation history retrieval in chat endpoint in `backend/routes/chat.py`
- [ ] T090 [P] Implement multi-turn context (fetch previous messages) in `backend/agents/task_agent.py`
- [ ] T091 [P] Implement message summarization for 20+ messages in `backend/routes/chat.py`
- [ ] T092 [P] Implement error handling with auto-retry in MCP tools in `backend/mcp/tools/base.py`
- [ ] T093 [P] Implement graceful error responses in chat endpoint in `backend/routes/chat.py`
- [ ] T094 [P] Create MessageHistory component in `frontend/components/Chat/MessageHistory.tsx`
- [ ] T095 Create error boundary component in `frontend/components/ErrorBoundary.tsx`
- [ ] T096 Implement conversation persistence tests in `backend/tests/test_conversation_history.py`
- [ ] T097 Implement multi-tool chaining tests in `backend/tests/test_integration.py`
- [ ] T098 Test message summarization with 25+ message conversation

---

## Phase 9: Testing & Quality Assurance

**Duration**: 1.5-2 days | **Critical Path**: YES | **Blocks**: Deployment

### Goal
Verify all acceptance criteria, run quality checks, achieve coverage targets, fix issues.

### Tasks

- [ ] T099 Run backend unit tests: `pytest backend/tests/ -v --cov=src --cov-report=html` and verify ≥95% coverage
- [ ] T100 Run backend type checking: `mypy backend/src/` and fix all errors
- [ ] T101 Run backend linting: `flake8 backend/src/ backend/tests/` and fix issues
- [ ] T102 Run frontend component tests: `npm test` in frontend/ and verify ≥90% coverage
- [ ] T103 Run frontend type checking: `npx tsc --noEmit` and fix all errors
- [ ] T104 Run frontend linting: `npx eslint .` and fix issues
- [ ] T105 [P] Verify all 17 success criteria from spec in `specs/features/06-chatbot.md`
- [ ] T106 [P] Verify user isolation at 3 levels (database, MCP tools, frontend)
- [ ] T107 Performance test: verify response times < 3 seconds in `backend/tests/test_performance.py`
- [ ] T108 Load test: verify 10 concurrent conversations in `backend/tests/test_load.py`
- [ ] T109 End-to-end test: create → list → complete → delete full workflow
- [ ] T110 Error handling test: trigger all error scenarios and verify graceful responses

---

## Phase 10: Deployment & Documentation

**Duration**: 1 day

### Tasks

- [ ] T111 [P] Update backend README with setup instructions in `backend/README.md`
- [ ] T112 [P] Update frontend README with setup instructions in `frontend/README.md`
- [ ] T113 Create backend API documentation in `backend/docs/api.md`
- [ ] T114 Create frontend component documentation in `frontend/docs/components.md`
- [ ] T115 Deploy frontend to Vercel
- [ ] T116 Deploy backend to cloud server
- [ ] T117 Register domain in OpenAI ChatKit domain allowlist
- [ ] T118 Configure production environment variables
- [ ] T119 Run production smoke tests (full CRUD workflow)
- [ ] T120 Create monitoring and logging setup

---

## Dependencies & Execution Order

### Critical Path (Must Complete Sequentially)

1. **Phase 1**: T001-T008 (Setup) → **Blocking for all phases**
2. **Phase 2**: T009-T020 (Foundational) → **Blocking for all user stories**
3. **Phase 3**: T021-T040 (US1: Create) → **Foundation for testing**
4. **Phase 9**: T099-T110 (Testing/QA) → **Must pass before Phase 10**
5. **Phase 10**: T111-T120 (Deployment) → **Final phase**

### Parallel Execution (After Phase 2)

- **Group A**: Phase 3 (US1: Create) → T021-T040
- **Group B**: Phase 4 (US2: View) → T041-T053 (parallel with Group A)
- **Group C**: Phase 5 (US3: Complete) → T054-T067 (parallel with Groups A & B)

### Sequential After US3

- **Phase 6**: Phase 6 (US4: Update) → T068-T077
- **Phase 7**: Phase 7 (US5: Delete) → T078-T088
- **Phase 8**: Supporting Features → T089-T098 (parallel with Phase 6-7)

---

## Implementation Strategy

### Recommended Approach: MVP First

**Week 1 (MVP - Days 1-6)**:
1. Phase 1: Setup (1 day)
2. Phase 2: Infrastructure (1 day)
3. Phase 3: User Story 1 - Create (2 days)
4. Phase 4: User Story 2 - View (1 day) [PARALLEL with Phase 5]
5. Phase 5: User Story 3 - Complete (1 day)
6. MVP Testing & Bug Fixes (1 day)

**Week 2 (Full Implementation - Days 7-12)**:
7. Phase 6: User Story 4 - Update (1 day)
8. Phase 7: User Story 5 - Delete (1 day)
9. Phase 8: Supporting Features (1 day) [PARALLEL with Phase 6-7]
10. Phase 9: Full QA (1.5 days)
11. Phase 10: Deployment (1 day)

### Developer Recommendations

1. **Use TDD**: Write tests BEFORE implementation for each MCP tool
2. **Test User Isolation**: Verify at every step that user_id validation works
3. **Monitor Performance**: Log response times throughout development
4. **Commit Frequently**: One commit per task (or per user story)
5. **Parallel Development**: Assign different developers to different user stories after Phase 2

---

## Task Status Tracking

Use this checklist to track overall progress:

### Setup & Infrastructure (Phase 1-2)
- [ ] Phase 1 Setup (T001-T008) - 8 tasks
- [ ] Phase 2 Foundational (T009-T020) - 12 tasks

### User Stories (Phase 3-7)
- [ ] Phase 3 User Story 1 (T021-T040) - 20 tasks
- [ ] Phase 4 User Story 2 (T041-T053) - 13 tasks
- [ ] Phase 5 User Story 3 (T054-T067) - 14 tasks
- [ ] Phase 6 User Story 4 (T068-T077) - 10 tasks
- [ ] Phase 7 User Story 5 (T078-T088) - 11 tasks

### Supporting & Quality (Phase 8-10)
- [ ] Phase 8 Supporting Features (T089-T098) - 10 tasks
- [ ] Phase 9 Testing & QA (T099-T110) - 12 tasks
- [ ] Phase 10 Deployment (T111-T120) - 10 tasks

---

## Quick Reference: Task Lookup

### By File (Backend)

| File | Tasks |
|------|-------|
| `backend/models.py` | T011-T014 |
| `backend/db.py` | T016 |
| `backend/middleware.py` | T018 |
| `backend/mcp/server.py` | T019, T027, T047, T060, T074, T083 |
| `backend/mcp/tools/add_task.py` | T026 |
| `backend/mcp/tools/list_tasks.py` | T046 |
| `backend/mcp/tools/complete_task.py` | T059 |
| `backend/mcp/tools/update_task.py` | T073 |
| `backend/mcp/tools/delete_task.py` | T082 |
| `backend/agents/task_agent.py` | T020, T031, T048, T061, T075, T084 |
| `backend/routes/chat.py` | T028-T033, T089-T093 |

### By File (Frontend)

| File | Tasks |
|------|-------|
| `frontend/app/layout.tsx` | T008 |
| `frontend/app/chatbot/page.tsx` | T035, T038 |
| `frontend/components/Chat/ChatWindow.tsx` | T034, T050 |
| `frontend/components/Chat/ToolVisualization.tsx` | T049 |
| `frontend/components/Chat/MessageHistory.tsx` | T094 |
| `frontend/lib/chat-client.ts` | T036 |
| `frontend/hooks/useChat.ts` | T037 |

---

**Version**: 1.0
**Last Updated**: 2025-12-15
**Status**: Ready for Implementation
**Next Command**: `/sp.implement` to begin execution
