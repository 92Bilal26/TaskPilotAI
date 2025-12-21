# Quickstart: ChatKit Integration Setup

**Time Required**: 10-15 minutes
**Complexity**: Beginner-friendly
**Prerequisites**: Phase 2 backend + frontend running

---

## Overview

This guide walks you through integrating ChatKit in 5 steps:

1. **Backend**: Add session creation endpoint
2. **Frontend**: Configure ChatKit with session management
3. **Layout**: Load ChatKit JS library
4. **Dependencies**: Install required packages
5. **Test**: Verify it works

---

## Step 1: Backend Session Endpoint

**File**: `backend/routes/chatkit.py`

```python
from fastapi import APIRouter, Request
from openai import OpenAI
import os

router = APIRouter()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@router.post("/sessions")
async def create_chatkit_session(request: Request):
    """Create ChatKit session and return client_secret for frontend"""

    workflow_id = os.getenv("CHATKIT_WORKFLOW_ID")

    if not workflow_id:
        return {
            "status": "error",
            "message": "ChatKit workflow not configured"
        }

    try:
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
        return {
            "status": "error",
            "message": f"Failed to create session: {str(e)}"
        }
```

**Register route in** `backend/main.py`:

```python
from routes import chatkit

app.include_router(chatkit.router, prefix="/api/chatkit", tags=["chatkit"])
```

---

## Step 2: Frontend Configuration

**File**: `frontend/lib/chatkit-config.ts`

```typescript
import type { ChatKitConfig } from '@openai/chatkit-react'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export const chatKitConfig: ChatKitConfig = {
  api: {
    async getClientSecret(existing?: string): Promise<string> {
      // Reuse existing secret if available
      if (existing) {
        console.log('Reusing existing ChatKit client secret')
        return existing
      }

      try {
        console.log('Creating new ChatKit session')

        const response = await fetch(`${API_URL}/api/chatkit/sessions`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          }
        })

        if (!response.ok) {
          throw new Error(`Failed: ${response.statusText}`)
        }

        const data = await response.json()

        if (data.status !== 'success') {
          throw new Error(data.message || 'Unknown error')
        }

        const clientSecret = data.data.client_secret
        console.log('Got ChatKit session:', data.data.session_id)

        return clientSecret
      } catch (error) {
        console.error('Error getting ChatKit session:', error)
        throw error
      }
    }
  }
}
```

---

## Step 3: Load ChatKit JS Library

**File**: `frontend/app/layout.tsx`

Add script to `<head>`:

```tsx
export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <head>
        {/* OpenAI ChatKit JS Library */}
        <script
          src="https://cdn.platform.openai.com/deployments/chatkit/chatkit.js"
          async
        ></script>
      </head>
      <body>{children}</body>
    </html>
  )
}
```

---

## Step 4: ChatKit Page Component

**File**: `frontend/app/chatkit/page.tsx`

```tsx
'use client'

import { useChatKit } from '@openai/chatkit-react'
import { chatKitConfig } from '@/lib/chatkit-config'
import { useState, useEffect } from 'react'

export default function ChatKitPage() {
  const [isReady, setIsReady] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    try {
      setIsReady(true)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error')
    }
  }, [])

  return (
    <div className="w-full h-screen flex flex-col bg-white">
      <header className="bg-blue-600 text-white p-4">
        <h1 className="text-2xl font-bold">TaskPilot AI Chat</h1>
        <p className="text-sm opacity-90">Ask me to manage your tasks</p>
      </header>

      <main className="flex-1 overflow-hidden">
        {!isReady && (
          <div className="flex items-center justify-center h-full">
            <div className="text-center">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
              <p className="text-gray-600">Loading ChatKit...</p>
            </div>
          </div>
        )}

        {error && (
          <div className="flex items-center justify-center h-full">
            <div className="text-center text-red-600">
              <p className="text-lg font-bold">Error</p>
              <p className="text-sm">{error}</p>
              <button
                onClick={() => window.location.reload()}
                className="mt-4 px-4 py-2 bg-blue-600 text-white rounded"
              >
                Retry
              </button>
            </div>
          </div>
        )}

        {isReady && !error && (
          <ChatKitComponent config={chatKitConfig} />
        )}
      </main>
    </div>
  )
}

// ChatKit Component Wrapper
function ChatKitComponent({ config }: { config: any }) {
  const chatKit = useChatKit(config)

  if (!chatKit) {
    return (
      <div className="flex items-center justify-center h-full">
        <p className="text-gray-600">Initializing ChatKit...</p>
      </div>
    )
  }

  return (
    <div className="w-full h-full">
      {/* ChatKit renders here automatically */}
      <div id="chatkit-container" className="w-full h-full" />
    </div>
  )
}
```

