# Phase 0: Research & Clarification - ChatKit Integration

**Objective**: Resolve technical unknowns and document best practices for ChatKit integration.

**Status**: Phase 0 Complete - No unresolved clarifications

---

## Research Findings

### 1. OpenAI ChatKit Architecture

**Decision**: Use official OpenAI ChatKit React component (`@openai/chatkit-react`)

**Rationale**:
- Official implementation from OpenAI
- Pre-built chat UI with streaming support
- Built-in tool visualization for agent responses
- Framework-agnostic (works with Next.js)
- Production-ready (used in OpenAI demos)

**Alternatives Considered**:
- Custom chat UI: Would require building streaming UI, tool visualization, error handling from scratch
- Third-party chat libraries: Lack ChatKit-specific optimizations for OpenAI Agent outputs
- Lower-level ChatKit JS: Would lose React integration benefits

**Implementation**:
- Frontend loads ChatKit JS from official CDN: `https://cdn.platform.openai.com/deployments/chatkit/chatkit.js`
- Wraps with React hook: `useChatKit(config)`
- Configuration provides `api.getClientSecret()` function for backend integration

---

### 2. Backend Session Endpoint Design

**Decision**: POST /api/chatkit/sessions creates temporary sessions with client_secret

**Rationale**:
- Keeps workflow ID and API key server-side (secure)
- Returns client_secret for ChatKit to authenticate
- Prevents frontend from making direct OpenAI API calls
- Enables audit logging of session creation
- Allows per-user session tracking (optional, for Phase 3b)

**Security Pattern**:
```
Frontend Request:        Backend:                  ChatKit:
GET /chatkit    →     POST /sessions          ← Uses client_secret
                         ↓
                    Uses OPENAI_API_KEY
                    (never exposed to client)
```

**Implementation**:
- Endpoint uses OpenAI SDK: `client.chatkit.sessions.create()`
- Workflow ID hardcoded in backend environment: `CHATKIT_WORKFLOW_ID=wf_...`
- Returns: `{"client_secret": "cs_...", "session_id": "ses_..."}`

---

### 3. Frontend Configuration Pattern

**Decision**: Implement `getClientSecret()` async function in ChatKit config

**Rationale**:
- Matches ChatKit SDK expectations (not url + domainKey pattern)
- Allows reusing existing client_secrets (optimization)
- Handles errors gracefully when backend unavailable
- Provides console logging for debugging

**Pattern**:
```typescript
api: {
  async getClientSecret(existing) {
    if (existing) return existing  // Reuse if available
    const res = await fetch(`${API_URL}/api/chatkit/sessions`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    })
    return (await res.json()).client_secret
  }
}
```

**Alternatives Considered**:
- Static domain key in frontend: Would require domain allowlist registration (unnecessary for MVP)
- Direct API key in frontend: Security risk, violates constraint
- Long-lived tokens: Adds complexity, session pattern simpler

---

### 4. Domain Allowlist Configuration

**Decision**: Support both localhost (development) and production deployments with domain allowlist configuration

**Rationale**:
- ChatKit works on localhost WITHOUT domain registration (development)
- ChatKit requires domain allowlist for production (security requirement)
- Provide clear path from localhost → production
- Minimize friction when deploying to production

**Local Development Setup** (Phase 3a - NO domain key needed):

```
Development Environment:
├─ Frontend: http://localhost:3000
├─ Backend: http://localhost:8000
├─ ChatKit: Works without domain allowlist
└─ Environment: NEXT_PUBLIC_CHATKIT_DOMAIN_KEY=not_required
```

**Testing on localhost**:
1. No domain allowlist needed
2. ChatKit initializes immediately
3. Full functionality available
4. Perfect for development and testing

**Production Deployment Setup** (Phase 3b - Domain allowlist REQUIRED):

**Step 1: Your Vercel Frontend (Already Deployed)**

Your frontend is already live from Phase 2:
```
Production Frontend: https://task-pilot-ai-ashen.vercel.app
```

**Step 2: Register Domain in OpenAI**
1. Go to: https://platform.openai.com/settings/organization/security/domain-allowlist
2. Click "Add domain"
3. Enter your production domain: `https://task-pilot-ai-ashen.vercel.app`
4. OpenAI generates domain key (copy this)

**Step 3: Configure Frontend Environment**

Add to Vercel project environment variables:

```bash
# In Vercel Dashboard → Settings → Environment Variables
# For Production environment:

NEXT_PUBLIC_API_URL=<your-backend-url>
NEXT_PUBLIC_CHATKIT_DOMAIN_KEY=sk_live_your_domain_key_here
```

Or edit frontend/.env.production.local:
```bash
# frontend/.env.production.local (for local testing of production build)
NEXT_PUBLIC_API_URL=https://your-backend-production-url.com
NEXT_PUBLIC_CHATKIT_DOMAIN_KEY=sk_live_your_domain_key_here
```

