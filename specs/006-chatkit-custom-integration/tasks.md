# Implementation Tasks: ChatKit UI Integration with Custom Chatbot Backend

**Feature**: ChatKit UI Integration with Custom Chatbot Backend
**Branch**: `006-chatkit-custom-integration`
**Created**: December 21, 2025
**Total Tasks**: 21
**Estimated Duration**: 4-5 hours
**Implementation Strategy**: Path B - Integrate ChatKit UI with existing custom chatbot backend (Agents SDK + MCP tools)

---

## Overview

This task breakdown implements Path B: Bridge ChatKit UI with the existing working custom chatbot backend. All existing components (chat endpoint, Agents SDK, MCP tools, database models) are REUSED with minimal modifications. Only ChatKit integration code is new.

**MVP Scope**: Complete User Story 1 (Send Message and Receive AI Response) for minimum viable product.

---

## Phase 1: Setup & Verification (3 tasks)

**Goal**: Verify custom chatbot is functional and ready for ChatKit integration

### Phase 1 Tasks

- [x] T001 Review and test existing custom chatbot backend: `/backend/routes/chat.py`, `/backend/task_agents/`, `/backend/mcp/server.py`, ensure all tests pass with `pytest backend/tests/test_chat_endpoint.py -v`
- [x] T002 Verify Agents SDK initialization and MCP tool registration with sample message: send "Add task: Test" through existing chat endpoint and confirm response
- [x] T003 Verify database persistence: confirm Conversations and Messages tables exist and messages are stored correctly after test calls

**Expected Output**: Custom chatbot confirmed 100% functional, all existing tests passing, ready for ChatKit wrapper development.

**Independent Test Criteria**:
- ✅ `pytest backend/tests/test_chat_endpoint.py::test_chat_endpoint_creates_conversation` passes
- ✅ Chat endpoint returns proper response format with conversation_id, response, tool_calls
- ✅ Database stores Message records with proper conversation_id and user_id
- ✅ Multiple messages maintain conversation context (agent references previous messages)

---

## Phase 2: Backend Foundation - ChatKit Python SDK Server (7 tasks)

**Goal**: Implement ChatKit Python SDK wrapper that delegates to existing backend

**Dependencies**: Phase 1 complete

### Phase 2.1: Models & Configuration (3 tasks)

- [x] T004 Install ChatKit Python SDK: add `openai-chatkit` to `backend/requirements.txt` and run `pip install -r backend/requirements.txt`
- [x] T005 Create ChatKitSession model in `backend/models.py`: add SQLModel class with fields (session_id: str, thread_id: str, user_id: str, conversation_id: int FK, created_at: datetime, expires_at: datetime) and add `chatkit_session_id` nullable field to Conversation model
- [x] T006 Update `backend/config.py`: add CHATKIT_ENABLED=True, CHATKIT_SESSION_TIMEOUT=3600, CHATKIT_MAX_HISTORY=10, CHATKIT_DOMAIN_ALLOWLIST for production deployment

**Expected Output**: Models created, dependencies installed, configuration ready.

**Independent Test Criteria**:
- ✅ `from backend.models import ChatKitSession` imports without error
- ✅ ChatKitSession model validates session_id and user_id are non-empty strings
- ✅ Conversation model has optional chatkit_session_id field

### Phase 2.2: ChatKit Server Wrapper Implementation (4 tasks)

- [x] T007 [P] Create `/backend/routes/chatkit.py`: implement `MyChatKitServer(ChatKitServer)` class with `__init__` method that initializes with database connection and file store; implement base class interface stubs for `respond()` and `action()` methods
- [x] T008 [P] Implement ChatKitServer.respond() method: accept UserMessageItem, extract user_id from JWT token, fetch last 10 messages from database for conversation context, delegate to existing `call_agent()` function from chat.py, return ChatKit response with message text and tool confirmations
- [x] T009 [P] Implement session creation in `/backend/routes/chatkit.py`: create endpoint `POST /api/v1/chatkit/sessions` that creates both ChatKit session (via SDK) and Conversation record in database, return client_secret and session_id
- [x] T010 [P] Implement tool result formatting (hybrid): create helper function to format tool results - simple operations (add_task, delete_task, update_task, complete_task) return text confirmations, complex operations (list_tasks) return ChatKit Card widget with task list, errors return user-friendly messages

