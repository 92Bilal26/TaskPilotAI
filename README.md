# TaskPilotAI - Phase 3 🤖

**The Evolution of Todo: AI-Powered Chatbot with OpenAI Integration**

Hackathon II Phase 3 (Status: ✅ COMPLETE) - Natural Language Task Management

A spec-driven, full-stack AI-powered todo chatbot built with Next.js, FastAPI, PostgreSQL, and OpenAI API for autonomous task management through natural language.

---

## ✨ Features

Phase 3 extends Phase 2 with AI-powered chatbot capabilities for natural language task management:

### Phase 2 Foundation Features (Preserved)
- ✅ User Authentication (Signup/Login with Better Auth)
- ✅ Task Dashboard with full CRUD operations
- ✅ Multi-user Support with complete isolation
- ✅ PostgreSQL persistence with SQLModel ORM
- ✅ JWT Authentication and CORS support

### Phase 3 AI Features (NEW) 🤖
1. **Natural Language Processing** – Understand user intent through OpenAI GPT-4 Turbo
2. **Autonomous Tool Selection** – OpenAI automatically selects correct tool based on user message
3. **Chat Interface** – Real-time chat-based task management
4. **Multi-turn Conversations** – Context-aware conversations with history (last 20 messages)
5. **5 MCP Tools** – Autonomous execution of:
   - `add_task` – Create tasks from natural language
   - `list_tasks` – Query tasks with optional filtering
   - `complete_task` – Toggle task completion status
   - `update_task` – Modify task details
   - `delete_task` – Remove tasks
6. **Conversation Management** – Store and retrieve full conversation histories
7. **OpenAI Integration** – Real API calls to gpt-4-turbo-preview model
8. **Error Handling** – Graceful error recovery with informative messages

---

## 🚀 Quick Start

### ⚡ Ultra Quick Start (2 minutes)

**Live Application:**
- **Frontend**: https://task-pilot-ai-ashen.vercel.app/dashboard
- **Backend API**: https://taskpilot-api-5l18.onrender.com/docs

**Quick Demo:**
1. Visit https://task-pilot-ai-ashen.vercel.app/dashboard
2. Click "Sign Up" → Create account with email/password
3. Create a task with title and description
4. Use checkbox to mark task complete
5. Click "Edit" to modify task details
6. Click "Delete" to remove task

Done! 🎉

### Local Development (Optional)

Start backend and frontend locally for development:

```bash
# Terminal 1: Start backend
cd /home/bilal/TaskPilotAI/backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# Terminal 2: Start frontend
cd /home/bilal/TaskPilotAI/frontend
npm install
npm run dev
# Visit: http://localhost:3000
```

---

### Prerequisites

**For Production (Live):**
- Browser with internet connection
- No local setup required!

**For Local Development:**
- **Node.js**: 18+ (for frontend)
- **Python**: 3.13+ (for backend)
- **npm**: Latest (for package management)
- **pip**: Latest (for Python packages)

### Installation (Local Development)

```bash
# Clone the repository
git clone https://github.com/92Bilal26/TaskPilotAI.git
cd TaskPilotAI

# Frontend setup
cd frontend
npm install

# Backend setup (in separate terminal)
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

### 🎮 Two Ways to Use

#### Option 1: Production (Live Web Application) ⭐ Recommended

**No installation needed. Just visit:**

```
https://task-pilot-ai-ashen.vercel.app/dashboard
```

**Features:**
- ✅ Instant access - no setup required
- ✅ Automatically syncs between devices
- ✅ Secure JWT authentication
- ✅ Real-time task updates
- ✅ Responsive mobile & desktop design

#### Option 2: Local Development

**Run backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
# API available at http://localhost:8000
# Swagger docs at http://localhost:8000/docs
```

**Run frontend (in another terminal):**
```bash
cd frontend
npm run dev
# Open http://localhost:3000 in browser
```

**Environment Configuration:**
The app automatically detects environment (local vs production) and connects to the correct API endpoint. No manual configuration needed!

---

### 📚 Comprehensive Documentation

This project includes detailed guides and specifications:

| Document | Purpose | Location |
|----------|---------|----------|
| **ENVIRONMENT_SETUP.md** | Environment configuration (local vs production) | `/frontend/` |
| **Frontend CLAUDE.md** | Frontend development guidelines | `/frontend/` |
| **Backend CLAUDE.md** | Backend development guidelines | `/backend/` |
| **Main CLAUDE.md** | Overall development methodology | `/` |
| **/specs/** | Detailed feature specifications | `/specs/` |
| **Phase 2 Blueprint** | Full-stack specification | `/.claude/skills/taskpilot-phase2-blueprint/` |

---

## 🏗️ Project Structure

```
TaskPilotAI/
├── frontend/                           # Next.js React application (Vercel)
│   ├── app/                            # App Router pages
│   │   ├── page.tsx                    # Home page
│   │   ├── signin/                     # Sign in page
│   │   ├── signup/                     # Sign up page
│   │   └── dashboard/                  # Task dashboard (main app)
│   ├── components/                     # React components
│   │   ├── Layout/                     # Sidebar, Header components
│   │   ├── Tasks/                      # TaskCard, TaskEditModal
│   │   ├── Search/                     # SearchBar component
│   │   ├── Toast/                      # Toast notifications
│   │   └── ui/                         # UI primitives (Button, Input, etc)
│   ├── lib/                            # Utility functions
│   │   ├── api.ts                      # API client with JWT
│   │   ├── config.ts                   # Environment detection
│   │   ├── useAuth.ts                  # Auth hook
│   │   └── useToast.ts                 # Toast hook
│   ├── types/                          # TypeScript interfaces
│   ├── .env.development                # Local API URL
│   ├── .env.production                 # Production API URL
│   ├── ENVIRONMENT_SETUP.md            # Environment configuration guide
│   ├── CLAUDE.md                       # Frontend guidelines
│   └── package.json                    # Dependencies
│
├── backend/                            # FastAPI Python application (Render)
│   ├── main.py                         # FastAPI entry point
│   ├── models.py                       # SQLModel ORM models (User, Task)
│   ├── schemas.py                      # Pydantic schemas
│   ├── db.py                           # Database connection
│   ├── routes/                         # API endpoints
│   │   ├── auth.py                     # Authentication endpoints
│   │   └── tasks.py                    # Task CRUD endpoints
│   ├── middleware/                     # Auth middleware (JWT)
│   ├── requirements.txt                # Python dependencies
│   ├── .env                            # Environment variables
│   ├── CLAUDE.md                       # Backend guidelines
│   └── Dockerfile                      # Container configuration
│
├── specs/                              # Feature specifications
│   ├── overview.md                     # Project overview
│   ├── features/                       # Feature specifications
│   │   ├── authentication.md
│   │   ├── task-crud.md
│   │   └── ...
│   └── database/                       # Database schema
│
├── .claude/                            # Claude Code automation
│   ├── skills/                         # Reusable skills
│   │   ├── render-deployment/          # Render backend deployment
│   │   └── taskpilot-phase2-blueprint/ # Phase 2 full-stack blueprint
│   └── commands/                       # Custom commands
│
├── .specify/                           # Spec-Kit Plus config
│   └── memory/constitution.md          # Project constitution
│
├── CLAUDE.md                           # Main development guide
├── README.md                           # This file
└── .gitignore                          # Git ignore rules
```

### Key Directories

- **`/frontend`** – Next.js 16 React application (TypeScript)
- **`/backend`** – FastAPI Python REST API
- **`/specs`** – Feature specifications and requirements
- **`/.claude`** – Claude Code skills and automation scripts
- **`/.specify`** – Spec-Kit Plus configuration

---

## 🧪 Testing

### Frontend Tests

```bash
cd frontend
npm test
```

### Backend Tests

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pytest -v
```

### Test Coverage

Phase 2 components are thoroughly tested:

**Frontend:**
- Component unit tests
- API integration tests
- Authentication flow tests
- ≥90% code coverage

**Backend:**
- Endpoint unit tests
- Database operation tests
- JWT authentication tests
- User isolation verification
- ≥95% code coverage

---

## 🔍 Code Quality

### Frontend Quality

```bash
cd frontend

# Type checking
npm run type-check

# Linting
npm run lint

# Format code
npm run format
```

### Backend Quality

```bash
cd backend

# Type checking
mypy .

# Linting
flake8 .

# Format code
black .
```

### Quality Gates (All Required)

**Frontend:**
- ✅ TypeScript compilation with no errors
- ✅ ESLint passing
- ✅ ≥90% code coverage
- ✅ No console warnings

**Backend:**
- ✅ mypy passes (strict mode)
- ✅ flake8 passes (PEP 8)
- ✅ pytest passes with ≥95% coverage
- ✅ All endpoints working

All quality gates must pass before deployment.

---

## 📝 Development Workflow

This project follows **Spec-Driven Development** with strict **Test-First (TDD)** methodology:

### Phase 2 Development Phases

1. **Backend Development**
   - Define database schema with SQLModel
   - Implement REST API endpoints with FastAPI
   - Add JWT authentication middleware
   - Enforce user isolation at database level
   - Write comprehensive tests
   - Deploy to Render

2. **Frontend Development**
   - Create Next.js pages and React components
   - Implement API client with automatic token attachment
   - Build authentication forms (signup/signin)
   - Create task management UI (create, read, update, delete)
   - Add search and filter functionality
   - Deploy to Vercel

3. **Integration Testing**
   - Test complete authentication flow
   - Verify user isolation (can't access other users' tasks)
   - Test all CRUD operations end-to-end
   - Verify error handling and edge cases

4. **Deployment**
   - Backend → Render.com with environment variables
   - Frontend → Vercel with automatic deployments
   - Database → Neon PostgreSQL (serverless)
   - Environment detection (local vs production)

---

## 📊 Data Model

### User Object

```json
{
  "id": "uuid",
  "email": "user@example.com",
  "name": "User Name",
  "emailVerified": false,
  "createdAt": "2025-12-14T10:30:00Z"
}
```

### Task Object

```json
{
  "id": "uuid",
  "user_id": "uuid",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2025-12-14T10:30:00Z",
  "updated_at": "2025-12-14T10:30:00Z"
}
```

### Database Schema

**Users Table:**
- `id` (UUID) - Primary key
- `email` (String, Unique) - User email
- `name` (String) - User name
- `password_hash` (String) - Encrypted password
- `email_verified` (Boolean) - Email verification status
- `created_at` (Timestamp) - Account creation time
- `updated_at` (Timestamp) - Last update time

**Tasks Table:**
- `id` (UUID) - Primary key
- `user_id` (UUID) - Foreign key to Users
- `title` (String, 1-200 chars) - Task title
- `description` (String, max 1000 chars) - Task description
- `completed` (Boolean) - Task completion status
- `created_at` (Timestamp) - Task creation time
- `updated_at` (Timestamp) - Last update time

---

## ⚠️ API Error Handling

The API provides clear, consistent error responses:

| Status | Error | Meaning |
|--------|-------|---------|
| 400 | Invalid input | Missing required fields or validation failed |
| 401 | Unauthorized | Invalid or missing JWT token |
| 403 | Forbidden | User doesn't have permission (task owner check) |
| 404 | Not found | Task or user doesn't exist |
| 409 | Conflict | Email already registered |
| 500 | Server error | Unexpected server error |

**Example Error Response:**
```json
{
  "detail": "Task not found"
}
```

---

## 📖 API Endpoints Reference

### Authentication

```http
POST /auth/signup
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123",
  "name": "User Name"
}

Response: { "access_token": "...", "refresh_token": "..." }
```

```http
POST /auth/signin
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}

Response: { "access_token": "...", "refresh_token": "..." }
```

### Tasks

```http
# Get all user's tasks
GET /tasks
Authorization: Bearer <access_token>

# Create task
POST /tasks
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "title": "Task title",
  "description": "Optional description"
}

# Update task
PUT /tasks/{id}
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "title": "Updated title",
  "description": "Updated description"
}

# Toggle task completion
PATCH /tasks/{id}/complete
Authorization: Bearer <access_token>

# Delete task
DELETE /tasks/{id}
Authorization: Bearer <access_token>

# Filter tasks by status
GET /tasks/filter/pending
GET /tasks/filter/completed
Authorization: Bearer <access_token>
```

### Swagger Documentation

Interactive API documentation available at:
```
https://taskpilot-api-5l18.onrender.com/docs
```

---

## 🔧 Technology Stack

### Frontend
| Component | Technology | Purpose |
|---|---|---|
| **Framework** | Next.js 16+ | React app framework with SSR |
| **Language** | TypeScript 5.6+ | Type-safe JavaScript |
| **Styling** | Tailwind CSS 3.4+ | Utility-first CSS |
| **UI Components** | shadcn/ui | Reusable component library |
| **State Management** | React Hooks | Local state management |
| **HTTP Client** | Fetch API | HTTP requests |
| **Deployment** | Vercel | Automatic CI/CD deployment |

### Backend
| Component | Technology | Purpose |
|---|---|---|
| **Framework** | FastAPI 0.109+ | Modern Python web framework |
| **Database** | Neon PostgreSQL | Serverless SQL database |
| **ORM** | SQLModel 0.0.14+ | SQL + Pydantic validation |
| **Authentication** | JWT | Stateless token-based auth |
| **Server** | Gunicorn + Uvicorn | ASGI application server |
| **Deployment** | Render | Containerized cloud deployment |

### Development Tools
| Tool | Purpose |
|---|---|
| **pytest** | Python testing framework |
| **mypy** | Python type checking |
| **flake8** | Python code linting |
| **black** | Python code formatting |
| **ESLint** | JavaScript linting |
| **Prettier** | Code formatting |

---

## 🎯 Quality Standards

### Frontend Quality
- **Type Safety**: 100% TypeScript with strict mode
- **Linting**: ESLint + Prettier formatting
- **Component Testing**: Unit tests for all components
- **Integration Testing**: API and auth flow testing
- **Code Coverage**: ≥90% coverage target
- **Accessibility**: WCAG 2.1 AA compliance
- **Responsive Design**: Mobile-first approach

### Backend Quality
- **Type Hints**: 100% type hints on all functions
- **Code Style**: PEP 8 compliant (enforced by flake8)
- **Type Safety**: 100% mypy compliance (strict mode)
- **Unit Tests**: All endpoints tested
- **Integration Tests**: Full workflows tested
- **Code Coverage**: ≥95% coverage target
- **API Documentation**: Swagger/OpenAPI documentation

### Documentation
- **README.md**: Setup and usage instructions
- **CLAUDE.md**: Development methodology guides
- **API Docs**: Swagger at `/docs` endpoint
- **Environment Setup**: Dynamic environment configuration
- **Specs**: Feature specifications in `/specs/`
- **Code Comments**: Self-documenting code

---

## 📚 Phase 2 Constitution

This project follows a strict **Constitution** defined in `.specify/memory/constitution.md`. The constitution establishes:

- **Core Principles**: Spec-driven development, test-first (TDD), multi-user architecture
- **Deployment Standards**: Automatic environment detection, zero manual config
- **Quality Gates**: All gates must pass before deployment
- **User Isolation**: Enforced at database, API, and middleware levels
- **Non-Negotiable Rules**: JWT authentication required, all endpoints protected, tests before features

**Key Constraints:**
- JWT tokens required for all authenticated endpoints
- User isolation verified at 3 levels (database, API, middleware)
- Environment auto-detection (localhost vs production)
- Comprehensive error handling and validation

---

## 🚀 Next Steps (Phase 3+)

Phase 2 is now complete! Future phases will add:

- **Phase 3**: AI Chatbot - Natural language task management
  - OpenAI integration for task understanding
  - Natural language parsing and task extraction
  - Conversational interface

- **Phase 4**: Kubernetes Deployment
  - Docker containerization
  - Kubernetes manifests
  - Minikube local testing

- **Phase 5**: Cloud Deployment
  - DigitalOcean DOKS (Kubernetes)
  - Event streaming with Kafka
  - Distributed tracing with Dapr
  - Auto-scaling and load balancing

---

## 📝 Contributing

This is a hackathon project following strict spec-driven development. All contributions must:

1. Start with a specification in `/specs/`
2. Include comprehensive tests (TDD)
3. Pass all quality gates
   - Frontend: TypeScript compilation, ESLint, ≥90% coverage
   - Backend: mypy, flake8, pytest with ≥95% coverage
4. Follow the constitution principles
5. Maintain user isolation and security standards
6. Document changes and update this README

---

## 📄 License

MIT License - See LICENSE file for details

---

## 👤 Author

**92Bilal26** (Bilal Ahmed)
- Email: talibebaqi@gmail.com
- GitHub: https://github.com/92Bilal26

---

## 🔗 Resources

### Live Application
- **Frontend**: https://task-pilot-ai-ashen.vercel.app/dashboard
- **Backend API**: https://taskpilot-api-5l18.onrender.com
- **API Docs**: https://taskpilot-api-5l18.onrender.com/docs

### Repository
- **Project Repository**: https://github.com/92Bilal26/TaskPilotAI
- **Phase 1 Branch**: https://github.com/92Bilal26/TaskPilotAI/tree/phase-1
- **Phase 2 Branch**: https://github.com/92Bilal26/TaskPilotAI/tree/phase-2

### Documentation
- **Constitution**: `.specify/memory/constitution.md`
- **Specifications**: `/specs/` directory
- **Frontend Guide**: `/frontend/ENVIRONMENT_SETUP.md`
- **Phase 2 Blueprint**: `/.claude/skills/taskpilot-phase2-blueprint/`

### Deployment
- **Frontend Host**: Vercel (Auto-deploys from phase-2 branch)
- **Backend Host**: Render.com (Docker container)
- **Database**: Neon PostgreSQL (Serverless)

---

## 📞 Support

For questions or issues:

1. Check the live application at https://task-pilot-ai-ashen.vercel.app/dashboard
2. Review specification files in `/specs/`
3. Check environment setup in `/frontend/ENVIRONMENT_SETUP.md`
4. Review constitution in `.specify/memory/constitution.md`
5. Check API documentation at https://taskpilot-api-5l18.onrender.com/docs
6. Open an issue on GitHub

---

**Last Updated**: 2025-12-14
**Status**: Phase 2 Complete ✅
**Points Earned**: 150 Points
**Deadline**: Dec 14, 2025 (Phase 2 Deadline)
**Next Milestone**: Phase 3 - AI Chatbot Integration
