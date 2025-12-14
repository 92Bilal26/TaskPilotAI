# Render Deployment Subagents

This document describes the specialized subagents used by the Render deployment skill to automate backend deployment to Render.com.

---

## Overview

The Render deployment skill uses 4 specialized subagents to handle different aspects of the deployment workflow:

1. **render-configurator** - Service configuration and setup
2. **deployment-troubleshooter** - Issue diagnosis and resolution
3. **deployment-verifier** - Health checks and validation
4. **environment-manager** - Environment variable management

---

## Subagent: render-configurator

### Purpose
Configures Render web service settings and prepares the deployment environment.

### Model
`sonnet` (Claude Sonnet 4.5) - High capability model for complex configuration tasks

### Tools Available
- `Read` - Read configuration files and documentation
- `Write` - Generate configuration templates
- `Bash` - Execute git commands and file operations
- `WebFetch` - Fetch Render documentation if needed

### Responsibilities

#### 1. Service Configuration
- Determine optimal service settings
- Configure root directory
- Set Python version
- Choose appropriate region

#### 2. Build Command Configuration
```bash
# Standard build command
pip install -r requirements.txt

# Verifies:
- requirements.txt exists in backend directory
- All dependencies are properly specified
- gunicorn is included
```

#### 3. Start Command Configuration
```bash
# Production start command
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT

# Components:
- main:app → FastAPI application entry point
- --workers 4 → Number of concurrent workers
- --worker-class uvicorn.workers.UvicornWorker → ASGI server
- --bind 0.0.0.0:$PORT → Bind to Render-assigned port
```

#### 4. Environment Variables Setup
Generates complete environment variable configuration:
```env
DATABASE_URL=postgresql://...
JWT_SECRET=...
JWT_ALGORITHM=HS256
JWT_EXPIRY_SECONDS=604800
JWT_REFRESH_EXPIRY_SECONDS=1209600
BETTER_AUTH_SECRET=...
CORS_ORIGINS=[...]
ENVIRONMENT=production
```

#### 5. Auto-Deploy Configuration
- Enable continuous deployment from GitHub
- Set up webhook for automatic deployments
- Configure branch tracking

### Input
- Project name
- Backend directory path
- Git branch
- Database connection string
- JWT secrets
- CORS origins

### Output
- Complete Render service configuration
- Environment variables template
- Deployment settings documentation

---

## Subagent: deployment-troubleshooter

### Purpose
Diagnoses deployment failures and provides automated fixes.

### Model
`sonnet` (Claude Sonnet 4.5) - High capability for complex problem-solving

### Tools Available
- `Read` - Read deployment logs and error messages
- `Grep` - Search for error patterns in logs
- `Bash` - Execute diagnostic commands
- `WebFetch` - Fetch Render documentation for troubleshooting

### Responsibilities

#### 1. Log Analysis
Analyzes Render deployment logs to identify:
- Build failures
- Runtime errors
- Configuration issues
- Missing dependencies
- Port binding errors

#### 2. Common Issue Detection

**Issue: Repository Access**
```
Error: "It looks like we don't have access to your repo"
Diagnosis: GitHub authorization not granted
Fix: Authorize Render GitHub app in GitHub settings
Automated: No (requires manual user action)
```

**Issue: Requirements File Not Found**
```
Error: "Could not open requirements file: No such file or directory"
Diagnosis: Root directory not set or incorrect
Fix: Set Root Directory to "backend" in Render settings
Automated: Yes (provide exact setting to change)
```

**Issue: Gunicorn Not Installed**
```
Error: "gunicorn: command not found"
Diagnosis: gunicorn missing from requirements.txt
Fix: Add "gunicorn>=21.2.0" to requirements.txt
Automated: Yes (can modify file and commit)
```

**Issue: Port Binding Error**
```
Error: "gunicorn: error: unrecognized arguments: --port 10000"
Diagnosis: Incorrect port parameter syntax
Fix: Change "--port $PORT" to "--bind 0.0.0.0:$PORT"
Automated: Yes (provide corrected start command)
```

**Issue: Database Connection Failed**
```
Error: "sqlalchemy.exc.DatabaseError: connection refused"
Diagnosis: DATABASE_URL incorrect or missing sslmode
Fix: Verify DATABASE_URL and add "?sslmode=require" for Neon
Automated: Partial (can verify format, user must confirm credentials)
```

**Issue: CORS Errors**
```
Error: "Access-Control-Allow-Origin header missing"
Diagnosis: Frontend URL not in CORS_ORIGINS
Fix: Add frontend URL to CORS_ORIGINS environment variable
Automated: Yes (provide updated CORS_ORIGINS value)
```

#### 3. Fix Generation
For each identified issue:
1. Provide clear explanation of the problem
2. Explain why it occurred
3. Provide step-by-step fix instructions
4. If automated, make the necessary changes
5. Verify fix was successful

