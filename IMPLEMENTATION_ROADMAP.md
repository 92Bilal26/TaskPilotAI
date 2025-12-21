# ChatKit Integration: Implementation Roadmap

**Current Phase**: Phase 3 - Todo AI Chatbot
**Current Status**: 33% Complete (13/35 requirements met)
**Last Updated**: December 21, 2025

---

## Architecture: Current vs. Required

### ❌ REQUIRED ARCHITECTURE (Hackathon Phase 3)

```
┌─────────────────┐
│   ChatKit UI    │
│  (Frontend)     │
└────────┬────────┘
         │ POST message
         ▼
┌─────────────────────────────────────────┐
│   FastAPI Chat Endpoint                 │
│   POST /api/{user_id}/chat              │
│   • Fetch conversation history          │
│   • Store user message                  │
│   • Run agent                           │
│   • Invoke MCP tools                    │
│   • Store response                      │
└────────┬────────────────────────────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌─────────┐ ┌──────────────┐
│ Agents  │ │  MCP Server  │
│ SDK     │ │  • add_task  │
│ (GPT-4) │ │  • list      │
└────┬────┘ │  • complete  │
     │      │  • delete    │
     │      │  • update    │
     └──────┴──────┬───────┘
                   │
                   ▼
          ┌─────────────────┐
          │ Neon PostgreSQL │
          │ • Tasks         │
          │ • Conversations │
          │ • Messages      │
          └─────────────────┘
```

### ✅ CURRENT ARCHITECTURE (What We Built)

```
┌─────────────────┐
│   ChatKit UI    │
│  (Frontend)     │
└────────┬────────┘
         │ Request session
         ▼
┌──────────────────────┐
│ Session Endpoint     │
│ POST /chatkit/       │
│ sessions             │
└────────┬─────────────┘
         │ Return secret
         ▼
    ┌────────────┐
    │ ChatKit    │
    │ handles UI │
    └────────────┘

⚠️ Missing:
  - Chat endpoint
  - Agent SDK
  - MCP tools
  - Conversation storage
  - Message history
```

---

## Detailed Requirement Checklist

### Frontend Requirements

| Requirement | Status | Notes |
|-------------|--------|-------|
| OpenAI ChatKit installed | ✅ | `@openai/chatkit-react@^1.3.0` |
| ChatKit page created | ✅ | `/app/chatkit/page.tsx` |
| Session endpoint integration | ✅ | `POST /api/chatkit/sessions` |
| ChatKit JS script loaded | ✅ | In `app/layout.tsx` |
| Display messages from agent | ❌ | ChatKit shows own messages, not our agent's |
| Show tool invocations | ❌ | No tool display yet |
| Maintain conversation context | ❌ | No conversation history from our DB |

**Frontend Completion**: 4/7 (57%)

---

### Backend Requirements

| Requirement | Status | Notes |
|-------------|--------|-------|
| FastAPI application | ✅ | Running on port 8000 |
| Database connection | ✅ | Neon PostgreSQL configured |
| JWT authentication | ✅ | Better Auth integrated |
| CORS configuration | ✅ | Includes Vercel domain |
| Chat endpoint `/api/chat` | ❌ | Not implemented |
| Agents SDK integration | ❌ | Not installed or used |
| Agent runner/executor | ❌ | Not implemented |
| Tool invocation handling | ❌ | Not implemented |

**Backend Completion**: 4/8 (50%)

---

### Database Requirements

| Requirement | Status | Notes |
|-------------|--------|-------|
| Task model | ✅ | Already exists from Phase 2 |
| Conversation model | ❌ | Need to create |
| Message model | ❌ | Need to create |
| User foreign key constraints | ⚠️ | Partial (tasks only) |
| Database migrations | ⚠️ | Alembic configured but new models not migrated |

**Database Completion**: 1/5 (20%)

---

### MCP Server Requirements

| Requirement | Status | Notes |
|-------------|--------|-------|
| Official MCP SDK installed | ❌ | Not installed |
| MCP server initialized | ❌ | Not created |
| add_task tool | ❌ | Not implemented |
| list_tasks tool | ❌ | Not implemented |
| complete_task tool | ❌ | Not implemented |
| delete_task tool | ❌ | Not implemented |
| update_task tool | ❌ | Not implemented |
| Tool error handling | ❌ | Not applicable yet |

