# ✅ TaskPilotAI Integration Testing Checklist

**Last Updated**: December 14, 2025
**Backend Status**: ✅ Live on Render at https://taskpilot-api-5l18.onrender.com
**Frontend Status**: 🚀 Ready to deploy to Vercel
**Database Status**: ✅ Connected to Neon PostgreSQL

---

## PRE-DEPLOYMENT TESTING (Do This Before Deploying Frontend)

### 1. Backend Health Checks

```bash
# Test 1: Health endpoint (no auth required)
curl -s https://taskpilot-api-5l18.onrender.com/health

# Expected Response:
# {"status":"ok","message":"TaskPilotAI API is running"}

# Test 2: Check backend is accessible
curl -I https://taskpilot-api-5l18.onrender.com/health
# Expected: HTTP/1.1 200 OK
```

**Checklist:**
- [ ] Health endpoint returns 200
- [ ] No connection timeout
- [ ] JSON response is valid

### 2. Database Connection Verification

**Check Backend Logs in Render Dashboard:**
1. Go to https://dashboard.render.com
2. Select `taskpilot-api` service
3. Click **Logs** tab
4. Look for: `Application startup complete`
5. Should NOT see: `sqlalchemy.exc.DatabaseError` or connection errors

**Checklist:**
- [ ] "Application startup complete" in logs
- [ ] No database connection errors
- [ ] No SQLModel/SQLAlchemy errors

### 3. Test Authentication Endpoints

#### Signup Endpoint Test
```bash
curl -X POST https://taskpilot-api-5l18.onrender.com/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test.user@example.com",
    "password": "SecurePassword123!",
    "name": "Test User"
  }'

# Expected Response (200 OK):
# {
#   "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
#   "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
#   "token_type": "bearer"
# }
```

**Checklist:**
- [ ] Signup returns 200 OK
- [ ] access_token is a valid JWT
- [ ] refresh_token is present
- [ ] token_type is "bearer"

#### Signin Endpoint Test
```bash
curl -X POST https://taskpilot-api-5l18.onrender.com/auth/signin \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test.user@example.com",
    "password": "SecurePassword123!"
  }'

# Expected Response (200 OK):
# {
#   "access_token": "...",
#   "refresh_token": "...",
#   "token_type": "bearer"
# }
```

**Checklist:**
- [ ] Signin returns 200 OK
- [ ] access_token is a valid JWT
- [ ] Can signin with correct credentials
- [ ] Signin fails (401) with wrong password

### 4. Test Protected Task Endpoints

#### Create Task
```bash
# Replace TOKEN with actual JWT from signup/signin
TOKEN="your-access-token-here"

curl -X POST https://taskpilot-api-5l18.onrender.com/tasks \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Buy groceries",
    "description": "Milk, eggs, bread"
  }'

# Expected Response (200 OK):
# {
#   "id": "uuid-string",
#   "user_id": "uuid-string",
#   "title": "Buy groceries",
#   "description": "Milk, eggs, bread",
#   "completed": false,
#   "created_at": "2025-12-14T00:00:00Z",
#   "updated_at": "2025-12-14T00:00:00Z"
# }
```

**Checklist:**
- [ ] Create task returns 200 OK
- [ ] Task has unique ID
- [ ] Task has user_id (from JWT)
- [ ] Timestamps are ISO 8601 format
- [ ] Create task without auth returns 401

#### Get Tasks
```bash
TOKEN="your-access-token-here"

curl -X GET https://taskpilot-api-5l18.onrender.com/tasks \
  -H "Authorization: Bearer $TOKEN"

# Expected Response (200 OK):
# [
#   {"id": "...", "title": "Buy groceries", ...},
#   {"id": "...", "title": "Walk dog", ...}
# ]
```

**Checklist:**
- [ ] Get tasks returns 200 OK
- [ ] Returns array of tasks
- [ ] Only returns user's own tasks (user isolation)
- [ ] Without auth returns 401

