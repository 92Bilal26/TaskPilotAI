# Phase 3 Deployment Checklist

## Quick Summary: What's Different?

| Area | What Changes |
|------|--------------|
| **Frontend (Vercel)** | Add ChatKit widget + environment variables |
| **Backend (Render)** | Add CORS for ChatKit + OpenAI API key |
| **Database (Neon)** | No changes needed |
| **Authentication** | No changes needed |
| **Deployment Process** | Same as Phase 2 (git push) |

---

## ✅ Pre-Deployment Checklist

### Backend (Render)

- [ ] **CORS Configuration Updated**
  ```python
  # In backend/main.py, verify:
  # allow_origins includes your Vercel URL
  # Example: "https://yourapp.vercel.app"
  ```

- [ ] **OpenAI API Key Ready**
  ```bash
  # Have your key from openai.com
  # Format: sk-... (starts with sk-)
  ```

- [ ] **Code Changes Tested Locally**
  ```bash
  cd backend
  python -m pytest tests/
  # All tests pass
  ```

- [ ] **Environment Variables Listed**
  ```
  DATABASE_URL=postgresql://...
  JWT_SECRET=...
  ENVIRONMENT=production
  OPENAI_API_KEY=sk-...  [NEW]
  CHATKIT_SESSION_TIMEOUT=3600  [NEW]
  ```

### Frontend (Vercel)

- [ ] **ChatKit Config Updated**
  ```typescript
  # In frontend/lib/chatkit-config.ts
  # Uses NEXT_PUBLIC_API_URL environment variable
  # Uses NEXT_PUBLIC_DOMAIN_KEY environment variable
  ```

- [ ] **Environment Variables Ready**
  ```
  NEXT_PUBLIC_API_URL=https://taskpilot-backend.onrender.com
  NEXT_PUBLIC_DOMAIN_KEY=taskpilot-production  [NEW]
  ```

- [ ] **Build Succeeds**
  ```bash
  cd frontend
  npm run build
  # No errors
  ```

- [ ] **ChatKit Widget Imported**
  ```typescript
  # Verify ChatKitWidget component exists in:
  # frontend/components/ChatKit/ChatKitWidget.tsx
  ```

---

## 🚀 Deployment Steps

### Step 1: Backend Deployment (5 minutes)

```bash
# 1. Update CORS in code
nano backend/main.py
# Add your Vercel URL to allow_origins list
# Save and commit

# 2. Commit changes
cd /home/bilal/TaskPilotAI
git add backend/main.py
git commit -m "feat: Phase 3 - Add CORS for ChatKit"

# 3. Go to Render dashboard
# https://dashboard.render.com

# 4. Select TaskPilot Backend service
# Settings → Environment
# Add: OPENAI_API_KEY = sk-...
# Add: CHATKIT_SESSION_TIMEOUT = 3600
# Save (auto-deploys)

# 5. Wait for deployment (2-3 minutes)
# Check Logs for "Application is running"
```

**Verification:**
```bash
# Should see in logs:
# "ChatKit server initialized"
# No CORS errors
# No "OpenAI API key" errors
```

### Step 2: Frontend Deployment (3 minutes)

```bash
# 1. Update environment files
nano frontend/.env.production
# Make sure NEXT_PUBLIC_DOMAIN_KEY=taskpilot-production
# Save

# 2. Update ChatKit config if needed
nano frontend/lib/chatkit-config.ts
# Verify it uses process.env.NEXT_PUBLIC_API_URL
# Verify it uses process.env.NEXT_PUBLIC_DOMAIN_KEY

# 3. Commit changes
git add frontend/lib/chatkit-config.ts frontend/.env.production
git commit -m "feat: Phase 3 - Add ChatKit configuration"

# 4. Push to GitHub (auto-deploys to Vercel)
git push origin main

# 5. Go to Vercel dashboard
# https://vercel.com
# Should auto-deploy
# Wait for "Ready" status (1-2 minutes)

# 6. Add environment variables in Vercel
# Settings → Environment Variables
# Add: NEXT_PUBLIC_DOMAIN_KEY = taskpilot-production
# Redeploy (if not auto-deployed)
```

**Verification:**
```bash
# Check build logs - should have "Build successful"
# No errors about missing env variables
```

### Step 3: Full End-to-End Test (5 minutes)

```bash
# 1. Open production frontend
# https://yourapp.vercel.app/dashboard

# 2. Log in with your account

# 3. Open ChatKit widget (button in header)
# Should load without errors

# 4. Send test message
# "Create a task called 'Phase 3 Test'"

# 5. Wait for response
# Should see AI response in chat

# 6. Verify task was created
# Look in task list
# Should see "Phase 3 Test" task

# 7. Check browser console (F12)
# Should NOT see:
#   - CORS errors
#   - 401 Unauthorized
#   - Connection failed

# 8. All user data is isolated
# Log in as different user
# Should NOT see "Phase 3 Test" task
```

---

## 🔧 Quick Configuration Files

### Required CORS Update (backend/main.py)

```python
# Add after FastAPI app creation

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://yourapp.vercel.app",  # ← UPDATE with your Vercel URL
        "http://localhost:3000",
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

### Render Environment Variables

| Variable | Value | Where |
|----------|-------|-------|
| `DATABASE_URL` | `postgresql://...` | Keep from Phase 2 |
| `JWT_SECRET` | `your-secret-key` | Keep from Phase 2 |
| `ENVIRONMENT` | `production` | Keep from Phase 2 |
| `OPENAI_API_KEY` | `sk-...` | **ADD NEW** |
| `CHATKIT_SESSION_TIMEOUT` | `3600` | **ADD NEW** |

