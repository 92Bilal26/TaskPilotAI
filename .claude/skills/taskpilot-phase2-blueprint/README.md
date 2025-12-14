# 🚀 TaskPilot Phase 2 Blueprint

**Generate production-ready full-stack web applications from a single command**

Transform your task management idea into a complete, deployed web application with authentication, database, and cloud hosting—all automated.

---

## Overview

This blueprint generates a **complete full-stack web application** with:

- ✅ **Frontend**: Next.js 16 + React 19 + TypeScript + Tailwind CSS
- ✅ **Backend**: FastAPI + SQLModel + JWT Authentication
- ✅ **Database**: PostgreSQL (Neon serverless)
- ✅ **Deployment**: Auto-deploy to Vercel (frontend) + Render (backend)
- ✅ **Authentication**: Multi-user with JWT tokens + password hashing
- ✅ **Testing**: Comprehensive test suites (85%+ coverage)
- ✅ **Documentation**: Complete guides and API docs

---

## What You Get

### Frontend Application
```
frontend/
├── app/
│   ├── page.tsx                    # Landing page
│   ├── layout.tsx                  # Root layout
│   ├── globals.css                 # Global styles
│   ├── auth/
│   │   ├── signin/page.tsx        # Signin page
│   │   └── signup/page.tsx        # Signup page
│   └── dashboard/
│       └── page.tsx                # Task management dashboard
├── lib/
│   ├── api.ts                      # ApiClient class
│   ├── auth-client.ts              # Better Auth integration
│   └── utils.ts                    # Utility functions
├── types/
│   └── index.ts                    # TypeScript interfaces
├── package.json                    # Dependencies
├── tsconfig.json                   # TypeScript config
├── tailwind.config.ts              # Tailwind config
└── next.config.js                  # Next.js config
```

### Backend Application
```
backend/
├── main.py                         # FastAPI app entry point
├── models.py                       # SQLModel User & Task models
├── config.py                       # Pydantic settings
├── db.py                           # Database connection
├── routes/
│   ├── auth.py                    # Authentication endpoints
│   └── tasks.py                   # Task CRUD endpoints
├── middleware/
│   └── auth.py                    # JWT middleware
├── tests/
│   ├── test_auth.py               # Auth tests
│   ├── test_models.py             # Model tests
│   └── test_integration.py        # Integration tests
├── requirements.txt                # Python dependencies
└── .env.template                   # Environment variables template
```

### Complete Documentation
```
docs/
├── README.md                       # Project overview
├── ARCHITECTURE.md                 # System architecture
├── API_DOCUMENTATION.md            # API endpoints reference
├── DEPLOYMENT.md                   # Deployment guide
├── RENDER_DEPLOYMENT_GUIDE.md      # Backend deployment
├── VERCEL_DEPLOYMENT_GUIDE.md      # Frontend deployment
├── NEON_SETUP_GUIDE.md             # Database setup
├── INTEGRATION_TESTING.md          # Testing guide
└── DEPLOYMENT_SUMMARY.md           # Deployment overview
```

---

## Quick Start

### Generate Your Full-Stack App

```bash
# Using Claude Code
/blueprint-phase2 MyTaskApp

# Or with custom options
/blueprint-phase2 MyTaskApp \
  --description "Team task management system" \
  --features real-time-updates,file-attachments \
  --database-provider neon \
  --frontend-deployment vercel \
  --backend-deployment render
```

### What Happens Next

1. **Project Scaffolding** (~5 min)
   - Frontend structure created
   - Backend structure created
   - Database schema defined
   - Tests generated

2. **Configuration** (~5 min)
   - Environment variables set up
   - Deployment configs created
   - CI/CD pipeline configured

3. **Initial Commit** (~2 min)
   - Git repository initialized
   - All files committed
   - Pushed to GitHub

4. **Deployment** (~30 min)
   - Database created on Neon
   - Backend deployed to Render
   - Frontend deployed to Vercel
   - Integration tested

**Total Time**: 30-60 minutes to live deployment! 🚀

