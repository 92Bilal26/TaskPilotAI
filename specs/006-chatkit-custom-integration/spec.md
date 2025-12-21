# Feature Specification: ChatKit UI Integration with Custom Chatbot Backend

**Feature Branch**: `006-chatkit-custom-integration`
**Created**: December 21, 2025
**Status**: Draft
**Input**: User description: "Integrate OpenAI ChatKit interface with existing custom chatbot backend (Agents SDK + MCP tools) to create full-featured AI task management chatbot. Bridge ChatKit frontend UI with custom chat endpoint for complete hackathon Phase 3 compliance with conversation persistence and tool invocation."

---

## Clarifications

### Session 2025-12-21

- **Q1**: Which ChatKit integration approach should we use - Recommended (OpenAI-hosted workflow) or Advanced (self-hosted)? **→ A**: Advanced self-hosted approach using ChatKit Python SDK wrapper around existing Agents SDK + MCP backend (Option B)
- **Q2**: How should tool execution results be displayed in ChatKit - plain text, interactive widgets, or hybrid? **→ A**: Hybrid approach - plain text confirmations for simple operations (add/delete/update), interactive widgets for complex results (list_tasks shows task list card) (Option C)

---

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.
  
  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - Send Message and Receive AI Response (Priority: P1)

A user accesses the ChatKit UI page, types a natural language message (e.g., "Add a task to buy groceries"), and receives an AI-generated response. The backend processes the message through the OpenAI Agents SDK, which uses MCP tools to manage tasks in the database.

**Why this priority**: This is the core functionality - the complete flow from user input through AI processing to response. Without this, the chatbot is non-functional. It demonstrates complete integration of ChatKit UI with the custom backend.

**Independent Test**: Can be fully tested by a user typing a message and receiving a response, demonstrating that ChatKit UI is correctly connected to the custom chat endpoint with agent processing.

**Acceptance Scenarios**:

1. **Given** user is authenticated and on the ChatKit page, **When** user types "Add a task to buy groceries" and presses send, **Then** message appears in chat, backend processes it with the AI agent, and response appears (e.g., "I've added 'Buy groceries' to your tasks")

2. **Given** user message requires tool invocation, **When** agent identifies the need for add_task tool, **Then** tool is executed with correct parameters and response includes confirmation

3. **Given** user sends multiple messages in sequence, **When** each message is processed, **Then** agent maintains conversation context from previous messages

---

### User Story 2 - Tool Invocations Display in ChatKit UI (Priority: P2)

The ChatKit UI clearly displays when the AI agent invokes MCP tools and shows confirmations. Users see not just the AI response, but also what actions were taken (e.g., "Task added: Buy groceries").

**Why this priority**: Transparency and feedback. Users need to see what actions the AI is taking on their behalf. This builds trust and helps them understand if the agent correctly interpreted their request.

**Independent Test**: Can be tested by sending a task management command and verifying that the ChatKit UI displays both the AI response AND tool execution confirmations.

**Acceptance Scenarios**:

1. **Given** user says "Add a task to buy milk", **When** agent invokes add_task tool, **Then** ChatKit UI displays message indicating the action (e.g., "✓ Task created: Buy milk")

2. **Given** user lists tasks with "Show me all tasks", **When** agent invokes list_tasks tool, **Then** ChatKit UI displays the returned task list in a readable format

3. **Given** agent invokes multiple tools (e.g., find_task_by_name then delete_task), **When** all tools execute successfully, **Then** ChatKit UI shows confirmations for each step

---

### User Story 3 - Conversation History Persists and Loads (Priority: P3)

When a user closes the ChatKit and returns later, their previous conversation history is loaded from the database. They can see all previous messages and continue the conversation from where they left off.

**Why this priority**: Persistence enables practical usage - users can maintain multi-session conversations without losing context. However, it depends on Stories 1-2 working first, so it's lower priority.

**Independent Test**: Can be tested by saving a conversation, closing the app, reopening it, and verifying conversation history appears and agent can reference previous messages.

**Acceptance Scenarios**:

1. **Given** user has completed a conversation with multiple messages, **When** user closes and reopens the ChatKit page, **Then** previous conversation appears in the chat history

2. **Given** conversation history is loaded, **When** user sends a new message, **Then** agent can reference context from previous messages in the conversation

3. **Given** multiple conversations exist for the user, **When** ChatKit page loads, **Then** user can switch between different conversation threads

---

### User Story 4 - Session Management Links ChatKit to Database (Priority: P3)

When a ChatKit session is created, the backend automatically creates a corresponding Conversation in the database. All messages sent through ChatKit are stored in this Conversation with proper user isolation.

**Why this priority**: This enables P1 and P3. It's foundational but somewhat invisible to users - they only care that persistence works (P3).

