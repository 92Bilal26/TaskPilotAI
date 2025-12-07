# API Documentation

## Authentication Endpoints
- POST /auth/signup - Register new user
- POST /auth/signin - Login user
- POST /auth/refresh - Refresh access token

## Task Endpoints
- GET /tasks - List all user tasks
- POST /tasks - Create new task
- GET /tasks/{id} - Get specific task
- PUT /tasks/{id} - Update task
- DELETE /tasks/{id} - Delete task
- PATCH /tasks/{id}/complete - Toggle task completion

## Filtering Endpoints
- GET /tasks/filter/pending - Get pending tasks
- GET /tasks/filter/completed - Get completed tasks