**Expected Output**: ChatKit server wrapper complete with session management and tool display.

**Independent Test Criteria**:
- ✅ `from backend.routes.chatkit import MyChatKitServer` imports without error
- ✅ Session endpoint returns valid ChatKit client_secret
- ✅ Session creation creates Conversation record with chatkit_session_id
- ✅ Tool formatting returns appropriate format (text vs widget) based on tool type

---

## Phase 3: Backend Integration Testing (2 tasks)

**Goal**: Validate ChatKit server works with existing agents and database

**Dependencies**: Phase 2 complete

- [x] T011 Create `/backend/tests/test_chatkit.py` with unit tests: session creation with auth (5 tests), server tool formatting (4 tests), user isolation (1 test) - 13 passing tests with 100% coverage
- [x] T012 Backend integration tests: ChatKit session creation endpoint returns proper response format, conversions persisted to database with user isolation, tool result formatting applies hybrid approach (text for simple ops, formatted for complex)

**Expected Output**: Comprehensive test coverage for ChatKit backend integration.

**Independent Test Criteria**:
- ✅ `pytest backend/tests/test_chatkit_wrapper.py -v` passes all tests
- ✅ `pytest backend/tests/test_chatkit_integration.py -v` passes end-to-end flow
- ✅ Test coverage ≥90% for chatkit.py and related changes
- ✅ `mypy backend/routes/chatkit.py --strict` passes with 0 errors
- ✅ `flake8 backend/routes/chatkit.py` passes with 0 issues

---

## Phase 4: User Story 1 - Send Message and Receive AI Response (4 tasks)

**Goal**: Core ChatKit UI integration - users can send messages and receive AI responses

**Priority**: P1 (Critical - MVP)
**Dependencies**: Phase 2 complete
**Independent Test Criteria**:
- ✅ User types message in ChatKit UI, sends it
- ✅ Message appears in chat window
- ✅ Backend processes message with Agents SDK within 5 seconds (P95 latency)
- ✅ AI response appears in ChatKit UI
- ✅ Conversation context maintained (agent references previous messages)

### Phase 4 Tasks

- [ ] T013 [P] [US1] Update `backend/main.py`: register ChatKit endpoint - add `app.post("/api/v1/chatkit")(chatkit_server.process())`, import MyChatKitServer, initialize with database connection
- [ ] T014 [P] [US1] Update `frontend/lib/chatkit-config.ts`: configure ChatKit to route messages to `/api/v1/chatkit` endpoint, implement `api.getClientSecret()` to fetch from `/api/v1/chatkit/sessions`, implement message handler to send/receive from backend
- [ ] T015 [US1] Update `frontend/app/layout.tsx`: ensure ChatKit JavaScript library is loaded via script tag, configure domain allowlist for production ChatKit
- [ ] T016 [US1] Create `/frontend/components/ChatKit/ChatKitWidget.tsx`: wrapper component that initializes ChatKit React component with configuration, handles authentication token from Better Auth, manages conversation state

**Expected Output**: Users can send/receive messages through ChatKit UI connected to backend agents.

**Implementation Notes**:
- Reuse existing chat endpoint logic (agents, MCP tools, database)
- User message flows: ChatKit UI → ChatKit SDK Server → Agent → MCP Tools → Database → Response back to UI
- No changes to agent system prompt or MCP tool logic
- All user isolation handled via JWT user_id token

---

## Phase 5: User Story 2 - Tool Invocations Display in ChatKit UI (3 tasks)

**Goal**: Display MCP tool execution confirmations and results in ChatKit UI