---

## Technology Stack

### Frontend (Next.js Application)

| Component | Technology | Version |
|-----------|-----------|---------|
| Framework | Next.js | 16.0.0 |
| UI Library | React | 19.0.0 |
| Language | TypeScript | 5.6.0 |
| Styling | Tailwind CSS | 3.4.0 |
| Auth SDK | Better Auth | 1.4.5 |
| Routing | App Router | Native |
| Deployment | Vercel | Latest |

### Backend (FastAPI Application)

| Component | Technology | Version |
|-----------|-----------|---------|
| Framework | FastAPI | 0.109+ |
| Language | Python | 3.13+ |
| ORM | SQLModel | 0.0.14+ |
| Authentication | JWT (python-jose) | 3.3+ |
| Password Hash | bcrypt (passlib) | 1.7+ |
| ASGI Server | Gunicorn + Uvicorn | 21.2+ / 0.27+ |
| Deployment | Render | Latest |

### Database (PostgreSQL)

| Component | Technology | Version |
|-----------|-----------|---------|
| Database | PostgreSQL | 15+ |
| Provider | Neon (serverless) | Latest |
| ORM | SQLModel | 0.0.14+ |
| Migrations | Alembic | 1.12+ |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User's Browser                           │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ↓
        ┌─────────────────────────────┐
        │  Vercel Frontend            │
        │  (Next.js 16 + React 19)    │
        │  https://app.vercel.app     │
        └────────────┬────────────────┘
                     │
      NEXT_PUBLIC_API_URL = Backend URL
                     │
                     ↓
        ┌─────────────────────────────┐
        │  Render Backend             │
        │  (FastAPI + Gunicorn)       │
        │  https://api.onrender.com   │
        └────────────┬────────────────┘
                     │
                     ↓
        ┌─────────────────────────────┐
        │  Neon PostgreSQL            │
        │  (Managed Database)         │
        │  Serverless PostgreSQL      │
        └─────────────────────────────┘
```

---

## API Endpoints

### Authentication (Public)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/signup` | Create new user account |
| POST | `/auth/signin` | Login with credentials |
| POST | `/auth/refresh` | Refresh access token |

### Tasks (Protected - Requires JWT)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/tasks` | List user's tasks |
| POST | `/tasks` | Create new task |
| GET | `/tasks/{id}` | Get specific task |
| PUT | `/tasks/{id}` | Update task |
| DELETE | `/tasks/{id}` | Delete task |
| PATCH | `/tasks/{id}/complete` | Toggle completion |
| GET | `/tasks/filter/pending` | Get pending tasks |
| GET | `/tasks/filter/completed` | Get completed tasks |

### Health Check

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check endpoint |

---

## Database Schema

### User Table
```sql
CREATE TABLE user (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    emailVerified BOOLEAN DEFAULT FALSE,
    createdAt TIMESTAMP DEFAULT NOW(),
    updatedAt TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_user_email ON user(email);
```

### Task Table
```sql
CREATE TABLE task (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES user(id) ON DELETE CASCADE,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_task_user_id ON task(user_id);
CREATE INDEX idx_task_created_at ON task(created_at);
```

---

## Features

### Core Features (Included)

- ✅ **User Authentication**: Signup, signin, token refresh
- ✅ **User Isolation**: Each user sees only their own tasks
- ✅ **Task CRUD**: Create, read, update, delete tasks
- ✅ **Task Completion**: Toggle task completion status
- ✅ **Task Filtering**: Filter by pending/completed
- ✅ **Responsive UI**: Works on desktop, tablet, mobile
- ✅ **Password Security**: Bcrypt hashing with salt
- ✅ **JWT Tokens**: Access + refresh token pattern
- ✅ **Auto-Deploy**: Push to GitHub → auto-deploy
- ✅ **Health Checks**: Monitor backend status

### Optional Features (Add via Parameters)

