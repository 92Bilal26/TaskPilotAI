# Implementation Plan: TaskPilotAI Phase 3 - AI-Powered Chatbot

**Branch**: `phase-3` | **Date**: 2025-12-15 | **Spec**: `specs/features/06-chatbot.md` | **Deadline**: December 21, 2025

**Input**: Complete Phase 3 specifications from `specs/features/06-chatbot.md` with clarifications and quality validation

**Summary**: Build an AI-powered conversational interface for task management using OpenAI ChatKit (frontend), Agents SDK + MCP (backend), and Neon PostgreSQL. Users interact with a chatbot via natural language to create, view, update, delete, and complete tasks. System maintains conversation history, enforces user isolation at 3 levels, implements stateless server architecture, and provides real-time response streaming with tool visualization.

---

## Technical Context

**Frontend Stack**: Next.js 16+, TypeScript, @openai/chatkit-react, Tailwind CSS
**Backend Stack**: FastAPI, Python 3.13+, OpenAI Agents SDK, Official MCP SDK, SQLModel
**Database**: Neon PostgreSQL (extended from Phase 2)
**Authentication**: JWT tokens (from Phase 2 Better Auth)
**Performance Goals**:
- Task creation response < 5 seconds
- Chat responses < 3 seconds
- MCP tools < 500ms response
- Support 10 concurrent conversations
**Constraints**:
- Stateless server (zero in-memory state)
- Official SDKs only (ChatKit, MCP, Agents)
- User isolation required at 3 levels
- Message summarization at 20-message threshold

---

## Constitution Check

**GATE: Must pass before Phase 3 implementation. Re-check after all features complete.**

### Phase 3 Principles (8 core)
- ✅ Spec-Driven Development (maintained from Phase 1-2)
- ✅ Test-First Development (maintained from Phase 1-2)
- ✅ OpenAI ChatKit Integration (NEW)
- ✅ OpenAI Agents SDK Integration (NEW)
- ✅ Official MCP SDK (NEW)
- ✅ MCP-First Architecture (NEW)
- ✅ Stateless Chat Endpoint (NEW)
- ✅ Multi-User Architecture (maintained from Phase 2)

### Non-Negotiables
- ❌ Cannot build custom chat UI (must use ChatKit)
- ❌ Cannot implement custom tool framework (must use Official MCP SDK)
- ❌ Cannot use basic Completions API (must use Agents SDK)
- ❌ Cannot keep state in server memory (all state in database)
- ✅ Must enforce user isolation (3 levels: database, tools, frontend)
- ✅ Must persist all state to database
- ✅ Must follow spec-driven development
- ✅ Must write tests first (≥95% backend, ≥90% frontend)

### Quality Gates (14 total)

**Specification Gates** (6)
- ✅ Specification written with 7 user stories
- ✅ 16 functional requirements documented
- ✅ 17 success criteria defined
- ✅ 7 edge cases identified
- ✅ API contracts fully specified
- ✅ Architecture decisions documented

**Code Quality Gates** (5)
- Backend: ≥95% test coverage with pytest
- Backend: 0 type errors with mypy
- Frontend: ≥90% component test coverage
- All: PEP 8 / ESLint compliance
- All: No hardcoded secrets or API keys

**Functional Gates** (8)
- All MCP tools functional (add, list, complete, delete, update)
- Chat endpoint stateless and database-backed
- Conversation history persists and retrieves correctly
- User isolation enforced at all 3 levels
- Streaming responses work end-to-end
- Tool visualization appears in ChatKit
- Error handling with graceful degradation
- Multi-turn conversation context maintained

**GATE STATUS**: ✅ All 14 gates established; will verify post-implementation

---

## Clarifications Applied (Session 2025-12-15)

Based on user feedback during specification clarification phase:

1. **Q1: Context Window Limits for 100+ Message Conversations**
   - **Decision**: Auto-summarize messages older than 20 messages; replace with brief summary
   - **Rationale**: Prevents token overflow while maintaining coherent conversation context
   - **Implementation**: Triggered when message count > 20; older messages → summary record
   - **SC-015**: "Conversation history summarizes messages after 20-message threshold; context maintained without data loss"

