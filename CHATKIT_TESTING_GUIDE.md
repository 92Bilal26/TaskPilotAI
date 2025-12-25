# ChatKit Testing Guide

## Phase 1: Verify ChatKit Page Loads

### Step 1: Hard Refresh Frontend (Clear Cache)

The frontend configuration has been updated. You need to clear the cache to load the new version.

**In your browser:**

1. Navigate to `http://localhost:3000/chatkit`
2. Press `Ctrl+Shift+R` (Windows/Linux) or `Cmd+Shift+R` (Mac) to hard refresh
3. Wait for page to load (you should see a loading message first)

### Step 2: Check Browser Console for Errors

After the page loads:

1. Open Developer Tools: Press `F12` or `Right-click → Inspect`
2. Go to **Console** tab
3. Look for these messages in order:

   **✅ EXPECTED (should see these):**
   - `ChatKitWidget mounted with config: ...`
   - `ChatKit is ready!`
   - `Got ChatKit session: { session_id: ..., conversation_id: ... }`
   - No red error messages

   **❌ UNEXPECTED (should NOT see these):**
   - `Unrecognized key: 'fetch'` ← If you see this, cache wasn't cleared
   - `Invalid client secret format` ← Session endpoint issue
   - `Error getting ChatKit session` ← Authorization or API issue

### Step 3: Verify ChatKit UI Elements

After page loads, verify you see:

- [ ] **Header**: "TaskPilot AI Chat" with subtitle "Powered by OpenAI ChatKit"
- [ ] **Message Input Field**: At the bottom with placeholder "Ask me to add, update, or delete tasks..."
- [ ] **History Button**: Conversation switcher (💬 button showing conversation count)
- [ ] **Back Button**: To return to dashboard
- [ ] **Chat Area**: Empty initially, waiting for first message

**If any of these are missing**, check console for errors and skip to Troubleshooting section.

---

## Phase 2: Test Chatbot Functionality

### Test 1: Create Task via Chatbot

**Objective:** Verify that the chatbot can create a task using natural language

**Steps:**

1. Click in the message input field at the bottom
2. Type: `Create a task to buy groceries`
3. Press Enter or click Send
4. Wait for response (look for "Assistant is responding..." in console)

**Expected Result:**
- ✅ Message appears in chat with your text
- ✅ Assistant responds with task creation confirmation
- ✅ Task appears in backend database
- ✅ Confirmation includes task ID and status

**Check Backend:**
```bash
sqlite3 /home/bilal/TaskPilotAI/taskpilot.db "SELECT id, title, completed FROM task WHERE title LIKE '%grocery%';"
```

Should show: `1 | Buy groceries | 0`

---

### Test 2: List Tasks via Chatbot

**Objective:** Verify that the chatbot can list all tasks

**Steps:**

1. In ChatKit, type: `Show me all my tasks`
2. Press Enter
3. Wait for response

**Expected Result:**
- ✅ Assistant lists all your tasks
- ✅ Shows task IDs, titles, completion status
- ✅ Includes the task you just created

---

### Test 3: Update/Edit Task via Chatbot

**Objective:** Verify that the chatbot can update an existing task

**Steps:**

1. In ChatKit, type: `Update task 1 to Buy groceries and cook dinner`
2. Press Enter

**Expected Result:**
- ✅ Assistant confirms the task update
- ✅ Original task description changed
- ✅ `updated_at` timestamp updated

**Check Backend:**
```bash
sqlite3 /home/bilal/TaskPilotAI/taskpilot.db "SELECT id, title, updated_at FROM task WHERE id = 1;"
```

---

### Test 4: Complete Task via Chatbot

**Objective:** Verify that the chatbot can mark a task as complete

**Steps:**

1. In ChatKit, type: `Mark task 1 as complete`
2. Press Enter

**Expected Result:**
- ✅ Assistant confirms task completion
- ✅ Task shows as completed in conversation
- ✅ `completed` field set to 1 in database

**Check Backend:**
```bash
sqlite3 /home/bilal/TaskPilotAI/taskpilot.db "SELECT id, title, completed FROM task WHERE id = 1;"
```

Should show: `1 | Buy groceries and cook dinner | 1`

