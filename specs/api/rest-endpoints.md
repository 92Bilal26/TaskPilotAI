# REST API Endpoints - Phase 2

## Base URL

- **Development**: `http://localhost:8000`
- **Production**: `https://api.example.com` (to be determined)

## Authentication

All endpoints require JWT token in the request header:

```
Authorization: Bearer <jwt_token>
```

JWT tokens are issued by Better Auth during login. The token contains:
- `user_id`: The user's UUID
- `email`: The user's email
- `exp`: Token expiration time

## Rate Limiting

**Phase 2 Status**: No rate limiting implemented.
- All authenticated users can make unlimited requests
- Rate limiting will be added in Phase 4/5 with Kubernetes and API gateway
- Better Auth handles brute-force protection for authentication endpoints (built-in)

## Response Format

All responses are JSON with the following structure:

### Success Response
```json
{
  "status": "success",
  "data": { ... }
}
```

### Error Response
```json
{
  "status": "error",
  "message": "Error description",
  "code": "ERROR_CODE"
}
```

## HTTP Status Codes

| Code | Meaning | Use Case |
|------|---------|----------|
| 200 | OK | Successful GET, PUT, PATCH |
| 201 | Created | Successful POST |
| 400 | Bad Request | Invalid input validation |
| 401 | Unauthorized | Missing/invalid JWT token |
| 403 | Forbidden | Trying to access another user's tasks |
| 404 | Not Found | Task doesn't exist |
| 409 | Conflict | Duplicate resource |
| 500 | Server Error | Unexpected error |

## Endpoints

### 1. GET /api/tasks

**List all tasks for authenticated user**

**Parameters:**
| Name | Type | Location | Required | Description |
|------|------|----------|----------|-------------|
| status | string | query | No | Filter: "all" (default), "pending", "completed" |
| sort | string | query | No | Sort by: "created" (default), "title", "updated" |

**Example Requests:**
```bash
# Get all tasks
curl -H "Authorization: Bearer <token>" http://localhost:8000/api/tasks

# Get pending tasks
curl -H "Authorization: Bearer <token>" "http://localhost:8000/api/tasks?status=pending"

# Get completed tasks, sorted by title
curl -H "Authorization: Bearer <token>" "http://localhost:8000/api/tasks?status=completed&sort=title"
```

**Response (200 OK):**
```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "title": "Buy groceries",
      "description": "Milk, eggs, bread",
      "completed": false,
      "created_at": "2025-12-07T10:30:00Z",
      "updated_at": "2025-12-07T10:30:00Z"
    },
    {
      "id": 2,
      "title": "Call mom",
      "description": null,
      "completed": true,
      "created_at": "2025-12-06T15:45:00Z",
      "updated_at": "2025-12-07T09:00:00Z"
    }
  ]
}
```

**Error (401 Unauthorized):**
```json
{
  "status": "error",
  "message": "Invalid or missing authentication token",
  "code": "UNAUTHORIZED"
}
```

---

### 2. POST /api/tasks

**Create a new task**

**Request Body:**
| Field | Type | Required | Constraint |
|-------|------|----------|-----------|
| title | string | Yes | 1-200 characters |
| description | string | No | Max 1000 characters |

**Example Request:**
```bash
curl -X POST http://localhost:8000/api/tasks \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Buy groceries",
    "description": "Milk, eggs, bread"
  }'
```

**Response (201 Created):**
```json
{
  "status": "success",
  "data": {
    "id": 3,
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false,
    "created_at": "2025-12-07T11:00:00Z",
    "updated_at": "2025-12-07T11:00:00Z"
  }
}
```

**Error (400 Bad Request):**
```json
{
  "status": "error",
  "message": "Title is required and must be 1-200 characters",
  "code": "VALIDATION_ERROR"
}
```

---

### 3. GET /api/tasks/{id}

**Get a specific task**

**Parameters:**
| Name | Type | Location | Required | Description |
|------|------|----------|----------|-------------|
| id | integer | path | Yes | Task ID |

**Example Request:**
```bash
curl -H "Authorization: Bearer <token>" http://localhost:8000/api/tasks/1
```

