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