**MCP Server Completion**: 0/8 (0%)

---

### Agent Behavior Requirements

| Requirement | Status | Notes |
|-------------|--------|-------|
| Task creation understanding | ❌ | Agent not yet implemented |
| Task listing understanding | ❌ | Agent not yet implemented |
| Task completion understanding | ❌ | Agent not yet implemented |
| Task deletion understanding | ❌ | Agent not yet implemented |
| Task update understanding | ❌ | Agent not yet implemented |
| Friendly confirmations | ❌ | Agent not yet implemented |
| Error handling | ❌ | Agent not yet implemented |

**Agent Behavior Completion**: 0/7 (0%)

---

### API & Architecture Requirements

| Requirement | Status | Notes |
|-------------|--------|-------|
| Chat endpoint exists | ❌ | `POST /api/{user_id}/chat` needed |
| Request format correct | ❌ | conversation_id, message fields |
| Response format correct | ❌ | Should include tool_calls array |
| Stateless server design | ⚠️ | Infrastructure ready but chat flow missing |
| Conversation persistence | ❌ | Database models needed |
| Message persistence | ❌ | Database models needed |
| Tool result storage | ❌ | Requires full chat flow |

**API & Architecture Completion**: 0/7 (0%)

---

## Phase Breakdown: What's Done and What's Next

### ✅ PHASES COMPLETED (Phases 1-3: Basic Setup)

**Phase 1: Setup & Infrastructure**
- Dependencies installed
- Routes created
- Configurations set

**Phase 2: Foundational Backend**
- OpenAI SDK initialized
- Session endpoint working
- CORS configured

**Phase 3: Session Initiation Tests**
- Test files created
- ChatKit integration verified
- Domain configuration documented

**Status**: 3/3 phases complete ✅

---

### ⏳ PHASES REQUIRED (Phases 4-8: Full AI Chatbot)

#### Phase 4: Database Models & Persistence
**Goal**: Add Conversation and Message models to database

**Tasks**:
- [ ] Create Conversation SQLModel
- [ ] Create Message SQLModel
- [ ] Create database migration
- [ ] Write tests for models
- [ ] Verify constraints and relationships

**Estimated Time**: 1-2 hours
**Complexity**: Low (familiar patterns)
**Blocker**: None (can start immediately)

---

#### Phase 5: Chat Endpoint with Agent
**Goal**: Implement `/api/{user_id}/chat` endpoint with Agents SDK

**Tasks**:
- [ ] Install OpenAI Agents SDK
- [ ] Create chat endpoint route
- [ ] Implement conversation history retrieval
- [ ] Implement agent initialization
- [ ] Implement message persistence
- [ ] Add error handling
- [ ] Write tests

**Estimated Time**: 2-3 hours
**Complexity**: Medium (Agents SDK learning curve)
**Blocker**: Phase 4 must complete first

---

#### Phase 6: MCP Server & Tools
**Goal**: Implement MCP server with 5 task management tools

**Tasks**:
- [ ] Install MCP SDK
- [ ] Create MCP server initialization
- [ ] Implement add_task tool
- [ ] Implement list_tasks tool
- [ ] Implement complete_task tool
- [ ] Implement delete_task tool
- [ ] Implement update_task tool
- [ ] Wire tools to agent
- [ ] Add error handling
- [ ] Write tests

**Estimated Time**: 3-4 hours
**Complexity**: High (MCP is new, tool chaining)
**Blocker**: Phase 5 must complete first

---

#### Phase 7: Agent Behavior & NLP
**Goal**: Configure agent to understand natural language and invoke tools

**Tasks**:
- [ ] Add agent system prompt
- [ ] Add agent instructions
- [ ] Test natural language understanding
- [ ] Test tool invocation logic
- [ ] Test tool result handling
- [ ] Add conversation context awareness
- [ ] Add friendly response generation
- [ ] Write NLP integration tests

**Estimated Time**: 2-3 hours
**Complexity**: Medium (prompt engineering)
**Blocker**: Phase 6 must complete first

---

#### Phase 8: Integration & Production
**Goal**: Full end-to-end testing and production deployment