---

## Step 5: Environment Variables

### Backend (.env)

```bash
OPENAI_API_KEY=sk_live_YOUR_KEY_HERE
CHATKIT_WORKFLOW_ID=wf_6946b383d368819081b556e6e5fa66330d48d0c9ea4fccd8
```

### Frontend (.env.local)

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## Step 6: Install Dependencies

### Backend

```bash
cd backend
pip install -r requirements.txt
```

**requirements.txt should include**:
```
openai>=1.12.0
openai-chatkit>=0.1.0
```

### Frontend

```bash
cd frontend
npm install
```

**Already included in** `package.json`:
```json
{
  "dependencies": {
    "@openai/chatkit-react": "latest",
    "next": "16+",
    "react": "19+"
  }
}
```

---

## Step 7: Start Services

### Terminal 1: Backend

```bash
cd backend
uvicorn main:app --reload --port 8000
```

**Expected output**:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

### Terminal 2: Frontend

```bash
cd frontend
npm run dev
```

**Expected output**:
```
  ▲ Next.js 16.0.0
  - Local:        http://localhost:3000
```

---

## Step 8: Test It

1. **Open browser**: http://localhost:3000/chatkit

2. **Expected to see**:
   - ChatKit header: "TaskPilot AI Chat"
   - Loading spinner (briefly)
   - Chat input field

3. **Check browser console** (F12):
   ```
   Creating new ChatKit session
   Got ChatKit session: ses_...
   ChatKit is ready
   ```

4. **Test message**:
   - Type: "Hello"
   - Press Enter
   - Agent should respond

---

## Verification Checklist

- [ ] Backend running (port 8000)
- [ ] Frontend running (port 3000)
- [ ] OPENAI_API_KEY set in backend/.env
- [ ] CHATKIT_WORKFLOW_ID set in backend/.env
- [ ] NEXT_PUBLIC_API_URL set in frontend/.env.local
- [ ] ChatKit page loads at http://localhost:3000/chatkit
- [ ] Browser console shows "Got ChatKit session"
- [ ] Can type and send message
- [ ] Agent responds
- [ ] No error messages

---

## Step 9: Production Deployment Setup (Your Vercel App)

Your frontend is already deployed to Vercel from Phase 2. Now configure it for ChatKit production:

**Your Production Frontend**: https://task-pilot-ai-ashen.vercel.app

### 5-Step Production Configuration

1. **Register Domain in OpenAI** ⭐ FIRST STEP
   - Go to: https://platform.openai.com/settings/organization/security/domain-allowlist
   - Click "Add domain"
   - Enter: `https://task-pilot-ai-ashen.vercel.app`
   - Copy the domain key generated (save it)

2. **Set Environment Variables in Vercel Dashboard**
   - Go to: https://vercel.com/dashboard
   - Find your project: `TaskPilotAI` or similar
   - Click Settings → Environment Variables
   - Add for **Production** environment:
     ```
     NEXT_PUBLIC_API_URL=https://your-backend-production-url.com
     NEXT_PUBLIC_CHATKIT_DOMAIN_KEY=sk_live_<your_key_here>
     ```

