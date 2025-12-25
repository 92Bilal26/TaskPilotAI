# ChatKit Task Synchronization Fix

## Problem
ChatKit was successfully creating tasks and listing them within the ChatKit interface, but these tasks were not appearing in the dashboard's task list. The issue was that tasks created via ChatKit showed up with different user_id values or missing user_id.

**Symptoms**:
- Dashboard shows 1 total task
- ChatKit shows 2 tasks ("Repair mobile", "Purchase a mobile")
- Dashboard's GET /tasks endpoint returns different results than ChatKit's list_tasks()

## Root Cause
When the OpenAI Agents SDK called MCP tools (add_task, list_tasks, etc.), it was not passing the `user_id` parameter. The tools expect `user_id` as the first parameter for user isolation, but they were being called without it.

The user_id was embedded in the message text as `"[User ID: {user_id}] {message}"`, but the LLM agent wasn't extracting it properly from the message.

## Solution
Created wrapper functions that automatically inject the `user_id` into all MCP tool calls. This ensures user isolation at the tool level.

### Changes Made

**File**: `/backend/routes/chatkit.py`

**Changes**:
1. Added the current user message to the thread before processing:
   ```python
   await self.store.add_thread_item(thread.id, input, context)
   ```

2. Created wrapper functions for each MCP tool that capture `user_id` from the context and automatically inject it:
   ```python
   def add_task_wrapper(title: str, description: str = None):
       """Add a task with automatic user isolation"""
       logger.info(f"add_task called for user {user_id}")
       return mcp_add_task(user_id=user_id, title=title, description=description)

   def list_tasks_wrapper(status: str = "all"):
       """List tasks with automatic user isolation"""
       logger.info(f"list_tasks called for user {user_id}")
       return mcp_list_tasks(user_id=user_id, status=status)
   ```

3. Passed wrapped tools to the agent instead of raw tools:
   ```python
   wrapped_tools = [
       add_task_wrapper,
       list_tasks_wrapper,
       delete_task_wrapper,
       complete_task_wrapper,
       update_task_wrapper,
       find_task_by_name_wrapper,
   ]
   task_agent = create_task_agent(tools=wrapped_tools)
   ```

## How It Works

### Authentication Flow
1. User logs in via dashboard → receives JWT token with user_id in payload
2. User opens ChatKit → sends messages with Authorization: Bearer <JWT>
3. JWT middleware extracts user_id and sets request.state.user_id

### ChatKit Request Flow
1. `chatkit_protocol_endpoint` receives request with Authorization header
2. Extracts user_id from request.state.user_id (set by JWT middleware)
3. Creates context object with user_id
4. Passes context to ChatKit server's `respond()` method

### Tool Execution Flow
1. `respond()` method creates wrapper functions that capture user_id from context closure
2. These wrapper functions are passed to the agent instead of raw tools
3. When agent calls `add_task("Buy milk")`, it actually calls:
   ```
   add_task_wrapper("Buy milk")
   → mcp_add_task(user_id="user-123", title="Buy milk", description=None)
   ```
4. MCP tool receives user_id and creates task with correct user_id in database

### Dashboard Fetch Flow
1. Dashboard sends GET /tasks with Authorization header
2. JWT middleware extracts same user_id from token
3. API endpoint filters tasks: `WHERE user_id = "<user_id>"`
4. Now includes tasks created by ChatKit (same user_id)

## Verification

### To verify the fix works:

1. **In ChatKit**:
   - Send message: "Create a task called 'Test Task'"
   - ChatKit confirms task creation
   - ChatKit shows task in list

2. **In Dashboard**:
   - Refresh the page or wait for auto-refresh (every 1 second)
   - The new task should appear in the task list
   - Total tasks count should increase

### Debug Logging
Check backend logs for debug messages:
```
INFO: ChatKit respond: user=<user-id>, thread=<thread-id>
INFO: Added user message to thread: <message-id>
INFO: Initialized MCP with 6 wrapped tools
INFO: add_task called for user <user-id>
```

## User Isolation Guarantee

The fix ensures user isolation at three levels:

1. **Middleware Level**: JWT token validation ensures only authenticated users can access ChatKit
2. **Tool Level**: Wrapper functions inject user_id into every tool call
3. **Database Level**: MCP tools filter all queries by user_id

This prevents users from:
- Accessing other users' tasks
- Creating tasks for other users
- Listing tasks from other users
- Modifying other users' tasks

## Testing

To test user isolation:

1. **User A**:
   - Creates task via ChatKit
   - Verifies task appears in dashboard

2. **User B** (in separate browser session):
   - Should NOT see User A's tasks
   - Creates own task via ChatKit
   - Verifies only their own task appears

If both users see the same tasks, there's a user isolation breach.

## Performance Impact

- **Negligible**: Wrapper functions add minimal overhead (simple parameter injection)
- **Tool creation**: Wrappers are created once per ChatKit request
- **Database**: Same filtered queries as before (no additional DB queries)

## Related Issues Fixed

This fix also ensures:
- ChatKit can properly update tasks (update_task has user_id)
- ChatKit can properly delete tasks (delete_task has user_id)
- ChatKit can properly complete tasks (complete_task has user_id)
- ChatKit can properly find tasks (find_task_by_name has user_id)

All tool operations now maintain user isolation.