#### 4. Prevention Recommendations
Suggests configuration improvements to prevent future issues:
- Add validation checks
- Improve error messages
- Update documentation
- Create deployment checklist

### Input
- Render deployment logs
- Error messages
- Current configuration
- Previous deployment history

### Output
- Issue diagnosis report
- Step-by-step fix instructions
- Automated fixes (when possible)
- Prevention recommendations

---

## Subagent: deployment-verifier

### Purpose
Verifies successful deployment and validates all endpoints and connections.

### Model
`haiku` (Claude Haiku 4.5) - Fast, efficient model for verification tasks

### Tools Available
- `Bash` - Execute curl commands for endpoint testing
- `Read` - Read configuration and expected responses

### Responsibilities

#### 1. Health Check Verification
```bash
# Test health endpoint
curl -s https://taskpilot-api-xyz.onrender.com/health

# Expected response:
{
  "status": "ok",
  "message": "TaskPilotAI API is running"
}

# Validates:
- Returns HTTP 200
- JSON response is valid
- No connection errors
- Response time < 500ms
```

#### 2. API Endpoint Testing
```bash
# Test signup endpoint
curl -X POST https://taskpilot-api-xyz.onrender.com/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123!","name":"Test"}'

# Expected response:
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer"
}

# Validates:
- Signup works
- Returns valid JWT tokens
- Database connection working
```

#### 3. Database Connection Verification
Checks Render logs for:
```
[INFO] Application startup complete
[INFO] Database connected successfully
```

Ensures:
- SQLModel tables created
- No connection errors
- Queries executing successfully

#### 4. CORS Verification
```bash
# Test CORS with frontend origin
curl -H "Origin: https://frontend.vercel.app" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: Content-Type" \
  -X OPTIONS \
  https://taskpilot-api-xyz.onrender.com/tasks

# Expected response headers:
Access-Control-Allow-Origin: https://frontend.vercel.app
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, PATCH
Access-Control-Allow-Headers: Content-Type, Authorization
```

#### 5. JWT Authentication Verification
```bash
# Test protected endpoint without token (should fail)
curl https://taskpilot-api-xyz.onrender.com/tasks

# Expected: 401 Unauthorized

# Test protected endpoint with valid token (should succeed)
curl -H "Authorization: Bearer $TOKEN" \
  https://taskpilot-api-xyz.onrender.com/tasks

# Expected: 200 OK with task list
```

#### 6. Performance Metrics
Measures and reports:
- Health check response time
- API endpoint response times
- Database query times
- Cold start time (on free tier)

### Input
- Live backend URL
- Expected responses
- Test credentials
- Performance thresholds

### Output
- Verification report (all checks passed/failed)
- Performance metrics
- Any warnings or issues found
- Recommendations for optimization

---

## Subagent: environment-manager

### Purpose
Manages environment variables, secrets, and configuration across environments.

### Model
`haiku` (Claude Haiku 4.5) - Efficient for configuration management

### Tools Available
- `Read` - Read .env files and configuration
- `Write` - Generate .env templates and documentation

### Responsibilities

#### 1. Environment Variable Generation
Creates complete .env template for backend:

```env
# Database Configuration
DATABASE_URL=postgresql://user:password@host:port/database?sslmode=require

# JWT Configuration
JWT_SECRET=your-jwt-secret-minimum-32-characters-required
JWT_ALGORITHM=HS256
JWT_EXPIRY_SECONDS=604800
JWT_REFRESH_EXPIRY_SECONDS=1209600

# Better Auth
BETTER_AUTH_SECRET=your-better-auth-secret-minimum-32-characters

# CORS Configuration
CORS_ORIGINS=["https://frontend.vercel.app","http://localhost:3000"]

# Environment
ENVIRONMENT=production
```

#### 2. Secret Validation
Validates all secrets meet requirements:
- JWT_SECRET: minimum 32 characters
- BETTER_AUTH_SECRET: minimum 32 characters
- DATABASE_URL: valid PostgreSQL connection string format
- CORS_ORIGINS: valid JSON array of URLs

#### 3. Environment-Specific Configuration

**Development (.env.local)**
```env
DATABASE_URL=postgresql://localhost/taskpilot_dev
JWT_SECRET=dev-secret-key-for-testing-only
CORS_ORIGINS=["http://localhost:3000","http://localhost:8000"]
ENVIRONMENT=development
```

**Production (Render Dashboard)**
```env
DATABASE_URL=postgresql://neon-production-db/...
JWT_SECRET=production-secret-32-plus-characters-random-generated
CORS_ORIGINS=["https://taskpilot.vercel.app"]
ENVIRONMENT=production
```

#### 4. Security Recommendations
Provides guidance on:
- Secret generation (use `openssl rand -base64 32`)
- Secret rotation schedules
- Preventing secrets in code/commits
- Using different secrets per environment
- Database credential management

