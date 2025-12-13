# Phase 2 Remaining Tasks - Detailed Breakdown

**Status**: Backend ✅ | Frontend UI ✅ | API Client ✅ | Wiring ⏳
**Due**: December 14, 2025 (4 days)
**Points**: 150

---

## Priority 1: Frontend Component Wiring (5-6 hours) ⏳ START HERE

These tasks wire the frontend UI components to the backend API.

### Task 1.1: Wire Signin Form
**File**: `frontend/app/auth/signin/page.tsx`
**What to do**:
1. Import `apiClient` from `@/lib/api`
2. On form submit, call `await apiClient.signin(email, password)`
3. If success: save token & redirect to `/dashboard`
4. If error: show error message in UI
5. Add loading state while request pending
6. Handle 401 (invalid credentials)

**Acceptance**:
- ✓ User can signin with valid credentials
- ✓ Token saved to localStorage
- ✓ Redirects to dashboard
- ✓ Shows error for invalid credentials
- ✓ Loading spinner shows while submitting

---

### Task 1.2: Wire Signup Form
**File**: `frontend/app/auth/signup/page.tsx`
**What to do**:
1. Import `apiClient` from `@/lib/api`
2. On form submit, call `await apiClient.signup(email, password, name)`
3. If success: save token & redirect to `/dashboard`
4. If error (409 - email exists): show "Email already registered"
5. Add password validation on frontend (length, match)
6. Add loading state while request pending

**Acceptance**:
- ✓ User can signup with valid data
- ✓ Token saved to localStorage
- ✓ Redirects to dashboard
- ✓ Shows error for existing email
- ✓ Validates password requirements
- ✓ Loading spinner shows

---

### Task 1.3: Protect Routes (Auth Guard)
**File**: `frontend/app/layout.tsx` or new middleware
**What to do**:
1. Create a hook `useAuth()` that checks if token exists in localStorage
2. Create `ProtectedRoute` component wrapper
3. Wrap `/dashboard` pages with ProtectedRoute
4. If no token: redirect to `/auth/signin`
5. Check on mount & whenever token changes
6. Handle logout by clearing token

**Acceptance**:
- ✓ Can't access /dashboard without auth
- ✓ Redirects to signin if token missing
- ✓ Can access /dashboard with valid token
- ✓ Logout clears token

---

### Task 1.4: Wire Dashboard Task List
**File**: `frontend/app/dashboard/page.tsx`
**What to do**:
1. On component mount, call `await apiClient.getTasks()`
2. Display tasks in list
3. Add loading spinner while fetching
4. Handle error if fetch fails
5. Show empty state if no tasks
6. Refresh list after task creation/deletion

**Acceptance**:
- ✓ Loads and displays user's tasks
- ✓ Shows spinner while loading
- ✓ Shows empty state
- ✓ Handles errors gracefully

---

### Task 1.5: Wire Task Creation Form
**File**: `frontend/app/dashboard/page.tsx` or component
**What to do**:
1. Import `apiClient.createTask()`
2. On form submit, call `createTask(title, description)`
3. Add to task list if success
4. Show error message if fails
5. Clear form on success
6. Show loading state while submitting

**Acceptance**:
- ✓ Creates task via API
- ✓ Task appears in list immediately
- ✓ Shows success feedback
- ✓ Shows error if creation fails
- ✓ Form clears after success

---

