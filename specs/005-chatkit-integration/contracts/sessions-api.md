# API Contract: ChatKit Sessions Endpoint

**Endpoint**: `POST /api/chatkit/sessions`
**Description**: Create a new ChatKit session for secure frontend authentication
**Version**: 1.0
**Status**: Ready for Implementation

---

## Request

### HTTP Method & Path
```
POST /api/chatkit/sessions
```

### Headers
```
Content-Type: application/json
Authorization: Bearer <jwt_token> (Optional in Phase 3a, Required in Phase 3b)
```

### Request Body
**Empty body (no parameters required)**

```json
{}
```

**Alternative** (for future user association):
```json
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

---

## Success Response

### HTTP Status
```
200 OK
```

### Response Body
```json
{
  "status": "success",
  "data": {
    "client_secret": "cs_live_abc123def456ghi789jkl012",
    "session_id": "ses_abc123def456ghi789jkl012"
  }
}
```

### Response Headers
```
Content-Type: application/json
```

---

## Error Responses

### 400 Bad Request
**Cause**: Invalid request format or missing required fields

```json
{
  "status": "error",
  "message": "Invalid request body"
}
```

### 401 Unauthorized
**Cause**: Missing or invalid OpenAI API key

```json
{
  "status": "error",
  "message": "OpenAI authentication failed: Invalid API key"
}
```

### 500 Internal Server Error
**Cause**: Server misconfiguration or OpenAI service failure

```json
{
  "status": "error",
  "message": "OpenAI service error: Could not create session"
}
```

**Specific cases**:

**Missing OPENAI_API_KEY**
```json
{
  "status": "error",
  "message": "OpenAI API key not configured"
}
```

**Missing CHATKIT_WORKFLOW_ID**
```json
{
  "status": "error",
  "message": "ChatKit workflow not configured"
}
```

**OpenAI API Timeout**
```json
{
  "status": "error",
  "message": "OpenAI service temporarily unavailable"
}
```

**OpenAI Rate Limited**
```json
{
  "status": "error",
  "message": "Rate limited by OpenAI. Please try again in a moment."
}
```

---

## HTTP Status Code Reference

| Status | Meaning | Cause |
|--------|---------|-------|
| 200 | Session created successfully | Normal operation |
| 400 | Bad request | Invalid JSON or missing fields |
| 401 | Unauthorized | Invalid OpenAI API key |
| 429 | Too many requests | Rate limit exceeded |
| 500 | Internal server error | Server or OpenAI service error |
| 503 | Service unavailable | OpenAI API down |

---

## Examples

### Example 1: Successful Session Creation

**Request**:
```bash
curl -X POST http://localhost:8000/api/chatkit/sessions \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Response** (200 OK):
```json
{
  "status": "success",
  "data": {
    "client_secret": "cs_live_8a7b6c5d4e3f2g1h0i9j8k7l6m5n4o3p",
    "session_id": "ses_9z8y7x6w5v4u3t2s1r0q9p8o7n6m5l4k"
  }
}
```

### Example 2: Invalid API Key

**Request**:
```bash
curl -X POST http://localhost:8000/api/chatkit/sessions \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Response** (401 Unauthorized):
```json
{
  "status": "error",
  "message": "OpenAI authentication failed: Invalid API key"
}
```

**Browser console**:
```javascript
Error: Failed to get ChatKit session: Unauthorized
```

### Example 3: Service Unavailable

**Request**:
```bash
curl -X POST http://localhost:8000/api/chatkit/sessions \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Response** (503 Service Unavailable):
```json
{
  "status": "error",
  "message": "OpenAI service temporarily unavailable"
}
```

**Browser shows**: "Service temporarily down. Please try again."

---

## Implementation Notes

### Backend (FastAPI)

