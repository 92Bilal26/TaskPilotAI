# ChatKit Setup for Render Backend

**Status**: Phase 3 ChatKit integration requires specific configuration on Render

---

## Environment Variables for Render

Add these to your Render backend dashboard under **Environment** → **Environment Variables**:

### Required Variables

| Variable | Value | Notes |
|----------|-------|-------|
| `OPENAI_API_KEY` | `sk-proj-xxxxxxxxxxxxx` | Get from https://platform.openai.com/account/api-keys (Required for Agents SDK) |

### Optional Variables (Pre-configured in backend)

| Variable | Default Value | Purpose |
|----------|---------------|---------|
| `CHATKIT_ENABLED` | `True` | Enable/disable ChatKit feature |
| `CHATKIT_SESSION_TIMEOUT` | `3600` | Session timeout in seconds (1 hour) |
| `CHATKIT_MAX_HISTORY` | `10` | Max conversation history to send to agent |
| `DATABASE_URL` | `sqlite:///./taskpilot.db` | PostgreSQL connection (if using cloud DB) |

### Already Configured (in config.py - No Action Needed)

```python
# Domain Allowlist - Vercel frontend domain is already allowed
CHATKIT_DOMAIN_ALLOWLIST: List[str] = [
    "localhost:3000",
    "localhost:8000",
    "127.0.0.1:3000",
    "task-pilot-ai-ashen.vercel.app",  # ✅ Vercel frontend
    "taskpilot-api-5l18.onrender.com"  # ✅ Render backend
]

# CORS Origins - Vercel domain is already allowed
CORS_ORIGINS: List[str] = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1:3000",
    "https://task-pilot-ai-ashen.vercel.app",  # ✅ Vercel frontend
    "https://taskpilot-api-5l18.onrender.com"  # ✅ Render backend
]

# ChatKit Server Configuration
CHATKIT_ENABLED: bool = True
CHATKIT_SESSION_TIMEOUT: int = 3600  # 1 hour
CHATKIT_MAX_HISTORY: int = 10
```

---

## ChatKit API Routes

Your Render backend exposes these ChatKit endpoints:

### 1. Create ChatKit Session
```
POST /api/v1/chatkit/sessions
```

**Purpose**: Initialize a new ChatKit session for conversation persistence

**Headers Required**:
```
Authorization: Bearer <jwt_token>
Origin: https://task-pilot-ai-ashen.vercel.app
```

**Response**:
```json
{
  "client_secret": "session-uuid",
  "session_id": "ses-uuid",
  "conversation_id": 123
}
```

**What it does**:
- ✅ Validates user authentication (JWT token)
- ✅ Validates origin domain against CHATKIT_DOMAIN_ALLOWLIST
- ✅ Creates a new conversation in database
- ✅ Links ChatKit session to database conversation for persistence
- ✅ Returns session credentials to frontend

---

### 2. ChatKit Protocol Endpoint
```
POST /api/v1/chatkit
```

**Purpose**: Handle ChatKit protocol requests (messages, responses, streaming)

**Headers Required**:
```
Authorization: Bearer <jwt_token>
Origin: https://task-pilot-ai-ashen.vercel.app
Content-Type: application/json
```

**What it does**:
- ✅ Validates user authentication (JWT token)
- ✅ Validates origin domain against CHATKIT_DOMAIN_ALLOWLIST
- ✅ Receives ChatKit protocol messages from frontend
- ✅ Processes through Agents SDK with MCP tools
- ✅ Returns streaming responses (Server-Sent Events)
- ✅ Persists conversation to database

**Response**:
- `text/event-stream` - Server-Sent Events for streaming responses
- Includes ChatKit protocol events (messages, tool calls, completions)

---

## How It Works (Request Flow)

```
1. Frontend (Vercel) creates session
   ↓
2. POST /api/v1/chatkit/sessions
   ├─ JWT validation ✅
   ├─ Origin validation ✅
   ├─ Create conversation ✅
   └─ Return client_secret

3. Frontend sends user message
   ↓
4. POST /api/v1/chatkit (with ChatKit protocol message)
   ├─ JWT validation ✅
   ├─ Origin validation ✅
   ├─ Extract user_id from JWT
   ├─ Load conversation history
   ├─ Call Agents SDK with MCP tools
   ├─ Tools inject user_id (user isolation)
   ├─ Stream response events
   └─ Persist messages to database

5. Response streams to frontend
   ├─ User message saved
   ├─ Tool calls executed
   ├─ AI response generated
   └─ All saved to conversation
```

---

## What Render Backend Provides

### Security Features
- ✅ **JWT Authentication**: Validates user identity
- ✅ **Domain Validation**: Blocks requests from unauthorized origins
- ✅ **User Isolation**: Tools receive user_id, tasks are per-user
- ✅ **Session Timeout**: Auto-expire sessions after 1 hour

