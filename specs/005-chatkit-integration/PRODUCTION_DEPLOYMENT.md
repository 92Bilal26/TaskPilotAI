# Production Deployment Guide: ChatKit Integration

**Your Production Frontend**: https://task-pilot-ai-ashen.vercel.app
**Status**: Ready for ChatKit integration in production
**Time Required**: 15 minutes

---

## Overview

Your TaskPilotAI frontend is already deployed on Vercel from Phase 2. This guide explains how to enable ChatKit for production by:

1. Registering your Vercel domain with OpenAI
2. Setting environment variables in Vercel
3. Updating backend CORS configuration
4. Testing the production ChatKit integration

---

## Prerequisites

- ✅ Frontend deployed on Vercel: https://task-pilot-ai-ashen.vercel.app
- ✅ Backend with OpenAI API key (for session creation)
- ✅ CHATKIT_WORKFLOW_ID configured: `wf_6946b383d368819081b556e6e5fa66330d48d0c9ea4fccd8`
- ✅ OpenAI account with API access

---

## Step 1: Register Domain with OpenAI

This is the critical first step. OpenAI needs to whitelist your domain for ChatKit to work.

### 1a. Go to OpenAI Domain Allowlist

1. Visit: https://platform.openai.com/settings/organization/security/domain-allowlist
2. Sign in with your OpenAI account
3. Click **"Add domain"**

### 1b. Enter Your Production Domain

```
Domain: https://task-pilot-ai-ashen.vercel.app
```

⚠️ **Important**:
- Include the `https://` protocol
- Match the exact domain (case-sensitive)
- Do NOT include `/chatkit` or any path

### 1c. Generate and Save Domain Key

1. OpenAI generates a domain key (looks like: `sk_test_...`)
2. **Copy and save this key securely**
3. You'll need this in Step 2

**Domain Key Format**: `sk_test_[alphanumeric_string]`

---

## Step 2: Configure Environment Variables in Vercel

Set environment variables so your production app has the correct API endpoints and domain key.

### 2a. Open Vercel Dashboard

1. Go to: https://vercel.com/dashboard
2. Find your project (likely named `TaskPilotAI` or similar)
3. Click the project name

### 2b. Navigate to Environment Variables

1. Click **Settings** tab (top navigation)
2. Left sidebar → **Environment Variables**
3. You'll see existing variables (like `NEXT_PUBLIC_API_URL`)

### 2c. Add Production Variables

Click **Add** and create two new variables for **Production** environment:

| Name | Value | Notes |
|------|-------|-------|
| `NEXT_PUBLIC_API_URL` | `https://your-backend-url.com` | Your production backend API URL (e.g., Railway, Render, custom) |
| `NEXT_PUBLIC_CHATKIT_DOMAIN_KEY` | `sk_test_[your_key]` | The domain key from OpenAI (Step 1c) |

**Example**:
```
NEXT_PUBLIC_API_URL = https://taskpilot-api.railway.app
NEXT_PUBLIC_CHATKIT_DOMAIN_KEY = sk_test_YOUR_DOMAIN_KEY_HERE
```

### 2d. Set Environment for Production

Make sure to set these variables for **Production** environment only:
- ✅ Production
- ❌ Preview
- ❌ Development (use .env.local locally)

---

## Step 3: Update Backend CORS Configuration

Your backend needs to allow requests from your Vercel domain.

### 3a. Update backend/main.py

```python
from fastapi.middleware.cors import CORSMiddleware

# Configure allowed origins
allowed_origins = [
    "http://localhost:3000",  # Local development
    "http://localhost:8000",  # Local development
    "https://task-pilot-ai-ashen.vercel.app",  # Your production
    "https://your-custom-domain.com",  # If you have a custom domain
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 3b. Redeploy Backend

If your backend is on Railway, Render, or similar:

```bash
# Option 1: Git push (auto-deploys)
git add backend/main.py
git commit -m "fix: Add Vercel domain to CORS allowed origins"
git push