#### Update Task
```bash
TOKEN="your-access-token-here"
TASK_ID="uuid-of-task"

curl -X PUT https://taskpilot-api-5l18.onrender.com/tasks/$TASK_ID \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated title",
    "description": "Updated description"
  }'

# Expected Response (200 OK):
# {"id": "...", "title": "Updated title", ...}
```

**Checklist:**
- [ ] Update task returns 200 OK
- [ ] Updated fields reflect changes
- [ ] created_at remains unchanged
- [ ] updated_at changes
- [ ] Can't update other user's tasks (403)

#### Delete Task
```bash
TOKEN="your-access-token-here"
TASK_ID="uuid-of-task"

curl -X DELETE https://taskpilot-api-5l18.onrender.com/tasks/$TASK_ID \
  -H "Authorization: Bearer $TOKEN"

# Expected Response: 204 No Content
```

**Checklist:**
- [ ] Delete task returns 204 No Content
- [ ] Task no longer appears in GET /tasks
- [ ] ID is not reused for new tasks
- [ ] Can't delete other user's tasks (403)

#### Toggle Completion
```bash
TOKEN="your-access-token-here"
TASK_ID="uuid-of-task"

curl -X PATCH https://taskpilot-api-5l18.onrender.com/tasks/$TASK_ID/complete \
  -H "Authorization: Bearer $TOKEN"

# Expected Response (200 OK):
# {"id": "...", "completed": true, ...}
```

**Checklist:**
- [ ] Completion toggle returns 200 OK
- [ ] completed field changes (false → true, true → false)
- [ ] updated_at changes
- [ ] created_at unchanged

---

## FRONTEND LOCAL TESTING (Before Deploying to Vercel)

### 1. Frontend Build Test

```bash
cd /home/bilal/TaskPilotAI/frontend

# Install dependencies
npm install

# Type check
npm run type-check

# Build for production
npm run build

# Expected: "✓ Next.js compilation successful"
```

**Checklist:**
- [ ] npm install completes without errors
- [ ] npm run type-check passes (0 TypeScript errors)
- [ ] npm run build succeeds
- [ ] No warnings in build output
- [ ] .next folder created successfully

### 2. Frontend Local Development Test

```bash
cd /home/bilal/TaskPilotAI/frontend

# Ensure .env.local exists with correct backend URL
echo "NEXT_PUBLIC_API_URL=https://taskpilot-api-5l18.onrender.com" > .env.local

# Start dev server
npm run dev

# Visit http://localhost:3000 in browser
```

**Checklist:**
- [ ] Dev server starts without errors
- [ ] Page loads at http://localhost:3000
- [ ] No console errors (F12 → Console)
- [ ] Signin page displays correctly
- [ ] Signup page displays correctly

### 3. Frontend-Backend Integration (Local)

#### Test Signup Flow
1. Visit http://localhost:3000
2. Click "Sign Up"
3. Enter email: `test@example.com`
4. Enter password: `Test123!`
5. Enter name: `Test User`
6. Click "Sign Up" button

**Expected Behavior:**
- Form submits
- No console errors
- Redirects to dashboard
- Browser shows task list (initially empty)

**Checklist:**
- [ ] Signup form submits
- [ ] Backend accepts signup request
- [ ] Tokens stored in localStorage (check DevTools → Application → localStorage)
- [ ] Redirects to /dashboard
- [ ] Dashboard loads without errors

#### Test Create Task
1. On dashboard, fill in task form
2. Title: "Test Task"
3. Description: "This is a test"
4. Click "Create Task"

**Expected Behavior:**
- Task appears in list
- No console errors
- Form clears for next task

**Checklist:**
- [ ] Task appears in list immediately
- [ ] Task shows correct title and description
- [ ] Timestamps display correctly
- [ ] No API error messages
- [ ] Task persists (visible in backend database)

