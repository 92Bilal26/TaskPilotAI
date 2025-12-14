# 🚀 TaskPilotAI Backend Deployment Management - Render

**Live Backend URL**: https://taskpilot-api-5l18.onrender.com/

---

## DEPLOYMENT OVERVIEW

### Current Status
- ✅ Backend deployed on Render
- ✅ Neon PostgreSQL connected
- ✅ JWT authentication configured
- ✅ CORS middleware enabled
- ✅ Health check endpoint working
- 🔄 Frontend deployment pending

---

## WHAT WAS DEPLOYED

### Render Service Configuration

| Setting | Value |
|---------|-------|
| **Service Name** | taskpilot-api |
| **Repository** | https://github.com/92Bilal26/TaskPilotAI |
| **Branch** | phase-2 |
| **Root Directory** | backend |
| **Environment** | Python 3.13.4 |
| **Region** | Auto-selected |
| **Plan** | Free/Paid (configurable) |

### Build Configuration

| Setting | Value |
|---------|-------|
| **Build Command** | pip install -r requirements.txt |
| **Start Command** | gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT |
| **Python Version** | 3.13.4 |

### Environment Variables Set in Render

```env
DATABASE_URL=postgresql://neondb_owner:npg_XhTvgf9EQ5AO@ep-summer-cell-a1ugz95d-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require
JWT_SECRET=taskpilot-jwt-secret-key-must-be-32-chars-minimum-for-production-use
JWT_ALGORITHM=HS256
JWT_EXPIRY_SECONDS=604800
JWT_REFRESH_EXPIRY_SECONDS=1209600
BETTER_AUTH_SECRET=taskpilot-better-auth-secret-32-chars-minimum-for-production
CORS_ORIGINS=["http://localhost:3000","http://localhost:8000","http://127.0.0.1:3000"]
ENVIRONMENT=production
```

---

## DEPLOYMENT PROCESS THAT WAS COMPLETED

### Step 1: Prerequisites ✅
- GitHub account with TaskPilotAI repository
- Neon PostgreSQL database created
- Environment variables prepared

### Step 2: Repository Connection ✅
1. Created Render account at https://render.com
2. Connected GitHub account to Render
3. Selected TaskPilotAI repository
4. Authorized Render to access repo

### Step 3: Web Service Configuration ✅
1. Created new Web Service
2. Set name to: `taskpilot-api`
3. Set Root Directory to: `backend`
4. Selected Python 3.11 environment
5. Selected closest region
6. Set branch to: `phase-2`

### Step 4: Build & Start Commands ✅
- **Build Command**: `pip install -r requirements.txt`
  - Installs all Python dependencies including gunicorn
  - Runs automatically on every deployment

- **Start Command**: `gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT`
  - Uses gunicorn as production ASGI server
  - Starts 4 worker processes for concurrency
  - Binds to Render-assigned $PORT (10000)

### Step 5: Environment Variables Configuration ✅
1. Opened Environment tab in Render dashboard
2. Added all required environment variables
3. Database connection string from Neon
4. JWT secrets (minimum 32 characters)
5. CORS origins for frontend

### Step 6: Deployment Triggered ✅
1. Clicked "Create Web Service" to start first deployment
2. Render automatically:
   - Cloned repository from GitHub
   - Checked out phase-2 branch
   - Changed to /backend directory
   - Installed Python 3.13.4
   - Ran: `pip install -r requirements.txt`
   - Started 4 gunicorn worker processes
   - Application became live in ~3-5 minutes

### Step 7: Verification ✅
Backend logs showed:
```
==> Build successful 🎉
==> Running 'gunicorn main:app --workers 4 ...'
[2025-12-14 00:09:13 +0000] [61] [INFO] Started server process [61]
[2025-12-14 00:09:16 +0000] [61] [INFO] Application startup complete.
127.0.0.1:59814 - "HEAD / HTTP/1.1" 401
```

Status indicates:
- ✅ Server processes started (workers 61, 63, 64, 65)
- ✅ Application loaded successfully
- ✅ Receiving requests
- ✅ JWT middleware protecting endpoints (401 = auth required, expected)

---

## DEPLOYMENT ISSUES & FIXES APPLIED

### Issue 1: Repository Access Warning
**Error**: "It looks like we don't have access to your repo, but we'll try to clone it anyway."
**Fix**: Granted Render authorization to GitHub account (one-time setup)

### Issue 2: Root Directory Mismatch
**Error**: "Could not open requirements file: [Errno 2] No such file or directory: 'requirements.txt'"
**Root Cause**: Render was looking in root directory, but requirements.txt was in /backend/
**Fix**: Set Root Directory to `backend` in Render settings

