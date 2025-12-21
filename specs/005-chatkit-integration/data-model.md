# Phase 1: Data Model - ChatKit Integration

**Objective**: Define entities, fields, relationships, and validation rules for ChatKit integration.

**Status**: Phase 1 Complete - Ready for contracts/

---

## Entity: ChatKit Session

ChatKit sessions are temporary credentials issued by OpenAI for frontend authentication to a specific agent workflow.

### Fields

| Field | Type | Required | Constraints | Notes |
|-------|------|----------|-------------|-------|
| `session_id` | string | Yes | Unique, immutable | Issued by OpenAI API |
| `client_secret` | string | Yes | Unique, immutable | Used by ChatKit JS to authenticate |
| `workflow_id` | string | Yes | Constant value | `wf_6946b383d368819081b556e6e5fa66330d48d0c9ea4fccd8` |
| `user_id` | string | Optional | Foreign key to users.id | Authenticated user who created session (Phase 3b) |
| `created_at` | ISO 8601 | Yes | Auto-set, immutable | Timestamp when session created |
| `expires_at` | ISO 8601 | Yes | Auto-set | Session expiry time (set by OpenAI SDK) |
| `status` | enum | Yes | active, expired | Current session state |

### Example

```json
{
  "session_id": "ses_abc123def456",
  "client_secret": "cs_xyz789uvw012",
  "workflow_id": "wf_6946b383d368819081b556e6e5fa66330d48d0c9ea4fccd8",
  "user_id": "user_123",
  "created_at": "2025-12-20T10:30:00Z",
  "expires_at": "2025-12-21T10:30:00Z",
  "status": "active"
}
```

### Validation Rules

1. **session_id**
   - Pattern: `ses_[a-zA-Z0-9]{20,}`
   - Never exposed to frontend
   - Only used for backend audit logging

2. **client_secret**
   - Pattern: `cs_[a-zA-Z0-9]{20,}`
   - Returned to frontend for ChatKit initialization
   - Not logged (sensitive)

3. **workflow_id**
   - Must be: `wf_6946b383d368819081b556e6e5fa66330d48d0c9ea4fccd8`
   - Hardcoded in backend .env
   - Never exposed to frontend

4. **user_id** (Optional)
   - Valid UUID format (if provided)
   - Must exist in users table
   - Allows per-user session tracking (future)

5. **created_at, expires_at**
   - ISO 8601 format with timezone
   - expires_at always >= created_at
   - created_at immutable after creation

6. **status**
   - Values: `active`, `expired`
   - Transient (not persisted in current design)
   - Determined by comparing current time vs expires_at

---

## Relationships

### Session → Workflow (1:1)

Each session connects to exactly one workflow.

```
ChatKit Session
    ↓
Workflow (wf_6946b383d368819081b556e6e5fa66330d48d0c9ea4fccd8)
    ↓
OpenAI Agent with task tools
```

### Session → User (N:1, Phase 3b)

Many sessions per user; each session created by one user.

```
User
    ├── Session 1 (created 2025-12-20 10:00)
    ├── Session 2 (created 2025-12-20 11:00)
    └── Session 3 (created 2025-12-20 12:00)
```

**Current State** (Phase 3a): user_id is optional/null
**Phase 3b**: Will require user_id for all sessions

---

## State Transitions

### Session Lifecycle

```
[Created]
   ↓
[Active] ← Valid for API calls
   ↓
[Expired] ← No longer valid (time-based expiry)
```

**Timeline**:
- Created: When backend calls `client.chatkit.sessions.create()`
- Expires: After duration set by OpenAI (typically 24-48 hours)
- Cleanup: OpenAI cleans up expired sessions server-side

---

## Storage Model (Phase 3a vs 3b)

### Current (Phase 3a)

**In-Memory/Transient**: Not stored to database
- Created on request
- Returned to frontend
- Discarded after use
- Perfect for stateless architecture

**Rationale**:
- Phase 3a focuses on ChatKit UI integration
- No conversation history yet
- Simplifies implementation
- Each page load gets fresh session

### Future (Phase 3b)

**Persistent Storage**: Will add to PostgreSQL

```sql
CREATE TABLE chatkit_sessions (
  id SERIAL PRIMARY KEY,
  session_id VARCHAR(255) UNIQUE NOT NULL,
  client_secret VARCHAR(255) NOT NULL,
  workflow_id VARCHAR(255) NOT NULL,
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  expires_at TIMESTAMP NOT NULL,
  status VARCHAR(50) DEFAULT 'active',

  CONSTRAINT valid_expiry CHECK (expires_at >= created_at)
);

CREATE INDEX idx_sessions_user_id ON chatkit_sessions(user_id);
CREATE INDEX idx_sessions_status ON chatkit_sessions(status);
```

