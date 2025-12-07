# Feature: Task CRUD Operations - Phase 2

## Overview

Implement Task Create, Read, Update, Delete operations as REST API endpoints with multi-user support and persistent storage.

## User Stories

- As a logged-in user, I can create a new task with title and optional description
- As a logged-in user, I can view all my tasks (pending and completed)
- As a logged-in user, I can filter tasks by status (pending or completed)
- As a logged-in user, I can update a task's title and/or description
- As a logged-in user, I can mark a task as complete/incomplete
- As a logged-in user, I can delete a task
- As a logged-in user, I can only see and modify my own tasks (not other users' tasks)

## Acceptance Criteria

### Create Task
- [ ] POST /api/tasks endpoint exists
- [ ] Title is required (1-200 characters)
- [ ] Description is optional (max 1000 characters)
- [ ] Task is created with completed = false
- [ ] Task is associated with authenticated user
- [ ] Returns 201 Created with task object
- [ ] Returns 400 Bad Request for invalid input

### Read/List Tasks
- [ ] GET /api/tasks endpoint exists
- [ ] Returns all tasks for authenticated user
- [ ] Returns empty list if no tasks exist
- [ ] Supports status filter (all, pending, completed)
- [ ] Supports sort parameter (created, title, updated)
- [ ] Tasks are ordered by created_at (newest first) by default
- [ ] Returns 200 OK with array of tasks
- [ ] Only authenticated user's tasks are returned

### Get Single Task
- [ ] GET /api/tasks/{id} endpoint exists
- [ ] Returns task object if it belongs to user
- [ ] Returns 404 if task doesn't exist
- [ ] Returns 403 if task belongs to different user
- [ ] Returns 200 OK with task object

### Update Task
- [ ] PUT /api/tasks/{id} endpoint exists
- [ ] Can update title, description, or both
- [ ] At least one field must be provided
- [ ] Title must be 1-200 characters (if provided)
- [ ] Description must be max 1000 characters (if provided)
- [ ] updated_at timestamp is refreshed
- [ ] Returns 200 OK with updated task
- [ ] Returns 404 if task doesn't exist
- [ ] Returns 403 if task belongs to different user
- [ ] Returns 400 if validation fails

### Mark Complete
- [ ] PATCH /api/tasks/{id}/complete endpoint exists
- [ ] Accepts completed boolean parameter
- [ ] Toggles task between pending and completed
- [ ] updated_at timestamp is refreshed
- [ ] Returns 200 OK with updated task
- [ ] Returns 404 if task doesn't exist
- [ ] Returns 403 if task belongs to different user
- [ ] Returns 400 if validation fails

### Delete Task
- [ ] DELETE /api/tasks/{id} endpoint exists
- [ ] Deletes task from database
- [ ] Only deletes if task belongs to user
- [ ] Returns 200 OK on success
- [ ] Returns 404 if task doesn't exist
- [ ] Returns 403 if task belongs to different user
- [ ] Task is removed from all listings

## Data Model

### Task Object

```typescript
interface Task {
  id: number                    // Auto-incrementing primary key
  user_id: string              // UUID of task owner
  title: string                // 1-200 characters, required
  description?: string         // 0-1000 characters, optional
  completed: boolean           // true or false, default false
  created_at: string          // ISO 8601 UTC timestamp
  updated_at: string          // ISO 8601 UTC timestamp
}
```

### Example Task

```json
{
  "id": 1,
  "user_id": "user-123-uuid",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2025-12-07T10:30:00Z",
  "updated_at": "2025-12-07T10:30:00Z"
}
```

## API Endpoints

### 1. Create Task
```
POST /api/tasks
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}

Response: 201 Created
{
  "status": "success",
  "data": {
    "id": 1,
    "user_id": "user-123",
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false,
    "created_at": "2025-12-07T10:30:00Z",
    "updated_at": "2025-12-07T10:30:00Z"
  }
}
```

### 2. List Tasks
```
GET /api/tasks?status=pending&sort=created
Authorization: Bearer <token>

Response: 200 OK
{
  "status": "success",
  "data": [
    { task1 },
    { task2 }
  ]
}
```

### 3. Get Single Task
```
GET /api/tasks/{id}
Authorization: Bearer <token>

Response: 200 OK
{
  "status": "success",
  "data": { task }
}
```

### 4. Update Task
```
PUT /api/tasks/{id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Buy groceries and fruits"
}

Response: 200 OK
{
  "status": "success",
  "data": { updated_task }
}
```

### 5. Mark Complete
```
PATCH /api/tasks/{id}/complete
Authorization: Bearer <token>
Content-Type: application/json

{
  "completed": true
}

Response: 200 OK
{
  "status": "success",
  "data": { updated_task }
}
```

### 6. Delete Task
```
DELETE /api/tasks/{id}
Authorization: Bearer <token>

Response: 200 OK
{
  "status": "success",
  "message": "Task deleted successfully"
}
```

## Implementation Details

### Database Queries

**Get all tasks for user**
```python
tasks = db.query(Task).filter(Task.user_id == user_id).order_by(Task.created_at.desc()).all()
```

**Get pending tasks**
```python
tasks = db.query(Task).filter(
  Task.user_id == user_id,
  Task.completed == False
).order_by(Task.created_at.desc()).all()
```

**Get task and verify ownership**
```python
task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
if not task:
  raise HTTPException(status_code=404)
```

**Create task**
```python
task = Task(
  user_id=user_id,
  title=request.title,
  description=request.description or None,
  completed=False
)
db.add(task)
db.commit()
```

**Update task**
```python
task.title = request.title or task.title
task.description = request.description or task.description
task.updated_at = datetime.utcnow()
db.commit()
```

### Validation Rules

| Field | Rule | Error |
|-------|------|-------|
| title | 1-200 chars | "Title must be 1-200 characters" |
| title | Not empty after trim | "Title cannot be empty" |
| description | Max 1000 chars | "Description max 1000 characters" |
| user_id | Must match token | 403 Forbidden |
| id | Must exist | 404 Not Found |
| completed | Boolean only | "Completed must be boolean" |

### Timestamp Format

All timestamps are ISO 8601 with UTC timezone:
- Format: `YYYY-MM-DDTHH:MM:SSZ`
- Example: `2025-12-07T10:30:00Z`
- Use `datetime.utcnow()` in Python
- Serialize with `.isoformat() + 'Z'`

### Error Handling

```python
# Validation error
raise HTTPException(
  status_code=400,
  detail="Title must be 1-200 characters"
)

# Not found
raise HTTPException(
  status_code=404,
  detail="Task not found"
)

# Forbidden (wrong user)
raise HTTPException(
  status_code=403,
  detail="You do not have permission to access this task"
)

# Unauthorized (no token)
raise HTTPException(
  status_code=401,
  detail="Authentication required"
)
```

## Frontend Integration

### React Hook for Task Operations

```typescript
function useTaskCRUD() {
  const { session } = useSession()

  const createTask = async (title: string, description?: string) => {
    const response = await fetch('/api/tasks', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${session.token}`
      },
      body: JSON.stringify({ title, description })
    })
    return response.json()
  }

  const getTasks = async (status = 'all') => {
    const response = await fetch(`/api/tasks?status=${status}`, {
      headers: {
        'Authorization': `Bearer ${session.token}`
      }
    })
    return response.json()
  }

  const updateTask = async (id: number, updates: Partial<Task>) => {
    const response = await fetch(`/api/tasks/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${session.token}`
      },
      body: JSON.stringify(updates)
    })
    return response.json()
  }

  const deleteTask = async (id: number) => {
    const response = await fetch(`/api/tasks/${id}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${session.token}`
      }
    })
    return response.json()
  }

  const toggleComplete = async (id: number, completed: boolean) => {
    const response = await fetch(`/api/tasks/${id}/complete`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${session.token}`
      },
      body: JSON.stringify({ completed })
    })
    return response.json()
  }

  return { createTask, getTasks, updateTask, deleteTask, toggleComplete }
}
```

## Testing Strategy

### Unit Tests
- Validation logic for each field
- Database operations (CRUD)
- Error handling

### Integration Tests
- Full API endpoint flows
- User isolation (task access control)
- Authentication with JWT tokens

### E2E Tests
- User signs up
- User creates task
- User updates task
- User marks task complete
- User deletes task
- User logs out

