# TaskPilotAI Backend Guidelines

## Technology Stack
- **Framework**: FastAPI
- **Database**: SQLModel ORM with Neon PostgreSQL
- **Authentication**: JWT with Better Auth
- **Testing**: pytest with 95% coverage requirement

## Project Structure
- `/backend/models/` - SQLModel ORM models
- `/backend/routes/` - API endpoints
- `/backend/middleware/` - Authentication and request processing
- `/backend/tests/` - Unit and integration tests
- `/backend/config.py` - Configuration management
- `/backend/db.py` - Database connection and session management
- `/backend/main.py` - FastAPI application entry point

## Testing Requirements
- All endpoints must have unit tests
- All models must have validation tests
- JWT middleware must be tested
- User isolation must be verified at 3 levels (DB, API, middleware)
- Minimum 95% code coverage required
