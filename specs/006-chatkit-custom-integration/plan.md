# Implementation Plan: ChatKit UI Integration with Custom Chatbot Backend

**Branch**: `006-chatkit-custom-integration` | **Date**: December 21, 2025 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/006-chatkit-custom-integration/spec.md`

**Note**: This plan is filled by the `/sp.plan` command and covers Phase 0 (Research) and Phase 1 (Design & Contracts).

## Summary

**Feature**: Integrate OpenAI ChatKit UI with existing custom chatbot backend (Agents SDK + MCP tools) using advanced self-hosted approach with ChatKit Python SDK wrapper.

**Technical Approach**: Wrap existing `/api/{user_id}/chat` Agents SDK endpoint with a ChatKit Python SDK `ChatKitServer` implementation that handles ChatKit protocol, delegating business logic to existing agents/MCP tools.

**Outcome**: Full-stack AI task management chatbot with ChatKit UI frontend + custom agents backend, achieving 100% Hackathon Phase 3 compliance with conversation persistence, tool invocation, and database integration.

## Technical Context

**Language/Version**: Python 3.11+ (backend), TypeScript/React (frontend)
**Primary Dependencies**:
  - Backend: FastAPI, OpenAI Agents SDK, ChatKit Python SDK (`openai-chatkit`), SQLModel, Neon PostgreSQL
  - Frontend: React 19, Next.js 16+, @openai/chatkit-react, TypeScript
**Storage**: Neon PostgreSQL (Conversations, Messages, Tasks tables)
**Testing**: pytest (backend), Vitest/Jest (frontend)
**Target Platform**: Web (Vercel for frontend, Cloud host for backend)
**Project Type**: Full-stack web application (frontend + backend)
**Performance Goals**:
  - Message latency: P95 < 5 seconds (FR-SC-001)
  - Agent tool invocation success: 95%+ (FR-SC-005)
  - Message persistence accuracy: 100% (FR-SC-003)
  - User isolation enforcement: 0% unauthorized access (FR-SC-004)
**Constraints**:
  - Reuse existing chat endpoint (no new endpoint architecture)
  - Minimal backend modifications (ChatKit wrapper only)
  - No changes to agent system prompt or MCP tools
  - Database schema already exists (use existing models)
**Scale/Scope**:
  - 2-4 hour implementation (4-5 tasks including research + design)
  - ~1000 LOC for ChatKit wrapper + config changes
  - 4 user stories (P1: core messaging, P2: tool display, P3: persistence/sessions)
  - Multi-user support with full user isolation

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**TaskPilotAI Constitution Assessment** (from `.specify/memory/constitution.md` Phase 1 spec):

| Gate | Status | Notes |
|------|--------|-------|
| **Spec-Driven Development** | ✅ PASS | Feature 006 spec complete with clarifications; ready for implementation |
| **Test-First (TDD)** | ✅ PASS | Will implement tests before code for ChatKit wrapper + integration tests |
| **In-Memory State** | ⚠️ N/A | Phase 3 (not Phase 1); uses database persistence instead |
| **Clean Code Standards** | ✅ PASS | All new code will follow PEP 8, type hints, docstrings |
| **CLI-First Interface** | ⚠️ N/A | Phase 3 is web-based with ChatKit UI (not CLI) |
| **Minimal Viable Complexity** | ✅ PASS | Wraps existing backend; no new complexity added |
| **Hackathon Phase 3 Compliance** | ✅ PASS | ChatKit + Agents SDK + MCP + Database Persistence all covered |

**Gate Evaluation**: ✅ **PASSES** - Phase 3 is different from Phase 1 constitution but follows its spirit: spec-driven, test-first, clean code. Constitutional goals are context-appropriate for Phase 3.

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

**Structure Decision**: Full-stack web application with existing backend + frontend (Option 2)

```text
backend/
├── routes/
│   ├── chatkit.py              # NEW: ChatKit Python SDK server wrapper
│   ├── chat.py                 # EXISTING: /api/{user_id}/chat endpoint
│   └── ...
├── task_agents/
│   └── official_openai_agent.py # EXISTING: Agents SDK
├── mcp/
│   ├── server.py               # EXISTING: MCP server
│   └── tools/                  # EXISTING: 6 task tools
├── models.py                   # EXISTING: SQLModel (add ChatKit session linking)
├── config.py                   # UPDATE: Add ChatKit config
├── main.py                     # UPDATE: Register ChatKit endpoint
└── tests/
    ├── test_chatkit_wrapper.py # NEW: ChatKit server wrapper tests
    ├── test_chatkit_integration.py # NEW: End-to-end tests
    └── ...

