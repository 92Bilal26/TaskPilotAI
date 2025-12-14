# 🚀 Render Backend Deployment Skill

Automated deployment skill for deploying FastAPI backends to Render.com with complete configuration, troubleshooting, and verification.

---

## Overview

This Claude Code skill automates the entire process of deploying a FastAPI backend to Render.com, including:

- ✅ Service configuration and setup
- ✅ Environment variable management
- ✅ Build and start command configuration
- ✅ Deployment troubleshooting and fixes
- ✅ Health check and API verification
- ✅ Continuous deployment setup
- ✅ Complete documentation generation

---

## Features

### 🎯 Complete Automation
- Automatically configures Render web service
- Generates all required environment variables
- Sets up optimal build and start commands
- Enables continuous deployment from GitHub

### 🔧 Intelligent Troubleshooting
- Detects and diagnoses deployment issues
- Provides automated fixes for common problems
- Analyzes logs and error messages
- Prevents future issues with recommendations

### ✅ Comprehensive Verification
- Tests health endpoints
- Verifies API functionality
- Validates database connections
- Checks CORS configuration
- Measures performance metrics

### 📚 Documentation Generation
- Creates deployment management guide
- Generates integration testing checklist
- Provides troubleshooting procedures
- Documents all configuration settings

---

## Quick Start

### Prerequisites

1. **Render Account**: Sign up at https://render.com
2. **GitHub Repository**: Code must be in GitHub
3. **Database**: PostgreSQL database (e.g., Neon)
4. **Backend Code**: FastAPI application ready to deploy

### Usage

```bash
# Invoke the skill via Claude Code
/render-deploy \
  --project TaskPilotAI \
  --backend-dir backend \
  --branch phase-2 \
  --database-url "postgresql://user:pass@host/db?sslmode=require" \
  --jwt-secret "your-32-char-minimum-secret" \
  --cors-origins "https://frontend.vercel.app,http://localhost:3000"
```

### Parameters

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `project_name` | Yes | Name of your project | `TaskPilotAI` |
| `backend_directory` | Yes | Backend code directory | `backend` |
| `git_branch` | Yes | Git branch to deploy | `phase-2` |
| `database_url` | Yes | PostgreSQL connection string | `postgresql://...` |
| `jwt_secret` | Yes | JWT secret (32+ chars) | `your-secret-key` |
| `cors_origins` | Yes | Allowed CORS origins | `https://app.vercel.app` |
| `python_version` | No | Python version | `3.13` (default) |
| `workers` | No | Gunicorn workers | `4` (default) |
| `render_plan` | No | Render pricing plan | `free` (default) |

---

## What Gets Deployed

### Render Service Configuration

```yaml
Service Name: {project-name}-api
Service Type: Web Service
Runtime: Python 3.13
Region: Auto-selected
Root Directory: backend/
Build Command: pip install -r requirements.txt
Start Command: gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
```

### Environment Variables

```env
DATABASE_URL=postgresql://...
JWT_SECRET=your-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRY_SECONDS=604800
JWT_REFRESH_EXPIRY_SECONDS=1209600
BETTER_AUTH_SECRET=your-auth-secret
CORS_ORIGINS=["https://frontend.vercel.app"]
ENVIRONMENT=production
```

### Output

After successful deployment, you receive:

1. **Live Backend URL**: `https://{service-name}.onrender.com`
2. **Health Endpoint**: `https://{service-name}.onrender.com/health`
3. **API Documentation**: `https://{service-name}.onrender.com/docs`
4. **Management Guide**: `RENDER_BACKEND_MANAGEMENT.md`
5. **Deployment Guide**: `RENDER_DEPLOYMENT_GUIDE.md`
6. **Testing Checklist**: `INTEGRATION_TESTING_CHECKLIST.md`
7. **Deployment Summary**: `DEPLOYMENT_SUMMARY.md`

---

## Deployment Workflow

The skill executes the following steps:

### 1. Account Setup (Manual - 2 min)
- Create Render account
- Connect GitHub account
- Authorize Render app

### 2. Repository Connection (Manual - 2 min)
- Import GitHub repository
- Select branch to deploy

### 3. Service Configuration (Automated - 3 min)
- Configure root directory
- Set build command
- Set start command
- Configure Python version

### 4. Environment Variables (Automated - 3 min)
- Generate all required variables
- Validate secrets
- Set in Render dashboard

### 5. Initial Deployment (Automated - 5 min)
- Trigger first deployment
- Monitor build progress
- Handle any errors

### 6. Verification (Automated - 2 min)
- Test health endpoint
- Verify API endpoints
- Check database connection
- Validate CORS

### 7. Documentation (Automated - 1 min)
- Generate management guide
- Create testing checklist
- Document configuration

**Total Time**: 10-20 minutes

---

## Troubleshooting Capabilities

The skill automatically detects and fixes:

### ✅ Repository Access Issues
**Problem**: Cannot access GitHub repository
**Fix**: Provides authorization instructions

### ✅ Missing Requirements File
**Problem**: `requirements.txt` not found
**Fix**: Automatically sets root directory to `backend`

### ✅ Missing Gunicorn
**Problem**: `gunicorn: command not found`
**Fix**: Adds `gunicorn>=21.2.0` to requirements.txt

### ✅ Port Binding Errors
**Problem**: Incorrect gunicorn port parameter
**Fix**: Updates start command to use `--bind 0.0.0.0:$PORT`