#### Test Edit Task
1. Click on task to edit
2. Change title: "Updated Task"
3. Click "Update"

**Expected Behavior:**
- Task updates in list
- No console errors

**Checklist:**
- [ ] Task title updates immediately
- [ ] No API errors
- [ ] updated_at timestamp changes
- [ ] created_at remains same

#### Test Delete Task
1. Click delete button on task
2. Confirm deletion

**Expected Behavior:**
- Task disappears from list
- No console errors

**Checklist:**
- [ ] Task removed from list
- [ ] No API errors
- [ ] Backend confirms deletion

#### Test Complete/Uncomplete
1. Click checkbox on task
2. Task should mark as complete

**Expected Behavior:**
- Checkbox toggles
- Task appears in completed section (if filtered)

**Checklist:**
- [ ] Checkbox toggles state
- [ ] completed field updates
- [ ] Task moves to completed section
- [ ] Can uncomplete task

#### Test Filter
1. Click "Pending" filter
2. Only pending tasks show
3. Click "Completed" filter
4. Only completed tasks show
5. Click "All" filter
6. All tasks show

**Checklist:**
- [ ] Pending filter works
- [ ] Completed filter works
- [ ] All filter shows everything
- [ ] No console errors

#### Test Logout
1. Click "Logout" button
2. Redirects to signin page
3. Tokens cleared from localStorage

**Checklist:**
- [ ] Logout clears tokens
- [ ] Redirects to /signin
- [ ] Can't access /dashboard without login
- [ ] localStorage is empty