### Task 1.6: Wire Task Update Functionality
**File**: `frontend/components/TaskCard.tsx` or similar
**What to do**:
1. Add edit button/modal to TaskCard
2. On edit submit, call `await apiClient.updateTask(taskId, {title, description})`
3. Update task in list
4. Show loading & error states
5. Handle 404 (task not found)
6. Handle 403 (not user's task)

**Acceptance**:
- ✓ Can edit task title/description
- ✓ Changes reflected immediately
- ✓ Shows loading while updating
- ✓ Handles errors

---

### Task 1.7: Wire Task Delete Functionality
**File**: `frontend/components/TaskCard.tsx` or similar
**What to do**:
1. Add delete button to TaskCard
2. Show confirmation before delete
3. Call `await apiClient.deleteTask(taskId)`
4. Remove from list if success
5. Show error if deletion fails
6. Handle 404 & 403 errors

**Acceptance**:
- ✓ Can delete task after confirmation
- ✓ Task removed from list
- ✓ Shows error if delete fails
- ✓ Shows loading while deleting

---

### Task 1.8: Wire Task Toggle Complete
**File**: `frontend/components/TaskCard.tsx` or similar
**What to do**:
1. Add checkbox/toggle button to TaskCard
2. On click, call `await apiClient.toggleTask(taskId)`
3. Update completed status in list
4. Show loading while updating
5. Revert on error

**Acceptance**:
- ✓ Can toggle task completion
- ✓ Status updates immediately
- ✓ Shows loading while updating
- ✓ Reverts if update fails

---

### Task 1.9: Wire Task Filtering
**File**: `frontend/app/dashboard/page.tsx`
**What to do**:
1. Add filter buttons: All | Pending | Completed
2. When "Pending" clicked, call `apiClient.getPendingTasks()`
3. When "Completed" clicked, call `apiClient.getCompletedTasks()`
4. When "All" clicked, call `apiClient.getTasks()`
5. Update task list with filtered results
6. Show loading while filtering

**Acceptance**:
- ✓ Filter buttons work
- ✓ Correct tasks displayed for each filter
- ✓ Loading state shown
- ✓ Can switch between filters

---

### Task 1.10: Add Error Handling Display
**File**: Multiple component files
**What to do**:
1. Create error message component/toast
2. On API errors, display appropriate messages
3. Auto-clear error messages after 3 seconds
4. Allow manual dismiss

**Acceptance**:
- ✓ Errors displayed clearly
- ✓ User understands what went wrong
- ✓ Errors auto-dismiss or can be dismissed

---

### Task 1.11: Add Loading States
**File**: Multiple component files
**What to do**:
1. Show spinner during API calls
2. Disable buttons while loading
3. Use existing animation classes (animate-spin, etc.)
4. Show loading skeleton for task list
5. Disable form inputs while submitting

**Acceptance**:
- ✓ Spinner shows during API calls
- ✓ Buttons disabled while loading
- ✓ Clear visual feedback to user

---

## Priority 2: End-to-End Testing (1-2 hours)

### Task 2.1: Test Signup Flow
**Steps**:
1. Open app at localhost:3000
2. Click "Sign up"
3. Fill form with: unique email, password, name
4. Submit form
5. Should see dashboard
6. Verify token in localStorage

---

### Task 2.2: Test Signin Flow
**Steps**:
1. Logout (clear token)
2. Go to signin page
3. Enter email & password from previous signup
4. Submit
5. Should see dashboard
6. Verify token in localStorage

---

### Task 2.3: Test Task CRUD
**Steps**:
1. Create task: "Buy groceries" with description
2. See task in list
3. Edit task: change title
4. Verify change in list
5. Toggle completion
6. Verify status changed
7. Delete task
8. Verify removed from list

---

### Task 2.4: Test Task Filtering
**Steps**:
1. Create multiple tasks
2. Complete some tasks
3. Click "Pending" filter
4. Verify only incomplete tasks shown
5. Click "Completed" filter
6. Verify only complete tasks shown
7. Click "All" filter
8. Verify all tasks shown

---

### Task 2.5: Test User Isolation
**Steps**:
1. Signup as User A
2. Create tasks in User A's account
3. Logout
4. Signup as User B
5. Verify User B cannot see User A's tasks
6. Logout and signin as User A
7. Verify only User A's tasks shown

---

## Priority 3: Deployment (2-3 hours)

### Task 3.1: Deploy Backend to Railway or Render
**Steps**:
1. Create account at Railway.app or Render.com
2. Connect GitHub repository
3. Deploy backend with environment variables
4. Get public backend URL
5. Verify health endpoint works

---

### Task 3.2: Deploy Frontend to Vercel
**Steps**:
1. Update `frontend/.env.local` with production API URL
2. Push to GitHub
3. Go to vercel.com
4. Import GitHub project
5. Set environment variables
6. Deploy

---

### Task 3.3: Test Production Flow
**Steps**:
1. Open frontend URL from Vercel
2. Signup with test account
3. Create tasks
4. Edit tasks
5. Delete tasks
6. Test filtering
7. Verify everything works

---

## Priority 4: Final Polish (1 hour)

### Task 4.1: Create Demo Video
**Requirements**:
- Max 90 seconds
- Show: signup, dashboard, create task, edit task, delete task, filter tasks

---

### Task 4.2: Update README
**Sections**:
- Project overview
- Features
- Tech stack
- Setup instructions
- How to run locally

---

## Task Summary

| Task | Time | Status |
|------|------|--------|
| 1.1-1.11: Component Wiring | 5-6 hrs | ⏳ Pending |
| 2.1-2.5: E2E Testing | 2 hrs | ⏳ Pending |
| 3.1-3.3: Deployment | 3 hrs | ⏳ Pending |
| 4.1-4.2: Final Polish | 1 hr | ⏳ Pending |
| **TOTAL** | **11-12 hrs** | |

---

**Next**: Start with Task 1.1 (Wire signin form)
**Timeline**: Complete by December 14, 2025
**Points**: 150

*Generated: 2025-12-10*