frontend/
├── app/
│   ├── chatkit/
│   │   └── page.tsx            # EXISTING: ChatKit page
│   ├── layout.tsx              # UPDATE: ChatKit script loading
│   └── ...
├── lib/
│   ├── chatkit-config.ts       # UPDATE: Message routing config
│   ├── chat-client.ts          # EXISTING: Chat API client
│   └── ...
├── components/
│   ├── ChatKit/
│   │   └── ChatKitWidget.tsx   # NEW: ChatKit UI wrapper component
│   └── ...
└── __tests__/
    ├── chatkit-integration.test.ts # NEW: Frontend integration tests
    └── ...
```

## Phase 0: Research & Unknowns

**Status**: Research consolidated from user clarifications + official documentation

### Key Decisions Made

| Unknown | Decision | Rationale | Alternatives |
|---------|----------|-----------|--------------|
| **ChatKit Integration** | Advanced self-hosted (ChatKit Python SDK wrapper) | Full control over agents/MCP, reuses existing backend, custom tool display | Recommended (Agent Builder - less control, hosted by OpenAI) |
| **Tool Display** | Hybrid (text + widgets) | Simple ops→text, complex→widgets (e.g., list_tasks card) | All text (simpler), all widgets (too complex) |
| **Backend Approach** | Wrap existing `/api/{user_id}/chat` with ChatKitServer | Minimal changes, reuses agents/MCP/DB entirely | New ChatKit-specific endpoint (more work) |
| **Session Mapping** | ChatKit sessions → Conversation records | Links ChatKit sessions to database, enables persistence | Separate session store (duplicate data) |
| **Widget Framework** | ChatKit Python SDK widget system (Card, ListView, Button, Form) | Official, well-tested, supports actions and validation | Custom widget implementation (risky, slower) |
| **Message Format** | ChatKit event-based protocol with streaming support | Standard protocol, handles multi-turn context, tool results | Custom JSON (non-standard, harder to debug) |

### Research Sources

- **Official ChatKit Docs**: `/chatkit_doc_from_web.md` - Advanced integration, ChatKitServer API
- **Official Videos**: `/chatkit_youtube_video_transcript*.md` - Implementation patterns
- **Hackathon Phase 3 Spec**: `/hakcathon_2_doc.md` lines 620+ - ChatKit + Agents SDK + MCP + Persistence requirements
- **Existing Custom Chatbot**: `/backend/routes/chat.py`, `/backend/task_agents/`, `/backend/mcp/` - Proven working implementation

---

## Phase 1: Design & API Contracts

### 1.1 Data Model Design

**New/Modified Entities**:

```
ChatKitSession:
  - session_id (str): Unique session ID from ChatKit SDK
  - thread_id (str): ChatKit internal thread identifier
  - user_id (str): User from JWT
  - conversation_id (int FK): Links to Conversation
  - created_at (datetime)
  - expires_at (datetime): Session expiration

Conversation (EXISTING - ADD FIELD):
  - chatkit_session_id (str FK): Link to ChatKit session (nullable for non-ChatKit conversations)

Message (EXISTING - NO CHANGES NEEDED):
  - Already stores user/assistant messages with tool_calls JSON
  - Supports multi-turn context retrieval
```

**Data Relationships**:
```
User (from Better Auth)
  ├─ Conversations (1:N)
  │  ├─ ChatKit Sessions (1:N, via chatkit_session_id)
  │  └─ Messages (1:N)
  │     └─ tool_calls (JSON array of execution records)
  └─ Tasks (1:N, managed by MCP tools)
```

### 1.2 API Contracts

**ChatKit Python SDK Server Implementation** (new endpoint):

```python
# /backend/routes/chatkit.py (NEW)

POST /api/v1/chatkit
  Body: ChatKit event stream (binary/protobuf)
  Returns: ChatKit response stream

  Implements ChatKitServer interface:
    - async def respond(thread: ThreadMetadata, input: UserMessageItem | ClientToolCallOutputItem, context: RequestContext) -> AsyncIterator[Event]
    - async def action(thread, action, sender, context) -> AsyncIterator[Event]
    - Database: Store threads as Conversations, messages as Messages

Key classes to implement:
  - MyChatKitServer(ChatKitServer) - Main server class
    - __init__(data_store, file_store) - Initialize with DB/file store
    - respond() - Process user messages and return agent responses
    - Delegate to existing Agents SDK + MCP tools