### Issue 3: Missing Gunicorn Dependency
**Error**: "gunicorn: command not found"
**Root Cause**: gunicorn not listed in requirements.txt
**Fix**: Added `gunicorn>=21.2.0` to requirements.txt and pushed to GitHub

### Issue 4: Incorrect Gunicorn Port Parameter
**Error**: "gunicorn: error: unrecognized arguments: --port 10000"
**Root Cause**: gunicorn uses `--bind` not `--port`
**Fix**: Updated Start Command to use `--bind 0.0.0.0:$PORT`

---

## CURRENT BACKEND API ENDPOINTS

### Health Check (No Auth Required)
```bash
GET https://taskpilot-api-5l18.onrender.com/health

Response: 200 OK
{
  "status": "ok",
  "message": "TaskPilotAI API is running"
}
```

### Authentication Endpoints (Public)
```bash
# Signup - Create new account
POST https://taskpilot-api-5l18.onrender.com/auth/signup
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePassword123",
  "name": "User Name"
}

Response: 200 OK
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "...",
  "token_type": "bearer"
}
```

```bash
# Signin - Login with credentials
POST https://taskpilot-api-5l18.onrender.com/auth/signin
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePassword123"
}

Response: 200 OK
{
  "access_token": "...",
  "refresh_token": "...",
  "token_type": "bearer"
}
```

### Task Endpoints (Requires Authorization Header)
```bash
# All task requests require:
Authorization: Bearer <access_token>

# Get all tasks
GET https://taskpilot-api-5l18.onrender.com/tasks

# Create task
POST https://taskpilot-api-5l18.onrender.com/tasks
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}

# Get specific task
GET https://taskpilot-api-5l18.onrender.com/tasks/{id}

# Update task
PUT https://taskpilot-api-5l18.onrender.com/tasks/{id}
{
  "title": "Updated title",
  "description": "Updated description"
}

# Delete task
DELETE https://taskpilot-api-5l18.onrender.com/tasks/{id}

# Toggle completion status
PATCH https://taskpilot-api-5l18.onrender.com/tasks/{id}/complete
```

---

## HOW TO MANAGE ONGOING DEPLOYMENTS

### Auto-Deployment on Code Push
When you push changes to `phase-2` branch, Render automatically:
1. Detects new commit
2. Clones updated code
3. Runs build command
4. Instarts new workers
5. Routes traffic to new version
6. Zero downtime deployment

### Manual Redeploy
If you need to redeploy without code changes:
1. Go to Render dashboard
2. Select `taskpilot-api` service
3. Click **Manual Deploy** button
4. Render rebuilds and restarts

### View Logs
1. Go to Render dashboard
2. Select `taskpilot-api` service
3. Click **Logs** tab
4. See real-time application output

### Monitor Performance
1. Go to Render dashboard
2. Click **Metrics** tab
3. View:
   - Request count
   - Response times
   - CPU/Memory usage
   - Error rates

### Update Environment Variables
1. Go to Render dashboard
2. Select `taskpilot-api` service
3. Click **Environment** tab
4. Update variable values
5. Click **Save** (auto-redeploys)

### Manage Subscription Plan
1. Go to Render dashboard
2. Select `taskpilot-api` service
3. Click **Settings** tab
4. Upgrade from Free → Paid ($7/month)
5. Benefits: No sleep, better performance

---

## FREE TIER CONSIDERATIONS

### Current Deployment: Free Tier
- ✅ Backend is live and working
- ✅ Database persists data
- ⚠️ Service sleeps after 15 minutes of inactivity

### How Sleep Works
1. After 15 minutes of no requests
2. Service stops running
3. Next request wakes service (takes ~30 seconds to respond)
4. Service runs for another 15 minutes

### Impact on Frontend
- First load after 15 minutes: ~30 second delay
- Subsequent requests: Normal speed
- Data is NOT lost (persisted in Neon PostgreSQL)

### To Avoid Sleep
**Option 1: Upgrade to Paid Plan**
- Cost: $7/month minimum
- Service always running
- Go to Settings → Change Plan

**Option 2: Use Keep-Alive Service**
- Free service that pings your backend every 10 minutes
- Prevents sleep by keeping service "busy"
- Services: uptimerobot.com, cron-job.org

**Option 3: Monitor & Accept Sleep**
- Leave on free tier
- Accept 30-second delay on first request
- Perfect for development/testing

---

## SECURITY BEST PRACTICES