2. **Q2: Concurrent Edit Conflict Resolution (Same User, Multiple Tabs)**
   - **Decision**: Last-write-wins with optimistic updates (silent overwrite)
   - **Rationale**: Simplest approach; acceptable for this use case
   - **Implementation**: No conflict detection; later edit silently overwrites earlier
   - **Frontend**: Shows optimistic update immediately without waiting for server
   - **SC-016**: "Concurrent edits from same user result in last-write-wins with no user notification (silent overwrite acceptable)"

3. **Q3: Agent Error Recovery for Failed MCP Tool Invocations**
   - **Decision**: Auto-retry failed tools once; inform user only if both attempts fail
   - **Rationale**: Handles transient failures gracefully; user sees failures only when persistent
   - **Implementation**: On tool failure → wait 500ms → retry once → if still fails, inform user
   - **SC-017**: "Tool failures trigger automatic retry; user informed only if retry also fails (max 1 retry)"

---

## Project Structure

### Full-Stack Architecture

```
TaskPilotAI/
├── specs/                                    # SPECIFICATIONS
│   ├── features/
│   │   └── 06-chatbot.md                    # Phase 3 chatbot spec (7 stories, 16 FR, 17 SC)
│   ├── checklists/
│   │   └── chatbot-requirements.md          # Quality validation (30/30 passing)
│   ├── phase-3-plan.md                      # This file (implementation plan)
│   ├── data-model.md                        # Entity definitions (NEW - to create)
│   ├── contracts/                           # API contracts (NEW - to create)
│   │   ├── chat-endpoint.openapi.yaml
│   │   ├── mcp-tools.openapi.yaml
│   │   └── conversation-model.json
│   └── quickstart.md                        # Development setup (NEW - to create)
│
├── backend/                                  # FASTAPI SERVER
│   ├── main.py                              # FastAPI entry point + app initialization
│   ├── models.py                            # SQLModel: User, Task, Conversation, Message
│   ├── db.py                                # Database connection (Neon PostgreSQL)
│   ├── middleware.py                        # JWT auth middleware, CORS, error handlers
│   ├── routes/
│   │   ├── auth.py                          # Auth endpoints (from Phase 2)
│   │   ├── tasks.py                         # Task CRUD endpoints (from Phase 2)
│   │   └── chat.py                          # NEW: Chat endpoint (POST /api/{user_id}/chat)
│   ├── mcp/                                 # MCP SERVER
│   │   ├── server.py                        # MCP server initialization & tool registration
│   │   └── tools/
│   │       ├── add_task.py                  # MCP tool: add_task
│   │       ├── list_tasks.py                # MCP tool: list_tasks
│   │       ├── complete_task.py             # MCP tool: complete_task
│   │       ├── delete_task.py               # MCP tool: delete_task
│   │       ├── update_task.py               # MCP tool: update_task
│   │       └── __init__.py                  # Tool registration
│   ├── agents/                              # AGENT LOGIC
│   │   └── task_agent.py                    # Agents SDK: task agent with tools
│   ├── tests/                               # BACKEND TESTS
│   │   ├── conftest.py                      # pytest fixtures
│   │   ├── test_mcp_tools.py                # Unit tests for 5 MCP tools (≥95% coverage)
│   │   ├── test_chat_endpoint.py            # Integration tests for chat endpoint
│   │   ├── test_user_isolation.py           # Tests for 3-level isolation enforcement
│   │   └── test_error_handling.py           # Error recovery and retry logic
│   ├── requirements.txt                     # Python dependencies
│   ├── .env.example                         # Environment variables template
│   ├── pyproject.toml                       # Project config (if using Poetry)
│   └── CLAUDE.md                            # Backend development guide
│
├── frontend/                                 # NEXT.JS APPLICATION
│   ├── app/
│   │   ├── layout.tsx                       # Root layout with auth check
│   │   ├── page.tsx                         # Home page (redirect to dashboard)
│   │   ├── dashboard/
│   │   │   └── page.tsx                     # Task dashboard (existing from Phase 2)
│   │   └── chatbot/
│   │       └── page.tsx                     # NEW: Chatbot page with ChatKit integration
│   ├── components/
│   │   ├── TaskForm.tsx                     # Task form (existing from Phase 2)
│   │   ├── TaskList.tsx                     # Task list display (existing from Phase 2)
│   │   └── Chat/
│   │       ├── ChatWindow.tsx               # NEW: ChatKit wrapper component
│   │       ├── ToolVisualization.tsx        # NEW: Display tool invocations and results
│   │       └── MessageHistory.tsx           # NEW: Conversation history display
│   ├── lib/
│   │   ├── api.ts                           # API client (existing from Phase 2)
│   │   └── chat-client.ts                   # NEW: Chat API client with streaming
│   ├── hooks/
│   │   └── useChat.ts                       # NEW: Chat state management hook
│   ├── types/
│   │   ├── task.ts                          # Task type definitions
│   │   └── chat.ts                          # NEW: Chat/conversation type definitions
│   ├── tests/                               # FRONTEND TESTS
│   │   ├── components/ChatWindow.test.tsx   # ChatKit component tests (≥90% coverage)
│   │   ├── hooks/useChat.test.ts            # Hook tests
│   │   ├── lib/chat-client.test.ts          # API client tests
│   │   └── integration/chatbot.integration.test.tsx
│   ├── package.json                         # Node dependencies
│   ├── tsconfig.json                        # TypeScript config
│   ├── tailwind.config.ts                   # Tailwind config
│   └── CLAUDE.md                            # Frontend development guide
│
├── docs/                                     # REFERENCE DOCUMENTATION (already created)
│   ├── REFERENCE-OPENAI-CHATKIT.md          # ChatKit setup and integration
│   ├── REFERENCE-OPENAI-AGENTS-SDK.md       # Agents SDK patterns
│   └── REFERENCE-MCP-PROTOCOL.md            # MCP specification and examples
│
├── .specify/memory/constitution.md          # Project governance (v3.0.0)
├── CLAUDE.md                                # Root development guide
├── README.md                                # Project overview
└── .env.example                             # Environment variables template
```