#### 5. Documentation Generation
Creates comprehensive environment variable documentation:
- What each variable does
- Required vs optional
- Default values
- Valid formats/values
- Where to obtain values
- Security considerations

### Input
- Project configuration
- Target environment (dev/staging/production)
- Database connection details
- Frontend URLs

### Output
- Complete .env template
- Environment variable documentation
- Security recommendations
- Validation checklist

---

## Subagent Interaction Flow

```
User Request: Deploy backend to Render
          ↓
[render-configurator]
- Creates service configuration
- Sets up environment variables
- Configures build/start commands
          ↓
User: Triggers deployment in Render
          ↓
[deployment-troubleshooter] (if errors occur)
- Analyzes logs
- Identifies issues
- Provides fixes
- Applies automated fixes
          ↓
Deployment succeeds
          ↓
[deployment-verifier]
- Tests health endpoint
- Verifies API endpoints
- Checks database connection
- Validates CORS
- Measures performance
          ↓
[environment-manager]
- Documents all environment variables
- Provides management procedures
- Generates security recommendations
          ↓
Deployment Complete ✅
```

---

## Subagent Coordination

### Parallel Execution
Some subagents can run in parallel:
- `environment-manager` can generate docs while `render-configurator` sets up service
- `deployment-verifier` can prepare test cases while deployment is in progress

### Sequential Dependencies
Other steps must be sequential:
1. `render-configurator` must complete before deployment starts
2. Deployment must succeed before `deployment-verifier` can test
3. `deployment-troubleshooter` only runs if issues are detected

### Error Handling
If any subagent fails:
1. Report failure clearly
2. Provide diagnostic information
3. Suggest remediation steps
4. Allow user to retry or abort

---

## Subagent Communication

### Information Shared Between Subagents

**render-configurator → deployment-verifier**
- Backend URL
- Expected endpoints
- Health check path

**deployment-troubleshooter → render-configurator**
- Configuration corrections
- Updated settings
- Fixes to apply

**environment-manager → render-configurator**
- Complete environment variable list
- Validated secrets
- Configuration recommendations

---

## Performance Characteristics

| Subagent | Model | Avg Time | Cost | Parallelizable |
|----------|-------|----------|------|----------------|
| render-configurator | Sonnet | 2-3 min | Medium | No |
| deployment-troubleshooter | Sonnet | 1-2 min | Medium | No |
| deployment-verifier | Haiku | 30-60 sec | Low | Yes |
| environment-manager | Haiku | 30-60 sec | Low | Yes |

**Total Estimated Time**: 5-8 minutes (excluding manual steps and Render build time)

---

## Quality Assurance

Each subagent performs self-validation:

**render-configurator**
- ✅ All required settings configured
- ✅ Environment variables complete
- ✅ Commands are valid syntax

**deployment-troubleshooter**
- ✅ Issue correctly identified
- ✅ Fix is appropriate
- ✅ Prevention steps documented

**deployment-verifier**
- ✅ All endpoints return expected status
- ✅ Response times within threshold
- ✅ No errors in logs

**environment-manager**
- ✅ All required variables present
- ✅ Secrets meet length requirements
- ✅ URLs are valid format

---

## Usage Example

```bash
# Invoke Render deployment skill
/render-deploy --project TaskPilotAI \
               --backend-dir backend \
               --branch phase-2 \
               --database-url $DATABASE_URL \
               --jwt-secret $JWT_SECRET \
               --cors-origins "https://taskpilot.vercel.app,http://localhost:3000"

# Subagents execute automatically:
[render-configurator] Generating service configuration...
[render-configurator] Environment variables configured ✅
[render-configurator] Build command: pip install -r requirements.txt ✅
[render-configurator] Start command: gunicorn main:app... ✅

# User triggers deployment in Render dashboard

[deployment-troubleshooter] Monitoring deployment logs...
[deployment-troubleshooter] Issue detected: gunicorn not found
[deployment-troubleshooter] Applying fix: Adding gunicorn to requirements.txt...
[deployment-troubleshooter] Fix applied ✅

[deployment-verifier] Testing health endpoint...
[deployment-verifier] Health check: 200 OK ✅
[deployment-verifier] Testing API endpoints...
[deployment-verifier] All endpoints verified ✅

[environment-manager] Generating documentation...
[environment-manager] RENDER_BACKEND_MANAGEMENT.md created ✅

Deployment complete! 🚀
Backend URL: https://taskpilot-api-5l18.onrender.com
```

---

## Extending Subagents

To add new capabilities:

1. Define new subagent in `manifest.json`
2. Document responsibilities in this file
3. Specify tools and model requirements
4. Define input/output interfaces
5. Add to coordination flow
6. Update skill-definition.yaml

---

**Last Updated**: December 14, 2025
**Version**: 1.0.0
**Status**: Production
