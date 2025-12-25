# ChatKit End-to-End Testing Guide

**Objective**: Test the complete flow from frontend (Vercel) to backend (Render) and verify ChatKit integration works

---

## Prerequisites

✅ Backend ChatKit endpoint tested and working
✅ Vercel build completed
✅ Render backend running
✅ OPENAI_API_KEY added to Render environment

---

## Test Scenario: Create Task via ChatKit

### Step 1: Open Vercel App

1. Go to: **https://task-pilot-ai-ashen.vercel.app**
2. Should see login page
3. **Screenshot**: Take screenshot of the page

**Expected**: Clean TaskPilotAI login screen

---

### Step 2: Sign In

1. Enter your credentials
2. Click **Sign In**
3. Wait for dashboard to load

**Expected**: Dashboard loads with tasks visible

---

### Step 3: Find ChatKit Button

1. Look at the **top right** of the dashboard header
2. Should see **"💬 Open Chat"** button (blue)
3. Next to it: **"+ New Task"** button

**Take screenshot** if you see the button

**Expected Result**:
- ✅ Button is visible and blue colored
- ✅ Text says "💬 Open Chat"
- ✅ Button is clickable

**If button is NOT visible**:
- Open **F12** (DevTools)
- Go to **Console** tab
- Look for any red errors
- Report the error

---

### Step 4: Click ChatKit Button

1. Click **"💬 Open Chat"** button
2. Wait 2-3 seconds for ChatKit widget to load

**Expected Result**:
- ✅ Button text changes to "✓ Chat Active" (green)
- ✅ ChatKit widget appears on right side
- ✅ Widget shows "TaskPilot AI Chat" header
- ✅ Input field says "Ask me to manage your tasks..."

**If ChatKit doesn't load**:
- Open **F12** (DevTools)
- Go to **Network** tab
- Look for requests to `/api/v1/chatkit/`
- Check if they return 200 (success) or error
- Report what you see

---

### Step 5: Send Test Message

1. Click in the ChatKit input field
2. Type: **"Add a task to buy groceries"**
3. Press **Enter** or click Send button
4. Wait 3-5 seconds for response

**Expected Result**:
- ✅ Your message appears in chat
- ✅ Loading indicator shows (spinning circle)
- ✅ AI responds with something like: "I've added 'Buy groceries' to your task list"
- ✅ Message appears in chat history

---

### Step 6: Verify Task Was Created

1. Look at the **left side** of the dashboard (Tasks section)
2. Should see a new task: **"Buy groceries"** in the list
3. Task should appear **within 1-2 seconds** (auto-refresh)

**Take screenshot** of both ChatKit and task list

**Expected Result**:
- ✅ New task "Buy groceries" appears in dashboard
- ✅ Task is marked as "Pending" (not completed)
- ✅ Task shows in the "Total Tasks" count
- ✅ Task shows in "Pending" count

**If task doesn't appear**:
- Wait 5 seconds (auto-refresh)
- Manually refresh page (F5)
- Check browser console for errors

---

### Step 7: Create Another Task (Test 2)

1. In ChatKit, type: **"Update the task to also buy milk"**
2. Press Enter
3. Wait for response

**Expected Result**:
- ✅ ChatKit responds with confirmation
- ✅ Dashboard task is updated
- ✅ Task now says "Buy groceries and milk" or similar

---

### Step 8: List All Tasks

1. In ChatKit, type: **"Show me all my tasks"**
2. Press Enter
3. Wait for response

**Expected Result**:
- ✅ ChatKit lists all tasks
- ✅ Shows task count and details
- ✅ Matches what's shown in dashboard

---

### Step 9: Complete a Task

1. In ChatKit, type: **"Mark the groceries task as done"**
2. Press Enter
3. Wait for response

**Expected Result**:
- ✅ ChatKit confirms task completed
- ✅ Dashboard task shows as "Completed" (with checkmark)
- ✅ "Completed" count increases
- ✅ "Pending" count decreases

---

## Success Criteria

All of these must be TRUE:

| Criterion | Status | Notes |
|-----------|--------|-------|
| Vercel app loads | ✅/❌ | Can sign in and see dashboard |
| ChatKit button visible | ✅/❌ | "💬 Open Chat" button appears in header |
| ChatKit widget opens | ✅/❌ | Chat interface appears when button clicked |
| Message sends | ✅/❌ | User message appears in chat |
| AI responds | ✅/❌ | ChatKit returns a response |
| Task created | ✅/❌ | New task appears in dashboard |
| Auto-refresh works | ✅/❌ | Task syncs within 1-2 seconds |
| Multiple tasks work | ✅/❌ | Can create/update multiple tasks |
| Task completion works | ✅/❌ | Can mark tasks as done |

