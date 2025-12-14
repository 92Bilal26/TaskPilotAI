# Environment Configuration Guide

This guide explains how the TaskPilotAI frontend automatically handles different environments (local development vs production deployment).

---

## Automatic Environment Detection ✅

The application **automatically detects** whether it's running locally or in production and uses the appropriate API URL. No manual configuration changes needed!

### How It Works

The app uses a **3-tier priority system** to determine the API URL:

1. **Environment Variables** (Highest Priority)
   - `.env.development` → Used during `npm run dev`
   - `.env.production` → Used during `npm run build` and on Vercel
   - `.env.local` → Overrides all (for local testing)

2. **Auto-Detection** (If no env var)
   - Checks `window.location.hostname`
   - If hostname includes `vercel.app` or `taskpilot` → Production API
   - If hostname is `localhost` or `127.0.0.1` → Local API

3. **Fallback** (If auto-detection fails)
   - Checks `NODE_ENV`
   - If `production` → Production API
   - If `development` → Local API

---

## Environment Files

### `.env.development` (Local Development)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Used when:**
- Running `npm run dev`
- Developing locally

### `.env.production` (Production Deployment)
```env
NEXT_PUBLIC_API_URL=https://taskpilot-api-5l18.onrender.com
```

**Used when:**
- Running `npm run build`
- Deployed on Vercel
- Production environment

### `.env.local` (Local Override - Optional)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Used when:**
- You want to override default settings locally
- Testing production API from local machine
- **Note**: This file is gitignored and won't be committed

### `.env.example` (Template)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Purpose:**
- Template for new developers
- Documents required environment variables
- Copy to `.env.local` for local development

---

## API URLs by Environment

| Environment | API URL | Frontend URL |
|-------------|---------|--------------|
| **Local Development** | http://localhost:8000 | http://localhost:3000 |
| **Vercel Production** | https://taskpilot-api-5l18.onrender.com | https://task-pilot-ai-ashen.vercel.app |

---

## Usage

### Local Development

```bash
# 1. Start backend (in backend directory)
cd backend
python -m uvicorn main:app --reload --port 8000

# 2. Start frontend (in frontend directory)
cd frontend
npm run dev

# Frontend will automatically use: http://localhost:8000
# Visit: http://localhost:3000
```

### Production Deployment (Vercel)

```bash
# 1. Commit changes
git add .
git commit -m "your changes"
git push origin phase-2

# 2. Vercel automatically deploys
# Frontend will automatically use: https://taskpilot-api-5l18.onrender.com
# Visit: https://task-pilot-ai-ashen.vercel.app
```

**No configuration changes needed!** ✅

---

## Centralized Configuration

All environment settings are managed in `lib/config.ts`:

```typescript
import { config, getApiUrl } from '@/lib/config';

// Get API URL
const apiUrl = getApiUrl(); // Automatically detects environment

// Check environment
if (config.app.environment === 'production') {
  // Production-specific code
}

// Use feature flags
if (config.features.enableDebugLogging) {
  console.log('Debug info');
}
```

### Available Config

```typescript
config.api.baseUrl          // API base URL (auto-detected)
config.api.timeout          // Request timeout (30s)
config.auth.tokenKey        // localStorage key for access token
config.auth.refreshTokenKey // localStorage key for refresh token
config.app.name             // Application name
config.app.version          // Application version
config.app.environment      // Current environment
config.features.*           // Feature flags
```

---

## Testing Different Environments

### Test Local API
```bash
# Just run npm run dev
npm run dev
# Uses: http://localhost:8000
```

### Test Production API from Local
```bash
# Option 1: Use .env.local
echo "NEXT_PUBLIC_API_URL=https://taskpilot-api-5l18.onrender.com" > .env.local
npm run dev

# Option 2: Set environment variable
NEXT_PUBLIC_API_URL=https://taskpilot-api-5l18.onrender.com npm run dev
```

### Test Production Build Locally
```bash
# Build for production
npm run build

# Start production server
npm start

# Uses: https://taskpilot-api-5l18.onrender.com (from .env.production)
```

---

## Vercel Environment Variables

When deploying to Vercel, environment variables are automatically set from `.env.production`.

