# ChatKit Complete Implementation for TaskPilotAI

**Status**: Ready to Implement
**Workflow ID**: `wf_6946b383d368819081b556e6e5fa66330d48d0c9ea4fccd8`

---

## Architecture Overview

```
User (Browser)
    ↓
Frontend (Next.js + ChatKit React)
    ↓ HTTP POST /api/chatkit/sessions (get client_secret)
    ↓ WebSocket /api/v1/chatkit (send messages)
    ↓
Backend (FastAPI)
    ├─ Session Endpoint: POST /api/chatkit/sessions
    ├─ ChatKit Endpoint: POST /api/v1/chatkit
    └─ ChatKit Server Class
        ↓
OpenAI API (Agent with Workflow ID)
    ↓ Response
    ↓
Backend → Frontend → ChatKit UI
```

---

## WHERE TO ADD YOUR ChatKit URL

### **1. Frontend Configuration** (MOST IMPORTANT)

**File**: `frontend/lib/chatkit-config.ts`

**Current (WRONG)**:
```typescript
api: {
  url: `${API_URL}/api/v1/chatkit`,  // ❌ WRONG
  domainKey: DOMAIN_KEY,
  fetch: authenticatedFetch,
}
```

**CORRECT**:
```typescript
api: {
  async getClientSecret(existing) {
    // This calls YOUR backend to get a session secret
    // URL: YOUR_BACKEND_URL/api/chatkit/sessions
    const res = await fetch(`${API_URL}/api/chatkit/sessions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    const { client_secret } = await res.json();
    return client_secret;
  }
}
```

**Value of `API_URL`**: Should be your backend URL:
- **Development**: `http://localhost:8000`
- **Production**: `https://your-backend-domain.com`

---

### **2. Backend Session Endpoint** (THE URL THAT RETURNS SECRET)

**File**: `backend/routes/chatkit.py` (NEW FILE)

**URL**: `POST /api/chatkit/sessions`

**What it does**: Creates a ChatKit session and returns `client_secret`

**Code**:
```python
from fastapi import APIRouter
from openai import OpenAI
import os
import json

router = APIRouter(prefix="/api/chatkit", tags=["chatkit"])
openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Your Workflow ID (VERY IMPORTANT!)
WORKFLOW_ID = "wf_6946b383d368819081b556e6e5fa66330d48d0c9ea4fccd8"

@router.post("/sessions")
async def create_chatkit_session():
    """
    Create a new ChatKit session

    Returns:
        dict with client_secret that frontend uses to initialize ChatKit
    """
    try:
        # Create session with OpenAI SDK
        session = openai_client.chatkit.sessions.create(
            workflow={"id": WORKFLOW_ID}  # YOUR WORKFLOW ID HERE!
        )

        return {
            "client_secret": session.client_secret,
            "session_id": session.id
        }
    except Exception as e:
        return {
            "error": str(e),
            "message": "Failed to create ChatKit session"
        }
```

---

### **3. Backend ChatKit WebSocket Endpoint** (THE URL THAT RECEIVES MESSAGES)

**File**: `backend/routes/chatkit.py` (ADD TO ABOVE FILE)

**URL**: `POST /api/v1/chatkit`

**What it does**: Receives messages, processes through ChatKit server, returns responses

**Code**:
```python
@router.post("/v1/chatkit")
async def chatkit_endpoint(request: Request):
    """
    ChatKit communication endpoint

    This endpoint receives WebSocket messages from ChatKit frontend,
    processes them through the ChatKit Server, and returns responses
    """
    try:
        body = await request.body()

        # Process through ChatKit Server
        result = await chatkit_server.process(body, {})

        # Return streaming or static response
        if isinstance(result, StreamingResult):
            return StreamingResponse(result, media_type="text/event-stream")
        else:
            return Response(content=result.json, media_type="application/json")

    except Exception as e:
        return {"error": str(e)}
```

---

### **4. Backend Main File** (REGISTER THE ROUTES)

**File**: `backend/main.py`

**Add these imports at top**:
```python
from routes.chatkit import router as chatkit_router
```

**Add this before app.run()**:
```python
# Include ChatKit routes
app.include_router(chatkit_router)
```

---

### **5. Environment Variables** (ADD THESE)

**File**: `backend/.env`

```
# OpenAI Configuration
OPENAI_API_KEY=sk_...  # Already exists

# ChatKit Configuration
CHATKIT_WORKFLOW_ID=wf_6946b383d368819081b556e6e5fa66330d48d0c9ea4fccd8
CHATKIT_MODEL=gpt-4.1
CHATKIT_TEMPERATURE=0.7

# Frontend URL (for CORS)
FRONTEND_URL=http://localhost:3000  # or your production URL
```

---

### **6. Frontend Layout** (ADD CHATKIT SCRIPT)

**File**: `frontend/app/layout.tsx`

**Add this in `<head>`**:
```html
<script
  src="https://cdn.platform.openai.com/deployments/chatkit/chatkit.js"
  async
></script>
```

---

### **7. Frontend ChatKit Config** (FIX THIS)

**File**: `frontend/lib/chatkit-config.ts`

