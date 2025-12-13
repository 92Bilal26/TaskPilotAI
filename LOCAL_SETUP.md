# TaskPilotAI - Local Development Setup Guide

## Python 3.13 Configuration Complete ✅

Your project is now configured to run with **Python 3.13.10** and all dependencies are installed.

### Current Environment Status

```
Python Version: 3.13.10
Virtual Environment: .venv/
Backend: FastAPI (installed)
Frontend: Next.js 16.0.7 (installed)
Database: SQLite (local development)
```

---

## Quick Start (Two Terminals)

### Terminal 1: Backend (FastAPI)

```bash
# Make sure you're in the project root
cd /home/bilal/TaskPilotAI

# Activate virtual environment
source .venv/bin/activate

# Start backend server
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Backend will be available at: **http://localhost:8000**

API Documentation: **http://localhost:8000/docs**

### Terminal 2: Frontend (Next.js)

```bash
# Make sure you're in the project root
cd /home/bilal/TaskPilotAI

# Install/ensure dependencies (if needed)
cd frontend
npm install

# Start development server
npm run dev
```

Frontend will be available at: **http://localhost:3000**

---

## Verification

### Verify Backend is Running
```bash
curl http://localhost:8000/health
# Expected response: {"status":"ok","message":"TaskPilotAI API is running"}
```

### Verify Frontend is Running
Open your browser and navigate to: **http://localhost:3000**

---

## Database Configuration

### Local Development (SQLite)
The backend is configured to use **SQLite** for local development:

```
Database File: backend/taskpilot.db
Location: /home/bilal/TaskPilotAI/backend/taskpilot.db
```

The database is automatically created when you start the backend.

### Environment Variables
Backend configuration is in: `backend/.env`

```
DATABASE_URL=sqlite:///./taskpilot.db
JWT_SECRET=dev-secret-key-change-in-production
CORS_ORIGINS=["http://localhost:3000","http://localhost:8000"]
ENVIRONMENT=development
```

---

## Development Commands

### Backend Commands

```bash
# Run backend
source .venv/bin/activate
cd backend
uvicorn main:app --reload

# Run tests
pytest -v

# Run type checking
mypy .

# Check code style
flake8 .

# Run coverage
pytest --cov=.
```

### Frontend Commands

```bash
cd frontend

# Development server
npm run dev

# Build for production
npm run build

# Run tests
npm run test

# Start production build
npm start
```

---

## Troubleshooting

### Backend Won't Start
```bash
# Make sure you're using Python 3.13
source .venv/bin/activate
python --version  # Should show Python 3.13.x

# Make sure backend dependencies are installed
pip install -r backend/requirements.txt
```

### Frontend Won't Start
```bash
cd frontend

# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Try again
npm run dev
```

### Port Already in Use
```bash
# Backend on different port:
uvicorn main:app --port 8001

# Frontend on different port:
PORT=3001 npm run dev
```

---

## Running Tests

### Backend Tests
```bash
source .venv/bin/activate
cd backend
pytest -v --cov=. --cov-report=html
```

### Frontend Tests
```bash
cd frontend
npm run test
```

---

## Project Structure

```
TaskPilotAI/
├── backend/                 # FastAPI application
│   ├── main.py             # Entry point
│   ├── config.py           # Settings
│   ├── models.py           # SQLModel definitions
│   ├── db.py               # Database setup
│   ├── routes/             # API endpoints
│   ├── middleware/         # Auth middleware
│   ├── .env                # Environment config
│   └── requirements.txt     # Python dependencies
│
├── frontend/               # Next.js application
│   ├── app/                # Next.js App Router
│   ├── components/         # React components
│   ├── lib/                # Utilities & API client
│   ├── package.json        # Node dependencies
│   └── tsconfig.json       # TypeScript config
│
├── .venv/                  # Python virtual environment
├── pyproject.toml          # Project config (Python 3.13)
└── LOCAL_SETUP.md          # This file
```

---

## Important Notes

### Python 3.13 Configuration
- **Requirement**: `requires-python = ">=3.13"` (updated in pyproject.toml)
- **Virtual Environment**: Created with Python 3.13.10
- **Packages**: Updated to versions compatible with Python 3.13

### Dependencies Updated for Python 3.13
The following packages were updated to support Python 3.13:
- FastAPI: 0.104.1 → 0.109.2
- Pydantic: 2.5.0 → 2.12.5 (with pydantic-core 2.41.5)
- SQLAlchemy: 2.0.23 → 2.0.44
- Uvicorn: 0.24.0 → 0.38.0

### Phase 1 Project Safe
- Phase 1 (console app) is preserved on the `phase-1` branch
- Phase 2 (web app) is on `phase-2` branch (current)
- Virtual environment is isolated to this directory

---

## Next Steps

1. **Start the backend**: `source .venv/bin/activate && cd backend && uvicorn main:app --reload`
2. **Start the frontend**: `cd frontend && npm run dev`
3. **Open browser**: Visit http://localhost:3000
4. **Check API docs**: Visit http://localhost:8000/docs

---

## Getting Help

- Backend logs are displayed in Terminal 1
- Frontend logs are displayed in Terminal 2
- API documentation: http://localhost:8000/docs
- Next.js documentation: https://nextjs.org/docs

---

**Setup completed on**: 2025-12-08
**Python Version**: 3.13.10
**Status**: Ready for local development ✅