3. **Update Backend CORS** (if needed)
   ```python
   # backend/main.py
   from fastapi.middleware.cors import CORSMiddleware

   allowed_origins = [
       "http://localhost:3000",  # Local development
       "https://task-pilot-ai-ashen.vercel.app"  # Your production
   ]

   app.add_middleware(
       CORSMiddleware,
       allow_origins=allowed_origins,
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

4. **Redeploy Frontend** (to apply environment variables)
   ```bash
   cd frontend
   git push  # Push to GitHub
   # Vercel auto-deploys on push
   # Wait for deployment to complete
   ```

5. **Test Production**
   - Visit: https://task-pilot-ai-ashen.vercel.app/chatkit
   - Verify ChatKit loads and works
   - Send test message to agent
   - Check browser console for "Got ChatKit session" message

### Multi-Environment Setup

| Stage | Frontend URL | Domain Key | Status |
|-------|--------------|-----------|--------|
| Local Dev | http://localhost:3000 | (not needed) | ✅ Works immediately |
| Production | https://task-pilot-ai-ashen.vercel.app | sk_live_... | ✅ Required |

### Environment Variables Summary

**For Local Development** (frontend/.env.local):
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_CHATKIT_DOMAIN_KEY=
```

**For Production** (Set in Vercel Dashboard):
```bash
NEXT_PUBLIC_API_URL=https://your-backend-url.com
NEXT_PUBLIC_CHATKIT_DOMAIN_KEY=sk_live_your_key_from_openai
```

**Backend** (backend/.env):
```bash
OPENAI_API_KEY=sk_live_your_key_here
CHATKIT_WORKFLOW_ID=wf_6946b383d368819081b556e6e5fa66330d48d0c9ea4fccd8
```

---

## Troubleshooting

### Problem: "Cannot GET /chatkit"

**Solution**: Frontend route not found

```bash
# Make sure frontend is running
npm run dev

# Check file exists: frontend/app/chatkit/page.tsx
ls frontend/app/chatkit/page.tsx
```

### Problem: "Failed to get ChatKit session"

**Solution**: Backend endpoint not working

```bash
# Test backend directly
curl -X POST http://localhost:8000/api/chatkit/sessions

# Should return JSON with client_secret
# If error: check OPENAI_API_KEY is valid
```

### Problem: "OpenAI API key not configured"

**Solution**: OPENAI_API_KEY not set

```bash
# Check backend/.env
cat backend/.env | grep OPENAI_API_KEY

# Should show: OPENAI_API_KEY=sk_...
# If not set, add it and restart backend
```

### Problem: Agent doesn't respond

**Causes**:
- Invalid OpenAI API key (test: `curl ...`)
- ChatKit workflow not configured (check CHATKIT_WORKFLOW_ID)
- Network issue (check browser Network tab)

**Debug**:
```bash
# Check backend logs
# Should show: "POST /api/chatkit/sessions"

# Check browser console
# Should show: "Got ChatKit session: ses_..."
```

---

## What's Next?

After verifying ChatKit works:

1. **Phase 3b**: Add conversation persistence + Agents SDK
2. **Phase 3c**: Add MCP tools for task operations
3. **Phase 3d**: Add streaming responses

For now, basic ChatKit integration is complete ✅

---

## Common Questions

**Q: Can I customize ChatKit appearance?**
A: Yes, see `chatkit-config.ts` theme options.

**Q: How long do sessions last?**
A: OpenAI manages session lifetime (typically 24-48 hours).

**Q: Can multiple users chat simultaneously?**
A: Yes, each browser session creates independent ChatKit session.

**Q: How do I debug issues?**
A: Check browser console (F12) for detailed error messages.

---

**Last Updated**: December 20, 2025
**Status**: Ready to Implement
**Docs**: See `/specs/005-chatkit-integration/` for detailed documentation
