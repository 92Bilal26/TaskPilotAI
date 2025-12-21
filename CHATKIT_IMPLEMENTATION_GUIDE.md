# ChatKit Implementation Guide for TaskPilotAI

**Version**: 1.0
**Date**: December 2025
**Approach**: Advanced Integration (Custom Backend)
**Status**: Ready for Implementation

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [What You Need to Provide](#what-you-need-to-provide)
4. [What Claude Code Will Handle](#what-claude-code-will-handle)
5. [Step-by-Step Implementation](#step-by-step-implementation)
6. [Backend Setup](#backend-setup)
7. [Frontend Setup](#frontend-setup)
8. [Testing & Deployment](#testing--deployment)

---

## Overview

**Current State**: Your app has a custom chatbot. You want to replace it with **OpenAI ChatKit**, which provides:
- ✅ Professional chat UI out-of-the-box
- ✅ Agent-based task handling
- ✅ Interactive widgets (forms, cards, buttons)
- ✅ Action support for backend integration
- ✅ Built-in conversation history
- ✅ Customizable themes

**Key Decision**: You're using **Advanced Integration** = ChatKit runs on YOUR backend (not OpenAI's), giving you full control over the agent logic.

---

## Architecture

### Current Setup
```
User → Next.js Frontend → Custom Chatbot → Task Management
```

### After ChatKit Implementation
```
User → Next.js Frontend (ChatKit UI)
                    ↓
            Your FastAPI Backend
                    ↓
        ChatKit Server (Python SDK)
                    ↓
        Agent Logic + Task Management
```

### Technology Stack
- **Frontend**: Next.js 16+ with React 19 + `@openai/chatkit-react`
- **Backend**: FastAPI + `openai-chatkit` Python SDK
- **Agent**: OpenAI API (gpt-4.1 or similar)
- **Storage**: SQLite or PostgreSQL (for thread management)

---

## What You Need to Provide

### 1. **OpenAI API Key** ✅ (Already have)
- Status: Already configured in backend `.env`
- Used for: Running agent inference and stream responses
- Location: `OPENAI_API_KEY` environment variable

### 2. **Backend Configuration Details** ❌ (Need from you)
Answer these questions:

**Q1: Where is your current custom chatbot code?**
- Backend files: `backend/routes/chat.py`? `backend/chatbot.py`?
- Frontend components: `frontend/components/Chatbot.tsx`? `frontend/app/chat/page.tsx`?

**Q2: How does your chatbot currently handle tasks?**
- What endpoints are used for task operations?
- How does the chatbot fetch/create/update tasks?
- Is there an agent or just prompt-based?

**Q3: What database do you prefer for ChatKit storage?**
- SQLite (simple, local)
- PostgreSQL (production-ready)
- Neon (from Phase 2, managed)

**Q4: What should the ChatKit agent be able to do?**
- Create tasks?
- List tasks?
- Update tasks?
- Delete tasks?
- Mark complete?
- All of the above?

**Q5: What system instructions for the agent?**
- Example: "You are an AI task management assistant that helps users manage their to-do list..."

---

## What Claude Code Will Handle

### Backend Implementation
- ✅ Create `ChatKitServer` class extending OpenAI's base
- ✅ Implement `respond()` method for agent logic
- ✅ Implement `action()` method for widget actions
- ✅ Create FastAPI endpoint: `/api/v1/chatkit` (POST)
- ✅ Implement session creation endpoint: `/api/v1/chatkit/sessions` (POST)
- ✅ Add database models for thread storage
- ✅ Integrate with your task management system

### Frontend Implementation
- ✅ Update ChatKit React configuration
- ✅ Create proper `getClientSecret()` function
- ✅ Add ChatKit JS script to layout
- ✅ Implement error handling and loading states
- ✅ Style ChatKit to match your app theme

### Testing & Validation
- ✅ Create unit tests for ChatKit integration
- ✅ Create integration tests for full flow
- ✅ Test session creation
- ✅ Test agent responses
- ✅ Test widget actions

---

## Step-by-Step Implementation

### Phase 1: Backend Setup (3 tasks)
1. **Create ChatKit Server class** - Handle incoming requests from ChatKit SDK
2. **Implement session endpoint** - Generate client secrets for frontend
3. **Integrate with task management** - Link ChatKit responses to your existing tasks API

### Phase 2: Frontend Setup (2 tasks)
1. **Update ChatKit configuration** - Fix API integration with `getClientSecret()`
2. **Add UI components** - Loading states, error handling, proper styling

### Phase 3: Testing (2 tasks)
1. **Unit tests** - Test individual components and functions
2. **Integration tests** - Test full end-to-end flow

### Phase 4: Deployment (1 task)
1. **Deploy and configure** - Set environment variables, verify security

---

## Backend Setup

### File Structure
```
backend/
├── main.py                          (Update: Add ChatKit endpoint)
├── chatkit_server.py               (NEW: ChatKit server class)
├── routes/
│   ├── chatkit.py                  (NEW: ChatKit endpoints)
│   └── tasks.py                    (Existing: Task management)
├── models/
│   ├── chatkit.py                  (NEW: Thread/session models)
│   └── task.py                     (Existing: Task model)
├── agents/
│   └── task_agent.py               (NEW: Agent logic)
└── .env                            (Already exists: OPENAI_API_KEY)
```

### Required Dependencies

**Add to `backend/requirements.txt`:**
```
openai>=1.0.0
openai-chatkit>=0.1.0
fastapi>=0.104.0
uvicorn>=0.24.0
sqlalchemy>=2.0.0
pydantic>=2.0.0
python-dotenv>=1.0.0
```

**Install:**
```bash
cd backend
pip install -r requirements.txt
```

### Backend Environment Variables

**In `backend/.env` (add if not present):**
```
# Already exists
OPENAI_API_KEY=sk_...

# Add these:
CHATKIT_MODEL=gpt-4.1
CHATKIT_TEMPERATURE=0.7
DATABASE_URL=sqlite:///./chatkit.db  # or PostgreSQL URL
```

---

## Frontend Setup

### File Structure
```
frontend/
├── app/
│   ├── chatkit/
│   │   └── page.tsx               (UPDATE: Fix ChatKit integration)
│   └── layout.tsx                 (UPDATE: Add ChatKit JS script)
├── lib/
│   ├── chatkit-config.ts          (UPDATE: Fix configuration)
│   └── useAuth.ts                 (Already exists)
└── components/
    └── ChatKitContainer.tsx        (NEW: Optional wrapper)
```

### Current Issues in Your Code

**PROBLEM 1: Wrong API configuration**

Current (broken):
```typescript
api: {
  url: `${API_URL}/api/v1/chatkit`,
  domainKey: DOMAIN_KEY,
  fetch: authenticatedFetch,
}
```

Fixed:
```typescript
api: {
  async getClientSecret(existing) {
    if (existing) return existing;
    
    const res = await fetch('/api/chatkit/sessions', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
    });
    const { client_secret } = await res.json();
    return client_secret;
  }
}
```

**PROBLEM 2: Missing ChatKit JS script**

Need to add to `frontend/app/layout.tsx`:
```html
<script
  src="https://cdn.platform.openai.com/deployments/chatkit/chatkit.js"
  async
></script>
```

---

## Information YOU Must Provide Before Implementation

### REQUIRED Information

Please answer all of these:

```
CHATKIT IMPLEMENTATION CHECKLIST
================================

1. CUSTOM CHATBOT LOCATION
   └─ Current custom chatbot is located at: ____________________
   └─ Examples: backend/routes/chat.py, frontend/components/Chat.tsx

2. TASK MANAGEMENT API
   └─ Task creation endpoint: POST /api/v1/tasks (example)
   └─ Task list endpoint: GET /api/v1/tasks
   └─ Other task endpoints: ____________________
   └─ Current task fields: title, description, completed, etc.

3. DATABASE PREFERENCE
   └─ Choice: [ ] SQLite  [ ] PostgreSQL  [ ] Neon
   └─ Existing DB location: ____________________

4. AGENT CAPABILITIES
   └─ What should ChatKit agent do?
   │  [ ] Create tasks
   │  [ ] Read/list tasks
   │  [ ] Update tasks
   │  [ ] Delete tasks
   │  [ ] Mark tasks complete
   │  [ ] Other: ____________________

5. AGENT SYSTEM INSTRUCTIONS
   └─ What should the agent be called?
   └─ What tone should it use?
   └─ Any special behaviors?
   └─ Example: "You are TaskMaster AI, a helpful assistant for managing tasks..."

6. AUTHENTICATION
   └─ Current auth method: JWT, Better Auth, etc.
   └─ Should ChatKit threads be per-user?
   └─ How to associate thread with user? ____________________

7. CUSTOMIZATION PREFERENCES
   └─ Theme color: ____________________
   └─ Enable file attachments? [ ] Yes [ ] No
   └─ Enable widgets? [ ] Yes [ ] No
   └─ Enable @mentions? [ ] Yes [ ] No
```

---

## Implementation Workflow

### Step 1: You Provide Information
- Fill out the checklist above
- Share your current chatbot code
- Provide task management endpoint details

### Step 2: Claude Code Implements Backend
- Creates ChatKit server class
- Creates session endpoint
- Integrates with your tasks API
- Writes database models
- Creates agent logic

### Step 3: Claude Code Implements Frontend
- Fixes ChatKit configuration
- Updates pages and components
- Adds proper error handling
- Styles to match your app

### Step 4: Testing
- Creates and runs unit tests
- Creates and runs integration tests
- Fixes any issues found

### Step 5: Deployment
- You deploy backend and frontend
- Verify ChatKit is working
- Test with real tasks

---

## Complete Task List

| # | Task | Owner | Duration | Status |
|---|------|-------|----------|--------|
| **Backend** |
| 1 | Create ChatKit server class | Claude Code | 2-3h | 🔴 Pending |
| 2 | Create session endpoint | Claude Code | 30m | 🔴 Pending |
| 3 | Integrate with task management | Claude Code | 3-4h | 🔴 Pending |
| **Frontend** |
| 4 | Fix ChatKit configuration | Claude Code | 15m | 🔴 Pending |
| 5 | Update layout and page | Claude Code | 20m | 🔴 Pending |
| **Testing** |
| 6 | Create unit tests | Claude Code | 1-2h | 🔴 Pending |
| 7 | Create integration tests | Claude Code | 1-2h | 🔴 Pending |
| **Deployment** |
| 8 | Deploy and verify | You + Claude Code | 30m | 🔴 Pending |

**Total Estimated Time**: 9-14 hours

---

## Key Concepts You Should Know

### ChatKit vs Custom Chatbot
| Aspect | Custom | ChatKit |
|--------|--------|---------|
| UI Component | Build from scratch | Pre-built, professional |
| Chat History | Manual management | Built-in |
| Widgets | Custom code | Rich components available |
| Styling | Full control | Configurable themes |
| Agent Integration | Custom | OpenAI SDK integration |
| Deployment | Simple | Simple (uses FastAPI) |

### Session Flow
```
1. User loads ChatKit page
   ↓
2. Frontend calls `getClientSecret()`
   ↓
3. Frontend sends POST /api/chatkit/sessions
   ↓
4. Backend creates session with OpenAI SDK
   ↓
5. Backend returns client_secret
   ↓
6. Frontend initializes ChatKit with secret
   ↓
7. ChatKit connects to backend via WebSocket
   ↓
8. User sends message
   ↓
9. Backend agent responds using ChatKit server
```

### Agent Loop
```
User Message
    ↓
ChatKit Server (on backend)
    ↓
OpenAI API (processes with agent)
    ↓
Parse response (tasks, widgets, etc)
    ↓
Call task APIs if needed
    ↓
Return formatted response + widgets
    ↓
Display in ChatKit UI
```

---

## Ready to Start?

### Next Action: Provide Information

1. **Copy the checklist above**
2. **Fill in all required information**
3. **Share current chatbot code location**
4. **Tell me: "I've provided ChatKit information, ready to implement"**

### Then I Will:
- Implement all backend code
- Implement all frontend code
- Create comprehensive tests
- Deploy and verify everything

---

## Questions During Implementation

If you have questions:
- **"What does X do?"** → I'll explain
- **"How do I test this?"** → I'll create tests
- **"Why doesn't this work?"** → I'll debug and fix
- **"Can I customize Y?"** → I'll implement customization

---

## Success Criteria

✅ ChatKit page loads without errors
✅ Frontend can create sessions
✅ Backend ChatKit server responds to messages
✅ Agent integrates with task management
✅ Chat history is stored and retrieved
✅ All tests pass with 90%+ coverage
✅ Works with your authentication system
✅ Deployed to production

---

**Status**: Waiting for your information to begin implementation