#### Test Multi-User Isolation
1. Signup as user1
2. Create 3 tasks as user1
3. Logout
4. Signup as user2
5. Create 2 tasks as user2
6. User2 should see only 2 tasks (not user1's 3 tasks)

**Checklist:**
- [ ] User1 tasks not visible to user2
- [ ] Each user sees only their own tasks
- [ ] Backend enforces isolation (try manually accessing user1's tasks via API)
- [ ] No data leakage between users

### 4. Browser Console Checks

Open DevTools (F12) while testing:

**Console Tab:**
- [ ] No red error messages
- [ ] No yellow warnings (OK if Next.js dev warnings)
- [ ] No 401/403/500 status code errors

**Network Tab:**
- [ ] All API calls return 200/201/204 status
- [ ] No 404 errors
- [ ] Backend URL matches configured API_URL
- [ ] Authorization headers present on protected routes

**Application Tab → localStorage:**
- [ ] After login: access_token is present
- [ ] After login: refresh_token is present
- [ ] After logout: tokens are cleared

---

## VERCEL DEPLOYMENT TESTING

### After Deploying Frontend to Vercel:

#### 1. Visit Frontend URL
```bash
# After deployment, Vercel provides: https://taskpilot-[id].vercel.app

# Visit this URL in browser
# Expected: Signin page loads without errors
```

**Checklist:**
- [ ] Frontend URL loads
- [ ] No "Cannot connect to backend" errors
- [ ] Signin page displays
- [ ] No console errors

#### 2. Test Signup on Vercel
1. Visit frontend URL
2. Click "Sign Up"
3. Enter new credentials
4. Click "Sign Up"

**Checklist:**
- [ ] Signup succeeds
- [ ] Redirects to dashboard
- [ ] Can create/edit/delete tasks
- [ ] No CORS errors in console

#### 3. Test Task Operations on Vercel
1. Create task: "Vercel Test Task"
2. Edit task: Change description
3. Mark complete: Click checkbox
4. Delete task: Click delete button

**Checklist:**
- [ ] All operations work on Vercel
- [ ] No network errors
- [ ] Backend URL is correct: https://taskpilot-api-5l18.onrender.com

#### 4. Test User Isolation on Vercel
1. Create user1, add tasks
2. Logout
3. Create user2, add different tasks
4. User2 sees only their tasks

**Checklist:**
- [ ] User isolation works in production
- [ ] No data leakage
- [ ] Each user's data is private

#### 5. Test Persistence
1. Create task on Vercel
2. Logout
3. Login again
4. Task still exists

**Checklist:**
- [ ] Data persists across sessions
- [ ] Neon database storing data
- [ ] No data loss on logout/login

---

## ERROR SCENARIOS TO TEST

### Test Invalid Authentication
```bash
# Try accessing protected endpoint without token
curl https://taskpilot-api-5l18.onrender.com/tasks

# Expected: 401 Unauthorized
```

**Checklist:**
- [ ] Returns 401 without token
- [ ] Returns 401 with invalid token
- [ ] Frontend shows error message

### Test Invalid Credentials
1. Visit frontend
2. Signin with wrong password
3. Should show error message

**Checklist:**
- [ ] Shows "Invalid credentials" error
- [ ] Does not create tokens
- [ ] Does not redirect

### Test Cross-User Access
Try manually accessing another user's task (if you know the ID):

```bash
# Assume you're user1, trying to access user2's task
TOKEN="user1-token"
TASK_ID="user2-task-id"

curl https://taskpilot-api-5l18.onrender.com/tasks/$TASK_ID \
  -H "Authorization: Bearer $TOKEN"

# Expected: 403 Forbidden or empty response
```

**Checklist:**
- [ ] Can't access other user's tasks
- [ ] Returns 403 or 404
- [ ] Backend enforces isolation

### Test Expired Token
1. Wait for token to expire (7 days in production)
2. Try making API request
3. Should get 401 Unauthorized

**Checklist:**
- [ ] Expired tokens rejected
- [ ] Frontend handles 401 gracefully
- [ ] User can login again with refresh token

---

## PERFORMANCE TESTING

### Backend Response Times
```bash
# Time how long requests take
time curl https://taskpilot-api-5l18.onrender.com/health

# Expected: < 200ms on Render free tier (may be 500ms+ if service was sleeping)
```

**Checklist:**
- [ ] Health check: < 500ms
- [ ] Signup: < 1 second
- [ ] Get tasks: < 1 second
- [ ] Create task: < 1 second

### Frontend Page Load
Use browser DevTools Lighthouse:
1. Visit frontend URL
2. Open DevTools (F12)
3. Go to Lighthouse tab
4. Click "Generate report"

**Checklist:**
- [ ] Lighthouse score > 50 (acceptable for dev)
- [ ] No critical performance issues
- [ ] Page interactive in < 3 seconds

### Database Performance
Monitor Neon dashboard:
1. Go to https://console.neon.tech
2. Check "Monitoring" section
3. Look at query times

**Checklist:**
- [ ] Database queries < 100ms
- [ ] No slow query warnings
- [ ] Connection pool healthy

---

## DEPLOYMENT READINESS CHECKLIST

### Backend ✅
- [x] Deployed to Render
- [x] Health endpoint working
- [x] Database connected
- [x] Authentication working
- [x] CORS configured
- [x] Environment variables set
- [x] Logs clean (no errors)

### Frontend 🚀
- [ ] Build succeeds locally
- [ ] Type checking passes
- [ ] All tests pass
- [ ] Environment variables correct
- [ ] Ready to deploy to Vercel

### Integration ✅
- [ ] Backend and frontend communicate
- [ ] Signup/signin works end-to-end
- [ ] Task CRUD works end-to-end
- [ ] User isolation enforced
- [ ] No CORS errors
- [ ] No console errors

### Documentation ✅
- [x] RENDER_BACKEND_MANAGEMENT.md - Complete
- [x] VERCEL_DEPLOYMENT_GUIDE.md - Complete
- [x] INTEGRATION_TESTING_CHECKLIST.md - This file
- [ ] Demo video recorded (after Vercel deployment)
- [ ] Hackathon submission ready

---

## NEXT STEPS

### 1. Complete Pre-Deployment Tests (NOW)
- [ ] Run all tests in "PRE-DEPLOYMENT TESTING" section
- [ ] Verify backend is working as expected

### 2. Deploy Frontend to Vercel
Follow: `/VERCEL_DEPLOYMENT_GUIDE.md`
- [ ] Create Vercel account
- [ ] Import GitHub repo
- [ ] Set root directory: `frontend`
- [ ] Set environment variable: `NEXT_PUBLIC_API_URL=https://taskpilot-api-5l18.onrender.com`
- [ ] Deploy

### 3. Post-Deployment Testing
- [ ] Run all tests in "VERCEL DEPLOYMENT TESTING" section
- [ ] Verify everything works end-to-end

### 4. Final Verification
- [ ] Both URLs working
- [ ] All features functional
- [ ] No errors in production
- [ ] User isolation verified
- [ ] Data persistence confirmed

### 5. Record Demo Video
Record 90-second video showing:
- Signup flow
- Create tasks
- Edit tasks
- Delete tasks
- Filter tasks
- Multi-user isolation (optional)

### 6. Submit to Hackathon
- [ ] Gather both URLs
- [ ] Include demo video
- [ ] Submit to hackathon form

---

## TROUBLESHOOTING DURING TESTING

### Frontend Can't Connect to Backend
**Problem**: "Failed to fetch" or "CORS error"
**Solution**:
1. Check NEXT_PUBLIC_API_URL is correct
2. Verify Render backend is running
3. Check Render CORS_ORIGINS includes frontend domain
4. Restart both frontend and backend

### Task Data Not Persisting
**Problem**: Tasks disappear after logout
**Solution**:
1. Check Neon database connection in backend logs
2. Verify DATABASE_URL is correct
3. Check Neon dashboard for storage issues
4. Check backend migrations ran (SQLModel auto-creates tables)

### Signup/Signin Returns 500 Error
**Problem**: Server error during authentication
**Solution**:
1. Check JWT_SECRET environment variable is set
2. Check BETTER_AUTH_SECRET is configured
3. Verify database connection is working
4. Check backend logs for specific error

### Tasks Not Filtering Correctly
**Problem**: Pending/completed filters not working
**Solution**:
1. Verify completed field is boolean in database
2. Check filter logic in frontend
3. Test API endpoints directly with curl
4. Check query parameters are correct

---

## TIPS FOR SUCCESSFUL TESTING

1. **Test Systematically**: Go through each section in order
2. **Document Issues**: Note any errors or unexpected behavior
3. **Check Logs**: Always look at browser console and backend logs
4. **Test Edge Cases**: Try wrong passwords, missing fields, etc.
5. **Verify Isolation**: Always test multi-user scenarios
6. **Monitor Performance**: Watch for slow responses on free tier
7. **Use DevTools**: Browser DevTools are your best friend for debugging

---

## QUICK REFERENCE

**Backend URL**: https://taskpilot-api-5l18.onrender.com
**Database**: Neon PostgreSQL
**Frontend (Local)**: http://localhost:3000
**Frontend (Production)**: https://taskpilot-[id].vercel.app (TBD)

**Testing Tools**:
- curl: Command-line API testing
- Browser DevTools: Network, console, storage debugging
- Render Dashboard: Backend logs and monitoring
- Vercel Dashboard: Frontend logs and monitoring
- Neon Dashboard: Database monitoring

**Key Files**:
- RENDER_BACKEND_MANAGEMENT.md - Backend deployment guide
- VERCEL_DEPLOYMENT_GUIDE.md - Frontend deployment guide
- INTEGRATION_TESTING_CHECKLIST.md - This file

---

**Status**: Ready for Frontend Deployment to Vercel ✅
**Last Updated**: December 14, 2025
**Backend Verified**: Yes ✅
**Next Action**: Deploy Frontend to Vercel