### ChatKit Features
- ✅ **Session Persistence**: Conversations saved to database
- ✅ **Streaming Responses**: Real-time chat experience
- ✅ **Tool Integration**: 5 MCP tools (add_task, list_tasks, delete_task, complete_task, update_task)
- ✅ **Conversation History**: Full history available for context

### Databases & Persistence
- ✅ **PostgreSQL** (Neon) for production
- ✅ **SQLite** for local development
- ✅ Stores: Conversations, Messages, ChatKit Sessions

---

## Environment Variables Checklist

### Required (Add to Render)
- [ ] `OPENAI_API_KEY` = `sk-proj-xxxxxxxxxxxxx`

### Optional (Render already has defaults)
- [ ] `CHATKIT_SESSION_TIMEOUT` = `3600` (optional)
- [ ] `CHATKIT_MAX_HISTORY` = `10` (optional)

### Already Configured (No action needed)
- ✅ `CHATKIT_ENABLED` = `True`
- ✅ `CHATKIT_WORKFLOW_ID` = `wf_6946b383d368819081b556e6e5fa66330d48d0c9ea4fccd8`
- ✅ `CHATKIT_DOMAIN_ALLOWLIST` includes `task-pilot-ai-ashen.vercel.app`
- ✅ `CORS_ORIGINS` includes `https://task-pilot-ai-ashen.vercel.app`

---

## Step-by-Step Render Setup

### 1. Add OPENAI_API_KEY to Render
1. Go to https://dashboard.render.com
2. Click your **TaskPilotAI** service
3. Go to **Environment** tab
4. Click **Add Environment Variable**
5. Name: `OPENAI_API_KEY`
6. Value: `sk-proj-xxxxxxxxxxxxx` (from OpenAI dashboard)
7. Click **Save**

### 2. Verify Backend Health
```bash
curl https://taskpilot-api-5l18.onrender.com/health
# Should return: {"status":"ok","message":"TaskPilotAI API is running"}
```

### 3. Test ChatKit Session Creation
```bash
curl -X POST https://taskpilot-api-5l18.onrender.com/api/v1/chatkit/sessions \
  -H "Authorization: Bearer <your-jwt-token>" \
  -H "Origin: https://task-pilot-ai-ashen.vercel.app"

# Should return:
# {
#   "client_secret": "session-uuid",
#   "session_id": "ses-uuid",
#   "conversation_id": 123
# }
```

---

## Common Issues & Fixes

### Issue 1: "Domain not allowed" error
**Cause**: Origin header not matching CHATKIT_DOMAIN_ALLOWLIST

**Fix**:
1. Ensure frontend is at `https://task-pilot-ai-ashen.vercel.app`
2. Check Origin header is included
3. Domain is already in allowlist ✅

### Issue 2: "User not authenticated" error
**Cause**: JWT token missing or invalid

**Fix**:
1. Include `Authorization: Bearer <token>` header
2. Token must be valid (not expired)
3. Token must have `user_id` claim

### Issue 3: ChatKit sessions not persisting
**Cause**: Database not configured properly

**Fix**:
1. Check `DATABASE_URL` environment variable (if using cloud DB)
2. Verify database tables are created
3. Check database connection

---

## Testing the Integration

### Local Testing
```bash
# Terminal 1: Start backend
cd backend
uvicorn main:app --reload --port 8000

# Terminal 2: Start frontend
cd frontend
npm run dev

# Visit http://localhost:3000
# Sign in, click "💬 Open Chat"
# Create a task via ChatKit
# Task should appear in dashboard within 1 second
```

### Production Testing
```bash
# Visit https://task-pilot-ai-ashen.vercel.app
# Sign in with your account
# Click "💬 Open Chat" button
# Send message: "Add a task to buy groceries"
# Check that:
#   ✅ ChatKit responds
#   ✅ Task appears in dashboard
#   ✅ Task has correct user_id (user isolation)
```

---

## File References

- **Backend config**: `/backend/config.py` (lines 7-49)
- **ChatKit endpoints**: `/backend/routes/chatkit.py` (lines 655-793)
- **Domain validation**: `/backend/routes/chatkit.py` (lines 675-685, 758-768)
- **User isolation**: `/backend/routes/chatkit.py` (lines 264-330)

---

## Summary

### What YOU need to do in Render:
1. ✅ Add `OPENAI_API_KEY` environment variable
2. ✅ That's it! Everything else is pre-configured

### What's ALREADY done:
- ✅ ChatKit routes implemented (`/api/v1/chatkit/sessions` and `/api/v1/chatkit`)
- ✅ Domain allowlist configured (includes Vercel)
- ✅ CORS configured (includes Vercel)
- ✅ User isolation implemented
- ✅ Session persistence ready
- ✅ MCP tools integrated

### When it's all working:
- Frontend (Vercel) talks to Backend (Render)
- ChatKit sessions are created
- Messages are processed through Agents SDK
- MCP tools execute (per user)
- Conversations persist to database
- Tasks sync to dashboard in real-time ✨

---

**Last Updated**: December 25, 2025
**Phase**: 3 - ChatKit Integration
**Status**: Ready for production deployment