---

## API Response Format

### Success Response

```json
{
  "status": "success",
  "data": {
    "client_secret": "cs_...",
    "session_id": "ses_..."
  }
}
```

### Error Response

```json
{
  "status": "error",
  "message": "Session creation failed: Invalid OpenAI API key"
}
```

---

## Validation & Constraints

### Backend Validation (POST /api/chatkit/sessions)

1. **API Key Validation**
   - OPENAI_API_KEY must be valid and set
   - Return 401 if missing
   - Return 400 if invalid format

2. **Workflow ID Validation**
   - CHATKIT_WORKFLOW_ID must be set
   - Must match expected value: `wf_6946b383d368819081b556e6e5fa66330d48d0c9ea4fccd8`
   - Return 500 if not configured

3. **OpenAI API Call**
   - Handle rate limiting (429)
   - Handle service unavailable (503)
   - Handle authentication errors (401)
   - Timeout after 10 seconds

4. **Response Validation**
   - session_id must be non-empty
   - client_secret must be non-empty
   - Both must follow expected patterns

### Frontend Validation (ChatKit Config)

1. **Response Status Check**
   - HTTP 200-299: Extract client_secret
   - HTTP 4xx/5xx: Show error message

2. **Secret Format Check**
   - Must be non-empty string
   - Should start with "cs_"
   - Pass to ChatKit component

---

## Error Scenarios

### Scenario 1: Invalid OpenAI API Key

```
User opens ChatKit page
Frontend calls: POST /api/chatkit/sessions
Backend checks: OPENAI_API_KEY
Result: Invalid or expired key
Response: { "status": "error", "message": "OpenAI authentication failed" }
Frontend shows: "Unable to start chat. Please check configuration."
Browser console: Detailed error for debugging
```

### Scenario 2: Workflow ID Not Configured

```
Backend missing: CHATKIT_WORKFLOW_ID env var
Response: { "status": "error", "message": "Server not configured for ChatKit" }
Frontend shows: "Chat service not available"
Backend logs: Critical configuration error
```

### Scenario 3: OpenAI Service Unavailable

```
POST request to OpenAI API times out
Backend catches timeout exception
Response: { "status": "error", "message": "OpenAI service temporarily unavailable" }
Frontend shows: "Service temporarily down. Try again in a moment."
User can retry
```

### Scenario 4: Network Failure

```
Frontend unable to reach backend
Fetch fails with network error
Frontend shows: "Network connection lost"
Provides manual retry button
```

---

## Size & Performance Estimates

| Metric | Value | Notes |
|--------|-------|-------|
| Session ID length | ~30-50 chars | Varies by OpenAI format |
| Client secret length | ~30-50 chars | Varies by OpenAI format |
| Session creation time | <2 seconds | Includes OpenAI API latency |
| Session lifetime | 24-48 hours | Set by OpenAI (varies) |
| Concurrent sessions | 50+ | No server-side limit |
| Memory per session | <1 KB | Minimal data, no storage in Phase 3a |

---

## Backward Compatibility

**Phase 3a** (Current):
- Sessions are transient
- Not stored in database
- No migration needed

**Phase 3b** (Future):
- Add persistent storage
- Migration: Create chatkit_sessions table
- Backward compatible: Old transient sessions abandoned

---

## Implementation Checklist

- [ ] Backend: POST /api/chatkit/sessions endpoint
  - [ ] Validates OPENAI_API_KEY
  - [ ] Validates CHATKIT_WORKFLOW_ID
  - [ ] Calls OpenAI SDK: `client.chatkit.sessions.create()`
  - [ ] Returns: { "client_secret": "...", "session_id": "..." }
  - [ ] Handles all error scenarios

- [ ] Frontend: getClientSecret() function
  - [ ] Called by ChatKit hook on initialization
  - [ ] Makes POST request to backend
  - [ ] Extracts client_secret from response
  - [ ] Handles errors gracefully
  - [ ] Returns secret to ChatKit component

- [ ] Tests
  - [ ] Backend: Session creation happy path
  - [ ] Backend: Error scenarios (invalid key, missing config, etc.)
  - [ ] Frontend: Successful session retrieval
  - [ ] Frontend: Error handling when backend fails
  - [ ] Integration: Full page load → session → ChatKit init

---

**Last Updated**: December 20, 2025
**Phase**: Phase 1 Complete
**Next**: Create contracts/ API specifications
