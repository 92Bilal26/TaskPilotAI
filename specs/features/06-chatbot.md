# Feature Specification: AI-Powered Todo Chatbot

**Feature Branch**: `phase-3`
**Created**: 2025-12-14
**Status**: Draft
**Input**: User description: "Phase 3 AI Chatbot with ChatKit (frontend), Agents SDK and MCP (backend) for natural language task management"

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Create Task via Natural Language (Priority: P1)

As a busy professional, I want to create a new task by simply typing "add a task to buy groceries" so that I can quickly capture ideas without formatting commands.

**Why this priority**: This is the most fundamental feature that demonstrates the chatbot's core value. Users need to be able to manage tasks naturally as the primary use case.

**Independent Test**: Can be fully tested by having a user type a task creation request and verifying the task appears in the task list with the correct title and description. Delivers immediate value even without other features.

**Acceptance Scenarios**:

1. **Given** user is signed in and on the chatbot page, **When** user types "add a task to buy groceries", **Then** chatbot creates task and responds "I've added 'Buy groceries' to your task list"
2. **Given** user is in a chat session, **When** user types "create a reminder: call mom tonight", **Then** chatbot creates task with title "Call mom" and description "tonight"
3. **Given** user types ambiguous request like "add stuff", **When** chatbot processes it, **Then** chatbot asks for clarification "What would you like to add?"
4. **Given** task title exceeds 200 characters, **When** chatbot processes it, **Then** chatbot truncates and informs user "Task title limited to 200 characters"

---

### User Story 2 - View Tasks via Conversational Query (Priority: P1)

As a task manager, I want to ask "show me my pending tasks" in plain language so that I can see what needs to be done without navigating menus.

**Why this priority**: Equal importance to creation - users need visibility of their tasks. This feature demonstrates chatbot understanding of task filters and natural language queries.

**Independent Test**: Can be fully tested by querying tasks and verifying correct filtering. Delivers value by providing quick task visibility.

**Acceptance Scenarios**:

1. **Given** user has 5 tasks (3 pending, 2 completed), **When** user asks "show me pending tasks", **Then** chatbot displays only 3 pending tasks with titles
2. **Given** user asks "what do I need to do?", **When** chatbot processes it, **Then** chatbot shows all pending tasks
3. **Given** user asks "list all my tasks", **When** chatbot processes it, **Then** chatbot shows both completed and pending tasks
4. **Given** user has no tasks, **When** user asks to see tasks, **Then** chatbot responds "You have no tasks yet. Would you like to create one?"

---

### User Story 3 - Mark Task Complete via Chat (Priority: P1)

As a productivity-focused user, I want to say "mark task 3 as done" or "complete the groceries task" so that I can track progress conversationally.

**Why this priority**: Critical for task lifecycle management. Users need to mark tasks complete to see progress and maintain accurate task lists.

**Independent Test**: Can be fully tested by marking tasks complete via chat and verifying status change. Delivers immediate productivity feedback.

**Acceptance Scenarios**:

1. **Given** user has task with title "Buy groceries", **When** user says "mark buy groceries as complete", **Then** chatbot completes task and confirms "I've marked 'Buy groceries' as complete"
2. **Given** user has 3 tasks, **When** user says "mark task 2 as done", **Then** chatbot completes the second task
3. **Given** task is already complete, **When** user says "mark it as done again", **Then** chatbot responds "That task is already completed. Want to mark it pending instead?"
4. **Given** user references non-existent task, **When** user says "complete task 99", **Then** chatbot responds "I can't find task 99. Here are your tasks: [list]"

---

### User Story 4 - Update Task Details (Priority: P2)

As a detail-oriented user, I want to say "change task 1 from 'buy groceries' to 'buy groceries and fruits'" so that I can refine task descriptions conversationally.

**Why this priority**: Important for task refinement but secondary to creation/viewing. Users may update task details after initial creation.

**Independent Test**: Can be fully tested by updating task title/description and verifying changes persist. Enhances task management completeness.

**Acceptance Scenarios**:

1. **Given** task exists with title "Buy groceries", **When** user says "update task 1 title to 'Buy groceries and fruits'", **Then** chatbot updates and confirms "Updated task to 'Buy groceries and fruits'"
2. **Given** task has no description, **When** user says "add description: organic items only", **Then** chatbot adds description to current task
3. **Given** user provides partial update, **When** user says "change due date", **Then** chatbot responds "Due dates aren't supported. Would you like to update the description instead?"

---

### User Story 5 - Delete Task Conversationally (Priority: P2)

As a task cleaner, I want to say "remove the old grocery task" so that I can delete tasks without navigating UI elements.

**Why this priority**: Important for task management but lower priority than core CRUD. Users delete tasks less frequently than create/view/complete.

**Independent Test**: Can be fully tested by deleting a task and verifying it no longer appears. Provides cleanup capability.

**Acceptance Scenarios**:

