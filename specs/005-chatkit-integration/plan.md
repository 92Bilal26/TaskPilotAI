# Implementation Plan: ChatKit Integration with Agent Builder Workflow

**Branch**: `005-chatkit-integration` | **Date**: December 20, 2025 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/005-chatkit-integration/spec.md`

## Summary

Integrate OpenAI ChatKit (official embeddable chat UI) with Agent Builder workflow for TaskPilotAI to enable users to chat with an AI agent via a web-based interface. Backend creates secure ChatKit sessions using OpenAI SDK; frontend loads ChatKit React component and initializes with client secrets from backend. Architecture maintains security by keeping workflow ID and API key server-side while frontend handles only UI rendering.

## Technical Context

**Language/Version**: Python 3.11+, TypeScript/React 19
**Primary Dependencies**:
- Backend: FastAPI, python-jose, openai>=1.12.0, openai-chatkit>=0.1.0
- Frontend: Next.js 16+, @openai/chatkit-react, TypeScript

**Storage**: Neon PostgreSQL (existing Phase 2 database)
**Testing**: pytest (backend), Jest/Vitest (frontend)
**Target Platform**: Web (Browser + FastAPI server)
**Project Type**: Full-stack web application (extends Phase 2)
**Performance Goals**: Session creation <2 seconds, message response <5 seconds, support 50+ concurrent sessions
**Constraints**: Session IDs unique, workflow ID immutable, client_secret never exposed to frontend
**Scale/Scope**: Stateless endpoint design, horizontal scalability built-in

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Phase 3 Constitution Requirements** (from `/specify/memory/constitution.md`):
- ✅ Spec-Driven Development: Specification complete and detailed
- ✅ Test-First Development: All code changes will include tests (≥95% backend, ≥90% frontend)
- ✅ OpenAI ChatKit Integration: Using official @openai/chatkit-react package
- ✅ OpenAI Agents SDK: Not required for Phase 3a (ChatKit is frontend only), will be used in Phase 3b
- ✅ Official MCP SDK: Not required for Phase 3a (ChatKit integration), will be used in Phase 3b
- ✅ No hardcoded secrets: Workflow ID stored in backend .env, API key never exposed
- ✅ Multi-user architecture maintained: Session creation respects authenticated user context

**Status**: ✅ **PASS** - All constraints satisfied

## Project Structure

### Documentation (this feature)

```text
specs/005-chatkit-integration/
├── spec.md                           # Feature specification
├── plan.md                           # This file (implementation plan)
├── checklists/
│   └── requirements.md               # Quality checklist (PASS status)
├── research.md                       # Phase 0 output (to be created)
├── data-model.md                     # Phase 1 output (to be created)
├── quickstart.md                     # Phase 1 output (to be created)
├── contracts/                        # Phase 1 output (to be created)
│   ├── sessions-api.md
│   └── chatkit-config.md
└── tasks.md                          # Phase 2 output (created by /sp.tasks, NOT /sp.plan)
```

### Source Code (repository root)

**Web Application (existing Phase 2 structure, extended for ChatKit)**:

```text
backend/
├── routes/
│   ├── chatkit.py                    # POST /api/chatkit/sessions endpoint (EXISTING)
│   └── ...
├── main.py                           # Routes registered (EXISTING)
├── requirements.txt                  # openai-chatkit>=0.1.0 added (EXISTING)
├── .env                              # OPENAI_API_KEY, CHATKIT_WORKFLOW_ID (EXISTING)
└── tests/
    └── test_chatkit.py               # Session creation tests (TO CREATE)

frontend/
├── app/
│   ├── chatkit/
│   │   └── page.tsx                  # ChatKit page (EXISTING)
│   └── layout.tsx                    # Script tag for ChatKit JS (EXISTING)
├── lib/
│   └── chatkit-config.ts             # getClientSecret() config (EXISTING)
├── components/
│   └── ChatKitComponent.tsx           # ChatKit React wrapper (TO CREATE)
├── .env.local                        # NEXT_PUBLIC_API_URL (EXISTING)
└── tests/
    └── chatkit.test.tsx              # ChatKit integration tests (TO CREATE)
```

**Structure Decision**:
- **Extends Phase 2**: Uses existing FastAPI backend and Next.js frontend
- **Minimal additions**: One endpoint in backend, one config file in frontend, one page component
- **Separation of concerns**: Backend handles security (session creation), frontend handles UI (ChatKit component)
- **Stateless design**: Each request is independent, no server-side conversation history for Phase 3a

## Complexity Tracking

**No Constitution violations to justify**. Feature is intentionally scoped to Phase 3a (ChatKit UI only).

Phase 3b will add:
- Agents SDK for intelligent tool orchestration
- MCP tools for task operations
- Conversation persistence in database
- Stateless chat endpoint