**Structure Decision**: Full-stack separation with frontend/ and backend/ directories. Backend implements stateless FastAPI chat endpoint with MCP server running in same process. Frontend uses ChatKit for UI, with direct chat API calls for communication. Database-backed conversation history enables stateless architecture.

---

## Implementation Phases

### Phase 0: Research & Specification ✅ COMPLETE
- ✅ Read hackathon requirements
- ✅ Read official ChatKit, Agents SDK, MCP documentation
- ✅ Create comprehensive specification (06-chatbot.md)
- ✅ Run specification clarification (3 questions answered)
- ✅ Validate specification (30/30 quality checks passing)
- ✅ Update constitution (v3.0.0)

### Phase 1: Design & API Contracts (NEXT)
**Duration**: 2-3 days

**Deliverables**:
1. **`specs/data-model.md`** - Entity definitions
   - Conversation entity: id, user_id, created_at, updated_at
   - Message entity: id, conversation_id, user_id, role (user/assistant), content, created_at
   - Task entity: (existing from Phase 2) extended with conversation references
   - Relationships and constraints

2. **`specs/contracts/`** - API contract files
   - `chat-endpoint.openapi.yaml` - OpenAPI spec for POST /api/{user_id}/chat
   - `mcp-tools.openapi.yaml` - MCP tool specifications
   - `conversation-model.json` - JSON schema for Conversation/Message

3. **`specs/quickstart.md`** - Local development guide
   - Database setup (Neon PostgreSQL)
   - Backend setup (FastAPI, MCP server, Agents SDK)
   - Frontend setup (Next.js, ChatKit)
   - Running locally and testing end-to-end
   - Example conversations and flows

