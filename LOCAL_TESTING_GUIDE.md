# Local Testing Guide - Phase 3 ChatKit UI Integration

**Test Date**: 2025-12-21
**Test User**: talibebaqi@gmail.com
**Test Password**: 92Bil@l26
**Environment**: Local (http://localhost:3000)
**Backend API**: http://localhost:8000

---

## Test Environment Status

### ✅ Servers Running
- Backend API: http://localhost:8000
  - Status: ✅ Running
  - Health Check: `{"status":"ok","message":"TaskPilotAI API is running"}`

- Frontend UI: http://localhost:3000
  - Status: ✅ Running
  - Framework: Next.js 16.0.7
  - URL: http://localhost:3000

---

## Testing Checklist

### Phase 1: Authentication & Login
- [ ] Open http://localhost:3000 in browser
- [ ] Click "Sign Up" or navigate to sign-up page
- [ ] Create account with test user credentials if needed
- [ ] OR sign in with existing account: `talibebaqi@gmail.com` / `92Bil@l26`
- [ ] Verify successful login (dashboard appears)
- [ ] Check JWT token is stored (check localStorage)

### Phase 2: ChatKit UI Initialization
- [ ] Navigate to ChatKit page/dashboard
- [ ] Verify ChatKit UI component loads
- [ ] Check no errors in browser console
- [ ] Verify conversation history loads (if any previous conversations)
- [ ] Check conversation switcher dropdown appears

### Phase 3: Create Task via ChatBot

**Test Case 1**: Create simple task
```
User Input to ChatBot: "Create a task to buy groceries"
Expected Response:
  - ✓ [Task created confirmation with emoji]
  - Database: Task should be created with:
    - title: "buy groceries"
    - user_id: logged-in user ID
    - status: pending
    - conversation_id: linked to current conversation
```

**Test Case 2**: Create task with description
```
User Input: "Create a task: Review project documents, description is review Q4 progress and provide feedback"
Expected Response:
  - ✓ [Task created confirmation]
  - Database: Task should have:
    - title: "Review project documents"
    - description: "review Q4 progress and provide feedback"
    - user_id: correct user
```

**Checklist**:
- [ ] Message sent appears in ChatKit UI
- [ ] Agent processes message (shows loading)
- [ ] Tool confirmation shows with ✓ emoji
- [ ] Task list widget displays (if list_tasks called)
- [ ] No errors in browser console
- [ ] Backend logs show task creation

### Phase 4: Edit Task via ChatBot

**Test Case 1**: Update task title
```
User Input: "Update the groceries task to say buy groceries and household items"
Expected Response:
  - ✓ [Task updated confirmation]
  - Database: Task title should change
  - Message: "Task updated: buy groceries and household items"
```

**Test Case 2**: Update task description
```
User Input: "Add to the groceries task: also remember to check prices"
Expected Response:
  - ✓ [Task updated confirmation]
  - Description should be updated
```

**Test Case 3**: Mark task as incomplete
```
User Input: "Mark the groceries task as not done"
Expected Response:
  - ✓ [Task updated confirmation]
  - Status changes to pending (if was completed)
```

**Checklist**:
- [ ] Edit command recognized by agent
- [ ] Tool feedback shows update confirmation ✓
- [ ] New values reflected in conversation
- [ ] Task history preserved in conversation
- [ ] No errors occur

### Phase 5: List Tasks via ChatBot

**Test Case 1**: View all tasks
```
User Input: "Show me all my tasks"
Expected Response:
  - 📋 Tasks list ready
  - Card widget displays with list of tasks
  - Shows title, completion status for each
  - Shows emoji (✓ for done, ○ for pending)
```

**Test Case 2**: View pending tasks
```
User Input: "What tasks do I need to do?"
Expected Response:
  - 📋 Tasks list ready
  - Shows only pending/incomplete tasks
  - Format: ○ Task Title
```

**Checklist**:
- [ ] List command triggers tool
- [ ] Card widget renders properly
- [ ] All tasks display with correct status
- [ ] Widget styling is correct
- [ ] No formatting errors

### Phase 6: Complete Task via ChatBot

**Test Case 1**: Mark task as done
```
User Input: "Mark the groceries task as complete"
Expected Response:
  - ✓ [Task marked complete]
  - Chat message confirms: "Task completed: buy groceries"
  - List shows ✓ instead of ○
```

**Test Case 2**: Complete task by ID
```
User Input: "Complete task 1"
Expected Response:
  - ✓ [Task completed confirmation]
  - Status updated in database
```

**Checklist**:
- [ ] Complete command recognized
- [ ] Tool confirmation shows ✓
- [ ] Database is_completed field set to true
- [ ] Conversation shows update
- [ ] Task list reflects completion

### Phase 7: Delete Task via ChatBot

**Test Case 1**: Delete specific task
```
User Input: "Delete the groceries task"
Expected Response:
  - ✓ [Task deleted successfully]
  - Chat message: "Task deleted"
  - Task no longer appears in list
```

**Test Case 2**: Delete task by ID
```
User Input: "Delete task 3"
Expected Response:
  - ✓ [Task deleted confirmation]
  - Database removes record
```

**Checklist**:
- [ ] Delete command recognized
- [ ] Tool confirmation shows ✓
- [ ] Task is removed from database
- [ ] Task no longer in list view
- [ ] Conversation history preserved (message remains)

### Phase 8: Conversation Persistence

**Test Case 1**: Switch conversations
```
Action: Click on different conversation in switcher
Expected:
  - ✓ History loads for selected conversation
  - UI updates with correct messages
  - Conversation ID in sessionStorage changes
```

**Test Case 2**: Reload page and resume conversation
```
Action:
  1. Create some tasks in conversation
  2. Reload page (F5)
Expected:
  - ✓ Same conversation loads automatically
  - ✓ All previous messages display
  - ✓ Task list shows correct state
```

**Checklist**:
- [ ] Conversation switcher dropdown works
- [ ] Clicking conversation loads history
- [ ] Page reload preserves conversation
- [ ] Messages appear in correct order
- [ ] Tool confirmations still display

### Phase 9: User Isolation (Security)

**Test Case 1**: Verify user isolation
```
Action:
  1. Note a conversation ID from browser
  2. Open another user's account (different user)
  3. Try to access first user's conversation via URL manipulation
Expected:
  - ✗ 403 Forbidden or 404 Not Found
  - Cannot see other user's tasks
```

**Checklist**:
- [ ] Cannot access other user's conversations
- [ ] Cannot modify other user's tasks
- [ ] JWT token required for all endpoints
- [ ] User isolation enforced at database level

### Phase 10: Error Handling

**Test Case 1**: Network error handling
```
Action: Stop backend, try to send message
Expected:
  - Error message displays
  - User can retry
  - Graceful error handling (no crash)
```

**Test Case 2**: Invalid input
```
Action: Send command that doesn't make sense to agent
Expected:
  - Agent handles gracefully
  - Returns informative response
  - System doesn't crash
```

**Checklist**:
- [ ] Network errors handled
- [ ] Error messages are clear
- [ ] Retry mechanism works
- [ ] No unhandled exceptions in console

---

## Testing Step-by-Step Manual

### Quick Start Test (5 minutes)

1. **Open frontend**
   ```
   http://localhost:3000
   ```

2. **Sign in**
   - Email: `talibebaqi@gmail.com`
   - Password: `92Bil@l26`

3. **Go to ChatKit**
   - Navigate to chat/ChatKit section
   - Verify ChatKit loads

4. **Create Task**
   - Type: "Create a task called test task"
   - Verify: ✓ confirmation appears

5. **View Tasks**
   - Type: "Show me all my tasks"
   - Verify: 📋 Card widget appears with task

6. **Complete Task**
   - Type: "Mark test task as done"
   - Verify: ✓ confirmation and status updates

7. **Delete Task**
   - Type: "Delete test task"
   - Verify: ✓ confirmation and task disappears

---

## API Endpoints to Test

### User Authentication
```bash
# Check auth status
curl http://localhost:8000/health

# Login (if needed)
curl -X POST http://localhost:8000/api/auth/signin \
  -H "Content-Type: application/json" \
  -d '{"email":"talibebaqi@gmail.com","password":"92Bil@l26"}'
```

### ChatKit Session
```bash
# Create ChatKit session
curl -X POST http://localhost:8000/api/v1/chatkit/sessions \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "Content-Type: application/json"
```

### Task Operations
```bash
# Create task
curl -X POST http://localhost:8000/api/tasks \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Task","description":"Test description"}'

# Get tasks
curl http://localhost:8000/api/tasks \
  -H "Authorization: Bearer <JWT_TOKEN>"

# Update task
curl -X PUT http://localhost:8000/api/tasks/1 \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"title":"Updated Title"}'

# Delete task
curl -X DELETE http://localhost:8000/api/tasks/1 \
  -H "Authorization: Bearer <JWT_TOKEN>"
```

---

## Expected Browser Console Output

### On Successful Operations
```
✓ Message sent
✓ Agent response received
✓ Tool invocation: add_task
✓ Task created with ID: 123
```

### What Should NOT Appear
```
❌ CORS errors
❌ "401 Unauthorized"
❌ "Cannot read properties of undefined"
❌ Network errors (unless testing error handling)
```

---

## Database Verification

### Verify Task Creation
```sql
-- Connect to PostgreSQL and run:
SELECT * FROM message WHERE user_id = 'test-user-id';
SELECT * FROM conversation WHERE user_id = 'test-user-id';
SELECT COUNT(*) as task_count FROM task WHERE user_id = 'test-user-id';
```

---

## Screenshots to Take

- [ ] Login screen
- [ ] Dashboard with ChatKit loaded
- [ ] Create task conversation
- [ ] Task list widget display
- [ ] Edit task conversation
- [ ] Complete task confirmation
- [ ] Delete task confirmation
- [ ] Conversation switcher dropdown
- [ ] Error handling (if applicable)

---

## Common Issues & Solutions

### Issue: Backend Connection Error
**Solution**:
1. Check backend is running: `curl http://localhost:8000/health`
2. Verify CORS is configured
3. Check `.env` file for API URL configuration

### Issue: ChatKit Not Initializing
**Solution**:
1. Check browser console for errors
2. Verify ChatKit API keys in environment
3. Check ChatKit domain configuration

### Issue: Tasks Not Persisting
**Solution**:
1. Verify database connection
2. Check user_id is being set correctly
3. Verify JWT token is valid

### Issue: Messages Not Sending
**Solution**:
1. Check network tab in DevTools
2. Verify backend is processing requests
3. Check agent is configured properly

---

## Success Criteria

✅ **All tests pass if**:
1. User can sign in with provided credentials
2. ChatKit UI loads without errors
3. Can create task via chatbot instruction
4. Can edit task via chatbot instruction
5. Can complete task via chatbot instruction
6. Can delete task via chatbot instruction
7. Can list tasks and see widget
8. Can switch conversations
9. Conversation history persists on reload
10. No cross-user access (security verified)

---

## Next Steps After Local Testing

After confirming all tests pass locally:

1. **Code Review**: Review all changes
2. **Performance Testing**: Load test with multiple concurrent users
3. **Security Audit**: Verify all endpoints require authentication
4. **Staging Deployment**: Deploy to staging environment
5. **UAT**: Have stakeholders test in staging
6. **Production Deployment**: Deploy to production

---

## Sign-Off Checklist

- [ ] All 10 phases tested successfully
- [ ] No errors in browser console
- [ ] No errors in backend logs
- [ ] Database shows correct data
- [ ] User isolation verified
- [ ] Conversation persistence verified
- [ ] All four CRUD operations working (Create, Read, Update, Delete)
- [ ] Ready for production deployment

---

**Local Testing Environment Setup**: ✅ COMPLETE
**Ready for Testing**: ✅ YES

**Backend**: http://localhost:8000
**Frontend**: http://localhost:3000
**Test Credentials**: talibebaqi@gmail.com / 92Bil@l26

Let's begin testing! 🧪