```python
from fastapi import APIRouter, Request, HTTPException
from openai import OpenAI

router = APIRouter()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@router.post("/sessions")
async def create_chatkit_session(request: Request):
    """Create ChatKit session and return client_secret for frontend"""

    # Validate configuration
    api_key = os.getenv("OPENAI_API_KEY")
    workflow_id = os.getenv("CHATKIT_WORKFLOW_ID")

    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="OpenAI API key not configured"
        )

    if not workflow_id:
        raise HTTPException(
            status_code=500,
            detail="ChatKit workflow not configured"
        )

    try:
        # Create session using OpenAI SDK
        session = client.chatkit.sessions.create(
            workflow={"id": workflow_id}
        )

        return {
            "status": "success",
            "data": {
                "client_secret": session.client_secret,
                "session_id": session.id
            }
        }

    except Exception as e:
        # Map OpenAI errors to HTTP status codes
        if "authentication" in str(e).lower():
            raise HTTPException(status_code=401, detail="OpenAI authentication failed")
        elif "rate_limit" in str(e).lower():
            raise HTTPException(status_code=429, detail="Rate limited by OpenAI")
        elif "timeout" in str(e).lower():
            raise HTTPException(status_code=503, detail="OpenAI service unavailable")
        else:
            raise HTTPException(status_code=500, detail="OpenAI service error")
```

### Frontend (Next.js/TypeScript)

```typescript
async function getClientSecret(existing?: string): Promise<string> {
  // Reuse existing if available
  if (existing) {
    console.log('Reusing existing ChatKit client secret')
    return existing
  }

  try {
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/chatkit/sessions`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    })

    if (!response.ok) {
      const error = await response.json()
      console.error('Session creation failed:', error.message)
      throw new Error(`Failed to get ChatKit session: ${error.message}`)
    }

    const data = await response.json()
    console.log('Got ChatKit session:', data.data.session_id)

    return data.data.client_secret
  } catch (error) {
    console.error('Error getting ChatKit session:', error)
    throw error
  }
}
```

---

## Testing

### Unit Test: Session Creation

```python
def test_create_chatkit_session_success(client):
    """Test successful session creation"""
    response = client.post("/api/chatkit/sessions")

    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert "client_secret" in response.json()["data"]
    assert "session_id" in response.json()["data"]
```

### Integration Test: Frontend → Backend → OpenAI

```python
def test_full_flow():
    """Test: Frontend calls backend → backend calls OpenAI → session created"""
    # 1. Frontend makes request
    response = client.post("/api/chatkit/sessions")

    # 2. Verify success
    assert response.status_code == 200
    data = response.json()["data"]

    # 3. Verify response format
    assert data["client_secret"].startswith("cs_")
    assert data["session_id"].startswith("ses_")

    # 4. Verify can be used by ChatKit
    config = {
        "api": {
            "getClientSecret": lambda: data["client_secret"]
        }
    }
    assert config["api"]["getClientSecret"]() == data["client_secret"]
```

---

## Security Considerations

1. **Never expose workflow ID to frontend**
   - ✅ Hardcoded in backend .env
   - ✅ Not included in response

2. **Never expose API key to frontend**
   - ✅ Only used on backend
   - ✅ Frontend makes request without key

3. **client_secret is sensitive**
   - ⚠️ Returned to frontend (required by ChatKit)
   - ⚠️ Not logged in production
   - ✅ Used only for ChatKit authentication

4. **session_id for audit logging only**
   - ✅ Tracked on backend
   - ✅ Not exposed to frontend

---

## Rate Limiting & Throttling

**Phase 3a** (Current):
- No rate limiting
- Each request creates a new session
- OpenAI API handles rate limiting (429 responses)

**Phase 3b** (Future):
- Consider rate limiting per user
- Cache sessions per user (reuse within time window)
- Add request throttling middleware

---

## Versioning

**Current Version**: 1.0

**Future Breaking Changes** would require:
- Version in URL: `/api/v2/chatkit/sessions`
- Backward compatibility period
- Migration guide

---

**Last Updated**: December 20, 2025
**Status**: Ready for Implementation
**Related**: [ChatKit Config Contract](./chatkit-config.md)