**Acceptance Criteria**:
- All 3 files created with complete specifications
- No ambiguities in data models or API contracts
- Developers can set up and run locally following quickstart

### Phase 2: Implementation (MAIN)
**Duration**: 5-7 days

**Deliverables**:

**Backend (FastAPI + MCP + Agents)**:
1. Database migration: Add Conversation and Message tables
2. SQLModel models: Conversation, Message (extend existing User, Task)
3. MCP server initialization with Official SDK
4. Implement 5 MCP tools (add_task, list_tasks, complete_task, delete_task, update_task)
   - Input validation (user_id, parameters)
   - User isolation enforcement (verify task ownership)
   - Error handling with auto-retry
   - Response formatting
5. Agents SDK integration: Create task_agent with MCP tools
6. Chat endpoint: `POST /api/{user_id}/chat`
   - Fetch conversation history from database
   - Run agent with message + tools
   - Stream responses back to client
   - Persist user message and assistant response
   - Handle errors gracefully
7. Middleware: JWT auth, CORS (allow ChatKit domain), error handlers
8. Comprehensive tests:
   - Unit tests for each MCP tool (≥95% coverage)
   - Integration tests for chat endpoint
   - User isolation enforcement tests
   - Error recovery and retry logic tests
   - Concurrency and stream handling tests

**Frontend (Next.js + ChatKit)**:
1. Install and configure @openai/chatkit-react
2. Create ChatWindow component wrapping ChatKit
3. Create Chatbot page: `app/chatbot/page.tsx`
4. Chat API client: `lib/chat-client.ts` with streaming support
5. useChat hook: State management for conversation
6. Tool visualization: Display MCP tool calls and results
7. Message history: Persist and display conversation
8. Error handling: Display errors to user, retry UI
9. Comprehensive tests:
   - Component tests for ChatWindow (≥90% coverage)
   - Hook tests for useChat
   - API client tests with mocking
   - Integration tests: full chatbot workflow

**Acceptance Criteria**:
- All 5 MCP tools working and tested
- Chat endpoint stateless and database-backed
- Conversation history persists and retrieves
- User isolation enforced at all 3 levels
- Streaming responses appear in ChatKit
- Tool visualization displays correctly
- Error handling with graceful degradation
- Multi-turn conversation context maintained
- Tests passing with required coverage (≥95% backend, ≥90% frontend)

### Phase 3: Deployment & Verification
**Duration**: 1-2 days

**Deliverables**:
1. Deploy frontend to Vercel
2. Register domain in OpenAI's ChatKit domain allowlist
3. Configure backend environment variables
4. Deploy backend to server (or cloud)
5. Verify end-to-end integration
6. Run quality gates and success criteria verification

**Acceptance Criteria**:
- Frontend deployed to production URL
- Backend running and accessible
- Database migrations applied
- All 17 success criteria verified
- Zero production errors

---

## Module Design & Contracts

### Backend Module: MCP Tools

**Responsibility**: Implement 5 MCP tools for task operations

**Tool 1: add_task**
```
Input:
  - user_id: string (from JWT token)
  - title: string (required, 1-200 chars)
  - description: string (optional, max 1000 chars)

Output:
  {
    "status": "success" | "error",
    "task_id": number,
    "title": string,
    "message": string
  }

Validation:
  - Title: required, non-empty, 1-200 chars
  - Description: optional, max 1000 chars
  - User ID: verify user exists and owns resource

Error Handling:
  - Validation error → return error status
  - Database error → auto-retry once, then error
```

**Tool 2: list_tasks**
```
Input:
  - user_id: string
  - status: "all" | "pending" | "completed" (optional, default: "all")

Output:
  {
    "status": "success" | "error",
    "tasks": [
      {
        "id": number,
        "title": string,
        "description": string,
        "completed": boolean,
        "created_at": string (ISO 8601)
      }
    ]
  }

Validation:
  - Status parameter: valid enum
  - User ID: verify ownership

Error Handling:
  - Invalid status → return error
  - No tasks found → return empty array with success status
```

