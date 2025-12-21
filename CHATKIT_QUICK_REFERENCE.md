# ChatKit Quick Reference

**TL;DR - Get ChatKit Running in 5 Minutes**

---

## 1️⃣ Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

---

## 2️⃣ Set Environment Variables

**Backend** (`backend/.env`):
```
OPENAI_API_KEY=sk_...
CHATKIT_WORKFLOW_ID=wf_6946b383d368819081b556e6e5fa66330d48d0c9ea4fccd8
```

**Frontend** (`frontend/.env.local`):
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 3️⃣ Start Servers

**Terminal 1 - Backend**:
```bash
cd backend
uvicorn main:app --reload --port 8000
```

**Terminal 2 - Frontend**:
```bash
cd frontend
npm run dev
```

---

## 4️⃣ Test ChatKit

Visit: **http://localhost:3000/chatkit**

You should see ChatKit chat interface loading. Type a message and chat with your AI agent!

---

## 📋 What Was Changed

| File | Change |
|------|--------|
| `backend/routes/chatkit.py` | ✅ Added `/sessions` endpoint |
| `frontend/lib/chatkit-config.ts` | ✅ Fixed configuration |
| `frontend/app/layout.tsx` | ✅ Added ChatKit JS script |
| `backend/requirements.txt` | ✅ Added ChatKit SDK |

---

## 🔑 Key Values

| Setting | Value |
|---------|-------|
| **Workflow ID** | `wf_6946b383d368819081b556e6e5fa66330d48d0c9ea4fccd8` |
| **Session URL** | `http://localhost:8000/api/chatkit/sessions` |
| **ChatKit URL** | `http://localhost:3000/chatkit` |

---

## ❓ Not Working?

### ChatKit won't load
```bash
# Check backend is running
curl http://localhost:8000/health
# Should respond: {"status":"ok"...}
```

### "Failed to get session"
```bash
# Check environment variables are set
echo $OPENAI_API_KEY  # Should show: sk_...
echo $CHATKIT_WORKFLOW_ID  # Should show: wf_...
```

### No response from agent
- Check browser console (F12) for errors
- Verify OpenAI API key is valid
- Check backend logs for errors

---

## 📚 Full Docs

- **Detailed Setup**: See `CHATKIT_DEPLOYMENT_GUIDE.md`
- **What Changed**: See `CHATKIT_IMPLEMENTATION_SUMMARY.md`
- **Architecture**: See `CHATKIT_IMPLEMENTATION_COMPLETE.md`

---

## ✅ You're Done!

ChatKit is now integrated. Just:
1. Start the servers
2. Visit the ChatKit page
3. Start chatting!
