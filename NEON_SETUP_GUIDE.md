# 🚀 NEON POSTGRESQL SETUP GUIDE FOR TASKPILOTAI

## ⏱️ Time to Complete: 5-10 minutes

---

## **STEP 1: Create Neon Account**

### Go to Neon Console
1. Open browser and go to: **https://console.neon.tech**
2. Click **Sign Up**
3. Choose signup method:
   - Email address (recommend)
   - Google account
   - GitHub account

4. Fill in details and verify email

✅ **DONE** - You now have a Neon account

---

## **STEP 2: Create a Neon Project**

1. After login, you'll see the Neon dashboard
2. Click **Create Project** (or it auto-creates one)
3. Give it a name: `taskpilot-ai` (or any name)
4. Region: Choose closest to you (e.g., `us-east-1`)
5. Click **Create Project**

⏳ **Wait 30 seconds for setup**

✅ **DONE** - Your PostgreSQL database is ready!

---

## **STEP 3: Get Your Connection String**

1. In the Neon dashboard, find your project
2. Look for **Connection String** section
3. Copy the PostgreSQL connection string
4. It will look like this:

```
postgresql://neon_user:AbC123XyZ@ep-fancy-lake-12345.us-east-1.aws.neon.tech/neondb?sslmode=require
```

### ⚠️ Important: Keep this secret!
This is like your database password. Don't share it.

---

## **STEP 4: Create Backend .env File**

Create a new file: `/home/bilal/TaskPilotAI/backend/.env`

Add these lines (replace with YOUR connection string):

```env
# Database
DATABASE_URL=postgresql://YOUR_USER:YOUR_PASSWORD@YOUR_HOST/YOUR_DB?sslmode=require

# JWT Configuration
JWT_SECRET=your-secret-key-here-min-32-chars-long-for-prod
JWT_ALGORITHM=HS256
JWT_EXPIRY_SECONDS=604800
JWT_REFRESH_EXPIRY_SECONDS=1209600

# Better Auth
BETTER_AUTH_SECRET=your-better-auth-secret-here-min-32-chars

# CORS
CORS_ORIGINS=["http://localhost:3000", "http://localhost:8000", "https://your-vercel-url.vercel.app"]

# Environment
ENVIRONMENT=production
```

### Example with Real Values:
```env
DATABASE_URL=postgresql://neon_user:abc123xyz@ep-fancy-lake-12345.us-east-1.aws.neon.tech/neondb?sslmode=require
JWT_SECRET=my-secret-key-that-is-32-chars-or-longer-production
JWT_ALGORITHM=HS256
JWT_EXPIRY_SECONDS=604800
JWT_REFRESH_EXPIRY_SECONDS=1209600
BETTER_AUTH_SECRET=my-better-auth-secret-32-chars-or-longer
CORS_ORIGINS=["http://localhost:3000","http://localhost:8000"]
ENVIRONMENT=production
```

✅ **DONE** - Backend is configured for Neon

---

## **STEP 5: Update Backend to Use Neon**

Your backend's `backend/config.py` should already have:

```python
class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./taskpilot.db"  # This will be overridden by .env
    # ... other settings
```

The `.env` file you created will **override** the default SQLite with your Neon PostgreSQL URL.

✅ **DONE**

---

## **STEP 6: Test Connection Locally**

Run this command to verify the connection works:

```bash
cd /home/bilal/TaskPilotAI/backend

# Start backend with Neon
python -m uvicorn main:app --reload --port 8000
```

### Expected Output:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

### If you see this, connection is working ✅

### If you see an error:
```
psycopg2.OperationalError: could not translate host name
```

This means the connection string is invalid. Double-check:
- ✓ Host name is correct
- ✓ Username is correct
- ✓ Password is correct (and no special characters need escaping)
- ✓ Database name is correct

---

## **STEP 7: Run Migrations (SQLModel Auto-creates Tables)**

The FastAPI backend uses SQLModel which **automatically creates tables** on startup.

Just start the server and tables are created in Neon:
```bash
python -m uvicorn main:app --reload
```

✅ **Tables automatically created in Neon!**

You can verify in Neon console:
1. Go to https://console.neon.tech
2. Click your project
3. Click **SQL Editor**
4. Run: `\dt` (shows all tables)

---

## **STEP 8: Test with Sample Data**

Once server is running, test signup:

```bash
curl -X POST "http://localhost:8000/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPassword123",
    "name": "Test User"
  }'
```

### Expected Response:
```json
{
  "access_token": "eyJhbGci...",
  "refresh_token": "eyJhbGci...",
  "token_type": "bearer"
}
```

✅ **Data is being stored in Neon!**

---

## **Summary: What You Just Did**

| Step | Action | Status |
|------|--------|--------|
| 1 | Created Neon account | ✅ |
| 2 | Created PostgreSQL database | ✅ |
| 3 | Got connection string | ✅ |
| 4 | Created backend `.env` file | ✅ |
| 5 | Configured backend for Neon | ✅ |
| 6 | Tested connection | ✅ |
| 7 | Created tables in Neon | ✅ |
| 8 | Tested with sample data | ✅ |

---

## **Next Steps: Deploy to Railway**

Now that your backend uses Neon PostgreSQL, you're ready to deploy!

1. Push code to GitHub with `.env` variables
2. Deploy to Railway.app
3. Set environment variables on Railway
4. Get public Railway URL
5. Update frontend `.env.local` with that URL
6. Deploy frontend to Vercel

---

## **Useful Neon Console Features**

### View Your Database:
1. https://console.neon.tech
2. Click your project
3. Click **SQL Editor**
4. Run queries directly (no need to use terminal)

### Check Connection Status:
- Green checkmark = Connected
- Red X = Connection failed

### Connection Pooling:
- For serverless (Railway), use: `?sslmode=require`
- Neon handles connection pooling automatically

---

## **Common Issues & Solutions**

### ❌ "password authentication failed"
- Copy connection string again from Neon
- Make sure password doesn't have special characters
- If it does, URL-encode it (e.g., `@` becomes `%40`)

### ❌ "could not translate host name"
- Check internet connection
- Make sure you copied full host name
- Verify no spaces in connection string

### ❌ "ssl: certificate_verify_failed"
- This is normal in development
- Connection string already has `?sslmode=require`
- Should work fine on production (Railway handles SSL)

### ✅ Everything working?
Great! You can now deploy to Railway with confidence! 🚀

---

## **Quick Reference**

```bash
# Show your current backend config
echo $DATABASE_URL

# Test Neon connection
python -c "
import os
from sqlmodel import create_engine, Session
engine = create_engine(os.getenv('DATABASE_URL'))
with Session(engine) as session:
    result = session.exec('SELECT 1')
    print('✅ Connected to Neon PostgreSQL!')
"

# Start backend with Neon
python -m uvicorn main:app --reload --port 8000
```

---

**Questions? Check Neon docs: https://neon.tech/docs**

**Ready to deploy? Next step is Railway! 🚀**