**Tool 3: complete_task**
```
Input:
  - user_id: string
  - task_id: number (required)

Output:
  {
    "status": "success" | "error",
    "task_id": number,
    "title": string,
    "completed": boolean,
    "message": string
  }

Validation:
  - Task ID: positive integer
  - Task exists: verify in database
  - User ownership: verify user_id matches task.user_id

Behavior:
  - Toggle completion: pending → completed, completed → pending
  - Update updated_at timestamp
```

**Tool 4: delete_task**
```
Input:
  - user_id: string
  - task_id: number (required)

Output:
  {
    "status": "success" | "error",
    "task_id": number,
    "title": string,
    "message": string
  }

Validation:
  - Task ID: positive integer
  - Task exists: verify in database
  - User ownership: verify ownership

Behavior:
  - Permanent deletion (no recovery)
  - Return deleted task info for confirmation
```

**Tool 5: update_task**
```
Input:
  - user_id: string
  - task_id: number (required)
  - title: string (optional)
  - description: string (optional)

Output:
  {
    "status": "success" | "error",
    "task_id": number,
    "title": string,
    "message": string
  }

Validation:
  - At least one of title/description provided
  - Title: 1-200 chars if provided
  - Description: max 1000 chars if provided
  - User ownership: verify ownership

Behavior:
  - Update only provided fields
  - Keep created_at unchanged
  - Update updated_at timestamp
```

### Backend Module: Chat Endpoint

**Responsibility**: Handle user messages and coordinate agent/tool execution

**Endpoint**: `POST /api/{user_id}/chat`

**Request**:
```json
{
  "conversation_id": 123,  // Optional: existing conversation
  "message": "Add a task to buy groceries"
}
```

**Response**:
```json
{
  "status": "success" | "error",
  "data": {
    "conversation_id": 123,
    "response": "I've added 'Buy groceries' to your task list.",
    "tool_calls": [
      {
        "tool": "add_task",
        "status": "success",
        "parameters": {"title": "Buy groceries"},
        "result": {"task_id": 42}
      }
    ]
  },
  "error": null | "error message"
}
```

**Stateless Flow**:
1. Receive message + user_id + optional conversation_id
2. JWT validation: Verify token, extract user_id
3. Fetch conversation: Load conversation history from database
4. Build message array: All previous messages + new user message
5. Store user message: Persist to database
6. Run agent: Pass messages + MCP tools to Agents SDK
7. Agent execution: Agents SDK selects tools, calls MCP tools, generates response
8. Stream response: Send back to client in real-time
9. Store response: Persist assistant message to database
10. Return response: Final response with tool calls info

**Error Handling**:
- Validation error: Return 400 with error message
- Tool failure: Auto-retry once, inform user if persistent
- Database error: Return 500 with recovery suggestion
- API error: Return 503 with retry guidance

### Frontend Module: ChatWindow Component

**Responsibility**: Wrap OpenAI ChatKit for Phase 3

**Props**:
```typescript
interface ChatWindowProps {
  conversationId?: number;
  onError?: (error: Error) => void;
}
```

**Features**:
- Display chat messages (user + assistant)
- Show tool visualizations (which tools were called, results)
- Input field for user messages
- Send button with loading state
- Error display with retry button
- Conversation history loading
- Auto-scroll to latest message

**Accepts**:
- Messages from ChatKit API
- Tool call events
- Error events

**Returns**:
- User messages to backend via chat API
- Conversation state to parent component

---

## Testing Strategy

### Backend Testing

**Unit Tests** (60-80 tests, ≥95% coverage)
```
test_mcp_tools.py:
  - test_add_task_valid
  - test_add_task_validation_errors (title length, etc.)
  - test_add_task_database_error_with_retry
  - test_list_tasks_all_status
  - test_list_tasks_pending_status
  - test_list_tasks_completed_status
  - test_list_tasks_user_isolation
  - test_list_tasks_empty_result
  - test_complete_task_toggle_pending
  - test_complete_task_toggle_completed
  - test_complete_task_not_found
  - test_complete_task_user_isolation
  - test_delete_task_success
  - test_delete_task_not_found
  - test_delete_task_user_isolation
  - test_update_task_title_only
  - test_update_task_description_only
  - test_update_task_both
  - test_update_task_validation
  - test_update_task_timestamp_handling
```

