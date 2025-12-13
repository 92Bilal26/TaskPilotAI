# Todo App - Phase 2 Overview

**Phase 2: Full-Stack Web Application**

Due: December 14, 2025
Points: 150

## Purpose

Transform the Phase 1 in-memory console app into a modern, multi-user web application with persistent storage, authentication, and REST API endpoints.

## Current Phase

Phase II: Full-Stack Web Application

## Technology Stack

### Frontend
- **Next.js 16+** (App Router)
- **TypeScript**
- **Tailwind CSS**
- **Better Auth** (Authentication)
- **React** (UI components)

### Backend
- **Python FastAPI** (REST API)
- **SQLModel** (ORM)
- **Neon Serverless PostgreSQL** (Database)
- **JWT** (Token-based authentication)

### Infrastructure
- **Vercel** (Frontend deployment)
- **FastAPI server** (Backend)
- **Neon DB** (Cloud database)
- **Better Auth** (Authentication provider)

## Features

### Phase 1 Features (Maintained)
- [x] Add Task
- [x] Delete Task
- [x] Update Task
- [x] View Task List
- [x] Mark as Complete

### Phase 2 New Features
- [ ] User Authentication (Signup/Signin)
- [ ] Multi-user support (tasks isolated per user)
- [ ] REST API endpoints
- [ ] Persistent database storage
- [ ] Responsive web UI
- [ ] JWT token-based authorization

## Data Isolation

Each user can only see and modify their own tasks. Task ownership is enforced at:
1. Database level (user_id foreign key)
2. API level (JWT token validation)
3. Frontend level (token attachment)

## Deliverables

1. **GitHub Repository** with:
   - `/frontend` - Next.js application
   - `/backend` - FastAPI server
   - `/specs` - All specification files
   - `CLAUDE.md` - Development instructions
   - `README.md` - Setup and usage guide

2. **Working Web Application** with:
   - User signup/signin flow
   - Task CRUD operations
   - Task filtering by status
   - Responsive UI
   - Error handling

3. **Deployed Application** on:
   - **Frontend**: Vercel
   - **Backend**: FastAPI server (local or hosted)
   - **Database**: Neon PostgreSQL

## Success Criteria

- [ ] All Phase 1 features work in web UI
- [ ] Authentication working (signup/signin)
- [ ] Task isolation per user
- [ ] All 6 REST API endpoints functional
- [ ] Frontend and backend properly integrated
- [ ] Database schema properly designed
- [ ] JWT authentication enforced
- [ ] Deployed to Vercel + working backend

## Clarifications

### Session 2025-12-07

- Q: Should guest/anonymous users be supported? → A: No, authenticated users only. All users must sign up and sign in.
- Q: How should expired JWT tokens be handled? → A: Automatic silent refresh. Backend issues refresh tokens; frontend refreshes before expiry.
- Q: How to handle concurrent edits to same task? → A: Last write wins. Later update overwrites earlier update (simplest for Phase 2).
- Q: Should deleted tasks be recoverable? → A: Hard delete (permanent). Tasks permanently removed from database.
- Q: Should API requests be rate limited? → A: No rate limiting in Phase 2. Can be added in Phase 4/5 with Kubernetes.

## Hackathon Requirements Verification

**Reference**: `/hakcathon_2_doc.md` (Lines 198-288)

### Phase 2 Objective Compliance
✅ **Objective**: "Transform the console app into a modern multi-user web application with persistent storage."

### All 5 Basic Level Features Covered
- ✅ Add Task → `specs/features/task-crud.md`
- ✅ Delete Task → `specs/features/task-crud.md`
- ✅ Update Task → `specs/features/task-crud.md`
- ✅ View Task List → `specs/features/task-crud.md`
- ✅ Mark Complete → `specs/features/task-crud.md`

### RESTful API Endpoints ✅
All 6 endpoints specified in `specs/api/rest-endpoints.md`:
- POST /api/tasks (Create)
- GET /api/tasks (List)
- GET /api/tasks/{id} (Get single)
- PUT /api/tasks/{id} (Update)
- DELETE /api/tasks/{id} (Delete)
- PATCH /api/tasks/{id}/complete (Toggle)

*Note: We use JWT token in header instead of {user_id} in URL (more secure)*

### Technology Stack Match ✅
| Required | Our Stack | Status |
|----------|-----------|--------|
| Frontend | Next.js 16+ | ✅ MATCH |
| Backend | Python FastAPI | ✅ MATCH |
| ORM | SQLModel | ✅ MATCH |
| Database | Neon PostgreSQL | ✅ MATCH |
| Auth | Better Auth | ✅ MATCH |

### JWT Security Implementation ✅
- ✅ JWT tokens issued by Better Auth
- ✅ Frontend attaches token to Authorization header
- ✅ Backend verifies JWT signature
- ✅ User ID extracted from token
- ✅ Data filtered by user_id
- ✅ Shared secret (BETTER_AUTH_SECRET) used

### Deliverables Readiness ✅
- ✅ GitHub Repository: `/frontend`, `/backend`, `/specs` folders created
- ✅ CLAUDE.md: Development instructions created
- ✅ README.md: Setup guide exists
- ✅ Specifications: All requirement areas covered
- ✅ Monorepo: Structure follows hackathon guide

### Summary
**Status**: ✅ **ALL HACKATHON REQUIREMENTS MET OR EXCEEDED**
- No missing critical requirements
- Clarifications align with hackathon objectives
- Enhancements made for better security and UX
- Ready to proceed to planning phase

## Architecture

```
┌─────────────────┐          ┌──────────────────────┐          ┌──────────────────┐
│                 │          │   FastAPI Backend    │          │                  │
│  Next.js        │  HTTPS   │  ┌────────────────┐  │  HTTPS   │  Neon Database   │
│  Frontend       │◄────────▶│  │  REST API      │  │◄────────▶│  PostgreSQL      │
│  (Vercel)       │  JWT     │  │  + JWT Auth    │  │          │                  │
│                 │          │  └────────────────┘  │          │  - users table   │
│  - Signup       │          │                      │          │  - tasks table   │
│  - Sign in      │          │                      │          │  - relations     │
│  - Task CRUD    │          │                      │          │                  │
│  - Dashboard    │          │                      │          │                  │
└─────────────────┘          └──────────────────────┘          └──────────────────┘
```

## Next Steps

1. ✅ Create monorepo structure
2. Create database schema specification
3. Create API endpoint specification
4. Create authentication specification
5. Implement backend (FastAPI)
6. Implement frontend (Next.js)
7. Deploy to Vercel + backend
8. Test complete workflow
9. Commit to phase-2 branch