1. **Given** user has task "Buy groceries", **When** user says "delete the groceries task", **Then** chatbot removes task and confirms "I've removed 'Buy groceries' from your task list"
2. **Given** user says "delete task 5", **When** task exists, **Then** chatbot removes it and asks "Are you sure?" before permanent deletion
3. **Given** user references task that doesn't exist, **When** user says "delete task 99", **Then** chatbot responds "Task not found"

---

### User Story 6 - Multi-turn Conversation Context (Priority: P2)

As a conversational user, I want to chat back and forth, refining tasks across multiple messages, so that I can have a natural dialogue instead of one-command interactions.

**Why this priority**: Enhances conversational experience. Less critical than individual operations but important for natural interaction patterns.

**Independent Test**: Can be fully tested by sending multiple related messages and verifying context is maintained. Enhances user experience.

**Acceptance Scenarios**:

1. **Given** user creates task saying "add groceries", **When** user follows up with "and add 'milk and eggs' to the description", **Then** chatbot understands "it" refers to the grocery task and updates it
2. **Given** user in middle of task creation, **When** user says "never mind, let me think about this", **Then** chatbot doesn't create incomplete task
3. **Given** user mentions task name once, **When** user later refers to "that task", **Then** chatbot maintains context and operates on correct task

---

### User Story 7 - Error Recovery and Help (Priority: P3)

As a user learning the chatbot, I want helpful error messages and the ability to ask "what can you do?" so that I understand chatbot capabilities and can recover from mistakes.

**Why this priority**: Enhances usability but not core functionality. Useful for onboarding and error handling.

**Independent Test**: Can be fully tested by sending invalid requests and verifying helpful responses. Improves user experience.

**Acceptance Scenarios**:

1. **Given** user sends garbled message, **When** chatbot can't understand, **Then** chatbot asks "Did you mean...?" with suggestions
2. **Given** user asks "what can you do?", **When** chatbot receives help request, **Then** chatbot lists available commands: create, view, update, delete, complete tasks
3. **Given** operation fails, **When** error occurs, **Then** chatbot provides actionable next step like "Would you like to try again?"

---

### Edge Cases

- What happens when user mentions multiple tasks in one message? (System should handle single-task operations and ask for clarification if ambiguous)
- How does system handle task names with special characters? (Should accept and store as-is)
- What if conversation has 100+ messages? (Should maintain performance and context window limits)
- What if user tries to access another user's task? (System must prevent cross-user access and respond appropriately)
- What if OpenAI API is down? (Chatbot should gracefully inform user and suggest retry)
- What if database connection fails during task operation? (MCP tool should return error and chatbot should inform user)

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST accept natural language messages from authenticated users via ChatKit UI
- **FR-002**: System MUST process messages through OpenAI Agents SDK that autonomously selects appropriate MCP tools
- **FR-003**: System MUST expose 5 MCP tools (add_task, list_tasks, update_task, delete_task, complete_task) with input validation
- **FR-004**: MCP tools MUST store and retrieve data from Neon PostgreSQL database
- **FR-005**: System MUST enforce user data isolation - tasks accessible only to task owner (via user_id from JWT)
- **FR-006**: System MUST persist all conversations and messages to database for conversation history
- **FR-007**: Chatbot MUST confirm actions: "I've created...", "I've marked... as complete", etc.
- **FR-008**: Chat endpoint MUST be stateless - no in-memory conversation storage
- **FR-009**: System MUST support multi-turn conversations maintaining context across messages
- **FR-010**: System MUST stream responses from agent in real-time to ChatKit UI
- **FR-011**: ChatKit MUST visualize tool invocations showing which tools were called and results
- **FR-012**: System MUST validate task titles (1-200 chars) and descriptions (max 1000 chars) at MCP tool level
- **FR-013**: System MUST handle errors gracefully: tool failures, API errors, validation errors
- **FR-014**: Frontend MUST use @openai/chatkit-react for chat UI (no custom chat components)
- **FR-015**: Backend MUST use Official MCP SDK for tool definitions (no custom tool framework)
- **FR-016**: Backend MUST use OpenAI Agents SDK for agent orchestration (no manual tool invocation)

### Key Entities

- **Conversation**: Represents a chat session between user and chatbot (id, user_id, created_at, updated_at)
- **Message**: Individual message in conversation (id, conversation_id, user_id, role: "user"/"assistant", content, created_at)
- **Task**: Todo item managed through chatbot (id, user_id, title, description, completed, created_at, updated_at)
- **MCP Tool**: Standardized interface for task operations (name, parameters, return format, user_id validation)

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can create a task via chat in under 5 seconds from message send to confirmation
- **SC-002**: Chatbot correctly interprets task creation requests with 90%+ accuracy (tested via 100 diverse prompts)
- **SC-003**: Chatbot correctly filters and displays tasks matching user's natural language query 95%+ of the time
- **SC-004**: All task operations (create, read, update, delete, complete) function end-to-end without manual intervention
- **SC-005**: Chat responses appear in ChatKit UI within 3 seconds of agent processing completion
- **SC-006**: System handles 10 concurrent chatbot conversations without performance degradation
- **SC-007**: Conversation history persists across browser refresh and multi-session usage
- **SC-008**: User isolation is enforced: user cannot access another user's tasks or conversation history
- **SC-009**: MCP tools return results within 500ms under normal database load
- **SC-010**: Agent correctly chains multiple tools when needed (e.g., list then update in one turn)
- **SC-011**: Error messages guide users to recovery (100% of errors have actionable next steps)
- **SC-012**: Code coverage for backend MCP tools is ≥95%
- **SC-013**: Code coverage for chat endpoint is ≥90%
- **SC-014**: Frontend ChatKit integration has ≥90% component test coverage