**Replace entire file with**:
```typescript
import type { UseChatKitOptions } from '@openai/chatkit-react'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export const chatKitConfig: UseChatKitOptions = {
  // MOST IMPORTANT: The API configuration
  api: {
    async getClientSecret(existing) {
      // If we already have a secret, reuse it
      if (existing) {
        return existing
      }

      // Call YOUR backend session endpoint to get a new secret
      // This is the URL where you add: http://localhost:8000/api/chatkit/sessions
      const res = await fetch(`${API_URL}/api/chatkit/sessions`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      })

      if (!res.ok) {
        throw new Error('Failed to get ChatKit session')
      }

      const { client_secret } = await res.json()
      return client_secret
    },
  },

  // Theme customization
  theme: 'light',

  // Header configuration
  header: {
    enabled: true,
  },

  // Start screen
  startScreen: {
    greeting: 'Welcome to TaskPilot AI Chat',
    prompts: [
      {
        name: 'Create a task',
        prompt: 'Create a task to buy groceries',
        icon: 'write',
      },
      {
        name: 'List my tasks',
        prompt: 'Show me all my tasks',
        icon: 'search',
      },
      {
        name: 'Complete a task',
        prompt: 'Mark my first task as complete',
        icon: 'check',
      },
    ],
  },

  // Composer (input field)
  composer: {
    placeholder: 'Ask me to manage your tasks...',
  },

  // History
  history: {
    enabled: true,
  },

  // Event handlers
  onReady: () => {
    console.log('ChatKit is ready')
  },

  onError: (error) => {
    console.error('ChatKit error:', error)
  },
}

export function validateChatKitConfig() {
  const errors: string[] = []

  if (!API_URL) {
    errors.push('NEXT_PUBLIC_API_URL is not configured')
  }

  return {
    valid: errors.length === 0,
    errors,
  }
}
```

---

## COMPLETE FILE STRUCTURE

```
backend/
├── main.py
│   ├── Include ChatKit router
│   └── Add CORS for frontend
│
├── routes/chatkit.py               (NEW FILE)
│   ├── POST /api/chatkit/sessions  ← Frontend calls this to get secret
│   └── POST /api/v1/chatkit        ← ChatKit WebSocket messages
│
├── chatkit_server.py               (NEW FILE)
│   └── ChatKitServer class
│
└── .env
    ├── OPENAI_API_KEY
    ├── CHATKIT_WORKFLOW_ID
    └── FRONTEND_URL

frontend/
├── app/
│   ├── layout.tsx                  (UPDATE: Add ChatKit script in <head>)
│   ├── chatkit/
│   │   └── page.tsx                (UPDATE: Simplify component)
│   └── ...
│
├── lib/
│   ├── chatkit-config.ts           (UPDATE: Fix config)
│   └── ...
│
└── .env.local
    └── NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## STEP-BY-STEP IMPLEMENTATION

### **Step 1: Update Frontend Environment**

File: `frontend/.env.local`

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### **Step 2: Update Backend Environment**

File: `backend/.env`

```
OPENAI_API_KEY=sk_...  # Already exists
CHATKIT_WORKFLOW_ID=wf_6946b383d368819081b556e6e5fa66330d48d0c9ea4fccd8
FRONTEND_URL=http://localhost:3000
```

### **Step 3: Create ChatKit Routes**

Create: `backend/routes/chatkit.py`

(Code provided above)

### **Step 4: Create ChatKit Server**

Create: `backend/chatkit_server.py`

(I will provide this in next message)

### **Step 5: Update Main FastAPI File**

File: `backend/main.py`

Add:
```python
from routes.chatkit import router as chatkit_router
app.include_router(chatkit_router)
```

### **Step 6: Fix Frontend Config**

File: `frontend/lib/chatkit-config.ts`

(Code provided above)

### **Step 7: Add ChatKit Script to Layout**

File: `frontend/app/layout.tsx`

Add to `<head>`:
```html
<script
  src="https://cdn.platform.openai.com/deployments/chatkit/chatkit.js"
  async
></script>
```

### **Step 8: Simplify ChatKit Page**

File: `frontend/app/chatkit/page.tsx`

(I will provide simplified version)

---

## WHERE YOUR ChatKit URL GOES - SUMMARY

| Component | What it does | URL | File |
|-----------|-------------|-----|------|
| **Frontend** | Requests session secret | `http://localhost:8000/api/chatkit/sessions` | `frontend/lib/chatkit-config.ts` |
| **Backend Session** | Returns client secret | `POST /api/chatkit/sessions` | `backend/routes/chatkit.py` |
| **Backend Chat** | Handles messages | `POST /api/v1/chatkit` | `backend/routes/chatkit.py` |
| **Workflow** | Agent logic | `wf_6946b383d368819081b556e6e5fa66330d48d0c9ea4fccd8` | `backend/routes/chatkit.py` |

---

## KEY POINTS

✅ **Workflow ID**: `wf_6946b383d368819081b556e6e5fa66330d48d0c9ea4fccd8` goes in `backend/routes/chatkit.py`

✅ **Session Endpoint**: `http://localhost:8000/api/chatkit/sessions` goes in `frontend/lib/chatkit-config.ts`

✅ **ChatKit Script**: Goes in `frontend/app/layout.tsx` `<head>`

✅ **Environment Variable**: `NEXT_PUBLIC_API_URL=http://localhost:8000` goes in `frontend/.env.local`

---

## NEXT STEPS

Tell me: **"Ready to implement"** and I will:

1. ✅ Create complete `backend/routes/chatkit.py`
2. ✅ Create complete `backend/chatkit_server.py`
3. ✅ Update `frontend/lib/chatkit-config.ts`
4. ✅ Update `frontend/app/layout.tsx`
5. ✅ Update `frontend/app/chatkit/page.tsx`
6. ✅ Update `backend/main.py`
7. ✅ Create tests
8. ✅ Create deployment guide

All code will be ready to run!

---

**Your Workflow ID is safe and will be used in backend only (not exposed to frontend).**

Ready?