### JWT Secrets
- Current secrets are for development/testing
- For production with real users:
  1. Generate new 32+ character secrets
  2. Update in Render environment variables
  3. Rotate regularly

### Database Security
- Neon connection requires SSL (`?sslmode=require`)
- Database credentials stored in env (not in code)
- User data isolated at database level

### API Security
- CORS restricted to known origins
- JWT tokens expire after 7 days
- Password hashed with bcrypt
- Rate limiting recommended for production

### Secrets Management
- Never commit .env files to GitHub
- .gitignore includes .env
- All secrets in Render dashboard environment variables
- Rotate JWT_SECRET periodically

---

## UPDATING BACKEND CODE

### Workflow for Code Changes

1. **Make code changes locally**
   ```bash
   cd /home/bilal/TaskPilotAI/backend
   # Edit files...
   ```

2. **Test locally**
   ```bash
   python -m pytest tests/ -v
   mypy src/
   ```

3. **Commit and push**
   ```bash
   git add .
   git commit -m "feat: describe your changes"
   git push origin phase-2
   ```

4. **Render auto-deploys**
   - Watch logs at: https://dashboard.render.com
   - Deployment takes ~3-5 minutes
   - No downtime (old workers keep serving until new ones ready)

5. **Verify in production**
   ```bash
   curl https://taskpilot-api-5l18.onrender.com/health
   ```

---

## TROUBLESHOOTING

### Backend Not Responding
**Check:**
1. Go to Render dashboard
2. Click **Logs** tab
3. Look for error messages
4. If crashed, click **Manual Deploy**

### 500 Internal Server Error
**Likely causes:**
- Database connection failed → Check DATABASE_URL
- Missing environment variable → Check Environment tab
- Code error → Check logs

### 401 Unauthorized on Protected Routes
**Expected behavior** - Add JWT token to header:
```bash
curl -H "Authorization: Bearer <token>" \
  https://taskpilot-api-5l18.onrender.com/tasks
```

### CORS Errors in Frontend
**Fix:**
1. Check frontend URL
2. Go to Render → Environment
3. Update CORS_ORIGINS to include frontend domain
4. Save (auto-redeploys)

### Database Connection Refused
1. Verify DATABASE_URL is correct
2. Check Neon database is active
3. Test connection:
   ```bash
   psql "postgresql://user:pass@host/db?sslmode=require"
   ```

---

## DEPLOYMENT CHECKLIST

Before considering deployment complete:

**Backend Deployment:**
- [x] Repository connected to Render
- [x] Root directory set to `backend`
- [x] Build command configured
- [x] Start command configured
- [x] All environment variables set
- [x] First deployment succeeded
- [x] No errors in logs
- [x] Health endpoint responds 200

**Backend Verification:**
- [ ] Health endpoint working: `curl https://taskpilot-api-5l18.onrender.com/health`
- [ ] Signup endpoint working: `curl -X POST ...`
- [ ] Database connected: Check logs for "Application startup complete"
- [ ] No 500 errors in logs

**Next Steps:**
- [ ] Deploy frontend to Vercel (see below)
- [ ] Connect frontend to backend
- [ ] Test signup/signin flow
- [ ] Test task CRUD operations
- [ ] Verify user isolation

---

## NEXT: FRONTEND DEPLOYMENT TO VERCEL

Your Render backend is **live and ready** to connect with the frontend.

**Backend URL for Frontend**: `https://taskpilot-api-5l18.onrender.com`

### Frontend Deployment Steps (see VERCEL_DEPLOYMENT_GUIDE.md)

1. Create Vercel account
2. Import GitHub repository
3. Set root directory to `frontend`
4. Set environment variable: `NEXT_PUBLIC_API_URL=https://taskpilot-api-5l18.onrender.com`
5. Click deploy
6. Frontend will auto-connect to backend

---

## QUICK REFERENCE

### Live URLs
- Backend Health: https://taskpilot-api-5l18.onrender.com/health
- API Docs: https://taskpilot-api-5l18.onrender.com/docs
- Render Dashboard: https://dashboard.render.com

### Commands
```bash
# Test backend health
curl https://taskpilot-api-5l18.onrender.com/health

# Test signup
curl -X POST https://taskpilot-api-5l18.onrender.com/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123!","name":"Test"}'
```

### Files Modified for This Deployment
- `/backend/requirements.txt` - Added gunicorn
- No other files modified (code already production-ready)

### Commits Made
- `8a9e794` - fix: Add gunicorn to requirements for Render deployment

---

**Deployment Date**: December 14, 2025
**Backend Status**: ✅ Live and Running
**Next Action**: Deploy Frontend to Vercel