### To Update Vercel Environment Variables:

1. Go to https://vercel.com/dashboard
2. Select your project: `task-pilot-ai-ashen`
3. Go to **Settings** → **Environment Variables**
4. Add/update: `NEXT_PUBLIC_API_URL`
5. Redeploy

**Or** just update `.env.production` and push to GitHub—Vercel will use it automatically!

---

## Debugging

### Check which API URL is being used

**In Browser Console:**
```javascript
// Development mode shows:
[API Client] Initialized with URL: http://localhost:8000
[API Client] Environment: development

// Production mode shows:
[API Client] Initialized with URL: https://taskpilot-api-5l18.onrender.com
[API Client] Environment: production
```

### Verify Environment

**In Browser Console:**
```javascript
// Check current API URL
console.log(process.env.NEXT_PUBLIC_API_URL);

// Check if in production
console.log(process.env.NODE_ENV);
```

**In Code:**
```typescript
import { config } from '@/lib/config';

console.log('Environment:', config.app.environment);
console.log('API URL:', config.api.baseUrl);
```

---

## Common Issues

### Issue: Frontend can't connect to backend

**Symptoms:**
- Network errors in browser console
- "Failed to fetch" errors
- CORS errors

**Solutions:**

1. **Check backend is running:**
   ```bash
   curl http://localhost:8000/health
   # Should return: {"status":"ok","message":"TaskPilotAI API is running"}
   ```

2. **Check API URL is correct:**
   - Open browser console
   - Look for `[API Client] Initialized with URL:`
   - Verify it matches your backend URL

3. **Check CORS configuration:**
   - Backend must allow frontend origin
   - Update `backend/.env` CORS_ORIGINS to include your frontend URL

### Issue: Using wrong API URL

**Symptoms:**
- Local dev connects to production API
- Production connects to localhost (won't work)

**Solutions:**

1. **Clear .env.local:**
   ```bash
   rm frontend/.env.local
   ```

2. **Verify .env files:**
   ```bash
   cat frontend/.env.development  # Should have localhost
   cat frontend/.env.production   # Should have Render URL
   ```

3. **Restart dev server:**
   ```bash
   # Stop current server (Ctrl+C)
   npm run dev
   ```

### Issue: Environment variables not updating

**Solutions:**

1. **Restart Next.js dev server** (environment variables are cached)
   ```bash
   # Stop server (Ctrl+C)
   npm run dev
   ```

2. **Clear .next cache:**
   ```bash
   rm -rf .next
   npm run dev
   ```

3. **Rebuild for production:**
   ```bash
   npm run build
   ```

---

## Security Best Practices

### ✅ DO

- Keep `.env.local` in `.gitignore`
- Use different secrets for development and production
- Store sensitive secrets in Vercel dashboard (not in code)
- Use `NEXT_PUBLIC_` prefix only for client-side variables

### ❌ DON'T

- Commit `.env.local` to Git
- Put sensitive backend secrets in frontend env vars
- Use production secrets in development
- Hardcode API URLs in code

---

## File Structure

```
frontend/
├── .env.development         # Local development API URL
├── .env.production          # Production API URL (Vercel)
├── .env.local              # Local override (gitignored)
├── .env.example            # Template for new developers
├── lib/
│   ├── config.ts           # Centralized configuration
│   └── api.ts              # API client with auto-detection
└── ENVIRONMENT_SETUP.md    # This file
```

---

## Summary

🎯 **Zero Configuration Required!**

The app automatically:
- ✅ Detects local vs production environment
- ✅ Uses correct API URL for each environment
- ✅ Logs configuration in development mode
- ✅ Works seamlessly on Vercel after deployment

**For local development:**
```bash
npm run dev
```

**For production:**
```bash
git push origin phase-2
# Vercel auto-deploys with production settings
```

That's it! No manual configuration changes needed. 🚀

---

**Last Updated**: December 14, 2025
**Frontend URL (Production)**: https://task-pilot-ai-ashen.vercel.app
**Backend URL (Production)**: https://taskpilot-api-5l18.onrender.com
**Backend URL (Development)**: http://localhost:8000
