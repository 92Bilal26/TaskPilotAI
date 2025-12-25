# Phase 3 Deployment Guide: ChatKit on Vercel + Render

## Overview

Phase 3 adds ChatKit chatbot to your existing Phase 2 setup. The deployment process is **mostly the same**, but with important considerations for streaming responses and real-time communication.

**Deployment Architecture:**
```
Vercel (Frontend + ChatKit Widget)
    ↓ HTTPS POST /api/v1/chatkit
Render (Backend + ChatKit Server)
    ↓ Streaming Response (SSE)
    ↓ Response back to Vercel
    ↓ ChatKit Widget displays in browser
```

---

## Backend Deployment (Render)

### What's the Same from Phase 2
✅ FastAPI on Render
✅ Neon PostgreSQL connection
✅ JWT authentication middleware
✅ Environment variables (.env)

### What's NEW for Phase 3

#### 1. CORS Configuration (CRITICAL for ChatKit)

**Update `backend/main.py`:**

```python
from fastapi.middleware.cors import CORSMiddleware

# Add CORS middleware BEFORE other middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://yourdomain.vercel.app",  # Production frontend
        "http://localhost:3000",           # Local development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=[
        "Content-Type",
        "Authorization",
        "X-ChatKit-Domain-Key",
        "X-User-ID",
    ],
    expose_headers=["Content-Type"],
    max_age=3600,
)
```

**Why:** ChatKit widget makes requests from Vercel to Render. CORS must allow:
- Authorization headers (JWT token)
- X-ChatKit-Domain-Key header
- Content-Type for streaming responses

#### 2. Render Environment Variables

**Add to Render dashboard:**

```bash
# Existing (Phase 2)
DATABASE_URL=postgresql://...
JWT_SECRET=your-secret
ENVIRONMENT=production

# New (Phase 3)
OPENAI_API_KEY=sk-your-key-here
CHATKIT_SESSION_TIMEOUT=3600
```

**Steps on Render:**
1. Go to your service
2. Settings → Environment
3. Add `OPENAI_API_KEY` with your OpenAI key
4. Add `CHATKIT_SESSION_TIMEOUT=3600`
5. Deploy

#### 3. Streaming Response Support

FastAPI/Render supports streaming automatically. Verify in your code:

```python
from fastapi.responses import StreamingResponse

@router.post("/api/v1/chatkit")
async def chatkit_protocol_endpoint(request: Request):
    # ... process request ...
    result = await chatkit_server.process(body, context)

    from chatkit.server import StreamingResult
    if isinstance(result, StreamingResult):
        # Render supports streaming responses ✓
        return StreamingResponse(result, media_type="text/event-stream")
```

#### 4. Timeout Settings

**Render timeout for long-running requests:**

Update `render.yaml` or Render dashboard:

```yaml
# render.yaml (if using infrastructure-as-code)
services:
  - type: web
    name: taskpilot-backend
    runtime: python
    startCommand: uvicorn backend.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: UVICORN_TIMEOUT
        value: "120"  # 2 minutes for streaming responses
```

**Or in Render dashboard:**
1. Settings → Health Check
2. Set timeout to 120 seconds (supports streaming)

#### 5. Deployment Checklist for Backend

```bash
# Before deploying to Render:

# 1. Test CORS locally
curl -X POST http://localhost:8000/api/v1/chatkit \
  -H "Authorization: Bearer test-token" \
  -H "X-ChatKit-Domain-Key: chatkit-app" \
  -H "Content-Type: application/json" \
  -d '{"message": "test"}'

# 2. Verify OpenAI API key works
python3 -c "from openai import OpenAI; print('OpenAI OK')"

# 3. Check streaming endpoint
# Should return 200 with streaming response, not timeout

# 4. Verify environment variables
# Render dashboard shows all envs
```

---

## Frontend Deployment (Vercel)

### What's the Same from Phase 2
✅ Next.js on Vercel
✅ Better Auth integration
✅ JWT token storage in localStorage
✅ Environment variables

