# Feature: User Authentication - Phase 2

## Overview

Implement user authentication using **Better Auth** on the frontend and **JWT token validation** on the backend.

## Architecture

```
Frontend (Next.js)          Backend (FastAPI)            Database (Neon)
─────────────────          ─────────────────            ──────────────

[Better Auth]              [JWT Validation]             [users table]
    │                              │                          │
    ├─ signup() ─────────────────▶ POST /auth/signup ────────▶ Insert user
    │                              │                          │
    ├─ signin() ─────────────────▶ POST /auth/signin ────────▶ Query user
    │                              │                          │
    └─ JWT Token ───────────────▶ Validate Token ────────────▶ Get user_id
                                    │
                              Attach user_id to
                              all API requests
```

## User Registration (Signup)

### Requirements

1. User provides email and password
2. Better Auth validates input on frontend
3. Backend creates user in database
4. Backend issues JWT token
5. Token is stored in browser (session/cookie)

### Frontend Flow (Next.js + Better Auth)

```typescript
import { signUp } from "@/lib/auth-client"

async function handleSignup(email: string, password: string) {
  try {
    const { user, session } = await signUp.email({
      email,
      password,
      name: email.split('@')[0]
    })
    // Redirect to dashboard
  } catch (error) {
    // Show error message
  }
}
```

### Backend Requirements

**Endpoint:** `POST /auth/signup` (Better Auth endpoint)

**Input:**
```json
{
  "email": "alice@example.com",
  "password": "secure_password",
  "name": "Alice"
}
```

**Validation:**
- Email format is valid
- Email is not already registered
- Password is at least 8 characters
- Name is provided (optional)

**Success Response (201 Created):**
```json
{
  "user": {
    "id": "user-123-uuid",
    "email": "alice@example.com",
    "name": "Alice",
    "createdAt": "2025-12-07T10:00:00Z"
  },
  "session": {
    "token": "eyJhbGc...",
    "expiresAt": "2025-12-14T10:00:00Z"
  }
}
```

**Error Response (400 Bad Request):**
```json
{
  "status": "error",
  "message": "Email already registered",
  "code": "EMAIL_EXISTS"
}
```

## User Login (Signin)

### Requirements

1. User provides email and password
2. Better Auth validates credentials
3. Backend authenticates user
4. Backend issues JWT token
5. Token is stored in browser

### Frontend Flow (Next.js + Better Auth)

```typescript
import { signIn } from "@/lib/auth-client"

async function handleSignin(email: string, password: string) {
  try {
    const { user, session } = await signIn.email({
      email,
      password
    })
    // Redirect to dashboard
  } catch (error) {
    // Show error message
  }
}
```

### Backend Requirements

**Endpoint:** `POST /auth/signin` (Better Auth endpoint)

**Input:**
```json
{
  "email": "alice@example.com",
  "password": "secure_password"
}
```

**Validation:**
- Email exists in database
- Password matches stored hash
- Account is active (not suspended)

**Success Response (200 OK):**
```json
{
  "user": {
    "id": "user-123-uuid",
    "email": "alice@example.com",
    "name": "Alice"
  },
  "session": {
    "token": "eyJhbGc...",
    "expiresAt": "2025-12-14T10:00:00Z"
  }
}
```

**Error Response (401 Unauthorized):**
```json
{
  "status": "error",
  "message": "Invalid email or password",
  "code": "INVALID_CREDENTIALS"
}
```

## JWT Token Structure

### Token Format

```
Header.Payload.Signature
```

### Token Payload (decoded)

```json
{
  "sub": "user-123-uuid",
  "email": "alice@example.com",
  "iat": 1733568000,
  "exp": 1733654400,
  "aud": "todo-app"
}
```

### Fields

| Field | Type | Description |
|-------|------|-------------|
| sub | string | Subject (user ID) |
| email | string | User email |
| iat | integer | Issued at (Unix timestamp) |
| exp | integer | Expiration time (7 days) |
| aud | string | Audience (todo-app) |

## Token Lifecycle

### Token Issuance

1. User successfully authenticates
2. Backend generates JWT token with:
   - User ID as `sub`
   - Current timestamp as `iat`
   - Expiration time (7 days) as `exp`
   - Signed with SECRET_KEY