# Option 2: Manual deployment (see your hosting platform)
# Railway: Automatic on git push
# Render: Automatic on git push
# Heroku: heroku git:push heroku main
```

---

## Step 4: Redeploy Frontend to Apply Environment Variables

Push a new deployment to apply the environment variables.

### 4a. Push to GitHub

```bash
cd frontend
git add .
git commit -m "feat: Add ChatKit production configuration"
git push
```

### 4b. Vercel Auto-Deploys

Once you push:
1. Vercel automatically detects the push
2. Starts a new deployment
3. You can watch progress in Vercel Dashboard
4. Deployment completes in 1-2 minutes

### 4c. Verify Deployment

Go to Vercel Dashboard:
1. Click your project
2. Click **Deployments** tab
3. Look for the latest deployment (should say "✓ Ready")

---

## Step 5: Test Production ChatKit Integration

### 5a. Visit Production ChatKit

Open in browser:
```
https://task-pilot-ai-ashen.vercel.app/chatkit
```

### 5b. Verify ChatKit Loads

You should see:
- ✅ ChatKit header: "TaskPilot AI Chat"
- ✅ Input field: "Ask me to manage your tasks..."
- ✅ No error messages
- ✅ Chat interface ready

### 5c. Check Browser Console

Open DevTools (F12) → Console tab

**Should see**:
```
Creating new ChatKit session
Got ChatKit session: ses_...
ChatKit is ready
```

**Should NOT see**:
```
❌ CORS error
❌ Failed to get session
❌ Domain not registered
❌ Unauthorized
```

### 5d. Send Test Message

1. Type a test message: `"Hello"`
2. Press Enter or click Send
3. Verify:
   - ✅ Message appears in chat
   - ✅ Agent responds
   - ✅ No error messages

---

## Environment Variables Reference

### What Each Variable Does

| Variable | Purpose | Example |
|----------|---------|---------|
| `NEXT_PUBLIC_API_URL` | Backend URL for API calls | `https://taskpilot-api.railway.app` |
| `NEXT_PUBLIC_CHATKIT_DOMAIN_KEY` | Domain key from OpenAI | `sk_test_abc123...` |

### Local vs Production

**Local Development** (frontend/.env.local):
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
# NEXT_PUBLIC_CHATKIT_DOMAIN_KEY not needed (localhost doesn't require registration)
```

**Production** (Set in Vercel Dashboard):
```bash
NEXT_PUBLIC_API_URL=https://your-backend-url.com
NEXT_PUBLIC_CHATKIT_DOMAIN_KEY=sk_test_your_key_from_openai
```

### Backend Configuration

**backend/.env**:
```bash
OPENAI_API_KEY=sk_test_your_openai_key
CHATKIT_WORKFLOW_ID=wf_6946b383d368819081b556e6e5fa66330d48d0c9ea4fccd8
```

---

## Troubleshooting

### Problem: "Domain not registered" error

**Cause**: Domain not registered in OpenAI allowlist

**Solution**:
```
1. Go to: https://platform.openai.com/settings/organization/security/domain-allowlist
2. Verify domain is listed: https://task-pilot-ai-ashen.vercel.app
3. If not listed, add it (see Step 1)
4. Wait 5 minutes for changes to propagate
5. Clear browser cache (Ctrl+Shift+Delete)
6. Reload page
```

### Problem: ChatKit works locally but fails on production

**Causes**:
- Domain not registered
- Environment variable not set
- CORS blocking the request
- Backend API unreachable

**Debug Steps**:
```
1. Check browser console (F12 → Console)
   Look for CORS errors or network failures

2. Check Vercel environment variables
   Settings → Environment Variables → Production
   Verify NEXT_PUBLIC_CHATKIT_DOMAIN_KEY is set

3. Check OpenAI domain allowlist
   Visit: https://platform.openai.com/settings/organization/security/domain-allowlist
   Verify your domain is registered

4. Test backend connectivity
   Open browser console, run:
   fetch('https://your-backend-url.com/health')
     .then(r => r.json())
     .then(console.log)
   Should return JSON response