**Integration Tests** (15-20 tests)
```
test_chat_endpoint.py:
  - test_chat_create_conversation
  - test_chat_existing_conversation
  - test_chat_tool_execution (add_task)
  - test_chat_streaming_response
  - test_chat_multi_tool_execution
  - test_chat_error_recovery_with_retry
  - test_chat_message_persistence
  - test_chat_conversation_history_retrieval
```

**User Isolation Tests** (10-15 tests)
```
test_user_isolation.py:
  - test_user_cannot_see_other_user_tasks
  - test_user_cannot_update_other_user_task
  - test_user_cannot_delete_other_user_task
  - test_chat_token_validation
  - test_conversation_belongs_to_correct_user
  - test_message_history_user_isolation
```

**Error Handling Tests** (10-15 tests)
```
test_error_handling.py:
  - test_tool_failure_auto_retry
  - test_tool_persistent_failure
  - test_database_connection_error
  - test_validation_error_messages
  - test_missing_required_parameters
  - test_invalid_token
```

### Frontend Testing

**Component Tests** (30-40 tests, ≥90% coverage)
```
ChatWindow.test.tsx:
  - test_chatwindow_renders
  - test_chatwindow_sends_message
  - test_chatwindow_displays_response
  - test_chatwindow_shows_loading_state
  - test_chatwindow_displays_error
  - test_chatwindow_visualizes_tool_calls
  - test_chatwindow_handles_streaming
  - test_chatwindow_shows_conversation_history
```

**Hook Tests** (10-15 tests)
```
useChat.test.ts:
  - test_usechat_initialize_conversation
  - test_usechat_send_message
  - test_usechat_receive_response
  - test_usechat_error_state
  - test_usechat_conversation_history
```

**API Client Tests** (10-15 tests)
```
chat-client.test.ts:
  - test_chat_api_call
  - test_chat_api_with_token
  - test_chat_api_error_handling
  - test_chat_api_streaming
```

### Quality Gates

All tests must pass with:
- Backend: ≥95% coverage (pytest --cov)
- Frontend: ≥90% coverage (jest/vitest --coverage)
- No type errors: mypy (backend), TypeScript (frontend)
- No lint errors: flake8 (backend), ESLint (frontend)

---

## Success Criteria Verification Plan

| SC ID | Criteria | Verification Method |
|-------|----------|---------------------|
| SC-001 | Task creation < 5 seconds | Time API request from send to confirmation |
| SC-002 | 90%+ accuracy for task creation | Manual test: 100 diverse prompts, check success rate |
| SC-003 | 95%+ accuracy for task filtering | Manual test: 50 filter queries, check correctness |
| SC-004 | All operations end-to-end functional | Integration tests for all 5 operations |
| SC-005 | Responses < 3 seconds | Monitor response times in tests |
| SC-006 | 10 concurrent conversations | Load test with concurrent requests |
| SC-007 | History persists across sessions | Test: create conversation, refresh, verify history present |
| SC-008 | User isolation enforced | User isolation tests: cross-user access blocked |
| SC-009 | MCP tools < 500ms response | Profile MCP tool execution times |
| SC-010 | Multi-tool chaining works | Test: one message that requires 2+ tools |
| SC-011 | All errors have recovery guidance | Manual test: trigger each error type |
| SC-012 | ≥95% backend coverage | pytest --cov: verify backend coverage |
| SC-013 | ≥90% chat endpoint coverage | pytest --cov: verify chat route coverage |
| SC-014 | ≥90% frontend coverage | jest --coverage: verify component coverage |
| SC-015 | Message summarization after 20 | Create 25-message conversation, verify summary |
| SC-016 | Concurrent edits last-write-wins | Test: edit same task from 2 clients |
| SC-017 | Tool failures trigger retry | Mock tool failure, verify single retry + user info |

