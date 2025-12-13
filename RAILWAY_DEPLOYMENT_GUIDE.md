# 🚀 RAILWAY DEPLOYMENT GUIDE FOR TASKPILOTAI BACKEND

## ⏱️ Time to Complete: 10-15 minutes

---

## **STEP 1: Create Railway Account**

### Go to Railway Console
1. Open browser and go to: **https://railway.app**
2. Click **Login** or **Sign Up**
3. Choose signup method:
   - GitHub account (recommended - easier)
   - Google account
   - Email address

4. Complete signup and verify email

✅ **DONE** - You now have a Railway account

---

## **STEP 2: Create New Railway Project**

1. Go to **Dashboard** (after login)
2. Click **+ New Project**
3. Select **Deploy from GitHub** (recommended)
4. Authorize Railway to access your GitHub
5. Select your **TaskPilotAI** repository
6. Click **Create**

⏳ **Wait 30 seconds for project creation**

✅ **DONE** - Project created

---

## **STEP 3: Connect Your GitHub Repository**

1. In Railway dashboard, you should see your project
2. Click **GitHub** or the GitHub icon
3. Connect your TaskPilotAI repository
4. Select which branch to deploy (`phase-2`)

✅ **DONE** - GitHub connected

---

## **STEP 4: Add Neon PostgreSQL Database**

Railway can automatically provision PostgreSQL, but we want to use your existing Neon database.

### Option A: Use Your Existing Neon Database (Recommended)

1. In Railway dashboard, click **+ Add Service**
2. Select **PostgreSQL** but scroll and look for **External Database**
3. Or simply add environment variables instead (see Step 5)

### Option B: Skip (We'll use environment variables)

We'll configure the Neon connection string via environment variables in the next step.

---

## **STEP 5: Set Environment Variables**

### In Railway Dashboard:

1. Click on your project
2. Look for **Variables** or **Environment** tab
3. Click **+ Add Variable** and add these:

```
DATABASE_URL=postgresql://neondb_owner:npg_XhTvgf9EQ5AO@ep-summer-cell-a1ugz95d-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require

JWT_SECRET=taskpilot-jwt-secret-key-must-be-32-chars-minimum-for-production-use

JWT_ALGORITHM=HS256

JWT_EXPIRY_SECONDS=604800

JWT_REFRESH_EXPIRY_SECONDS=1209600

BETTER_AUTH_SECRET=taskpilot-better-auth-secret-32-chars-minimum-for-production

CORS_ORIGINS=["https://taskpilot-frontend.vercel.app","http://localhost:3000","http://127.0.0.1:3000"]

ENVIRONMENT=production
```

✅ **DONE** - Environment variables set

---

## **STEP 6: Configure Deployment Settings**

### In Railway Dashboard:

1. Click **Settings** for your project
2. Look for **Deployment** or **Build** settings
3. Set:
   - **Root Directory**: `backend` (if not auto-detected)
   - **Build Command**: Leave empty or use `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Or Create Procfile (optional):

If Railway doesn't auto-detect, create `Procfile` in `/backend/`:

```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

✅ **DONE** - Deployment configured

---

## **STEP 7: Deploy to Railway**

### Automatic Deployment (Recommended):

1. Make sure your GitHub repository is connected
2. Every push to `phase-2` branch will automatically deploy
3. OR click **Deploy** button in Railway dashboard

### Manual Deployment:

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Link your project
railway link

# Deploy
railway up
```

⏳ **Wait 2-5 minutes for deployment**

### Expected Output:
```
✓ Deployment successful
✓ Your app is live at: https://taskpilot-api-xyz123.railway.app
```

✅ **DONE** - Backend deployed!

---

## **STEP 8: Verify Deployment**

### Test Your Live Backend:

```bash
# Get your Railway URL from dashboard
RAILWAY_URL="https://taskpilot-api-xyz123.railway.app"

# Test health endpoint
curl -s "$RAILWAY_URL/health" | jq .

