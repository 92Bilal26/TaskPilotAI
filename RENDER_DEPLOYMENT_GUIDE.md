# 🚀 RENDER DEPLOYMENT GUIDE FOR TASKPILOTAI BACKEND

## ⏱️ Time to Complete: 10-15 minutes

---

## **STEP 1: Create Render Account**

### Go to Render Console
1. Open browser and go to: **https://render.com**
2. Click **Get Started** or **Sign Up**
3. Choose signup method:
   - GitHub account (recommended - easier deployment)
   - Google account
   - Email address

4. Complete signup and verify email

✅ **DONE** - You now have a Render account

---

## **STEP 2: Create New Web Service on Render**

1. Go to **Dashboard** (after login)
2. Click **+ New +** → **Web Service**
3. Connect your GitHub account if not already connected
4. Search for your **TaskPilotAI** repository
5. Select the repository and click **Connect**

⏳ **Wait 30 seconds for repository connection**

✅ **DONE** - Repository connected

---

## **STEP 3: Configure Web Service Settings**

In the Render web service creation form, fill in:

### Basic Settings:
- **Name**: `taskpilot-api` (or any name you prefer)
- **Root Directory**: `backend`
- **Environment**: `Python 3.11` (or latest available)
- **Region**: Select closest to you (e.g., `Oregon`, `Ohio`)
- **Branch**: `phase-2`

### Build & Start Commands:
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --port $PORT`

### Plan:
- Select **Free** plan (free tier available)
- Or select **Paid** for better performance

✅ **DONE** - Settings configured

---

## **STEP 4: Set Environment Variables**

### In Render Web Service Dashboard:

1. Go to **Environment** tab
2. Click **Add Environment Variable** and add these:

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

**Replace** values with your actual secrets and URLs!

✅ **DONE** - Environment variables set

---

## **STEP 5: Deploy to Render**

### Click Deploy:

1. Review all settings are correct
2. Click **Create Web Service**
3. Render will automatically:
   - Build your Python application
   - Install dependencies from requirements.txt
   - Start the web service

⏳ **Wait 3-5 minutes for first deployment**

### Watch the Logs:

- Render shows real-time deployment logs
- You should see:
  ```
  Building application...
  Installing dependencies...
  Starting application...
  Application is running on port 10000
  ```

✅ **DONE** - Backend deployed!

---

## **STEP 6: Get Your Render URL**

In Render Dashboard:

1. Your web service will have a public URL
2. Look at the top of the service page
3. Your URL will look like: `https://taskpilot-api-[random].onrender.com`
4. Copy and save this URL

### Important Notes:
- Free tier services sleep after 15 minutes of inactivity
- First request after sleep takes 30 seconds
- Paid tier keeps service always running
- URL is accessible 24/7 (but may be slow on free tier)

✅ **DONE** - Render URL saved

---

## **STEP 7: Verify Deployment**

### Test Your Live Backend:

```bash
# Replace with your Render URL
RENDER_URL="https://taskpilot-api-[random].onrender.com"

# Test health endpoint
curl -s "$RENDER_URL/health" | jq .

# Expected response:
# {"status":"ok","message":"TaskPilotAI API is running"}
```

### Test Signup Endpoint:

```bash
curl -X POST "$RENDER_URL/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPassword123",
    "name": "Test User"
  }' | jq .

# Expected response:
# {"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...","refresh_token":"...","token_type":"bearer"}
```

✅ **Backend is live and working!**

---

## **STEP 8: Monitor and Manage**

### View Logs:
1. Go to **Logs** tab in Render dashboard
2. See real-time application logs
3. Check for errors or issues

### Redeploy Anytime:
1. Push changes to GitHub (`phase-2` branch)
2. Render automatically redeploys
3. Or click **Manual Deploy** in dashboard

### View Metrics:
1. Go to **Metrics** tab
2. See:
   - Request count
   - Response times
   - CPU/Memory usage
   - Errors

---

## **STEP 9: Handle Free Tier Sleep**

### On Free Tier:
- Service sleeps after 15 minutes of inactivity
- First request wakes it up (takes ~30 seconds)
- Recommended for testing/development

### To Avoid Sleep:
- Upgrade to **Paid** plan ($7/month minimum)
- Or use **Railway.app** (also has free tier with better features)

