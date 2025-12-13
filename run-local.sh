#!/bin/bash

# TaskPilotAI Local Development Runner
# This script helps you start both backend and frontend for local development

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PATH="$PROJECT_ROOT/.venv"

echo "=========================================="
echo "TaskPilotAI - Local Development Setup"
echo "=========================================="
echo ""

# Check if venv exists
if [ ! -d "$VENV_PATH" ]; then
    echo "❌ Virtual environment not found at $VENV_PATH"
    echo "Please run LOCAL_SETUP.md instructions first."
    exit 1
fi

# Activate virtual environment
echo "✅ Activating Python 3.13 virtual environment..."
source "$VENV_PATH/bin/activate"

python_version=$($VENV_PATH/bin/python --version)
echo "   Python: $python_version"
echo ""

# Check if dependencies are installed
echo "✅ Verifying backend dependencies..."
if ! $VENV_PATH/bin/python -c "import fastapi; import uvicorn" 2>/dev/null; then
    echo "❌ Backend dependencies not installed."
    echo "Run: pip install -r backend/requirements.txt"
    exit 1
fi
echo "   FastAPI: OK"
echo ""

# Check if frontend dependencies are installed
echo "✅ Verifying frontend dependencies..."
if [ ! -d "$PROJECT_ROOT/frontend/node_modules" ]; then
    echo "❌ Frontend dependencies not installed."
    echo "Run: cd frontend && npm install"
    exit 1
fi
echo "   Node modules: OK"
echo ""

# Show instructions
echo "=========================================="
echo "Starting TaskPilotAI..."
echo "=========================================="
echo ""
echo "IMPORTANT: Open TWO MORE TERMINALS and run:"
echo ""
echo "Terminal 1 (Backend - FastAPI):"
echo "  cd $PROJECT_ROOT"
echo "  source .venv/bin/activate"
echo "  cd backend"
echo "  uvicorn main:app --reload"
echo ""
echo "Terminal 2 (Frontend - Next.js):"
echo "  cd $PROJECT_ROOT"
echo "  cd frontend"
echo "  npm run dev"
echo ""
echo "Then open your browser:"
echo "  Frontend:  http://localhost:3000"
echo "  Backend:   http://localhost:8000"
echo "  API Docs:  http://localhost:8000/docs"
echo ""
echo "=========================================="

# Offer to start backend
read -p "Start backend now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Starting backend..."
    cd "$PROJECT_ROOT/backend"
    exec $VENV_PATH/bin/uvicorn main:app --reload --host 0.0.0.0 --port 8000
fi