---

## Assumptions

- Users are already authenticated via Phase 2's Better Auth (specification assumes JWT tokens available)
- OpenAI API credentials are available and configured in backend environment
- Neon PostgreSQL database from Phase 2 is accessible and extended with Conversation/Message tables
- ChatKit domain allowlist is configured for production deployment
- Users have basic familiarity with task management concepts (title, description, status)
- Network connection is stable (no offline support required for Phase 3)
- Single message per user request (no batch operations in Phase 3)

---

## Constraints & Non-Negotiables

- **MUST use OpenAI ChatKit** - Cannot build custom chat UI
- **MUST use Official MCP SDK** - Cannot implement custom tool framework
- **MUST use OpenAI Agents SDK** - Cannot use basic Completions API
- **MUST be stateless** - No session variables or in-memory state
- **MUST enforce user isolation** - Tools must validate user_id ownership
- **MUST persist state to database** - Conversation and message history required
- **Spec-driven development** - Requirements must be clarified before implementation
- **Test-first** - Tests written before implementation (≥95% backend, ≥90% frontend)

---

## Out of Scope (Phase 3)

- File attachments in chat messages
- Voice input/output
- Real-time collaboration (multiple users chatting simultaneously)
- Advanced features like recurring tasks, subtasks, priorities
- Rate limiting or usage tracking
- User preferences or conversation settings
- ChatBot training or fine-tuning on user data
- Kubernetes deployment (deferred to Phase 4)

---

## Dependencies

- **Phase 1 Features**: Add Task, Delete Task, Update Task, View Tasks, Mark Complete (foundation for MCP tools)
- **Phase 2 Infrastructure**: Authentication (JWT tokens), User management, Multi-user database
- **Phase 2 Database**: Task, User tables (extended in Phase 3 with Conversation, Message tables)
- **External Services**: OpenAI API (Agents SDK), Neon PostgreSQL (database), ChatKit domain allowlist

---

## API Contracts

### Chat Endpoint

**POST /api/{user_id}/chat**

**Request**:
```json
{
  "conversation_id": 123,  // Optional: existing conversation
  "message": "Add a task to buy groceries"
}
```

**Response**:
```json
{
  "status": "success",
  "data": {
    "conversation_id": 123,
    "response": "I've added 'Buy groceries' to your task list.",
    "tool_calls": [
      {
        "tool": "add_task",
        "status": "success",
        "parameters": {"title": "Buy groceries"},
        "result": {"task_id": 42, "status": "created"}
      }
    ]
  }
}
```

### MCP Tools Specification

**add_task**
- Input: user_id, title (required), description (optional)
- Output: task_id, status, title
- Validation: title 1-200 chars, description max 1000 chars

**list_tasks**
- Input: user_id, status (optional: "all", "pending", "completed")
- Output: Array of {id, title, description, completed, created_at}
- Default status: "all" if not specified

**complete_task**
- Input: user_id, task_id
- Output: task_id, status, title
- Behavior: Toggles completion (pending → completed, completed → pending)

**delete_task**
- Input: user_id, task_id
- Output: task_id, status, title
- Behavior: Permanent deletion (no recovery)

**update_task**
- Input: user_id, task_id, title (optional), description (optional)
- Output: task_id, status, title
- Validation: Same as add_task

---

## Architecture Notes

### Stateless Design
- Chat endpoint receives message + optional conversation_id
- Fetches conversation history from database
- Runs agent with full message history
- Persists user message and assistant response to database
- Returns response to client
- **Zero in-memory state** on server

### Tool Invocation Flow
1. User sends message via ChatKit
2. Chat endpoint receives request (JWT validated)
3. Agent SDK receives message + MCP tools
4. Agent selects appropriate tool(s)
5. MCP tool executes (validates user_id, accesses database)
6. Tool returns result
7. Agent generates response
8. Response streamed to ChatKit
9. ChatKit displays message and tool visualizations

### User Isolation
- **Database level**: Foreign keys enforce task.user_id ownership
- **MCP tool level**: All tools receive user_id from JWT token, validate ownership
- **Frontend level**: JWT token attached to all requests

---

## Questions for Clarification

None currently - specification is complete based on hackathon requirements and reference documentation.

---

## Next Steps

1. Review this specification for completeness
2. Create quality checklist (`.specify/checklists/requirements.md`)
3. Run `/sp.clarify` if any clarifications needed
4. Proceed to `/sp.plan` for implementation planning
5. Generate implementation tasks via `/sp.tasks`

---

**Status**: Draft → Ready for Quality Validation