### Alternative: Use Keep-Alive Service
```bash
# Configure a cron job to ping your backend every 10 minutes
# This keeps the service awake on free tier
# Many free services available: cron-job.org, uptimerobot.com
```

---

## **STEP 10: Custom Domain (Optional)**

### Add Custom Domain:
1. In Render dashboard, go to **Settings**
2. Click **Add Domain**
3. Follow DNS configuration instructions
4. SSL certificate automatically provisioned

### Example:
```
api.yourdomain.com
```

✅ **DONE** - Custom domain configured (optional)

---

## **Summary: Render vs Railway**

| Feature | Render | Railway |
|---------|--------|---------|
| **Free Tier** | ✅ Yes (sleeps after 15 min) | ✅ Yes |
| **Paid Tier** | $7/month | $5/month minimum |
| **Deployment Speed** | ~3-5 min | ~2-3 min |
| **Performance** | Good | Excellent |
| **Free Tier Support** | Limited | Good |
| **Custom Domain** | ✅ Yes | ✅ Yes |
| **Database Integration** | External only | External only |

**Recommendation**:
- Use **Railway** if you want faster, more reliable service
- Use **Render** if you want to try free tier first
- Both work well with Neon PostgreSQL

---

## **What You Just Did**

| Step | Action | Status |
|------|--------|--------|
| 1 | Created Render account | ✅ |
| 2 | Connected GitHub repo | ✅ |
| 3 | Configured web service | ✅ |
| 4 | Set environment variables | ✅ |
| 5 | Deployed to Render | ✅ |
| 6 | Got Render URL | ✅ |
| 7 | Verified deployment | ✅ |
| 8 | Monitored logs | ✅ |
| 9 | Understood free tier | ✅ |

---

## **Next Steps: Deploy Frontend to Vercel**

Now that backend is deployed:

1. Note your Render URL: `https://taskpilot-api-[random].onrender.com`
2. Create `.env.local` in frontend with:
   ```
   NEXT_PUBLIC_API_URL=https://taskpilot-api-[random].onrender.com
   ```
3. Deploy frontend to Vercel (see VERCEL_DEPLOYMENT_GUIDE.md)
4. Test frontend + backend integration
5. Record demo video
6. Submit to hackathon

---

## **Troubleshooting**

### ❌ "Service not found" or "404"
- Wait 1-2 minutes for first deployment to complete
- Check build logs in Render dashboard
- Verify START_COMMAND is correct

### ❌ "Build failed"
- Check requirements.txt for syntax errors
- Verify Python version compatibility
- Check build logs in Render dashboard

### ❌ "Database connection refused"
- Verify DATABASE_URL is correct in environment variables
- Check Neon database is accessible from Render
- Verify SSL mode is set to `require`

### ❌ "Port error" or "Cannot bind to port"
- Use `$PORT` environment variable
- Render assigns port automatically
- Don't hardcode port 8000

### ❌ "Service is sleeping" (Free tier)
- First request after 15 min inactivity takes 30 seconds
- Either upgrade to paid, or use keep-alive service
- Or switch to Railway which has better free tier

### ✅ Everything working?

Great! Your backend is live and ready for frontend integration! 🚀

---

## **Quick Reference**

```bash
# Test your live Render backend
RENDER_URL="https://taskpilot-api-[random].onrender.com"
curl -s "$RENDER_URL/health"

# Your Render URL format
https://taskpilot-api-[random].onrender.com

# Environment variables needed
DATABASE_URL=[your-neon-connection-string]
JWT_SECRET=[32-char-minimum]
BETTER_AUTH_SECRET=[32-char-minimum]
CORS_ORIGINS=[your-frontend-urls]
ENVIRONMENT=production

# Start command for Python
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --port $PORT
```

---

## **Common Issues on Free Tier**

1. **Service goes to sleep after 15 minutes of inactivity**
   - First request takes 30 seconds to respond
   - Solution: Upgrade to paid plan or use keep-alive service

2. **Build takes longer**
   - Free tier has slower build resources
   - Solution: Upgrade to paid plan for faster builds

3. **Limited to 1 free service**
   - Free tier can only have 1 active web service
   - Solution: Delete other services or upgrade

---

**Questions? Check Render docs: https://render.com/docs**

**Ready to deploy frontend? See VERCEL_DEPLOYMENT_GUIDE.md! 🚀**