### What's NEW for Phase 3

#### 1. Environment Variables for ChatKit

**Create `.env.production` for Vercel:**

```bash
# Existing (Phase 2)
NEXT_PUBLIC_API_URL=https://taskpilot-backend.onrender.com

# New (Phase 3) - ChatKit Configuration
NEXT_PUBLIC_DOMAIN_KEY=taskpilot-production
NEXT_PUBLIC_OPENAI_API_KEY=sk-your-key-here  # Optional, if needed on frontend
```

**Steps on Vercel:**
1. Go to your project
2. Settings → Environment Variables
3. Add variable: `NEXT_PUBLIC_DOMAIN_KEY` = `taskpilot-production`
4. Redeploy

#### 2. Vercel Build Configuration

**No changes needed!** But verify `next.config.js`:

```javascript
// next.config.js
const nextConfig = {
  // Streaming is supported by Next.js ✓
  // No special config needed for ChatKit

  // Existing config (Phase 2)
  typescript: {
    ignoreBuildErrors: false,
  },
  reactStrictMode: true,
}

module.exports = nextConfig
```

#### 3. Update ChatKit Config for Production

**Update `frontend/lib/chatkit-config.ts`:**

```typescript
// Use environment variables for production
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
const DOMAIN_KEY = process.env.NEXT_PUBLIC_DOMAIN_KEY || 'chatkit-dev'

// In production, this becomes:
// API_BASE_URL = https://taskpilot-backend.onrender.com
// DOMAIN_KEY = taskpilot-production

const API_URL = `${API_BASE_URL}/api/v1/chatkit`
// Production: https://taskpilot-backend.onrender.com/api/v1/chatkit
```

#### 4. Deployment Checklist for Frontend

```bash
# Before deploying to Vercel:

# 1. Test ChatKit config
npm run build

# 2. Check environment variables in .env.local
cat .env.local | grep NEXT_PUBLIC_

# 3. Verify API endpoint is accessible
curl https://taskpilot-backend.onrender.com/health

# 4. Test in local production mode
npm run build && npm run start
# Open http://localhost:3000
# Try ChatKit widget

# 5. Push to GitHub (triggers Vercel deploy)
git add .
git commit -m "feat: Add Phase 3 ChatKit configuration"
git push origin main
```

---

## Complete Deployment Flow

### Step 1: Backend Deployment (Render)

```bash
# 1. Update backend/main.py with CORS
# 2. Add environment variables in Render dashboard
#    - OPENAI_API_KEY
#    - CHATKIT_SESSION_TIMEOUT
# 3. Push to GitHub (auto-deploys to Render)
git push origin main

# 4. Verify in Render logs
# Look for: "ChatKit server initialized"
# Should NOT see CORS errors
```

### Step 2: Frontend Deployment (Vercel)

```bash
# 1. Update frontend/lib/chatkit-config.ts
# 2. Update .env.production
# 3. Add NEXT_PUBLIC_DOMAIN_KEY to Vercel dashboard
# 4. Push to GitHub (auto-deploys to Vercel)
git push origin main

# 5. Verify in Vercel logs
# Should build successfully
# No errors about missing NEXT_PUBLIC_ variables
```

### Step 3: Verify End-to-End

```bash
# 1. Open Vercel production URL
# https://yourapp.vercel.app/dashboard

# 2. Open ChatKit widget
# Should load without errors

# 3. Send message to ChatKit
# Should get response from Render backend

# 4. Create task via ChatKit
# Task should appear in dashboard

# 5. Check browser console (F12)
# Should see: Authorization header with Bearer token
# Should see: Request to https://taskpilot-backend.onrender.com/api/v1/chatkit
```

---

## Troubleshooting Deployment Issues

### Issue 1: CORS Error in Browser

**Error:**
```
Access to XMLHttpRequest blocked by CORS policy
```