---

### Test 5: Delete Task via Chatbot

**Objective:** Verify that the chatbot can delete a task

**Steps:**

1. Create another test task: `Create a task to test deletion`
2. Then type: `Delete the test deletion task`
3. Press Enter

**Expected Result:**
- ✅ Assistant confirms task deletion
- ✅ Task ID no longer appears in list tasks response
- ✅ Task removed from database

---

## Phase 3: Conversation Persistence

### Test 6: Conversation Switching

**Objective:** Verify that you can switch between conversations and history is preserved

**Steps:**

1. Look at header - you should see a button showing `💬 N` (where N is number of conversations)
2. Click the conversation switcher button
3. You should see a dropdown with:
   - Current conversation (highlighted)
   - Previous conversations (if any)
   - Message count for each

**Expected Result:**
- ✅ Conversation list appears
- ✅ Current conversation is highlighted
- ✅ Can switch between conversations
- ✅ Each conversation preserves its history

---

## Troubleshooting

### Issue: "Unrecognized key: 'fetch'" error

**Solution:**
- Hard refresh the page: `Ctrl+Shift+R`
- Clear localStorage: Open DevTools Console and run:
  ```javascript
  localStorage.clear()
  sessionStorage.clear()
  location.reload()
  ```

### Issue: "Failed to get ChatKit session" error

**Solution:**
1. Check that you're signed in (look for user avatar/name)
2. Verify JWT token exists:
   ```javascript
   localStorage.getItem('access_token')  // Should return a long string
   ```
3. Check backend logs:
   ```bash
   tail -20 /tmp/backend.log
   ```
4. If no token, sign in again from dashboard

### Issue: Message input field not visible

**Solution:**
1. Check console for `TypeError` messages
2. Verify browser zoom is 100% (Ctrl+0)
3. Try different browser (Chrome, Firefox, Edge)
4. Clear browser cache completely:
   - Chrome: Ctrl+Shift+Delete
   - Firefox: Ctrl+Shift+Delete
   - Edge: Ctrl+Shift+Delete

### Issue: ChatKit loads but doesn't respond to messages

**Solution:**
1. Check that OpenAI API key is set:
   ```bash
   echo $OPENAI_API_KEY  # Should show non-empty value
   ```
2. Check backend logs for errors:
   ```bash
   tail -50 /tmp/backend.log | grep -i error
   ```
3. Verify agent initialization in backend:
   ```bash
   curl http://localhost:8000/health
   ```

---

## Success Criteria Checklist

Before proceeding to production, verify:

- [ ] ChatKit page loads at `http://localhost:3000/chatkit`
- [ ] No console errors about configuration
- [ ] "ChatKit is ready!" appears in console
- [ ] Message input field is visible
- [ ] History/conversation switcher is visible
- [ ] Can send a message and receive a response
- [ ] Create task test passes (task appears in database)
- [ ] List tasks test passes (all tasks shown)
- [ ] Update task test passes (task description updated)
- [ ] Complete task test passes (completed flag set)
- [ ] Delete task test passes (task removed from database)
- [ ] Conversation switching works
- [ ] History is preserved across conversations

---

## Next Steps After Testing

**If all tests pass locally:**

1. Update `.env` with Neon PostgreSQL connection:
   ```
   DATABASE_URL=postgresql://user:password@endpoint/database?sslmode=require
   ```

2. Backup current SQLite database:
   ```bash
   cp taskpilot.db taskpilot.db.backup
   ```

3. Create production database tables (Neon will handle schema)

4. Deploy to production:
   - Frontend: Vercel (keep existing deployment)
   - Backend: Render (keep existing deployment)
   - Database: Neon PostgreSQL (new setup)

5. Update environment variables in production:
   - Vercel: `NEXT_PUBLIC_API_URL` → production backend URL
   - Render: `DATABASE_URL` → Neon PostgreSQL

---

## Support

If you encounter any issues:

1. Check the troubleshooting section above
2. Verify backend logs: `tail -50 /tmp/backend.log`
3. Verify frontend logs: Open DevTools Console
4. Check that both services are running:
   ```bash
   ps aux | grep -E "(uvicorn|next)" | grep -v grep
   ```

