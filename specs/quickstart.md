# Phase 3 Development Quickstart Guide

**Date**: 2025-12-15
**Status**: Complete
**Version**: 1.0

This guide walks you through setting up Phase 3 locally and running the full chatbot end-to-end.

---

## Prerequisites

### System Requirements
- **OS**: Linux, macOS, or Windows (with WSL2)
- **Node.js**: 18+ (for frontend)
- **Python**: 3.13+ (for backend)
- **PostgreSQL**: Neon account (cloud database) or local PostgreSQL 14+
- **Git**: For version control

### Required Accounts
- [Neon.tech](https://neon.tech) - PostgreSQL hosting (free tier available)
- [OpenAI API](https://platform.openai.com) - For Agents SDK and API key
- [GitHub](https://github.com) - For repository access

### Installation Verification

```bash
# Check Node.js
node --version  # Expected: v18.0.0 or higher

# Check Python
python3 --version  # Expected: Python 3.13+

# Check PostgreSQL client (optional, for local testing)
psql --version  # Expected: psql (PostgreSQL) 14+
```

---

## Part 1: Database Setup

### Step 1a: Create Neon PostgreSQL Database

1. Go to [neon.tech](https://neon.tech)
2. Sign up / Log in to your account
3. Create a new project
4. Copy the connection string (looks like: `postgresql://user:password@host/database`)
5. Save it safely - you'll need this for backend `.env`

### Step 1b: (Optional) Local PostgreSQL Setup

If you prefer local development:

```bash
# macOS (using Homebrew)
brew install postgresql
brew services start postgresql
createdb taskpilot_phase3

# Linux (Ubuntu/Debian)
sudo apt-get install postgresql postgresql-contrib
sudo service postgresql start
sudo -u postgres createdb taskpilot_phase3

# Windows
# Download and install PostgreSQL from https://www.postgresql.org/download/windows/
# Run: createdb taskpilot_phase3
```

### Step 1c: Prepare Database URL

Format: `postgresql://[user]:[password]@[host]:[port]/[database]`

**Neon Example**:
```
postgresql://user:password@ep-abcd.us-east-1.aws.neon.tech/neondb
```

**Local PostgreSQL**:
```
postgresql://postgres:password@localhost:5432/taskpilot_phase3
```

---

## Part 2: Backend Setup (FastAPI)

### Step 2a: Create Backend Environment File

```bash
cd backend
cp .env.example .env
```

Edit `.env` with your credentials:

```env
# Database
DATABASE_URL=postgresql://user:password@host/dbname

# Authentication (from Phase 2)
BETTER_AUTH_SECRET=your-secret-key-here
JWT_SECRET=your-jwt-secret-key-here
JWT_EXPIRATION_HOURS=168

# OpenAI
OPENAI_API_KEY=sk-...your-api-key...

# MCP Server
MCP_SERVER_HOST=localhost
MCP_SERVER_PORT=8765

# Environment
ENVIRONMENT=development
```

### Step 2b: Create Python Virtual Environment

```bash
cd backend

# Create virtual environment
python3 -m venv venv

# Activate (Linux/macOS)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip
```

### Step 2c: Install Backend Dependencies

```bash
pip install -r requirements.txt
```

**Expected output**: All packages installed successfully (no errors)

### Step 2d: Initialize Database

```bash
# Apply migrations (create tables)
alembic upgrade head

# OR if migrations not set up yet:
python -c "
from models import SQLModel
from db import engine
SQLModel.metadata.create_all(engine)
print('Tables created successfully')
"
```

### Step 2e: Start Backend Server

```bash
# Start FastAPI server with auto-reload
uvicorn main:app --reload --port 8000

# Expected output:
# Uvicorn running on http://127.0.0.1:8000
# Application startup complete
```

**Keep this terminal open** - your backend is now running.

---

## Part 3: Frontend Setup (Next.js)

### Step 3a: Create Frontend Environment File

In a **new terminal**:

```bash
cd frontend
cp .env.example .env.local
```

Edit `.env.local`:

```env
# API endpoint
NEXT_PUBLIC_API_URL=http://localhost:8000

# ChatKit (will be configured in Step 4)
# NEXT_PUBLIC_CHATKIT_DOMAIN=your-domain.vercel.app
# NEXT_PUBLIC_CHATKIT_API_KEY=your-chatkit-api-key
```

### Step 3b: Install Frontend Dependencies

```bash
npm install

# Expected output: added X packages (no errors)
```

### Step 3c: Start Frontend Development Server

```bash
npm run dev

# Expected output:
# ready - started server on 0.0.0.0:3000, url: http://localhost:3000
```

**Keep this terminal open** - your frontend is now running.

---

## Part 4: ChatKit Configuration (Optional - for Production)

### For Local Development

You can skip this and use mock/test chat endpoint. ChatKit is required only for production deployment.

### For Production Deployment

1. **Deploy frontend to Vercel**:
   ```bash
   # Push to GitHub, connect to Vercel
   git push origin phase-3
   ```

2. **Register domain with OpenAI**:
   - Go to [ChatKit Domain Allowlist](https://platform.openai.com/settings/organization/security/domain-allowlist)
   - Add your Vercel domain (e.g., `taskpilot.vercel.app`)
   - Get ChatKit API key and domain key

3. **Update frontend `.env.local`**:
   ```env
   NEXT_PUBLIC_CHATKIT_DOMAIN=taskpilot.vercel.app
   NEXT_PUBLIC_CHATKIT_API_KEY=your-chatkit-api-key
   ```

4. **Update `frontend/app/chatbot/page.tsx`**:
   ```tsx
   import { ChatKit } from '@openai/chatkit-react';

   export default function ChatbotPage() {
     return (
       <ChatKit
         domain={process.env.NEXT_PUBLIC_CHATKIT_DOMAIN}
         apiKey={process.env.NEXT_PUBLIC_CHATKIT_API_KEY}
       />
     );
   }
   ```

---

## Testing the Full System

### Scenario 1: Create a Task via Chat

**Terminal 3** (with frontend running):

1. Go to http://localhost:3000/chatbot
2. Type in chat: `"Add a task to buy groceries"`
3. Expected response: `"I've added 'Buy groceries' to your task list."`
4. Tool visualization should show: `add_task - success`

### Scenario 2: List Your Tasks

1. Type: `"Show me my pending tasks"`
2. Expected: List of all pending tasks with titles
3. Tool visualization: `list_tasks - success`

### Scenario 3: Complete a Task

1. Type: `"Mark the groceries task as done"`
2. Expected: `"I've marked 'Buy groceries' as complete"`
3. Tool visualization: `complete_task - success`

### Scenario 4: Multi-turn Conversation

1. User: `"Add a new task"`
2. Assistant: `"I'd like to help. What should the task be?"`
3. User: `"Update that - make it about buying milk"`
4. Assistant updates the task

---

## Debugging & Troubleshooting

### Backend Issues

**Error: "Connection refused" to database**
```bash
# Check DATABASE_URL in .env
# Verify Neon/PostgreSQL is running
# Restart backend: Ctrl+C and uvicorn main:app --reload
```

**Error: "Module not found" (Python packages)**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**Error: "Port 8000 already in use"**
```bash
# Use different port
uvicorn main:app --reload --port 8001
# Update frontend .env: NEXT_PUBLIC_API_URL=http://localhost:8001
```

### Frontend Issues

**Error: "API_URL is undefined"**
```bash
# Check .env.local has NEXT_PUBLIC_API_URL
# Restart Next.js server: Ctrl+C and npm run dev
```

**Error: "Module not found" (Node packages)**
```bash
# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

**Error: "Port 3000 already in use"**
```bash
npm run dev -- -p 3001
```

### Database Issues

**Error: "Database does not exist"**
```bash
# If using local PostgreSQL:
createdb taskpilot_phase3

# If using Neon:
# Check connection string in .env
```

**Error: "Permission denied" on migrations**
```bash
# Make sure DATABASE_URL user has CREATE permissions
# Check with Neon/PostgreSQL admin
```

### Checking Logs

**Backend**:
```bash
# Uvicorn output shows request logs automatically
# Enable debug mode in .env:
ENVIRONMENT=debug
```

**Frontend**:
```bash
# Next.js logs appear in terminal
# Browser console: F12 → Console tab
```

---

## Example Conversations

### Example 1: Task Planning Session

```
User: "I need to organize my week. Add a task for Monday meeting"
Assistant: "I'll add that. What time is your Monday meeting?"
User: "It's at 10am"
Assistant: "I've added 'Monday meeting at 10am' to your task list."
[Tool: add_task - success]

User: "Also add grocery shopping for Saturday"
Assistant: "I've added 'Grocery shopping' to your task list for Saturday."
[Tool: add_task - success]

User: "Show my tasks for next week"
Assistant: "You have 2 tasks:
1. Monday meeting at 10am (pending)
2. Grocery shopping (pending)"
[Tool: list_tasks - success]
```

### Example 2: Task Completion

```
User: "Mark the Monday meeting as done"
Assistant: "I've marked 'Monday meeting at 10am' as complete."
[Tool: complete_task - success, completed=true]

User: "What's left to do?"
Assistant: "You have 1 pending task:
1. Grocery shopping"
[Tool: list_tasks status=pending - success]
```

### Example 3: Error Handling

```
User: "Delete task 999"
Assistant: "I couldn't find task 999. Here are your tasks:
1. Grocery shopping (pending)"
[Tool: delete_task - error, auto-retry attempted]

User: "Delete the grocery shopping task"
Assistant: "I've removed 'Grocery shopping' from your task list."
[Tool: delete_task - success]

User: "What tasks do I have?"
Assistant: "You have no tasks. Would you like to create one?"
[Tool: list_tasks - success, empty result]
```

---

## API Testing with cURL

### Test Chat Endpoint

```bash
# Get JWT token (from Phase 2 auth)
TOKEN="your-jwt-token-here"
USER_ID="550e8400-e29b-41d4-a716-446655440000"

# Send chat message
curl -X POST http://localhost:8000/api/$USER_ID/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "message": "Add a task to buy groceries"
  }'

# Response:
# {
#   "status": "success",
#   "data": {
#     "conversation_id": 123,
#     "response": "I've added 'Buy groceries' to your task list.",
#     "tool_calls": [...]
#   }
# }
```

### Test MCP Tools Directly

**Backend only** (not through API):

```python
# In Python shell with backend env
from mcp.tools import add_task, list_tasks
from uuid import uuid4

user_id = uuid4()

# Add task
result = add_task(
    user_id=str(user_id),
    title="Buy groceries",
    description="Milk, eggs, bread"
)
print(result)

# List tasks
tasks = list_tasks(user_id=str(user_id), status="all")
print(tasks)
```

---

## Running Tests

### Backend Tests

```bash
cd backend

# Run all tests with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_mcp_tools.py -v

# Run with detailed output
pytest -vvs

# Expected: All tests pass with ≥95% coverage
```

### Frontend Tests

```bash
cd frontend

# Run all tests
npm test

# Run with coverage
npm test -- --coverage

# Run specific test
npm test -- ChatWindow.test.tsx

# Expected: All tests pass with ≥90% coverage
```

---

## Quality Checks

### Backend Quality

```bash
cd backend

# Type checking
mypy src/

# Code style
flake8 src/ tests/

# All checks
pytest && mypy src/ && flake8 src/ tests/
```

### Frontend Quality

```bash
cd frontend

# TypeScript
npx tsc --noEmit

# ESLint
npx eslint . --ext .ts,.tsx

# All checks
npm test && npx tsc --noEmit && npx eslint .
```

---

## Stopping Services

**To stop backend**:
```bash
# In backend terminal
Ctrl+C
```

**To stop frontend**:
```bash
# In frontend terminal
Ctrl+C
```

**To shut down database**:
```bash
# Local PostgreSQL
brew services stop postgresql  # macOS
sudo service postgresql stop   # Linux

# Neon - no action needed (cloud-hosted)
```

---

## Next Steps

### After Local Testing

1. ✅ Verify all 5 MCP tools work
2. ✅ Confirm chat responses appear in ChatKit
3. ✅ Test conversation history persistence
4. ✅ Run quality checks (tests, types, lint)

### For Production Deployment

1. Deploy frontend to Vercel
2. Deploy backend to cloud server
3. Register domain in ChatKit allowlist
4. Configure environment variables in production
5. Run database migrations on production database
6. Verify SSL/TLS certificates

### For Further Development

- Reference `specs/features/06-chatbot.md` for detailed requirements
- Reference `specs/data-model.md` for database schema
- Reference `specs/contracts/` for API specifications
- Reference `docs/REFERENCE-*.md` for official SDK documentation

---

## Support & Resources

### Official Documentation

- [OpenAI ChatKit Reference](../docs/REFERENCE-OPENAI-CHATKIT.md)
- [OpenAI Agents SDK Reference](../docs/REFERENCE-OPENAI-AGENTS-SDK.md)
- [MCP Protocol Reference](../docs/REFERENCE-MCP-PROTOCOL.md)

### Specifications

- [Phase 3 Feature Specification](features/06-chatbot.md)
- [Data Model Specification](data-model.md)
- [API Contracts](contracts/)
- [Implementation Plan](phase-3-plan.md)

### External Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Model Context Protocol](https://modelcontextprotocol.io)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)

---

## Quick Reference Commands

```bash
# Backend
cd backend
source venv/bin/activate              # Activate venv
pip install -r requirements.txt       # Install dependencies
alembic upgrade head                  # Run migrations
uvicorn main:app --reload --port 8000 # Start server
pytest --cov=src                      # Run tests
mypy src/                             # Type check
flake8 src/ tests/                    # Lint code

# Frontend
cd frontend
npm install                           # Install dependencies
npm run dev                           # Start dev server
npm test                              # Run tests
npx tsc --noEmit                      # Type check
npx eslint .                          # Lint code

# Database
psql postgresql://user:password@host/db  # Connect (local)
\dt                                      # List tables
SELECT COUNT(*) FROM conversation;       # Query example
```

---

## Troubleshooting Checklist

- [ ] Node.js 18+ installed
- [ ] Python 3.13+ installed
- [ ] Database connection string correct
- [ ] Backend .env has all required variables
- [ ] Frontend .env.local has NEXT_PUBLIC_API_URL
- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000
- [ ] Database tables created (migration ran)
- [ ] JWT token valid for testing
- [ ] OpenAI API key configured
- [ ] All tests passing

---

**Version**: 1.0
**Last Updated**: 2025-12-15
**Status**: Ready for Development

---

## Getting Help

- Check error messages in terminal (backend/frontend logs)
- Review this quickstart for the specific error
- Check official SDK documentation in `/docs/`
- Review implementation plan in `specs/phase-3-plan.md`
- Refer to detailed specifications in `specs/features/06-chatbot.md`
