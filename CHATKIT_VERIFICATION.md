# ChatKit Verification Checklist

Use this guide to verify ChatKit integration is working correctly.

---

## ✅ Pre-Launch Checks

### 1. Dependencies Installed

```bash
cd backend
pip list | grep openai
```

**Expected output**:
```
openai                    1.12.0 (or higher)
openai-agents             0.1.0 (or higher)
openai-chatkit            0.1.0 (or higher)
```

**If missing**:
```bash
pip install -r requirements.txt
```

---

### 2. Environment Variables Set

**Check backend**:
```bash
cd backend
cat .env | grep -E "OPENAI_API_KEY|CHATKIT_WORKFLOW_ID"
```

**Expected**:
```
OPENAI_API_KEY=sk_...
CHATKIT_WORKFLOW_ID=wf_6946b383d368819081b556e6e5fa66330d48d0c9ea4fccd8
```

**Check frontend**:
```bash
cd frontend
cat .env.local | grep NEXT_PUBLIC_API_URL
```

**Expected**:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

### 3. Files Modified Correctly

```bash
# Check backend routes has /sessions endpoint
grep -n "create_chatkit_session" backend/routes/chatkit.py
# Should find the function definition

# Check frontend config has getClientSecret
grep -n "getClientSecret" frontend/lib/chatkit-config.ts
# Should find the async function

# Check layout has ChatKit script
grep -n "chatkit.js" frontend/app/layout.tsx
# Should find the script tag

# Check requirements has ChatKit SDK
grep "openai-chatkit" backend/requirements.txt
# Should show: openai-chatkit>=0.1.0
```

---

## ✅ Startup Checks

### 4. Backend Starts Successfully

```bash
cd backend
uvicorn main:app --reload --port 8000
```

**Expected output**:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

**If error**: Check OPENAI_API_KEY is valid

---

### 5. Frontend Starts Successfully

In a new terminal:
```bash
cd frontend
npm run dev
```

**Expected output**:
```
  ▲ Next.js 16.0.0
  - Local:        http://localhost:3000
```

**If error**: Check dependencies are installed (`npm install`)

---

## ✅ Runtime Checks

### 6. Health Check Endpoints

**Backend health**:
```bash
curl http://localhost:8000/health
```

**Expected response**:
```json
{"status": "ok", "message": "TaskPilotAI API is running"}
```

**ChatKit health**:
```bash
curl http://localhost:8000/api/v1/chatkit/health
```

**Expected response**:
```json
{"status": "ok", "service": "chatkit"}
```

---

### 7. Session Creation Test

```bash
curl -X POST http://localhost:8000/api/chatkit/sessions \
  -H "Content-Type: application/json"
```

**Expected response**:
```json
{
  "client_secret": "cs_...",
  "session_id": "ses_...",
  "status": "success"
}
```

**If error**:
- Check OPENAI_API_KEY is valid
- Check CHATKIT_WORKFLOW_ID is correct
- Check OpenAI API is accessible

---

### 8. Frontend Can Reach Backend

Open browser console (F12) and run:
```javascript
fetch('http://localhost:8000/health')
  .then(r => r.json())
  .then(console.log)
```

**Expected output**:
```
{status: "ok", message: "TaskPilotAI API is running"}
```

**If error**: Check NEXT_PUBLIC_API_URL is correct

---

## ✅ ChatKit Integration Test

### 9. Navigate to ChatKit Page

Visit: **http://localhost:3000/chatkit**

**Expected to see**:
- ChatKit header: "TaskPilot AI Chat"
- Input field: "Ask me to manage your tasks..."
- Loading spinner (briefly)
- Chat interface

---

### 10. Check Browser Console

Open DevTools (F12) → Console tab

**Should see**:
```
Creating new ChatKit session
Got ChatKit session: ses_...
ChatKit is ready
```

**Should NOT see**:
- Red error messages
- "Failed to get session"
- CORS errors
- Undefined references

---

### 11. Test Sending Message

1. Click in the ChatKit input field
2. Type: "Hello"
3. Press Enter or click Send

**Expected**:
- Message appears in chat
- Agent starts responding
- Response appears in chat
- No error messages

---

### 12. Check Backend Logs

Look at backend terminal where `uvicorn` is running

**Should see**:
```
INFO: POST /api/chatkit/sessions HTTP/1.1
INFO: Creating new ChatKit session
INFO: Created ChatKit session ses_... for user anonymous
INFO: POST /api/v1/chatkit HTTP/1.1
```

---

## ✅ Complete Checklist

- [ ] Dependencies installed (`openai-chatkit` in pip list)
- [ ] OPENAI_API_KEY set in backend/.env
- [ ] CHATKIT_WORKFLOW_ID set to `wf_6946b383d368819081b556e6e5fa66330d48d0c9ea4fccd8`
- [ ] NEXT_PUBLIC_API_URL set to `http://localhost:8000` in frontend/.env.local
- [ ] Backend starts without errors
- [ ] Frontend starts without errors
- [ ] `curl http://localhost:8000/health` returns {"status": "ok"}
- [ ] `curl -X POST http://localhost:8000/api/chatkit/sessions` returns client_secret
- [ ] ChatKit page loads at http://localhost:3000/chatkit
- [ ] Browser console shows "Got ChatKit session"
- [ ] Can send message to agent
- [ ] Agent responds with message
- [ ] Backend logs show session creation
- [ ] No error messages in browser console
- [ ] No error messages in backend logs

---

## 🚀 If All Checks Pass

**Congratulations! ChatKit is working!** 🎉

You can now:
1. Chat with your AI agent
2. Integrate with task management
3. Add custom agents
4. Deploy to production

---

## 🆘 Troubleshooting

### Problem: "Cannot GET /chatkit"

**Solution**: Check frontend is running and route exists
```bash
# Make sure frontend is running with: npm run dev
# Route should auto-exist in frontend/app/chatkit/page.tsx
```

---

### Problem: "Failed to get ChatKit session"

**Solution**: Backend endpoint not working

```bash
# Test endpoint directly
curl -X POST http://localhost:8000/api/chatkit/sessions -v

# Check error details
# If "Unauthorized" - OPENAI_API_KEY invalid
# If "Not Found" - route not registered
# If timeout - backend not running
```

---

### Problem: Agent doesn't respond

**Solution**: Session not created properly

```bash
# Verify session endpoint works
curl -X POST http://localhost:8000/api/chatkit/sessions | jq

# Should see: "client_secret": "cs_..."
# If empty or error - check OPENAI_API_KEY
```

---

### Problem: ChatKit script doesn't load

**Solution**: Check browser network tab

```bash
# In browser DevTools → Network tab
# Look for: https://cdn.platform.openai.com/deployments/chatkit/chatkit.js
# Should be 200 status (success)
# If failed - internet issue or ad blocker
```

---

### Problem: "CORS error"

**Solution**: Frontend and backend don't match

```bash
# Check backend CORS origins in config
# Should include: http://localhost:3000

# Verify in backend/config.py or main.py
# Look for: CORS_ORIGINS
```

---

## 📞 Get More Help

- **Quick Start**: `CHATKIT_QUICK_REFERENCE.md`
- **Detailed Setup**: `CHATKIT_DEPLOYMENT_GUIDE.md`
- **What Changed**: `CHATKIT_IMPLEMENTATION_SUMMARY.md`
- **Architecture**: `CHATKIT_IMPLEMENTATION_COMPLETE.md`

---

**Last Updated**: December 20, 2025
**Status**: Implementation Complete