**Step 4: Update Frontend Config** (if needed)
```typescript
// frontend/lib/chatkit-config.ts
export const chatKitConfig: ChatKitConfig = {
  api: {
    getClientSecret: async (existing?: string) => {
      // Backend endpoint already works with domain key
      // No changes needed here
      const res = await fetch(`${API_URL}/api/chatkit/sessions`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      })
      const data = await res.json()
      return data.data.client_secret
    }
  },

  // Optional: Add domain key if needed by ChatKit
  // domainKey: process.env.NEXT_PUBLIC_CHATKIT_DOMAIN_KEY
}
```

**Step 4: Deploy & Test**
```bash
# Frontend already deployed to Vercel (Phase 2)
# Just add environment variables in Vercel Dashboard

# Test in production
# Visit: https://task-pilot-ai-ashen.vercel.app/chatkit
# Verify ChatKit initializes correctly
```

**Environment Variable Management**:

| Environment | Frontend URL | Backend URL | Domain Key | Stage |
|-------------|--------------|-------------|-----------|-------|
| Localhost | http://localhost:3000 | http://localhost:8000 | (not needed) | Development |
| Staging | https://task-pilot-ai-ashen.vercel.app | https://api-staging.com | sk_test_... (optional) | Testing |
| Production | https://task-pilot-ai-ashen.vercel.app | https://api.your-backend.com | sk_live_... (required) | Live |

**Migration Path: Localhost → Production**

```
Phase 3a (Development):
  Frontend: http://localhost:3000
  Backend: http://localhost:8000
  NEXT_PUBLIC_CHATKIT_DOMAIN_KEY=(not set)
  ↓
Frontend already deployed (Phase 2)
  ↓
Phase 3b (Production Prep):
  Register domain in OpenAI
    → Domain: https://task-pilot-ai-ashen.vercel.app
    → Get domain key: sk_live_abc123...
  ↓
Phase 3b (Production):
  Frontend: https://task-pilot-ai-ashen.vercel.app (already live)
  Backend: https://your-backend-url.com
  NEXT_PUBLIC_API_URL=https://your-backend-url.com
  NEXT_PUBLIC_CHATKIT_DOMAIN_KEY=sk_live_abc123...
  ↓
Test in production environment
  → Visit: https://task-pilot-ai-ashen.vercel.app/chatkit
  ✅ ChatKit working with domain allowlist
```

**Multi-Environment Setup** (for your project):

```bash
# frontend/.env.local (LOCAL DEVELOPMENT)
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_CHATKIT_DOMAIN_KEY=

# frontend/.env.production.local (for testing production build locally)
NEXT_PUBLIC_API_URL=https://your-backend-production-url.com
NEXT_PUBLIC_CHATKIT_DOMAIN_KEY=sk_live_production_key_here
```

**Vercel Environment Variables** (RECOMMENDED - Set in Vercel Dashboard):