---

## Risk Analysis & Mitigation

### Risk 1: ChatKit Integration Complexity
**Impact**: High | **Probability**: Medium
**Description**: ChatKit is new, domain allowlist setup may be complex
**Mitigation**:
- Use reference documentation (REFERENCE-OPENAI-CHATKIT.md)
- Start with simple demo, gradually add features
- Test domain allowlist configuration early
- Have fallback: implement basic WebSocket fallback if needed

### Risk 2: Agents SDK Tool Selection Issues
**Impact**: Medium | **Probability**: Low
**Description**: Agent may not select correct tool for user intent
**Mitigation**:
- Write clear MCP tool descriptions
- Test with diverse user prompts (100+ test cases)
- Implement clarification flow for ambiguous requests
- Log tool selection for debugging

### Risk 3: Message Summarization Edge Cases
**Impact**: Low | **Probability**: Medium
**Description**: Summarizing 20+ messages may lose context
**Mitigation**:
- Implement careful summarization strategy
- Test with realistic conversations
- Allow option to fetch full history if needed
- Monitor conversation quality

### Risk 4: Concurrent Edit Conflicts
**Impact**: Low | **Probability**: Low
**Description**: Last-write-wins may cause silent data loss in rare cases
**Mitigation**:
- Document behavior clearly in UI
- Implement optimistic locking for critical operations
- Accept silent overwrites as acceptable per spec

### Risk 5: Database Performance Under Load
**Impact**: Medium | **Probability**: Low
**Description**: Storing all messages may degrade performance
**Mitigation**:
- Create indexes on user_id, conversation_id, created_at
- Implement conversation archival for old conversations
- Monitor query performance during testing
- Use database connection pooling

### Risk 6: OpenAI API Rate Limits
**Impact**: High | **Probability**: Medium
**Description**: Agent SDK calls may hit rate limits
**Mitigation**:
- Implement exponential backoff for retries
- Cache common responses if possible
- Monitor token usage and costs
- Have clear error messages for rate limit errors

---

## Next Steps

1. ✅ **Phase 0: Research & Specification** - COMPLETE
   - Specification created (06-chatbot.md)
   - Clarifications integrated (3 decisions made)
   - Quality validated (30/30 checks passing)

2. **Phase 1: Design & Contracts** - NEXT
   - [ ] Create `specs/data-model.md`
   - [ ] Create `specs/contracts/` directory with API specs
   - [ ] Create `specs/quickstart.md`
   - **Estimated time**: 2-3 days

3. **Phase 2: Implementation** - AFTER Phase 1
   - [ ] Database migrations (Conversation, Message tables)
   - [ ] Backend implementation (MCP server, chat endpoint, tests)
   - [ ] Frontend implementation (ChatKit, components, tests)
   - [ ] Quality verification (coverage, types, linting)
   - **Estimated time**: 5-7 days

4. **Phase 3: Deployment** - AFTER Phase 2
   - [ ] Deploy frontend to Vercel
   - [ ] Deploy backend to server
   - [ ] Configure ChatKit domain allowlist
   - [ ] Verify all integrations
   - **Estimated time**: 1-2 days

**Total Estimated Time**: 8-12 days
**Deadline**: December 21, 2025
**Status**: Ready for Phase 1 (Design)

---

## Key Files for Reference

- `specs/features/06-chatbot.md` - Complete specification (read first!)
- `specs/features/checklists/chatbot-requirements.md` - Quality validation (30/30 passing)
- `docs/REFERENCE-OPENAI-CHATKIT.md` - ChatKit setup guide
- `docs/REFERENCE-OPENAI-AGENTS-SDK.md` - Agents SDK patterns
- `docs/REFERENCE-MCP-PROTOCOL.md` - MCP specification
- `.specify/memory/constitution.md` - Project governance (v3.0.0)

---

**Version**: 1.0
**Last Updated**: 2025-12-15
**Status**: Ready for Phase 1 Design & Contracts
**Branch**: phase-3