3. Token sent to frontend in response

### Token Storage

**Frontend stores token:**
- In HTTP-only cookie (preferred, secure)
- Or in localStorage (less secure)
- Better Auth handles this automatically

**Token is automatically:**
- Attached to every API request in Authorization header
- Refreshed before expiration
- Cleared on logout

### Token Validation

**Backend validates on every API request:**

```python
async def get_current_user(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401)
        return user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

### Token Expiration

- JWT tokens expire after **7 days**
- Better Auth automatically refreshes tokens before expiry
- Expired tokens return 401 Unauthorized
- User must re-login after logout

## API Authorization

### Request with Token

All API requests must include Authorization header:

```http
GET /api/tasks HTTP/1.1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Host: api.example.com
```

### Automatic Token Attachment

Better Auth automatically attaches token to all requests:

```typescript
// Frontend API client
const response = await fetch('/api/tasks', {
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${session.token}` // Automatic
  }
})
```

### Token Extraction on Backend

```python
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthCredential

async def get_current_user(credentials: HTTPAuthCredential = Depends(HTTPBearer())) -> str:
    token = credentials.credentials
    # Validate and return user_id
    return user_id
```

## Session Management

### Session Creation

On successful login:
1. JWT token is issued
2. Better Auth creates session record in database
3. Session ID is stored in cookie
4. User is logged in and redirected to dashboard

### Session Validation

On every API request:
1. Check if token exists in Authorization header
2. Decode and validate JWT token
3. Extract user ID from token
4. Verify user exists and is active
5. Proceed with request

### Session Termination (Logout)

On logout:
1. User clicks "Logout" button
2. Better Auth clears session in database
3. Token is removed from browser (cookie/storage)
4. User is redirected to login page
5. All subsequent requests are 401 Unauthorized

## Security Considerations

### Password Security

- Passwords are hashed using **bcrypt** (default in Better Auth)
- Plaintext passwords are never stored
- Password hashing on backend (not frontend)

### Token Security

- Tokens are signed with SECRET_KEY (keep private!)
- Tokens contain no sensitive data (only user ID, email)
- Tokens expire after 7 days
- Tokens are transmitted over HTTPS only

### CORS Configuration

Allow frontend origin to make requests to backend:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-domain.com", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Environment Variables

**Never commit secrets to git!**

```env
# .env.local (frontend)
NEXT_PUBLIC_API_URL=http://localhost:8000

# .env (backend)
BETTER_AUTH_SECRET=your-super-secret-key
DATABASE_URL=postgresql://user:pass@host/db
JWT_SECRET=your-jwt-secret-key
JWT_EXPIRATION_HOURS=168  # 7 days
```

## Better Auth Setup

### Frontend Configuration

```typescript
// lib/auth-client.ts
import { createAuthClient } from "better-auth/client"

export const { signUp, signIn, signOut, useSession } = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  plugins: [
    // JWT plugin for token management
  ]
})
```

### Backend Configuration

```python
# main.py
from fastapi import FastAPI

app = FastAPI()

# Better Auth is managed by the JavaScript SDK
# Backend only validates tokens and authenticates requests
```

## Success Criteria

- [ ] User can sign up with email and password
- [ ] User can sign in with email and password
- [ ] JWT token is issued on successful login
- [ ] Token is automatically attached to API requests
- [ ] Backend validates token on every request
- [ ] User can access only their own tasks
- [ ] User can log out
- [ ] 401 error on invalid/expired tokens
- [ ] Password hashing works correctly
- [ ] CORS allows frontend to communicate with backend

## Error Handling

| Scenario | Status | Message |
|----------|--------|---------|
| Email already exists | 400 | Email already registered |
| Invalid email format | 400 | Invalid email format |
| Weak password | 400 | Password must be 8+ characters |
| Incorrect password | 401 | Invalid email or password |
| Missing JWT token | 401 | Authorization header required |
| Expired JWT token | 401 | Token expired, please login again |
| Invalid JWT token | 401 | Invalid token |
| User suspended | 403 | Account is suspended |