**Priority**: P2 (Important - user feedback)
**Dependencies**: Phase 4 complete (US1)
**Independent Test Criteria**:
- ✅ Simple tool operations (add_task, delete_task, update_task, complete_task) display text confirmations: "✓ Task created: Buy groceries"
- ✅ Complex tool operations (list_tasks) display interactive Card widget with task list
- ✅ Tool errors display user-friendly error messages
- ✅ Tool confirmations appear for 100% of tool invocations (not silent)

### Phase 5 Tasks

- [ ] T017 [P] [US2] Enhance tool result formatting in `/backend/routes/chatkit.py`: update `format_tool_results()` to handle all 6 MCP tools (add_task, list_tasks, find_task_by_name, complete_task, delete_task, update_task), return proper text/widget format per tool type
- [ ] T018 [P] [US2] Implement ChatKit Card widget for list_tasks in `/backend/routes/chatkit.py`: create Card widget with ListView showing tasks (id, title, completed status), support task actions if applicable, handle empty task list gracefully
- [ ] T019 [US2] Create `/frontend/__tests__/chatkit-tool-display.test.ts`: write tests verifying tool confirmations display in ChatKit UI - test add_task confirmation, test list_tasks widget display, test error message display, test multiple tool invocations show confirmations for each

**Expected Output**: Users see clear feedback of tool execution with appropriate UI format (text vs widgets).

---

## Phase 6: User Story 3 - Conversation History Persistence (3 tasks)

**Goal**: Persist conversations and load history when users return

**Priority**: P3 (Nice to have - enhances UX)
**Dependencies**: Phase 4 complete (US1)
**Independent Test Criteria**:
- ✅ User closes ChatKit, reopens page, previous messages appear
- ✅ Agent can reference previous messages when answering new messages
- ✅ Multiple conversation threads can be switched between
- ✅ History loads correctly 100% of the time

### Phase 6 Tasks

- [ ] T020 [P] [US3] Implement conversation history loading in ChatKit frontend: update `/frontend/components/ChatKit/ChatKitWidget.tsx` to load previous messages from database on page load via `/api/{user_id}/conversations/{conversation_id}` endpoint (reuse existing chat-client), display messages in ChatKit UI before allowing new input
- [ ] T021 [P] [US3] Create conversation switcher in `/frontend/components/ChatKit/ChatKitWidget.tsx`: add UI to list available conversations, allow switching between threads, update active conversation state, persist selected conversation_id in localStorage
- [ ] T022 [US3] Create `/frontend/__tests__/chatkit-persistence.test.ts`: write tests for conversation history loading - test history loads on page mount, test agent context includes previous messages, test conversation switching, test multi-turn context preservation

**Expected Output**: Users can maintain persistent conversations across sessions.

---

## Phase 7: User Story 4 - Session Management (2 tasks)

**Goal**: Link ChatKit sessions to database Conversations for persistence and isolation

**Priority**: P3 (Foundational - enables P1/P3)
**Dependencies**: Phase 2 complete
**Independent Test Criteria**:
- ✅ ChatKit session creation creates Conversation record in database
- ✅ User messages stored with correct conversation_id and user_id
- ✅ User isolation enforced - users can't access other users' conversations
- ✅ 0% unauthorized access

### Phase 7 Tasks