**Solution:**
```python
# In backend/main.py, verify CORS includes Vercel domain
allow_origins=[
    "https://yourapp.vercel.app",  # Must match your Vercel URL
    "http://localhost:3000",
],
```

**Check:**
```bash
# Get your actual Vercel URL
curl https://vercel.com/api/v13/projects/YOUR_PROJECT_ID

# Update CORS with exact URL (including https://)
```

### Issue 2: OpenAI API Key Not Working

**Error:**
```
OpenAI API key not configured
or
Invalid OpenAI API key
```

**Solution:**
```bash
# 1. Verify key in Render dashboard
# Settings → Environment Variables
# OPENAI_API_KEY should be visible

# 2. Restart Render service
# (sometimes env changes need restart)

# 3. Test key locally
python3 -c "
import os
os.environ['OPENAI_API_KEY'] = 'sk-...'
from openai import OpenAI
client = OpenAI()
print('Key is valid!')
"
```

### Issue 3: ChatKit Widget Won't Load

**Error:**
```
Chat widget blank or loading forever
```

**Solutions:**

1. **Check API endpoint:**
   ```typescript
   // In browser console
   console.log(process.env.NEXT_PUBLIC_API_URL)
   // Should show: https://taskpilot-backend.onrender.com
   ```

2. **Check domain key:**
   ```typescript
   console.log(process.env.NEXT_PUBLIC_DOMAIN_KEY)
   // Should show: taskpilot-production
   ```

3. **Verify JWT token exists:**
   ```javascript
   // In browser console
   console.log(localStorage.getItem('access_token'))
   // Should show JWT token (not null)
   ```

4. **Check network tab:**
   - Open DevTools → Network
   - Look for POST to `/api/v1/chatkit`
   - Check status (should be 200, not 401 or 403)
   - Check headers (Authorization: Bearer ...)

### Issue 4: Streaming Response Timeout

**Error:**
```
Request timeout after 30 seconds
or
502 Bad Gateway
```

**Solution:**

1. **Increase Render timeout:**
   - Render dashboard → Settings → Health Check
   - Set timeout to 120 seconds

2. **Check agent response time:**
   ```python
   # Add logging to measure
   start = time.time()
   result = Runner.run_streamed(agent, input)
   logger.info(f"Agent took {time.time() - start}s")
   ```

3. **Optimize agent instructions:**
   - Shorter instructions = faster response
   - Fewer tools = faster execution

### Issue 5: Tasks Don't Appear in Dashboard

**Error:**
```
ChatKit creates tasks but dashboard doesn't show them
```

**Solution:**
This is the user_id isolation issue. Verify:

1. **Check wrapper functions are injecting user_id:**
   ```python
   # In logs, should see:
   # "add_task called for user user-123"
   ```

2. **Verify database has user_id:**
   ```bash
   # In Neon dashboard SQL editor
   SELECT id, user_id, title FROM tasks;
   # All tasks should have user_id set
   ```

3. **Check API endpoint filters by user_id:**
   ```python
   # GET /tasks should only return user's tasks
   stmt = select(Task).where(Task.user_id == user_id)
   ```

---

## Performance Optimization for Production

### 1. Cache Static ChatKit Assets

**In Vercel (`next.config.js`):**

```javascript
const nextConfig = {
  headers: async () => {
    return [
      {
        source: '/:path*.js',
        headers: [
          { key: 'Cache-Control', value: 'public, max-age=31536000' }
        ]
      }
    ]
  }
}
```

### 2. Optimize Auto-Refresh Polling

**Current (every 1 second):**
```typescript
useEffect(() => {
  const interval = setInterval(() => fetchTasks(), 1000)
  return () => clearInterval(interval)
}, [showChat])
```

**Optimized (only when chat is visible):**
```typescript
useEffect(() => {
  if (!showChat) return

  // Fetch immediately when opening
  fetchTasks()

  // Then every 2 seconds (reduced from 1)
  const interval = setInterval(() => fetchTasks(), 2000)

  return () => clearInterval(interval)
}, [showChat])
```

### 3. Add Response Caching to Backend