### ✅ Database Connection Failures
**Problem**: Cannot connect to database
**Fix**: Validates DATABASE_URL and suggests adding `?sslmode=require`

### ✅ CORS Errors
**Problem**: Frontend can't access backend
**Fix**: Updates CORS_ORIGINS with frontend URL

---

## Subagents

The skill uses 4 specialized subagents:

### render-configurator (Sonnet)
- Configures Render web service
- Sets up environment variables
- Generates build/start commands

### deployment-troubleshooter (Sonnet)
- Analyzes deployment logs
- Diagnoses issues
- Applies automated fixes

### deployment-verifier (Haiku)
- Tests all endpoints
- Validates configuration
- Measures performance

### environment-manager (Haiku)
- Manages environment variables
- Validates secrets
- Generates documentation

Learn more: [SUBAGENTS.md](./SUBAGENTS.md)

---

## Examples

### Example 1: TaskPilotAI Backend

```bash
/render-deploy \
  --project TaskPilotAI \
  --backend-dir backend \
  --branch phase-2 \
  --database-url "postgresql://neondb_owner:password@host/neondb?sslmode=require" \
  --jwt-secret "taskpilot-jwt-secret-key-must-be-32-chars-minimum" \
  --cors-origins "https://taskpilot.vercel.app,http://localhost:3000"
```

**Result**:
- Backend deployed: https://taskpilot-api-5l18.onrender.com
- All endpoints working
- Database connected
- CORS configured
- Documentation generated

### Example 2: Custom Configuration

```bash
/render-deploy \
  --project MyApp \
  --backend-dir api \
  --branch main \
  --database-url $DATABASE_URL \
  --jwt-secret $JWT_SECRET \
  --cors-origins "https://myapp.com" \
  --python-version "3.12" \
  --workers 8 \
  --render-plan "starter"
```

---

## Requirements

### FastAPI Backend Must Have

1. **requirements.txt** in backend directory
   ```
   fastapi>=0.109.0
   uvicorn[standard]>=0.27.0
   gunicorn>=21.2.0
   sqlmodel>=0.0.14
   python-jose[cryptography]>=3.3.0
   passlib[bcrypt]>=1.7.4
   ```

2. **main.py** with FastAPI app
   ```python
   from fastapi import FastAPI

   app = FastAPI()

   @app.get("/health")
   async def health_check():
       return {"status": "ok"}
   ```

3. **Database models** (if using database)
   ```python
   from sqlmodel import SQLModel, Field

   class User(SQLModel, table=True):
       id: str = Field(primary_key=True)
       email: str
   ```

### External Services

1. **Render Account**: https://render.com
2. **GitHub Repository**: Public or private
3. **PostgreSQL Database**: Neon, Railway, or any PostgreSQL provider

---

## Limitations

- ✗ Render platform only (not AWS, GCP, Azure)
- ✗ FastAPI applications only (not Django, Flask)
- ✗ PostgreSQL databases only (not MySQL, MongoDB)
- ✗ GitHub repositories only (not GitLab, Bitbucket)
- ⚠️ Free tier sleeps after 15 minutes of inactivity

---

## Pricing

### Free Tier ($0/month)
- ✅ 750 hours/month
- ✅ Public GitHub repos
- ⚠️ Sleeps after 15 min inactivity
- ⚠️ 30-second cold start

### Starter Tier ($7/month)
- ✅ Always running (no sleep)
- ✅ Private GitHub repos
- ✅ Custom domains
- ✅ Email support

---

## Support

### Documentation
- [Skill Definition](./skill-definition.yaml)
- [Subagents Guide](./SUBAGENTS.md)
- [Deployment Guide](../../RENDER_DEPLOYMENT_GUIDE.md)
- [Management Guide](../../RENDER_BACKEND_MANAGEMENT.md)

### Resources
- Repository: https://github.com/92Bilal26/TaskPilotAI
- Issues: https://github.com/92Bilal26/TaskPilotAI/issues
- Email: support@taskpilotai.dev

---

## Advanced Usage

### Custom Build Commands

```yaml
# In skill invocation
--build-command "pip install -r requirements.txt && python manage.py migrate"
```

### Custom Start Commands

```yaml
# In skill invocation
--start-command "uvicorn main:app --host 0.0.0.0 --port $PORT"
```

### Environment-Specific Deployment

```bash
# Staging
/render-deploy --environment staging --branch develop

# Production
/render-deploy --environment production --branch main
```

---

## Verification Checklist

After deployment, the skill verifies:

- [x] Backend URL is accessible
- [x] Health endpoint returns 200 OK
- [x] API documentation available at /docs
- [x] Database connection successful
- [x] JWT authentication working
- [x] CORS configured correctly
- [x] All API endpoints functional
- [x] No errors in deployment logs

---

## Contributing

To extend this skill:

1. Add new subagent in `manifest.json`
2. Document in `SUBAGENTS.md`
3. Update `skill-definition.yaml`
4. Add tests for new functionality
5. Update this README

---

## Version History

### 1.0.0 (2025-12-14)
- ✅ Initial release
- ✅ Complete Render deployment automation
- ✅ 4 specialized subagents
- ✅ Automated troubleshooting
- ✅ Comprehensive documentation

---

## License

MIT License - See repository for details

---

## Acknowledgments

Built for TaskPilotAI Phase 2 deployment to support full-stack web application development.

---

**Status**: Production Ready ✅
**Version**: 1.0.0
**Last Updated**: December 14, 2025