```

**Modified Endpoints**:

```python
# /backend/routes/chat.py (EXISTING - NO CHANGES NEEDED)
POST /api/{user_id}/chat
  Request: { "conversation_id": int?, "content": str }
  Response: { "conversation_id": int, "response": str, "tool_calls": [...] }
  - Already implements the core agent processing
  - ChatKitServer will delegate to this or reuse agent logic
```

**Session Management**:

```python
# Existing session endpoint (keep as-is for compatibility)
POST /api/v1/chatkit/sessions
  Request: { }
  Response: { "client_secret": str, "session_id": str }
  - Returns ChatKit secret for frontend
  - Backend can optionally link to Conversation here
```

### 1.3 Integration Design

**Message Flow Architecture**:

```
┌─────────────────┐
│   ChatKit UI    │ (Frontend - @openai/chatkit-react)
└────────┬────────┘
         │ ChatKit protocol (binary event stream)
         ▼
┌─────────────────────────────────────────┐
│  ChatKit Python SDK Server              │ (NEW: /backend/routes/chatkit.py)
│  (Implements ChatKitServer interface)   │
│  - Handles sessions, threads, messages │
│  - Manages conversation persistence    │
└────────┬────────────────────────────────┘
         │ Delegates to existing code
         ▼
┌─────────────────────────────────────────┐
│  Existing Agents SDK                    │ (REUSED)
│  + MCP Tools                            │ (REUSED)
│  + Database Persistence                 │ (REUSED)
└─────────────────────────────────────────┘
```

**Tool Result Display (Hybrid Format)**:

```
Simple Tools (add_task, delete_task, update_task, complete_task):
  - Return plain text confirmations
  - Rendered as standard ChatKit text messages
  - Example: "✓ Task created: Buy groceries"

Complex Tools (list_tasks):
  - Return ChatKit Card widget with task list
  - Uses ListView for scrollable task display
  - Supports actions (click to open, archive, etc.)
  - Example: Card with task list inside, status indicators

Tool Errors:
  - Return user-friendly error message
  - Displayed as warning/error type message in ChatKit
  - Example: "Couldn't find task 'Buy milk' - did you mean something else?"
```

### 1.4 Quickstart Implementation Guide

**Local Development Setup**:

```bash
# 1. Install ChatKit Python SDK
pip install openai-chatkit

# 2. Create ChatKit server wrapper
# /backend/routes/chatkit.py implements ChatKitServer

# 3. Register endpoint in main.py
# app.post("/api/v1/chatkit")(server.process())

# 4. Frontend: Use existing ChatKit React component
# Components already in place, add message routing to /api/v1/chatkit

# 5. Test locally
pytest backend/tests/test_chatkit_wrapper.py
npm test frontend/__tests__/chatkit-integration.test.ts
```

**Production Deployment**:

```bash
# Same code works on Vercel + Cloud backend
# - Frontend deployed to Vercel (existing setup)
# - Backend deployed to Cloud (existing setup)
# - ChatKit wrapper works identically in both
# - Neon PostgreSQL handles conversation persistence
```

### 1.5 Configuration Changes

**Backend config updates**:

```python
# backend/config.py (UPDATE)

# Add ChatKit configuration
CHATKIT_ENABLED = True
CHATKIT_SESSION_TIMEOUT = 3600  # 1 hour
CHATKIT_MAX_HISTORY = 10  # Last 10 messages for context

# Keep existing Agents/MCP config
AGENT_MODEL = "gpt-4-turbo"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
```

**Frontend config updates**:

```typescript
// frontend/lib/chatkit-config.ts (UPDATE)

// Ensure messages route to backend ChatKit endpoint
export const chatKitConfig: UseChatKitOptions = {
  api: {
    async getClientSecret(existing?: string) {
      const res = await fetch('/api/v1/chatkit/sessions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      });
      return (await res.json()).client_secret;
    },
  },
  // ... rest of config
};
```

---

## Complexity Tracking

> **Constitution Check**: PASSES (as evaluated above)
> **Research**: COMPLETE (decisions made, alternatives documented)
> **Design**: COMPLETE (data model, API contracts, integration, quickstart)

---

---

## Next Steps

**Phase 2: Task Generation**

The implementation plan is complete. Next step is to run `/sp.tasks` to generate:
- Detailed task breakdown for Phase B (Verify, Integrate, Deploy)
- Estimated effort per task
- Task dependencies and ordering
- Success criteria per task

**Expected Output**: `/specs/006-chatkit-custom-integration/tasks.md` with 15-20 focused tasks for Path B implementation.