**In FastAPI:**

```python
from fastapi import Response

@router.get("/tasks")
async def list_tasks(request: Request):
    # ... get tasks ...

    return Response(
        content=json.dumps(tasks),
        headers={
            "Cache-Control": "no-cache, must-revalidate",  # No caching (real-time)
            "Content-Type": "application/json"
        }
    )
```

### 4. Monitor Production Performance

**Set up Render logs monitoring:**
```bash
# Watch for slow requests
grep "took.*s" /var/log/app.log | sort -rn

# Look for errors
grep "ERROR" /var/log/app.log
```

**Set up Vercel analytics:**
- Vercel dashboard → Analytics
- Monitor response times, edge function latency

---

## Rollback Plan

If Phase 3 deployment breaks anything:

**Frontend Rollback (Vercel):**
```bash
# Option 1: Use Vercel dashboard
# Deployments → Select previous working deployment → Promote

# Option 2: Git rollback
git revert HEAD  # Creates new commit undoing changes
git push origin main
```

**Backend Rollback (Render):**
```bash
# Option 1: Use Render dashboard
# Deploys → Select previous deployment → Redeploy

# Option 2: Git rollback
git revert HEAD
git push origin main  # Auto-deploys to Render
```

---

## Verification Checklist

Before considering Phase 3 deployment complete:

- [ ] Backend deployed to Render with ChatKit server
- [ ] CORS configured to allow Vercel origin
- [ ] OpenAI API key set in Render environment
- [ ] Frontend deployed to Vercel with ChatKit widget
- [ ] NEXT_PUBLIC_DOMAIN_KEY set in Vercel environment
- [ ] API endpoint uses HTTPS (not HTTP)
- [ ] JWT token properly stored and sent in Authorization header
- [ ] ChatKit widget loads without errors
- [ ] User can send message to chatbot
- [ ] Agent can call MCP tools
- [ ] Tasks created in ChatKit appear in dashboard
- [ ] Only logged-in user sees their own tasks
- [ ] Real-time sync works (dashboard updates after ChatKit creates task)
- [ ] Streaming responses work (no timeout errors)
- [ ] Browser console shows no CORS or 401 errors

---

## Summary: Phase 3 vs Phase 2 Deployment

| Aspect | Phase 2 | Phase 3 | Change |
|--------|---------|---------|--------|
| Frontend Platform | Vercel | Vercel | ✅ Same |
| Backend Platform | Render | Render | ✅ Same |
| Database | Neon PostgreSQL | Neon PostgreSQL | ✅ Same |
| Authentication | JWT | JWT | ✅ Same |
| CORS Configuration | Basic | **Requires ChatKit headers** | ⚠️ **NEW** |
| OpenAI Integration | None | **ChatKit + Agents SDK** | ⚠️ **NEW** |
| Response Type | JSON | **Streaming SSE** | ⚠️ **NEW** |
| Environment Variables | Basic | **ChatKit config added** | ⚠️ **NEW** |
| Timeout Settings | Standard | **Need 120s for streaming** | ⚠️ **NEW** |

**Bottom line:** No infrastructure changes needed, just configuration updates for streaming and ChatKit support.

---

## Next Steps

1. **Update backend for Phase 3:**
   ```bash
   cd backend
   git add main.py routes/chatkit.py
   git commit -m "feat: Phase 3 - Add ChatKit server configuration"
   ```

2. **Update frontend for Phase 3:**
   ```bash
   cd frontend
   git add lib/chatkit-config.ts .env.production
   git commit -m "feat: Phase 3 - Add ChatKit widget configuration"
   ```

3. **Deploy to production:**
   ```bash
   # Push to GitHub (triggers both Vercel and Render deploys)
   git push origin main
   ```

4. **Verify in production:**
   - Open https://yourapp.vercel.app
   - Test ChatKit chatbot
   - Check for errors in console

5. **Monitor production:**
   - Vercel dashboard → Analytics
   - Render dashboard → Logs