### Vercel Environment Variables

| Variable | Value | Where |
|----------|-------|-------|
| `NEXT_PUBLIC_API_URL` | `https://taskpilot-backend.onrender.com` | Keep from Phase 2 |
| `NEXT_PUBLIC_DOMAIN_KEY` | `taskpilot-production` | **ADD NEW** |

---

## ⚠️ Common Issues & Fixes

### Issue 1: CORS Error
```
Access to XMLHttpRequest blocked by CORS policy
```

**Fix:**
```python
# Update backend/main.py CORS
allow_origins=[
    "https://yourapp.vercel.app",  # Add YOUR exact Vercel URL
]
# Redeploy to Render
```

### Issue 2: OpenAI Key Error
```
Error: OpenAI API key not configured
```

**Fix:**
```bash
# In Render dashboard
# Add OPENAI_API_KEY environment variable
# Make sure it starts with "sk-"
# Restart service
```

### Issue 3: ChatKit Widget Won't Load
```
Chat widget is blank or hanging
```

**Fix:**
- Open browser DevTools (F12)
- Check Console tab for errors
- Check Network tab → POST /api/v1/chatkit
- Verify Authorization header is present
- Verify response status is 200 (not 401, 403, 502)

### Issue 4: Task Created in ChatKit Doesn't Appear in Dashboard
```
ChatKit says task created, but dashboard is empty
```

**Fix:**
- This is user_id isolation
- Verify wrapper functions are injecting user_id
- Check logs in Render: "add_task called for user"
- Query database to see if task has correct user_id

### Issue 5: Timeout When Creating Task
```
Request timeout after 30 seconds
```

**Fix:**
```bash
# In Render dashboard
# Settings → Health Check
# Increase timeout to 120 seconds
# Restart service
```

---

## 📊 Before & After Verification

### Phase 2 Features (Should Still Work)
- [ ] User signup/login with Better Auth
- [ ] Create/read/update/delete tasks via API
- [ ] Task list displayed in dashboard
- [ ] User isolation (can't see other users' tasks)

### Phase 3 New Features
- [ ] ChatKit widget loads in dashboard
- [ ] Can send message to ChatKit
- [ ] ChatKit responds with AI message
- [ ] Can ask ChatKit to create task via natural language
- [ ] Task appears in both ChatKit and dashboard
- [ ] Real-time sync works (dashboard updates when ChatKit creates task)
- [ ] User isolation maintained (ChatKit respects user_id)

---

## 🆘 Support Information

If deployment fails, check in this order:

1. **Check Render Logs**
   - Render dashboard → Select service → Logs
   - Look for errors about CORS, OpenAI, or ChatKit
   - Fix in code, commit, git push (auto-redeploys)

2. **Check Vercel Logs**
   - Vercel dashboard → Select project → Deployments
   - Click failed deployment → Logs
   - Look for build errors
   - Fix in code, commit, git push (auto-redeploys)

3. **Test Locally First**
   ```bash
   # Test backend locally
   cd backend && python -m uvicorn main:app --reload

   # Test frontend locally
   cd frontend && npm run dev

   # Open http://localhost:3000
   # Try ChatKit widget
   ```

4. **Check Browser Console**
   - F12 → Console tab
   - Send message in ChatKit
   - Look for any red errors
   - Check Network tab → POST /api/v1/chatkit request

5. **Review Deployment Guide**
   - Full troubleshooting in PHASE3_DEPLOYMENT_GUIDE.md
   - Contains detailed solutions

---

## ✅ Final Verification Checklist

Before declaring Phase 3 complete:

- [ ] Backend deployed to Render
- [ ] Frontend deployed to Vercel
- [ ] ChatKit widget visible on dashboard
- [ ] User can log in
- [ ] User can send message to ChatKit
- [ ] ChatKit responds with AI message
- [ ] User can ask ChatKit to create task
- [ ] Task appears in dashboard task list
- [ ] Dashboard auto-refreshes after ChatKit creates task
- [ ] Other users cannot see this user's tasks
- [ ] No CORS errors in browser console
- [ ] No 401/403 auth errors in network tab
- [ ] No timeouts (responses complete in < 30 seconds)

---

## Deployment Timeline

| Step | Time | Status |
|------|------|--------|
| 1. Update backend CORS | 5 min | ⏳ |
| 2. Add OpenAI key to Render | 2 min | ⏳ |
| 3. Wait for Render deploy | 3 min | ⏳ |
| 4. Update frontend config | 3 min | ⏳ |
| 5. Add domain key to Vercel | 2 min | ⏳ |
| 6. Wait for Vercel deploy | 2 min | ⏳ |
| 7. Test end-to-end | 5 min | ⏳ |
| **TOTAL** | **22 min** | ✅ |

**You should have Phase 3 deployed in under 30 minutes!**

---

## After Deployment: Monitor

**Render Monitoring:**
```bash
# Watch logs for errors
# Render dashboard → Logs
# Filter for: ERROR, CORS, OpenAI

# Check response times
# Should be < 10 seconds for ChatKit responses
```

**Vercel Monitoring:**
```bash
# Check build logs
# Vercel dashboard → Deployments
# All recent builds should show "Ready"

# Monitor performance
# Vercel dashboard → Analytics
# Track page load times
```

---

## Success! 🎉

Once all items are checked, Phase 3 is complete and your ChatKit chatbot is live in production on Vercel + Render!

You can now:
✅ Use ChatKit in production
✅ Create tasks via natural language conversation
✅ Have real-time sync between chat and dashboard
✅ Scale to multiple users with full isolation
