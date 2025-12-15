# Phase 3 Data Model Specification

**Date**: 2025-12-15
**Status**: Complete
**Version**: 1.0

---

## Overview

Phase 3 extends the Phase 2 database schema with new entities for conversation management. This specification defines three core entities:

1. **Conversation** - A chat session between user and chatbot
2. **Message** - Individual messages within a conversation
3. **Task** - Existing entity from Phase 2 (included for reference)

All entities use auto-incrementing integer IDs, UTC timestamps with timezone info (ISO 8601), and enforce user-based isolation.

---

## Entity: Conversation

**Purpose**: Represents a distinct chat session between a user and the chatbot

### Fields

| Field | Type | Nullable | Default | Notes |
|-------|------|----------|---------|-------|
| `id` | INTEGER | NO | auto-increment | Primary key, sequential ID |
| `user_id` | UUID/STRING | NO | N/A | Foreign key to User table; identifies conversation owner |
| `title` | VARCHAR(200) | YES | NULL | Optional conversation title (e.g., "Task Planning Session") |
| `created_at` | TIMESTAMP WITH TIMEZONE | NO | UTC now | When conversation started |
| `updated_at` | TIMESTAMP WITH TIMEZONE | NO | UTC now | Last message timestamp |
| `archived` | BOOLEAN | NO | FALSE | Soft delete flag for old conversations |

### Constraints

```sql
PRIMARY KEY (id)
FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
UNIQUE (user_id, id)  -- Implicit: user can only have one active conversation per ID
INDEX (user_id, created_at DESC)  -- For fast conversation listing
INDEX (user_id, updated_at DESC)  -- For sorting by recent activity
```

### Validations

- `user_id`: Required, must exist in User table
- `title`: Optional, max 200 characters if provided
- `created_at`: Auto-set to UTC now on creation, immutable after
- `updated_at`: Auto-set to UTC now on creation, updated on new message
- `archived`: Defaults to FALSE; set to TRUE for old conversations

### Relationships

- **1:N with Message**: One conversation has many messages
- **N:1 with User**: Many conversations belong to one user

### Lifecycle

1. **Creation**: POST /api/{user_id}/chat creates new Conversation
2. **Active**: user_id + id identify the active conversation
3. **Closure**: No explicit close; conversation lives indefinitely
4. **Archival**: After 90 days of inactivity, automatically archived
5. **Deletion**: Soft delete via archived flag (recovery possible)

---

## Entity: Message

**Purpose**: Represents an individual message in a conversation

### Fields

| Field | Type | Nullable | Default | Notes |
|-------|------|----------|---------|-------|
| `id` | INTEGER | NO | auto-increment | Primary key, sequential per conversation |
| `conversation_id` | INTEGER | NO | N/A | Foreign key to Conversation table |
| `user_id` | UUID/STRING | NO | N/A | Copy of conversation.user_id for isolation enforcement |
| `role` | ENUM('user', 'assistant') | NO | N/A | Who sent the message |
| `content` | TEXT | NO | N/A | Message text content (no length limit) |
| `tool_calls` | JSON | YES | NULL | Array of tool invocations and results (for assistant messages) |
| `created_at` | TIMESTAMP WITH TIMEZONE | NO | UTC now | When message was sent |

### Constraints

```sql
PRIMARY KEY (id)
FOREIGN KEY (conversation_id) REFERENCES conversation(id) ON DELETE CASCADE
FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
CHECK (role IN ('user', 'assistant'))
CHECK (LENGTH(content) > 0)  -- Content cannot be empty
INDEX (conversation_id, created_at ASC)  -- For conversation history retrieval
INDEX (user_id, created_at DESC)  -- For user's all messages
```

### Validations

- `conversation_id`: Required, must exist in Conversation table
- `user_id`: Required, must match conversation.user_id
- `role`: Must be 'user' or 'assistant'
- `content`: Required, non-empty, max 10,000 characters
- `tool_calls`: Optional JSON array; required for assistant messages with tool invocations
- `created_at`: Auto-set to UTC now, immutable after creation

### Relationships

- **N:1 with Conversation**: Many messages belong to one conversation
- **N:1 with User**: Many messages belong to one user (via user_id)

### Tool Calls Structure (JSON)