- 🔄 **Real-time Updates**: WebSocket support for live updates
- 📎 **File Attachments**: Attach files to tasks
- 👥 **Task Sharing**: Share tasks with other users
- 🔔 **Notifications**: Email/push notifications
- 📋 **Task Templates**: Pre-defined task templates
- 📊 **Analytics**: Usage analytics dashboard
- 🛠️ **Admin Panel**: Admin user management

---

## Deployment Workflow

### Step 1: Database Setup (Neon) - 5 minutes

1. Create Neon account at https://neon.tech
2. Create new PostgreSQL database
3. Copy connection string
4. Save to `backend/.env`

### Step 2: Backend Deployment (Render) - 15 minutes

1. Create Render account at https://render.com
2. Connect GitHub repository
3. Create web service
4. Set root directory to `backend`
5. Configure environment variables
6. Deploy

**Result**: Backend live at `https://{name}.onrender.com`

### Step 3: Frontend Deployment (Vercel) - 10 minutes

1. Create Vercel account at https://vercel.com
2. Import GitHub repository
3. Set root directory to `frontend`
4. Set `NEXT_PUBLIC_API_URL` to backend URL
5. Deploy

**Result**: Frontend live at `https://{name}.vercel.app`

### Step 4: Integration Testing - 10 minutes

1. Test signup/signin flow
2. Create/edit/delete tasks
3. Verify user isolation
4. Check performance

**Result**: Fully functional web application! ✅

---

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `app_name` | string | Yes | - | Application name |
| `description` | string | No | "A full-stack task management web application" | Project description |
| `features` | array | No | [] | Additional features |
| `database_provider` | string | No | "neon" | PostgreSQL provider |
| `frontend_deployment` | string | No | "vercel" | Frontend platform |
| `backend_deployment` | string | No | "render" | Backend platform |
| `include_analytics` | boolean | No | false | Include analytics |
| `include_admin_panel` | boolean | No | false | Include admin panel |
| `tailwind_ui` | boolean | No | true | Use Tailwind CSS |
| `initialize_git` | boolean | No | true | Initialize Git repo |

---

## Example Usage

### Basic Generation
```bash
/blueprint-phase2 MyTaskApp
```

### With Additional Features
```bash
/blueprint-phase2 MyTaskApp \
  --description "Team collaboration task manager" \
  --features real-time-updates,task-sharing,notifications \
  --include-analytics true
```

### Custom Deployment
```bash
/blueprint-phase2 MyTaskApp \
  --database-provider railway \
  --backend-deployment fly-io \
  --frontend-deployment netlify
```

---

## Quality Guarantees

### Testing
- ✅ Frontend test coverage: 85%+
- ✅ Backend test coverage: 95%+
- ✅ Integration tests: All critical paths
- ✅ E2E tests: Main user flows

### Type Safety
- ✅ TypeScript: 0 type errors
- ✅ Python mypy: 0 type errors (strict mode)
- ✅ Pydantic validation: All API inputs

### Code Quality
- ✅ ESLint: 0 warnings
- ✅ Flake8: 0 style errors
- ✅ PEP 8 compliant
- ✅ React best practices

### Security
- ✅ Password hashing: bcrypt with salt
- ✅ JWT tokens: Access + refresh pattern
- ✅ CORS: Restricted to known origins
- ✅ SQL injection: Prevented via ORM
- ✅ XSS: React auto-escaping
- ✅ User isolation: Database-level enforcement

---

## Phase 1 vs Phase 2 Comparison

| Feature | Phase 1 | Phase 2 |
|---------|---------|---------|
| **Type** | CLI Application | Full-Stack Web App |
| **UI** | Terminal (CLI + TUI) | Web Browser (React) |
| **Storage** | In-memory (lost on exit) | PostgreSQL (persistent) |
| **Users** | Single user | Multi-user with auth |
| **Deployment** | Local only | Cloud (Vercel + Render) |
| **Lines of Code** | ~8,400 | ~20,000 |
| **Test Count** | 84 | 150+ |
| **Build Time** | 10-30 minutes | 30-60 minutes |
| **Technologies** | Python only | TypeScript + Python |
| **Complexity** | Low | High |
| **Production Ready** | Demo/prototype | Yes |