---

## Troubleshooting

### Issue 1: ChatKit button not visible

**Symptoms**: Button doesn't appear in header

**Debug Steps**:
1. Open F12 → Console tab
2. Look for any error messages
3. Run: `localStorage.getItem('access_token')`
4. Should show a token (long string)

**Possible Causes**:
- [ ] Not authenticated (token missing)
- [ ] Build failed (missing files)
- [ ] Hydration mismatch (refresh page)

**Fix**:
- Refresh page (F5)
- Clear cache (Ctrl+Shift+Delete)
- Sign out and sign in again
- Check browser console for errors

---

### Issue 2: ChatKit doesn't load

**Symptoms**: Click button but nothing appears

**Debug Steps**:
1. Open F12 → Network tab
2. Click "💬 Open Chat" button
3. Look for request to `/api/v1/chatkit/sessions`
4. Check response status (200 = good, 4xx/5xx = error)

**Possible Causes**:
- [ ] Backend not responding
- [ ] OPENAI_API_KEY not set in Render
- [ ] CORS error
- [ ] Network timeout

**Fix**:
1. Verify Render backend is running: `curl https://taskpilot-api-5l18.onrender.com/health`
2. Check Render environment variables (OPENAI_API_KEY set?)
3. Restart Render service
4. Check browser console for errors

---

### Issue 3: Task doesn't appear in dashboard

**Symptoms**: ChatKit responds but task doesn't show

**Debug Steps**:
1. Wait 5 seconds (auto-refresh should trigger)
2. Manually refresh page (F5)
3. Check if task exists in database:
   ```bash
   curl -X POST https://taskpilot-api-5l18.onrender.com/api/v2/tasks \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json"
   ```

**Possible Causes**:
- [ ] Auto-refresh not working
- [ ] Task created but user_id mismatch
- [ ] Database not saving

**Fix**:
1. Manually refresh page
2. Check JWT token is valid
3. Check Render logs for database errors

---

### Issue 4: ChatKit message fails

**Symptoms**: Send message but get error

**Debug Steps**:
1. Open F12 → Network tab
2. Look for POST to `/api/v1/chatkit`
3. Check response (should be 200)
4. Look at response body for errors

**Possible Causes**:
- [ ] Backend error
- [ ] Invalid JWT token
- [ ] OPENAI_API_KEY invalid
- [ ] MCP tools failing

**Fix**:
1. Check Render logs
2. Verify OPENAI_API_KEY is correct
3. Restart Render service
4. Check backend error logs

---

## Expected Network Calls

When you use ChatKit, you should see these requests:

```
1. POST /api/v1/chatkit/sessions → 200 OK
   Response: { client_secret, session_id, conversation_id }

2. POST /api/v1/chatkit → 200 OK (streaming)
   Response: SSE events (tool calls, messages, completion)

3. GET /api/v2/tasks → 200 OK
   Response: List of tasks (auto-refresh every 1 second when ChatKit open)
```

---

## Final Checklist

Before declaring success:

- [ ] Vercel app loads and authenticates
- [ ] ChatKit button visible
- [ ] ChatKit widget opens
- [ ] Message sends without error
- [ ] AI responds within 5 seconds
- [ ] Task appears in dashboard within 2 seconds
- [ ] Multiple tasks can be created
- [ ] Tasks can be marked complete
- [ ] Dashboard updates in real-time
- [ ] No errors in browser console
- [ ] No CORS errors
- [ ] No authentication errors
- [ ] Backend responds to all requests

**If ALL checkmarks are TRUE**: 🎉 **Phase 3 ChatKit integration is COMPLETE and READY FOR PRODUCTION!**

---

## Test Scenarios to Try

### Scenario 1: Simple Task Creation
```
User: "Add a task called 'Buy milk'"
Expected: Task created with title "Buy milk"
```

### Scenario 2: Task with Description
```
User: "Create a task - title: Meeting at 2pm, description: Project discussion"
Expected: Task created with both title and description
```

### Scenario 3: Task Listing
```
User: "Show me all my tasks"
Expected: ChatKit lists all tasks with details
```

### Scenario 4: Task Completion
```
User: "Mark my first task as completed"
Expected: Task status changes to completed in dashboard
```

### Scenario 5: Task Deletion
```
User: "Delete the milk task"
Expected: Task removed from dashboard
```

---

**Good luck! Report your test results and any errors you encounter!** 🚀