```json
[
  {
    "tool": "add_task",
    "status": "success" | "error",
    "parameters": {
      "title": "Buy groceries",
      "description": "Milk, eggs, bread"
    },
    "result": {
      "task_id": 42,
      "status": "created"
    }
  },
  {
    "tool": "complete_task",
    "status": "success",
    "parameters": {
      "task_id": 40
    },
    "result": {
      "task_id": 40,
      "title": "Task name",
      "completed": true
    }
  }
]
```

### Lifecycle

1. **Creation**: Persisted immediately when message is sent
2. **User messages**: Store user's text, empty tool_calls
3. **Assistant messages**: Store response text + array of tool invocations
4. **Immutable**: Messages never updated after creation
5. **Deletion**: Cascade delete with conversation

---

## Entity: Task (Existing, for reference)

**Purpose**: Represents a todo item; existing entity from Phase 2

### Fields

| Field | Type | Nullable | Default | Notes |
|-------|------|----------|---------|-------|
| `id` | INTEGER | NO | auto-increment | Primary key |
| `user_id` | UUID/STRING | NO | N/A | Foreign key to User table |
| `title` | VARCHAR(200) | NO | N/A | Task title |
| `description` | TEXT | YES | NULL | Optional task description |
| `completed` | BOOLEAN | NO | FALSE | Task status |
| `created_at` | TIMESTAMP WITH TIMEZONE | NO | UTC now | Creation timestamp |
| `updated_at` | TIMESTAMP WITH TIMEZONE | NO | UTC now | Last modification timestamp |

### Constraints (Phase 2)

```sql
PRIMARY KEY (id)
FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
CHECK (LENGTH(title) >= 1 AND LENGTH(title) <= 200)
CHECK (LENGTH(description) <= 1000)  -- If description is not NULL
INDEX (user_id, completed)
INDEX (user_id, created_at DESC)
```

### Phase 3 Note

No changes to Task entity for Phase 3. MCP tools access existing Task table, just exposed via chatbot interface.

---

## Database Schema Diagram

```
┌─────────────────┐
│   user          │  (exists from Phase 2)
├─────────────────┤
│ id (UUID)       │ PK
│ email (UNIQUE)  │
│ name            │
│ created_at      │
└────────┬────────┘
         │
         ├─────────────┬──────────────────┬───────────────┐
         │             │                  │               │
         │ 1:N         │ 1:N              │ 1:N           │
         ▼             ▼                  ▼               │
     ┌─────────────────────────────────────────┐          │
     │ conversation                            │          │
     ├─────────────────────────────────────────┤          │
     │ id (INTEGER, auto-increment)  PK        │          │
     │ user_id (UUID)            FK, indexed   │          │
     │ title (VARCHAR(200), NULL)              │          │
     │ created_at (TIMESTAMP WITH TZ)          │          │
     │ updated_at (TIMESTAMP WITH TZ)          │          │
     │ archived (BOOLEAN)                      │          │
     └────────┬────────────────────────────────┘          │
              │                                           │
              │ 1:N                                       │
              ▼                                           │
     ┌──────────────────────────────────────────────┐    │
     │ message                                      │    │
     ├──────────────────────────────────────────────┤    │
     │ id (INTEGER, auto-increment)       PK       │    │
     │ conversation_id (INTEGER)          FK       │    │
     │ user_id (UUID)                     FK       │    │
     │ role (ENUM: 'user', 'assistant')           │    │
     │ content (TEXT)                             │    │
     │ tool_calls (JSON, NULL)                    │    │
     │ created_at (TIMESTAMP WITH TZ)             │    │
     └──────────────────────────────────────────────┘    │
                                                         │
     ┌──────────────────────────────────────────┐        │
     │ task                                     │◄───────┘
     ├──────────────────────────────────────────┤
     │ id (INTEGER, auto-increment)  PK        │ (Phase 2)
     │ user_id (UUID)            FK, indexed   │
     │ title (VARCHAR(200))                    │
     │ description (TEXT, NULL)                │
     │ completed (BOOLEAN)                     │
     │ created_at (TIMESTAMP WITH TZ)          │
     │ updated_at (TIMESTAMP WITH TZ)          │
     └──────────────────────────────────────────┘
```