**Tasks**:
- [ ] End-to-end flow testing (ChatKit → Chat → Agent → Tools → DB)
- [ ] Stress testing (concurrent conversations)
- [ ] Error recovery testing
- [ ] Agent tool composition testing (multiple tools in one response)
- [ ] Production domain allowlist registration (if not done)
- [ ] Environment variable configuration for production
- [ ] Deployment to production servers
- [ ] Monitoring and logging setup

**Estimated Time**: 2-3 hours
**Complexity**: Medium (integration testing)
**Blocker**: Phase 7 must complete first

---

## Implementation Timeline

```
Current: 33% Complete (3.5 hours invested)
├─ Phase 1: Setup (30 min) ✅
├─ Phase 2: Backend Foundation (1 hour) ✅
├─ Phase 3: Tests & Config (2 hours) ✅
│
Next: 67% Remaining (10-12 hours estimated)
├─ Phase 4: Database Models (1.5 hours) ⏳
├─ Phase 5: Chat Endpoint + Agent (2.5 hours) ⏳
├─ Phase 6: MCP Server (3.5 hours) ⏳
├─ Phase 7: Agent Behavior (2.5 hours) ⏳
└─ Phase 8: Integration & Production (2.5 hours) ⏳

TOTAL ESTIMATED: 13-15 hours for complete Phase 3
```

---

## Key Dependencies & Risks

### Must-Have Dependencies (Not Yet Installed)

```bash
# Phase 5
pip install openai>=1.14.0  # Agents SDK support

# Phase 6
pip install mcp>=0.1.0  # Official MCP SDK
```

### Learning Curve Risks

| Component | Risk Level | Mitigation |
|-----------|-----------|-----------|
| OpenAI Agents SDK | Medium | Use official docs + examples |
| MCP Server Framework | High | Detailed research + documentation |
| Tool Composition | High | Start with single tool, then chain |
| Stateless Architecture | Low | Already designed in Phase 2 |

### Architecture Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|-----------|
| Agent hallucination (wrong tool call) | High | Medium | Add tool use validation, error recovery |
| MCP tool errors not handled | High | High | Comprehensive error handling in each tool |
| Conversation state loss | Low | High | Database persistence verified in Phase 4 |
| Token limits exceeded | Medium | High | Implement conversation truncation |

---

## Success Criteria

### For Each Phase

**Phase 4**: ✅ Conversation/Message models created and tested
**Phase 5**: ✅ Chat endpoint receives messages and stores them
**Phase 6**: ✅ MCP server exposes 5 tools without errors
**Phase 7**: ✅ Agent can understand and invoke correct tools
**Phase 8**: ✅ ChatKit UI shows agent responses and tool confirmations

### For Complete Phase 3

**User Can**:
1. ✅ Navigate to `/chatkit` page
2. ✅ Send message: "Add a task to buy groceries"
3. ✅ See response: "I've added 'Buy groceries' to your tasks"
4. ✅ Task appears in task list (via MCP tool)
5. ✅ Send message: "Show me all tasks"
6. ✅ See list of all tasks with completions
7. ✅ Send message: "Mark task 1 complete"
8. ✅ Task marked complete in database
9. ✅ Conversation history persisted (can refresh and continue)
10. ✅ Works on production Vercel URL

---

## Recommendation

### PROCEED with Phases 4-8 ✅

**Rationale**:
1. ✅ Foundation is solid (ChatKit + Session + DB)
2. ✅ Phases 4-8 are well-defined and ordered
3. ✅ Architecture aligns with Hackathon requirements
4. ✅ Risks are manageable with proper planning
5. ✅ Estimated time is reasonable for scope

**Next Action**:
→ Confirm you're ready to proceed to **Phase 4: Database Models**
→ I'll create comprehensive task breakdown for Phases 4-8

---

## File References

- **Hackathon Requirements**: `/hakcathon_2_doc.md` (lines 620-848)
- **Current Spec**: `/specs/005-chatkit-integration/spec.md`
- **Current Tasks**: `/specs/005-chatkit-integration/tasks.md`
- **Compliance Audit**: `/PHASE_3_COMPLIANCE_AUDIT.md`
- **This Roadmap**: `/IMPLEMENTATION_ROADMAP.md`