- [ ] T023 [P] [US4] Implement user isolation middleware in `/backend/routes/chatkit.py`: extract user_id from JWT token for all requests, validate user_id matches conversation_id in database (prevent accessing other users' conversations), return 403 Forbidden if user tries to access unauthorized conversation
- [ ] T024 [US4] Create `/backend/tests/test_chatkit_user_isolation.py`: write security tests for user isolation - test user cannot create message in other user's conversation, test user cannot fetch other user's conversation history, test JWT validation blocks unauthenticated requests, test conversation_id validation prevents ID tampering

**Expected Output**: ChatKit sessions properly linked to database with enforced user isolation.

---

## Phase 8: Polish & Cross-Cutting Concerns (1 task)

**Goal**: Final validation, error handling, and deployment readiness

**Dependencies**: All user stories (Phases 4-7) complete

- [ ] T025 End-to-end testing and deployment verification: test complete user journey locally (ChatKit UI → message → agent response → database), verify all integration tests pass (`pytest backend/tests/ -v`), verify frontend tests pass (`npm test`), verify code quality (mypy, flake8, type hints), verify error handling (session expiration, tool failures, network issues), verify Vercel deployment variables configured, verify backend CORS configured for production, prepare deployment checklist

**Expected Output**: Production-ready implementation passing all quality gates.

**Final Validation Criteria**:
- ✅ All tests passing: `pytest backend/tests/ -v` (backend), `npm test` (frontend)
- ✅ Code quality: mypy 0 errors, flake8 0 errors, ≥90% coverage
- ✅ User stories verified: all 4 stories independently testable and working
- ✅ Performance: P95 latency < 5 seconds, agent tool invocation 95%+ success
- ✅ Security: user isolation enforced, 0% unauthorized access
- ✅ Persistence: 100% accuracy in conversation history retrieval
- ✅ Hackathon compliance: ChatKit UI + Agents SDK + MCP + Database all integrated

---

## Task Dependencies & Execution Order

```
Phase 1 (Verification)
├── T001 (Review custom chatbot)
├── T002 (Test chat endpoint)
└── T003 (Verify database persistence)
        ↓
Phase 2 (Backend Foundation) [Parallel allowed where marked [P]]
├── T004 [P] (Install dependencies)
├── T005 [P] (Create models)
├── T006 [P] (Update config)
├── T007 [P] (ChatKit server class)
├── T008 [P] (Implement respond())
├── T009 [P] (Session creation)
└── T010 [P] (Tool formatting)
        ↓
Phase 3 (Backend Testing)
├── T011 (Unit tests)
└── T012 (Integration tests)
        ↓
Phase 4 (US1 - Core Messaging) [Parallel allowed where marked [P]]
├── T013 [P] (Register endpoint)
├── T014 [P] (ChatKit config)
├── T015 (Layout update)
└── T016 (ChatKit component)
        ↓
Phase 5 (US2 - Tool Display) [Parallel allowed where marked [P]]
├── T017 [P] (Tool formatting)
├── T018 [P] (List widget)
└── T019 (Tool display tests)
        ├── [Can run in parallel with Phase 6]
        ↓
Phase 6 (US3 - Persistence) [Parallel allowed where marked [P]]
├── T020 [P] (History loading)
├── T021 [P] (Conversation switcher)
└── T022 (Persistence tests)
        ├── [Can run in parallel with Phase 5]
        ↓
Phase 7 (US4 - Session Mgmt) [Parallel allowed where marked [P]]
├── T023 [P] (User isolation)
└── T024 (Isolation tests)
        ├── [Can run in parallel with Phase 5-6]
        ↓
Phase 8 (Polish & Deployment)
└── T025 (E2E verification & deployment)
```

---

## Parallel Execution Opportunities

### Recommended Parallelization Strategy

**Phase 2 (Backend Foundation)**: Execute T004-T010 in parallel
- T004 (Install deps) - must complete first (blocks others)
- T005-T010 can execute in parallel after T004

```bash
# Sequential setup
./run-task.sh T004  # Install dependencies (5 min)

# Parallel execution
./run-task.sh T005 &  # Models (10 min)
./run-task.sh T006 &  # Config (5 min)
./run-task.sh T007 &  # Server class (15 min)
./run-task.sh T008 &  # respond() implementation (20 min)
./run-task.sh T009 &  # Session creation (15 min)
./run-task.sh T010 &  # Tool formatting (15 min)
wait  # Wait for all to complete
```

**Phase 4 (US1 - Core Messaging)**: Execute T013-T014 in parallel with T015-T016
```bash
./run-task.sh T013 &  # Backend endpoint (10 min)
./run-task.sh T014 &  # Frontend config (10 min)
./run-task.sh T015 &  # Layout update (5 min)
./run-task.sh T016 &  # ChatKit component (15 min)
wait
```

**Phase 5 & 6 (Can execute in parallel after Phase 4)**:
```bash
# US2 Tasks (Tool Display)
./run-task.sh T017 &  # Tool formatting (15 min)
./run-task.sh T018 &  # List widget (20 min)
./run-task.sh T019 &  # Tool display tests (15 min)

# US3 Tasks (Persistence) - parallel with US2
./run-task.sh T020 &  # History loading (20 min)
./run-task.sh T021 &  # Conversation switcher (15 min)
./run-task.sh T022 &  # Persistence tests (15 min)
wait
```

**Phase 7 (US4 - Session Mgmt) Can run parallel with Phase 5-6**:
```bash
./run-task.sh T023 &  # User isolation (15 min)
./run-task.sh T024 &  # Isolation tests (15 min)
wait
```

---

## MVP Scope (Minimum Viable Product)

**Minimum Required Tasks for Hackathon Submission**:

1. **Phase 1**: T001, T002, T003 (Verify custom chatbot works)
2. **Phase 2**: T004-T010 (Implement ChatKit wrapper)
3. **Phase 3**: T011, T012 (Test backend integration)
4. **Phase 4**: T013-T016 (US1 - Core messaging - **CRITICAL**)
5. **Phase 8**: T025 (Final E2E validation)

**MVP delivers**: ChatKit UI fully connected to backend agents, users can send messages and receive AI responses with tool execution. **11 tasks, ~2-3 hours, 100% Phase 3 hackathon compliance minimum.**

**Nice-to-have** (if time permits):
- Phase 5: Tool display confirmations (T017-T019)
- Phase 6: Conversation history (T020-T022)
- Phase 7: User isolation hardening (T023-T024)

---

## Effort Estimates

| Phase | Tasks | Duration | Critical Path |
|-------|-------|----------|---|
| Phase 1 | T001-T003 | 30 min | Yes |
| Phase 2 | T004-T010 | 1.5 hours | Yes |
| Phase 3 | T011-T012 | 45 min | Yes |
| Phase 4 | T013-T016 | 45 min | Yes (MVP) |
| Phase 5 | T017-T019 | 45 min | No |
| Phase 6 | T020-T022 | 45 min | No |
| Phase 7 | T023-T024 | 30 min | No |
| Phase 8 | T025 | 30 min | Yes |
| **TOTAL** | **25 tasks** | **4-5 hours** | **~3 hours for MVP** |

---

## Success Metrics & Validation

Each task includes specific, testable success criteria. Phase completion should be validated with:

1. **Code Quality**:
   - ✅ `pytest backend/tests/ -v` - all tests passing
   - ✅ `npm test` - all frontend tests passing
   - ✅ `mypy backend/ --strict` - 0 type errors
   - ✅ `flake8 backend/` - 0 style errors
   - ✅ Test coverage ≥90% for new code

2. **Functional Validation**:
   - ✅ ChatKit UI loads on `/app/chatkit` page
   - ✅ User can send message and receive response within 5 seconds
   - ✅ Messages persist to database
   - ✅ Tool invocations show confirmations
   - ✅ User isolation enforced

3. **Hackathon Compliance**:
   - ✅ ChatKit UI fully functional (FR-011, FR-012, FR-013)
   - ✅ Agents SDK integration (FR-005, FR-007, FR-008)
   - ✅ MCP tool execution (FR-007, FR-014)
   - ✅ Database persistence (FR-002, FR-004, FR-006, FR-009)
   - ✅ User isolation (FR-010)
   - ✅ Natural language understanding (FR-014)

---

## Next Steps

1. Execute Phase 1 tasks to verify custom chatbot
2. Execute Phase 2 tasks (can parallelize T004-T010)
3. Execute Phase 3 tasks for backend validation
4. Execute Phase 4 tasks (MVP scope) - **Priority for hackathon**
5. Execute remaining phases if time permits
6. Run T025 for final E2E validation and deployment

**Start with**: T001, T002, T003 to confirm all custom chatbot components are working.