5. Check backend CORS configuration
   Verify main.py includes your Vercel domain in allowed_origins
```

### Problem: "Failed to get ChatKit session"

**Causes**:
- Backend API unreachable
- OpenAI API key invalid
- Workflow ID misconfigured

**Solution**:
```bash
# Test backend endpoint directly
curl -X POST https://your-backend-url.com/api/chatkit/sessions \
  -H "Content-Type: application/json"

# Should return:
{
  "status": "success",
  "data": {
    "client_secret": "cs_...",
    "session_id": "ses_..."
  }
}

# If error, check:
1. Backend is running
2. OPENAI_API_KEY is valid
3. CHATKIT_WORKFLOW_ID is correct
```

### Problem: CORS error in browser console

**Error**: `Access to XMLHttpRequest blocked by CORS policy`

**Solution**:
```python
# Update backend/main.py CORS configuration
# Add your Vercel domain to allowed_origins:

allowed_origins = [
    "https://task-pilot-ai-ashen.vercel.app"
]

# Then redeploy backend
git push
```

---

## Verification Checklist

After deployment, verify all checks pass:

- [ ] Domain registered in OpenAI allowlist
- [ ] Environment variables set in Vercel Dashboard
- [ ] Backend CORS configuration updated
- [ ] Frontend redeployed (new deployment in Vercel)
- [ ] ChatKit page loads: https://task-pilot-ai-ashen.vercel.app/chatkit
- [ ] Browser console shows "Got ChatKit session"
- [ ] Can send message and receive response
- [ ] No CORS errors in browser console
- [ ] No authentication errors
- [ ] Backend responding to session requests

---

## Security Notes

### What's Exposed vs Protected

| Component | Exposure | Details |
|-----------|----------|---------|
| Domain Key | **Frontend** | Part of public JavaScript (necessary for ChatKit) |
| Client Secret | **Frontend** | Returned from backend (temporary, session-specific) |
| OpenAI API Key | **Backend Only** | Never exposed to frontend (secure) |
| Workflow ID | **Backend Only** | Never exposed to frontend (secure) |

### Best Practices

1. **Domain Key**: Safe to be in frontend code (domain-specific)
2. **API Key**: Never commit to repository, use environment variables
3. **Workflow ID**: Keep in backend .env for security
4. **CORS**: Only allow trusted domains

---

## Monitoring Production

### Logs to Check

**Vercel Logs**:
- Dashboard → Deployments → Click latest → Logs tab
- Look for errors during deployment

**Backend Logs**:
- Check your hosting platform (Railway, Render, etc.)
- Look for errors when session endpoints are called

### Testing Commands

```bash
# Test domain registration
curl https://api.openai.com/v1/info

# Test backend API
curl -X POST https://your-backend-url/api/chatkit/sessions

# Test frontend connectivity
curl https://task-pilot-ai-ashen.vercel.app/chatkit
```

---

## Rollback Steps (If Something Breaks)

If production ChatKit breaks:

### Quick Fix (Revert Environment Variable)

```
1. Go to Vercel Dashboard
2. Settings → Environment Variables
3. Find NEXT_PUBLIC_CHATKIT_DOMAIN_KEY
4. Click delete or disable
5. Vercel auto-redeployes
6. Production reverts to previous state
```

### Full Rollback

```bash
# Revert last commit
git revert HEAD

# Push to trigger redeploy
git push

# Vercel automatically deploys the reverted version
```

---

## Next Steps

After production ChatKit is working:

1. **Phase 3b**: Add conversation persistence to database
2. **Phase 3c**: Add Agents SDK for tool orchestration
3. **Phase 3d**: Add MCP tools for task operations
4. **Phase 3e**: Add streaming responses

For now, basic ChatKit integration in production is ✅ complete!

---

**Last Updated**: December 20, 2025
**Your Vercel App**: https://task-pilot-ai-ashen.vercel.app
**Status**: Ready for production ChatKit deployment
