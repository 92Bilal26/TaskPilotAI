# ChatKit Endpoints - Clarification

## Architecture Overview

```
User Browser (Frontend)
    ↓
    ├─ Chat Page: Uses /api/{user_id}/chat endpoint
    │    (Generic chat interface, not ChatKit)
    │
    └─ ChatKit Widget: Uses OpenAI ChatKit SDK
         ↓
         ChatKit Protocol (WebSocket/HTTP)
         ↓
         /api/v1/chatkit/sessions endpoint
         ↓
         MyChatKitServer (ChatKit Server implementation)
         ↓
         Agents SDK + MCP Tools
```

## Endpoint Comparison

### 1. `/api/{user_id}/chat` - Generic Chat API
**File**: `backend/routes/chat.py`
**Purpose**: Generic chat message endpoint
**Used By**: Regular chat page/interface
**Features**:
- Simple request/response pattern
- Single message processing
- Returns: response, tool_calls, conversation_id
- Not ChatKit-specific

**Test Command**:
```bash
curl -X POST http://localhost:8000/api/{user_id}/chat \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"content":"Your message here"}'
```

---

### 2. `/api/v1/chatkit/sessions` - ChatKit UI Server
**File**: `backend/routes/chatkit.py`
**Purpose**: OpenAI ChatKit SDK integration
**Used By**: ChatKit UI widget (frontend)
**Features**:
- Creates ChatKit session with client_secret
- Returns session_id, conversation_id
- Frontend SDK uses these credentials
- Implements ChatKitServer interface
- Handles streaming responses

**Test Command**:
```bash
curl -X POST http://localhost:8000/api/v1/chatkit/sessions \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json"
```

---

## Which One Is ChatKit UI?

**Answer**: `/api/v1/chatkit/sessions`

### Why?
1. **ChatKit SDK Integration**: Implements OpenAI ChatKit's ChatKitServer interface
2. **Session-based**: Returns session credentials for frontend SDK
3. **Streaming Support**: Handles async message processing
4. **Real-time Chat**: Used by ChatKit widget component
5. **Frontend WebSocket**: ChatKit SDK communicates via secure protocol

---

## Testing Flow

### Step 1: Create ChatKit Session
```bash
POST /api/v1/chatkit/sessions
Authorization: Bearer <JWT>
Response:
{
  "session_id": "...",
  "conversation_id": 123,
  "client_secret": "..."
}
```

### Step 2: Frontend Gets Session Credentials
Frontend receives session_id, conversation_id, client_secret

### Step 3: Frontend Initializes ChatKit SDK
```javascript
const chatkit = new ChatKit({
  clientSecret: response.client_secret,
  sessionId: response.session_id,
  // ... other config
});
```

### Step 4: User Sends Message
ChatKit SDK sends message to MyChatKitServer.respond()

### Step 5: Backend Processes Message
- Extracts user message
- Calls Agents SDK with MCP tools
- Agent invokes tools (add_task, list_tasks, etc.)
- Returns response with tool confirmations

---

## Summary

| Aspect | `/api/{user_id}/chat` | `/api/v1/chatkit/sessions` |
|--------|----------------------|---------------------------|
| **Purpose** | Generic chat API | ChatKit UI integration |
| **SDK** | Custom | OpenAI ChatKit SDK |
| **Type** | Request/Response | Session-based streaming |
| **Frontend** | Regular chat page | ChatKit widget |
| **Message Flow** | Direct HTTP | ChatKit protocol |
| **Real-time** | No | Yes (via SDK) |
| **Streaming** | No | Yes |
| **Tool Calls** | Via agent | Via ChatKit server |

---

## For ChatKit UI Testing (Frontend)

Use the **`/api/v1/chatkit/sessions`** endpoint:
1. ✅ Creates ChatKit session
2. ✅ Returns credentials for frontend SDK
3. ✅ Frontend SDK handles all message streaming
4. ✅ Backend processes messages via MyChatKitServer

---

## For Generic Chat Testing

Use the **`/api/{user_id}/chat`** endpoint:
1. Simple HTTP request/response
2. Good for testing agent directly
3. No ChatKit SDK required