**Response (200 OK):**
```json
{
  "status": "success",
  "data": {
    "id": 1,
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false,
    "created_at": "2025-12-07T10:30:00Z",
    "updated_at": "2025-12-07T10:30:00Z"
  }
}
```

**Error (404 Not Found):**
```json
{
  "status": "error",
  "message": "Task not found",
  "code": "NOT_FOUND"
}
```

**Error (403 Forbidden):**
```json
{
  "status": "error",
  "message": "You do not have permission to access this task",
  "code": "FORBIDDEN"
}
```

---

### 4. PUT /api/tasks/{id}

**Update a task**

**Parameters:**
| Name | Type | Location | Required | Description |
|------|------|----------|----------|-------------|
| id | integer | path | Yes | Task ID |

**Request Body:**
| Field | Type | Required | Constraint |
|-------|------|----------|-----------|
| title | string | No | 1-200 characters |
| description | string | No | Max 1000 characters |

**Rules:**
- At least one field must be provided
- Empty fields are not updated

**Example Request:**
```bash
curl -X PUT http://localhost:8000/api/tasks/1 \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Buy groceries and fruits"
  }'
```

**Response (200 OK):**
```json
{
  "status": "success",
  "data": {
    "id": 1,
    "title": "Buy groceries and fruits",
    "description": "Milk, eggs, bread",
    "completed": false,
    "created_at": "2025-12-07T10:30:00Z",
    "updated_at": "2025-12-07T12:00:00Z"
  }
}
```

**Error (400 Bad Request):**
```json
{
  "status": "error",
  "message": "At least one field (title or description) must be provided",
  "code": "VALIDATION_ERROR"
}
```

---

### 5. DELETE /api/tasks/{id}

**Delete a task**

**Parameters:**
| Name | Type | Location | Required | Description |
|------|------|----------|----------|-------------|
| id | integer | path | Yes | Task ID |

**Example Request:**
```bash
curl -X DELETE http://localhost:8000/api/tasks/1 \
  -H "Authorization: Bearer <token>"
```

**Response (200 OK):**
```json
{
  "status": "success",
  "message": "Task deleted successfully"
}
```

**Error (404 Not Found):**
```json
{
  "status": "error",
  "message": "Task not found",
  "code": "NOT_FOUND"
}
```

---

### 6. PATCH /api/tasks/{id}/complete

**Toggle task completion status**

**Parameters:**
| Name | Type | Location | Required | Description |
|------|------|----------|----------|-------------|
| id | integer | path | Yes | Task ID |

**Request Body:**
| Field | Type | Required | Constraint |
|-------|------|----------|-----------|
| completed | boolean | Yes | true or false |

**Example Request:**
```bash
curl -X PATCH http://localhost:8000/api/tasks/1/complete \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "completed": true
  }'
```

**Response (200 OK):**
```json
{
  "status": "success",
  "data": {
    "id": 1,
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": true,
    "created_at": "2025-12-07T10:30:00Z",
    "updated_at": "2025-12-07T13:00:00Z"
  }
}
```

## Error Codes

| Code | Meaning | HTTP Status |
|------|---------|-------------|
| UNAUTHORIZED | Invalid/missing token | 401 |
| FORBIDDEN | No permission | 403 |
| NOT_FOUND | Task doesn't exist | 404 |
| VALIDATION_ERROR | Invalid input | 400 |
| DUPLICATE | Task already exists | 409 |
| SERVER_ERROR | Unexpected error | 500 |

## Implementation Details

### JWT Token Extraction

Extract user ID from JWT token:

```python
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthCredential
import jwt

async def get_current_user(credentials: HTTPAuthCredential = Depends(HTTPBearer())) -> str:
    token = credentials.credentials
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    return payload["user_id"]
```

### User Isolation

All queries must filter by authenticated user:

```python
# Only get this user's tasks
tasks = db.query(Task).filter(Task.user_id == user_id).all()

# Delete only if task belongs to this user
task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
```

### Timestamps

All timestamps are in ISO 8601 format with UTC timezone:
- Format: `YYYY-MM-DDTHH:MM:SSZ`
- Example: `2025-12-07T10:30:00Z`