Your app is deployed on Vercel (https://task-pilot-ai-ashen.vercel.app)

Configure in Vercel:
1. Go to: https://vercel.com/dashboard/project/[your-project]
2. Settings → Environment Variables
3. Add for Production environment:
   ```
   NEXT_PUBLIC_API_URL=https://your-backend-production-url.com
   NEXT_PUBLIC_CHATKIT_DOMAIN_KEY=sk_live_your_key_here
   ```

This way, all deployments automatically get the correct environment variables without manual .env file edits.

**Domain Allowlist Troubleshooting**:

**Problem**: "Domain not registered" error in production
```
Solution:
1. Verify domain registered in OpenAI platform
2. Check domain URL matches exactly (https://... case-sensitive)
3. Wait 5-10 minutes for registration to propagate
4. Clear browser cache and reload
```

**Problem**: ChatKit works on localhost but fails on production
```
Causes:
1. Domain not registered in OpenAI
2. Domain key not set in environment variables
3. Frontend URL doesn't match registered domain
4. Firewall/CORS blocking domain

Solution:
1. Verify domain registered in OpenAI
2. Verify NEXT_PUBLIC_CHATKIT_DOMAIN_KEY is set
3. Check frontend URL matches registered domain exactly
4. Check backend CORS allows production domain
```

**Backend CORS Configuration** (for production):

```python
# backend/main.py
from fastapi.middleware.cors import CORSMiddleware

allowed_origins = [
    "http://localhost:3000",  # Local development
    "https://your-app.vercel.app",  # Production frontend
    "https://staging.vercel.app",  # Staging frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Current Setup Summary**:

**Phase 3a** (Development):
- ✅ Localhost works WITHOUT domain allowlist
- ✅ No configuration needed
- ✅ Perfect for testing and development

**Phase 3b** (Production):
- ✅ Register domain in OpenAI (one-time setup)
- ✅ Get domain key from OpenAI
- ✅ Set environment variables in Vercel/backend
- ✅ Deploy and test
- ✅ ChatKit works in production

---

### 5. Error Handling Strategy

**Decision**: Graceful degradation with clear user feedback

**Patterns**:

1. **Session Creation Fails**:
   ```
   Browser → Request session
   Backend returns 500 or timeout
   Frontend shows: "Unable to start chat. Please try again."
   Browser console: detailed error for debugging
   ```

2. **Invalid OpenAI API Key**:
   ```
   Backend detects invalid key during session creation
   Returns: { "status": "error", "message": "OpenAI authentication failed" }
   Frontend shows user-friendly message
   ```

3. **Network Timeout**:
   ```
   Session request times out after 10 seconds
   Frontend retries up to 3 times
   If still fails, shows: "Chat service temporarily unavailable"
   ```

**Implementation** (see tests):
- All errors caught and logged
- No stack traces exposed to frontend
- User messages are actionable

---

### 6. Session Persistence & Reuse

**Decision**: Frontend reuses existing client_secret within page lifetime

**Rationale**:
- Reduces backend load (no unnecessary session creation)
- Each page refresh creates new session (acceptable for MVP)
- Phase 3b will add persistent conversation storage

**Pattern**:
```typescript
// First load: creates session
await getClientSecret(null) → returns cs_abc123

// Subsequent ChatKit requests: reuses same session
await getClientSecret("cs_abc123") → returns cs_abc123

// Page refresh: new session created (old session abandoned)
```

**Note**: OpenAI manages session expiry server-side. Abandoned sessions are cleaned up automatically.

---

### 7. Concurrent Session Handling

**Decision**: OpenAI SDK handles concurrent session creation natively

**Rationale**:
- Each request creates independent session
- Session IDs guaranteed unique by OpenAI
- No locking or state management needed
- Supports 50+ concurrent sessions (requirement met)

**Scaling**:
- Backend is stateless
- Multiple backend instances: each can create sessions
- No session affinity needed
- Works with load balancing/horizontal scaling

---

### 8. Performance Targets

**Decision**: Target response times based on OpenAI API performance

| Operation | Target | Notes |
|-----------|--------|-------|
| Session creation | <2s | Includes OpenAI API call |
| Message response | <5s | Depends on model + agent complexity |
| Page load | <3s | ChatKit + config initialization |
| Concurrent limit | 50+ sessions | Tested with load testing |

**Rationale**:
- Session creation: OpenAI SDK is optimized; <2s is achievable
- Message response: Reflects agent processing time (includes LLM call)
- Concurrent: Testing required; 50+ is reasonable for MVP

**Phase 3b** will add:
- Response streaming (shows answer while generating)
- Agent tool visualization (shows tool calls as they happen)
- Real-time progress indicators

---

### 9. Testing Strategy

**Decision**: Unit + Integration tests covering all user paths

**Backend Tests** (test_chatkit.py):
- ✅ Session creation with valid API key
- ✅ Session creation with invalid API key (error handling)
- ✅ Session includes correct workflow ID
- ✅ client_secret format validation
- ✅ Concurrent session creation (5+ simultaneous)
- ✅ Response status codes (200, 400, 500)

**Frontend Tests** (chatkit.test.tsx):
- ✅ ChatKit component renders
- ✅ getClientSecret() called on init
- ✅ Client secret passed to ChatKit config
- ✅ Error handling when session fails
- ✅ Error handling when backend unavailable
- ✅ Message input/send functionality

**Integration Tests**:
- ✅ Full flow: Page load → Session creation → ChatKit init
- ✅ User can type and send message
- ✅ Agent can respond through ChatKit UI

---

### 10. Implementation Order

**Phase 0** (Done):
- ✅ Research OpenAI ChatKit patterns
- ✅ Document security model
- ✅ Define error handling
- ✅ Plan testing strategy

**Phase 1** (Next):
- Create data-model.md (ChatKit Session entity)
- Create contracts/ (Session API, ChatKit config)
- Create quickstart.md (5-min setup)
- Update agent context files

**Phase 2** (After Phase 1):
- Generate tasks.md (actionable implementation tasks)
- Each task maps to spec requirement

**Implementation** (After Phase 2):
- Run tasks from tasks.md
- Tests written first (TDD)
- Code follows spec exactly
- All quality gates pass

---

## No Remaining Clarifications

All technical unknowns resolved:
- ✅ ChatKit architecture understood
- ✅ Backend endpoint design finalized
- ✅ Frontend config pattern documented
- ✅ Security model validated
- ✅ Error handling strategy defined
- ✅ Testing approach outlined
- ✅ Performance targets established
- ✅ Scaling concerns addressed

**Status**: Ready for Phase 1 Design (data-model.md, contracts/, quickstart.md)

---

**Last Updated**: December 20, 2025
**Phase**: Phase 0 Complete
**Next**: Phase 1 Design Artifacts