**Independent Test**: Can be tested by verifying that ChatKit session creation triggers database Conversation creation and message storage works correctly.

**Acceptance Scenarios**:

1. **Given** user requests a ChatKit session, **When** backend creates the session, **Then** a new Conversation is created in database linked to the user

2. **Given** user sends a message through ChatKit, **When** message is processed, **Then** message is stored in database with proper conversation_id and user_id

3. **Given** multiple users use ChatKit, **When** each has their own session, **Then** conversations are properly isolated per user (no user can see another user's messages)

### Edge Cases

- What happens when ChatKit session expires or client secret becomes invalid?
- How does the system handle when MCP tools fail (e.g., task not found)?
- What happens if user sends an ambiguous message that agent cannot interpret?
- How does system handle network disconnection during message sending?
- What happens if user tries to access another user's conversation?
- What happens when conversation has more than 10 previous messages (pagination)?
- How does system handle special characters or very long messages (length limits)?
- What happens if agent repeatedly fails to invoke correct tools?

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.
-->

### Functional Requirements

- **FR-001**: System MUST accept ChatKit sessions initiated by authenticated users through the `/api/chatkit/sessions` endpoint
- **FR-002**: ChatKit session creation MUST link to a Conversation in the database, associating all messages with that conversation
- **FR-003**: System MUST accept user messages sent from ChatKit UI and route them to the `/api/{user_id}/chat` endpoint
- **FR-004**: System MUST fetch conversation history (last 10 messages) from database before processing new user message
- **FR-005**: System MUST process user message with OpenAI Agents SDK, passing conversation history and MCP tools to the agent
- **FR-006**: System MUST store user message in database before agent processing
- **FR-007**: System MUST execute MCP tools invoked by agent (add_task, list_tasks, find_task_by_name, complete_task, delete_task, update_task)
- **FR-008**: System MUST return agent response to ChatKit UI with tool execution results and confirmations
- **FR-009**: System MUST store assistant response and tool call information in database
- **FR-010**: System MUST implement user isolation - users can only access their own conversations and tasks
- **FR-011**: ChatKit UI MUST display agent responses with clear formatting and readability
- **FR-012**: ChatKit UI MUST show tool invocation confirmations (e.g., "✓ Task added: Buy groceries")
- **FR-013**: ChatKit UI MUST support multi-turn conversations - users can send multiple messages in sequence
- **FR-014**: System MUST handle natural language task commands (add, list, complete, delete, update) via agent interpretation
- **FR-015**: System MUST handle error cases gracefully (missing tasks, invalid inputs, agent failures) and return user-friendly error messages
- **FR-016**: System MUST support conversation refresh/session reset without losing database history
- **FR-017**: System MUST display tool results using hybrid format: plain text confirmations for simple operations (add_task, delete_task, update_task, complete_task) and interactive widget cards for complex results (list_tasks displays tasks as a Card widget)
- **FR-018**: System MUST implement ChatKit Python SDK server wrapper that implements ChatKitServer interface and delegates message processing to existing Agents SDK + MCP backend

### Key Entities *(include if feature involves data)*

- **ChatKit Session**: Session managed by ChatKit Python SDK server wrapper for frontend authentication
  - Attributes: session_id, client_secret (generated by ChatKit SDK), thread_id, user_id, created_at
  - Linked to: Conversation (one ChatKit session maps to one Conversation)
  - Implementation: ChatKit Python SDK wrapper implements ChatKitServer interface delegating to custom Agents SDK

- **Conversation**: Database record grouping related messages
  - Attributes: id, user_id, title (auto-generated from first message), created_at, updated_at, archived
  - Linked to: Messages (one-to-many), ChatKit session

- **Message**: Individual message in conversation
  - Attributes: id, conversation_id, user_id, role (user/assistant), content, tool_calls (JSON array), created_at
  - Types: User messages and assistant responses with tool execution records

- **Task**: Todo item managed by MCP tools
  - Attributes: id, user_id, title, description, completed, created_at, updated_at
  - Used by: add_task, list_tasks, complete_task, delete_task, update_task tools

- **Tool Call Record**: Records of MCP tool executions
  - Attributes: tool_name, parameters, result/status, timestamp
  - Stored in: Message.tool_calls JSON field

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

- **SC-001**: Users can send a message through ChatKit UI and receive an AI response within 5 seconds (P95 latency)
- **SC-002**: 100% of task management commands (add, list, complete, delete, update) are correctly interpreted and executed by the agent with proper tool invocations
- **SC-003**: All user messages and assistant responses are persisted to database, with 100% accuracy in conversation history retrieval
- **SC-004**: Users achieve complete task isolation - a user can only see and manage their own tasks and conversations (0% unauthorized access)
- **SC-005**: Agent successfully invokes MCP tools in 95%+ of task-related messages, with appropriate fallback/explanation when tool invocation is not needed
- **SC-006**: Tool execution errors (e.g., task not found) are handled gracefully with clear error messages presented to users in 100% of failure cases
- **SC-007**: Users can resume conversations - previous chat history loads correctly in 100% of cases, and agent can reference previous messages
- **SC-008**: ChatKit UI displays tool confirmations for 100% of tool invocations (not silently executing)
- **SC-009**: System maintains conversation context across multiple messages - agent references previous messages accurately in 95%+ of multi-turn conversations
- **SC-010**: Hackathon Phase 3 compliance: ChatKit UI + OpenAI Agents SDK + MCP Server + Database Persistence + Natural Language Understanding + Tool Invocation all working together seamlessly

---

## Assumptions

- ChatKit React component is already installed (`@openai/chatkit-react@^1.3.0`)
- ChatKit JavaScript library is loaded in frontend (via HTML script tag)
- ChatKit Python SDK is available and can be installed (`pip install openai-chatkit`)
- OpenAI Agents SDK is properly configured in backend with access to MCP tools
- MCP Server with all 6 task tools (add_task, list_tasks, find_task_by_name, complete_task, delete_task, update_task) is already implemented and functional
- Database models (Conversation, Message, Task) exist in SQLModel
- User authentication (Better Auth + JWT) is already functional
- Custom chatbot chat endpoint (`/api/{user_id}/chat`) exists and can be reused
- Agent system prompt for task management is already configured
- We will implement ChatKit Python SDK server wrapper (advanced self-hosted integration)

---

## Constraints & Tradeoffs

- **Scope**: This feature focuses on UI integration with existing backend - no changes to agent logic, MCP tools, or database schema
- **API Contract**: Reuses existing `/api/{user_id}/chat` endpoint - minimal backend modifications needed
- **Session Linking**: ChatKit session creation MUST create corresponding Conversation record to enable persistence (not optional)
- **User Isolation**: All operations MUST be filtered by user_id from JWT token - no administrative override in this phase

---

## Out of Scope

- Building new MCP tools (tools already exist)
- Modifying agent system prompt or behavior (use existing)
- Changing database schema (use existing models)
- File attachment handling
- Advanced ChatKit customization (theming is out of scope)
- Multi-language support
- Voice input/output

---

## Dependencies

### Internal Dependencies
- Existing custom chatbot backend (`/backend/routes/chat.py`)
- Existing Agents SDK implementation (`/backend/task_agents/official_openai_agent.py`)
- Existing MCP Server (`/backend/mcp/server.py`)
- Existing database models (Conversation, Message, Task)
- Existing authentication system (Better Auth)

### External Dependencies
- OpenAI ChatKit React component (`@openai/chatkit-react`)
- OpenAI ChatKit Python SDK (`openai-chatkit` pip package) - implements ChatKitServer for advanced self-hosted integration
- OpenAI API (for Agents SDK and model inference)
- ChatKit JavaScript library (loaded in HTML)

---

## Testing Strategy

### Unit Testing
- Session creation returns valid client_secret
- Message routing correctly formats requests to `/api/{user_id}/chat`
- Database storage of messages and conversations works correctly
- User isolation filters work (user can't access other users' data)

### Integration Testing
- Complete flow: ChatKit UI → Session creation → Conversation creation → Message sending → Agent processing → Tool invocation → Response return
- Multi-turn conversation context preservation
- Error handling and graceful fallbacks

### User Acceptance Testing
- User can send natural language task commands and receive appropriate responses
- Tool confirmations appear in ChatKit UI
- Conversation history persists and loads correctly
- User isolation is enforced

---

## Glossary

- **ChatKit**: OpenAI's embeddable chat UI component (official product)
- **ChatKit Python SDK**: Official OpenAI library for building self-hosted ChatKit servers (advanced integration)
- **ChatKitServer**: Base class from ChatKit Python SDK that defines server interface for handling messages, tools, and widgets
- **Session**: ChatKit session initiated per conversation/user (managed by ChatKit Python SDK)
- **Thread**: Internal ChatKit concept for message history within a session
- **Conversation**: Database record of related messages for one chat thread (maps to ChatKit thread)
- **Message**: Individual user or assistant response
- **Widget**: Interactive ChatKit UI component (Card, ListView, Button, Form, etc.) for displaying rich content
- **MCP Tools**: Model Context Protocol tools (add_task, list_tasks, etc.)
- **Agent**: OpenAI Agents SDK agent that interprets user messages and invokes tools
- **Tool Invocation**: Agent calling an MCP tool to perform an action
- **Stateless**: Server maintains no state between requests - all state in database
- **User Isolation**: Users can only access their own data (conversations, tasks)
- **Advanced Integration**: Self-hosted ChatKit approach where we implement ChatKitServer to handle messages (vs. Recommended where OpenAI hosts the workflow)