---

## SQL Migrations for Phase 3

### Migration 1: Create Conversation Table

```sql
CREATE TABLE conversation (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
    title VARCHAR(200),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    archived BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE INDEX idx_conversation_user_id ON conversation(user_id);
CREATE INDEX idx_conversation_user_created ON conversation(user_id, created_at DESC);
CREATE INDEX idx_conversation_user_updated ON conversation(user_id, updated_at DESC);
```

### Migration 2: Create Message Table

```sql
CREATE TABLE message (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER NOT NULL REFERENCES conversation(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
    role VARCHAR(50) NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL CHECK (LENGTH(content) > 0),
    tool_calls JSONB,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_message_conversation ON message(conversation_id, created_at ASC);
CREATE INDEX idx_message_user ON message(user_id, created_at DESC);
```

### Migration 3: Create Indexes for Performance

```sql
-- Conversation archival queries
CREATE INDEX idx_conversation_archived ON conversation(archived, updated_at DESC);

-- Message history pagination
CREATE INDEX idx_message_conversation_created ON message(conversation_id, created_at DESC);

-- Tool call searches (if needed for analytics)
CREATE INDEX idx_message_tool_calls ON message USING GIN (tool_calls);
```

---

## Data Types & Formats

### Timestamps

**Format**: ISO 8601 with UTC timezone
**Examples**:
- `2025-12-15T14:30:00Z` (UTC with Z suffix)
- `2025-12-15T14:30:00+00:00` (explicit offset)

**PostgreSQL Type**: `TIMESTAMP WITH TIME ZONE`

**Python Handling**:
```python
from datetime import datetime, timezone
now = datetime.now(timezone.utc).isoformat()  # Returns: "2025-12-15T14:30:00+00:00"
```

### User ID

**Type**: UUID (from Phase 2 Better Auth)
**Source**: Extracted from JWT token in request headers
**Validation**: All operations verify user_id matches token

### IDs (Conversation, Message, Task)

**Type**: SERIAL (auto-increment integer)
**Start**: 1 for first record
**Guarantee**: Never reused; monotonically increasing
**Scope**: Global per table (not per user)

### Enums

**role**: ENUM('user', 'assistant')
- `user`: Message sent by user
- `assistant`: Message generated by chatbot

---

## Constraints & Validations

### User Isolation

**Level 1: Database**
- Foreign key constraints enforce user_id ownership
- All queries filter by user_id
- Cannot access other user's conversations

**Level 2: Application**
- JWT token provides user_id
- MCP tools validate user_id matches token
- Message storage includes user_id copy

**Level 3: API**
- Chat endpoint requires valid JWT
- All requests routed by user_id from token

### Data Integrity

**Conversation Integrity**:
- Cannot have orphaned messages (CASCADE delete)
- Cannot have NULL user_id
- created_at immutable after creation

**Message Integrity**:
- Must reference existing conversation
- user_id must match conversation.user_id
- Content cannot be empty
- Role must be valid enum value

**Task Integrity**:
- Cannot have orphaned tasks (user deleted)
- Title required and bounded (1-200 chars)
- Timestamps track lifecycle

---

## Performance Considerations

### Indexes

| Table | Index | Reason |
|-------|-------|--------|
| conversation | (user_id) | Fast lookup of user's conversations |
| conversation | (user_id, created_at DESC) | Ordering conversations by creation date |
| conversation | (user_id, updated_at DESC) | Ordering by recent activity |
| message | (conversation_id, created_at ASC) | Retrieve conversation history in order |
| message | (user_id, created_at DESC) | Find user's recent messages |

### Query Optimization

**Conversation History Retrieval** (most common):
```sql
SELECT * FROM message
WHERE conversation_id = ? AND user_id = ?
ORDER BY created_at ASC
LIMIT 100;
```
Expected execution: <50ms with index on (conversation_id, created_at)

**User's Conversations**:
```sql
SELECT * FROM conversation
WHERE user_id = ? AND archived = FALSE
ORDER BY updated_at DESC;
```
Expected execution: <100ms with index on (user_id, updated_at DESC)

### Message Summarization