---

## Use Cases

### 1. Hackathon Projects (150 Points)
Generate a complete full-stack app for hackathon submission with deployment, authentication, and database.

### 2. SaaS MVP
Quickly prototype and deploy a multi-user SaaS application with authentication and payment-ready architecture.

### 3. Portfolio Projects
Build impressive full-stack projects with live deployment to showcase in job interviews.

### 4. Learning Full-Stack
Learn full-stack development by studying generated, production-ready code.

### 5. Client Projects
Rapid prototyping for client presentations with real deployment and functionality.

---

## Limitations

- ❌ Next.js + FastAPI stack only (not Vue, Django, etc.)
- ❌ PostgreSQL only (not MySQL, MongoDB)
- ❌ JWT authentication only (not OAuth, session-based)
- ❌ Requires external service accounts (Vercel, Render, Neon)
- ⚠️ Free tier has limitations (Render sleeps after 15 min)

---

## Roadmap (Phase 3+)

### Coming Soon
- 🤖 AI chatbot integration (OpenAI Agents SDK)
- 📱 Mobile app generation (React Native)
- 🔄 Real-time collaboration (WebSockets)
- 📊 Advanced analytics dashboard
- ☸️ Kubernetes deployment support
- 🌐 Multi-language support (i18n)

---

## Support

### Documentation
- [Skill Definition](./skill-definition.yaml)
- [Subagents Guide](./SUBAGENTS.md)
- [Implementation Guide](./IMPLEMENTATION_GUIDE.md)
- [Deployment Guide](./DEPLOYMENT.md)

### Resources
- Repository: https://github.com/92Bilal26/TaskPilotAI
- Issues: https://github.com/92Bilal26/TaskPilotAI/issues
- Email: support@taskpilotai.dev

---

## Requirements

### Accounts Needed
- ✅ GitHub account (free)
- ✅ Vercel account (free tier available)
- ✅ Render account (free tier available)
- ✅ Neon account (free tier available)

### Local Development
- Node.js 20+ (for frontend)
- Python 3.13+ (for backend)
- Git (for version control)
- npm (Node package manager)
- pip (Python package manager)

### System Requirements
- Disk space: ~200MB
- Memory: 1GB+
- Internet connection: Required for deployment

---

## Getting Started

1. **Generate Your App**
   ```bash
   /blueprint-phase2 YourAppName
   ```

2. **Follow Generated Guides**
   - Read `README.md` in generated project
   - Follow `DEPLOYMENT.md` for deployment steps
   - Check `ARCHITECTURE.md` for system overview

3. **Deploy to Production**
   - Set up Neon database
   - Deploy backend to Render
   - Deploy frontend to Vercel
   - Test live application

4. **Customize and Extend**
   - Add new features
   - Customize UI/UX
   - Integrate additional services
   - Scale as needed

---

## Examples in the Wild

✅ **TaskPilotAI** (Reference Implementation)
- Live: https://taskpilot-5l18.onrender.com
- Frontend: Next.js 16 + React 19
- Backend: FastAPI + PostgreSQL
- Deployment: Vercel + Render + Neon

---

## Contributing

To extend this blueprint:

1. Add new templates in `templates/`
2. Update subagent definitions in `manifest.json`
3. Document in `SUBAGENTS.md`
4. Update skill definition in `skill-definition.yaml`
5. Create PR with changes

---

## License

MIT License - See repository for details

---

## Acknowledgments

Built on top of:
- Phase 1 Blueprint (CLI application)
- Render Deployment Skill
- Modern web development best practices
- Production-ready patterns and architectures

---

**Status**: Production Ready ✅
**Version**: 2.0.0
**Phase**: 2 (Full-Stack Web Application)
**Last Updated**: December 14, 2025

---

Ready to build your full-stack web application? 🚀

```bash
/blueprint-phase2 YourAwesomeApp
```