# Test signup
curl -X POST "$RAILWAY_URL/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPassword123",
    "name": "Test User"
  }' | jq .
```

### Expected Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

✅ **Backend is live and working!**

---

## **STEP 9: Get Your Railway URL**

In Railway Dashboard:

1. Click your project
2. Look for **Domains** or **URL** section
3. Copy the public URL (looks like `https://taskpilot-api-xyz123.railway.app`)
4. Save this for later when deploying frontend

### Example Format:
```
https://taskpilot-api-abc123xyz.railway.app
```

✅ **DONE** - Railway URL saved

---

## **STEP 10: Monitor Logs**

### In Railway Dashboard:

1. Click **Logs** tab
2. Watch real-time application logs
3. Look for errors or issues

### If Deployment Fails:

Check logs for:
- **Build errors**: Fix and push again
- **Database connection error**: Verify DATABASE_URL environment variable
- **Port errors**: Railway automatically handles port via `$PORT` variable

---

## **Summary: What You Just Did**

| Step | Action | Status |
|------|--------|--------|
| 1 | Created Railway account | ✅ |
| 2 | Created Railway project | ✅ |
| 3 | Connected GitHub repo | ✅ |
| 4 | Set environment variables | ✅ |
| 5 | Configured deployment | ✅ |
| 6 | Deployed to Railway | ✅ |
| 7 | Verified deployment | ✅ |
| 8 | Got Railway URL | ✅ |

---

## **Next Steps: Deploy Frontend to Vercel**

Now that backend is deployed:

1. Note your Railway URL: `https://taskpilot-api-xyz123.railway.app`
2. Create `.env.local` in frontend with:
   ```
   NEXT_PUBLIC_API_URL=https://taskpilot-api-xyz123.railway.app
   ```
3. Deploy frontend to Vercel (see VERCEL_DEPLOYMENT_GUIDE.md)
4. Test frontend + backend integration
5. Record demo video
6. Submit to hackathon

---

## **Useful Railway Features**

### View Logs:
- Real-time application logs
- Deployment logs
- Error tracking

### Environment Variables:
- Add/edit variables anytime
- Deploy automatically restarts with new variables
- No need to redeploy code

### Domains:
- Railway gives free domain
- Can add custom domain (optional)
- HTTPS automatically enabled

### Database Connection:
- Neon PostgreSQL is external (not managed by Railway)
- Connection via DATABASE_URL environment variable
- No need to provision Railway PostgreSQL

---

## **Common Issues & Solutions**

### ❌ "502 Bad Gateway"
- Check database connection string
- Verify all environment variables are set
- Check application logs in Railway dashboard

### ❌ "Build failed"
- Check requirements.txt for syntax errors
- Verify Python version compatibility
- Check build logs in Railway dashboard

### ❌ "Database connection refused"
- Verify DATABASE_URL is correct
- Check Neon database is accessible from Railway
- Verify SSL mode is set to `require`

### ❌ "Port already in use"
- Railway handles port automatically via `$PORT` environment variable
- Make sure your Procfile or start command uses `$PORT`

### ✅ Everything working?

Great! Your backend is now live and ready for frontend integration! 🚀

---

## **Quick Reference**

```bash
# Test your live backend
RAILWAY_URL="https://taskpilot-api-abc123xyz.railway.app"
curl -s "$RAILWAY_URL/health"

# Your Railway URL format
https://taskpilot-api-[random-id].railway.app

# Environment variables you need
DATABASE_URL=[your-neon-connection-string]
JWT_SECRET=[32-char-minimum]
BETTER_AUTH_SECRET=[32-char-minimum]
CORS_ORIGINS=[your-frontend-urls]
ENVIRONMENT=production

# Next: Deploy frontend to Vercel
# See VERCEL_DEPLOYMENT_GUIDE.md
```

---

**Questions? Check Railway docs: https://docs.railway.app**

**Ready to deploy frontend? Next step is Vercel! 🚀**