When conversation exceeds 20 messages:
1. Fetch messages 1-N where N is oldest
2. Create summary: "User discussed: [topics]. Key decisions: [list]"
3. Delete messages 1-N from database
4. Insert summary message with special flag
5. Keep pagination working with message count

---

## Sequencing & Lifecycle

### Conversation Lifecycle

```
1. Created     → POST /api/{user_id}/chat creates Conversation
2. Active      → Messages added via message table
3. Last update → updated_at refreshed on new message
4. Old         → After 90 days without activity
5. Archived    → Set archived=TRUE (optional, for cleanup)
6. Deleted     → Cascade delete from message table
```

### Message Lifecycle

```
1. Sent        → POST /api/{user_id}/chat stores user message
2. Processing  → Agent processes with MCP tools
3. Responded   → POST stores assistant response with tool_calls
4. History     → Retrievable via GET /api/{user_id}/chat?conversation_id=123
5. Summarized  → If 20+ messages, messages 1-N replaced with summary
6. Deleted     → Cascade deleted with conversation
```

### Task Lifecycle (unchanged from Phase 2)

```
1. Created     → via add_task MCP tool
2. Updated     → via update_task MCP tool
3. Completed   → via complete_task MCP tool
4. Deleted     → via delete_task MCP tool
```

---

## SQLModel Examples (Python)

### Conversation Model

```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone
from typing import Optional, List
from uuid import UUID

class Conversation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", index=True)
    title: Optional[str] = Field(default=None, max_length=200)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    archived: bool = Field(default=False)

    # Relationships
    messages: List["Message"] = Relationship(back_populates="conversation")
    user: "User" = Relationship(back_populates="conversations")
```

### Message Model

```python
class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversation.id", index=True)
    user_id: UUID = Field(foreign_key="user.id", index=True)
    role: str = Field(min_length=1, max_length=50)  # 'user' or 'assistant'
    content: str = Field(min_length=1)  # Non-empty
    tool_calls: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Relationships
    conversation: Optional[Conversation] = Relationship(back_populates="messages")
    user: Optional["User"] = Relationship()
```

### Task Model (for reference)

```python
class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", index=True)
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
```

---

## API Response Models

### Conversation Response

```python
class ConversationResponse(BaseModel):
    id: int
    user_id: UUID
    title: Optional[str]
    created_at: datetime
    updated_at: datetime
    message_count: int
    archived: bool
```

### Message Response

```python
class MessageResponse(BaseModel):
    id: int
    conversation_id: int
    role: str  # 'user' or 'assistant'
    content: str
    tool_calls: Optional[list]
    created_at: datetime
```

### Chat Request

```python
class ChatRequest(BaseModel):
    conversation_id: Optional[int] = None
    message: str = Field(min_length=1, max_length=10000)
```

### Chat Response

```python
class ChatResponse(BaseModel):
    status: str  # 'success' or 'error'
    data: Optional[dict] = None
    error: Optional[str] = None

    class Data(BaseModel):
        conversation_id: int
        response: str
        tool_calls: list
```

---

## Backward Compatibility

### Phase 2 → Phase 3 Migration Path

1. **Add new tables**: Conversation and Message (no changes to User, Task)
2. **No breaking changes**: Existing Task endpoints continue to work
3. **New endpoint**: POST /api/{user_id}/chat for chatbot
4. **Migrations**: Run SQL migrations in order
5. **Rollback**: Can delete Conversation and Message tables to rollback

---

## Testing Considerations

### Unit Tests

```python
def test_conversation_creation():
    conv = Conversation(user_id=user.id)
    assert conv.created_at == conv.updated_at
    assert conv.archived == False

def test_message_tool_calls_json():
    msg = Message(
        conversation_id=conv.id,
        user_id=user.id,
        role="assistant",
        content="Done",
        tool_calls=[{"tool": "add_task", "status": "success"}]
    )
    assert isinstance(msg.tool_calls, dict)
```

### Integration Tests

```python
def test_conversation_cascade_delete():
    # Delete conversation
    # Verify all messages deleted

def test_user_isolation():
    # User 1 cannot see User 2's conversations
    # User 1 cannot see User 2's messages
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-12-15 | Initial schema for Phase 3 |

---

**Status**: Complete
**Ready for**: Backend implementation
**Next**: API contract specifications in `specs/contracts/`
