# Database Schema - Phase 2

## Overview

PostgreSQL schema with two main tables:
- `users` (managed by Better Auth)
- `tasks` (our application)

## Tables

### Users Table

**Managed by Better Auth** - Do not modify directly.

| Field | Type | Constraint | Description |
|-------|------|-----------|-------------|
| id | UUID | PRIMARY KEY | Unique user identifier |
| email | VARCHAR(255) | UNIQUE, NOT NULL | User email address |
| emailVerified | BOOLEAN | DEFAULT false | Email verification status |
| name | VARCHAR(255) | | User's display name |
| image | TEXT | | User profile image URL |
| createdAt | TIMESTAMP | DEFAULT NOW() | Account creation timestamp |
| updatedAt | TIMESTAMP | DEFAULT NOW() | Last update timestamp |

### Tasks Table

| Field | Type | Constraint | Description |
|-------|------|-----------|-------------|
| id | SERIAL | PRIMARY KEY | Auto-incrementing task ID |
| user_id | UUID | FOREIGN KEY (users.id), NOT NULL | Owner of the task |
| title | VARCHAR(200) | NOT NULL | Task title (1-200 chars) |
| description | TEXT | | Task description (max 1000 chars) |
| completed | BOOLEAN | DEFAULT false | Completion status |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp (UTC) |
| updated_at | TIMESTAMP | DEFAULT NOW() | Last modification timestamp (UTC) |

## Indexes

```sql
-- Foreign key index for fast user lookups
CREATE INDEX idx_tasks_user_id ON tasks(user_id);

-- Status filter optimization
CREATE INDEX idx_tasks_completed ON tasks(completed);

-- User + status combined index
CREATE INDEX idx_tasks_user_completed ON tasks(user_id, completed);
```

## Relationships

### tasks → users
- Many tasks belong to one user
- Foreign key: `tasks.user_id` → `users.id`
- ON DELETE CASCADE (delete all user's tasks when user is deleted)

## Constraints

### Data Integrity

```sql
-- Task title must not be empty
ALTER TABLE tasks ADD CONSTRAINT chk_title_not_empty
  CHECK (LENGTH(TRIM(title)) > 0);

-- Task title max length
ALTER TABLE tasks ADD CONSTRAINT chk_title_length
  CHECK (LENGTH(title) <= 200);

-- Description max length
ALTER TABLE tasks ADD CONSTRAINT chk_description_length
  CHECK (LENGTH(description) <= 1000);

-- Timestamps must be valid
ALTER TABLE tasks ADD CONSTRAINT chk_timestamps
  CHECK (created_at <= updated_at);
```

## Sample Data

### User
```sql
INSERT INTO users (id, email, name, createdAt, updatedAt)
VALUES (
  'user-123',
  'alice@example.com',
  'Alice',
  NOW(),
  NOW()
);
```

### Tasks
```sql
INSERT INTO tasks (user_id, title, description, completed, created_at, updated_at)
VALUES (
  'user-123',
  'Buy groceries',
  'Milk, eggs, bread',
  false,
  NOW(),
  NOW()
);
```

## Query Examples

### Get all tasks for a user
```sql
SELECT * FROM tasks
WHERE user_id = $1
ORDER BY created_at DESC;
```

### Get pending tasks
```sql
SELECT * FROM tasks
WHERE user_id = $1 AND completed = false
ORDER BY created_at DESC;
```

### Get completed tasks
```sql
SELECT * FROM tasks
WHERE user_id = $1 AND completed = true
ORDER BY created_at DESC;
```

### Update task
```sql
UPDATE tasks
SET title = $1, description = $2, updated_at = NOW()
WHERE id = $3 AND user_id = $4;
```

### Delete task
```sql
DELETE FROM tasks
WHERE id = $1 AND user_id = $2;
```

## Neon Database Setup

1. Create account at [neon.tech](https://neon.tech)
2. Create a new database
3. Copy the connection string: `postgresql://user:password@host/database`
4. Store in environment variable: `DATABASE_URL`

## Migration Strategy

Use SQLModel to create tables automatically on app startup (development).

For production, use proper migration tools like Alembic.

## Performance Considerations

- User ID + Completed status index for fast filtering
- User ID index for task retrieval
- Completed status index for dashboard stats
- Foreign key constraint for data integrity
