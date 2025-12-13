# 🚀 VERCEL DEPLOYMENT GUIDE FOR TASKPILOTAI FRONTEND

## ⏱️ Time to Complete: 5-10 minutes

---

## **STEP 1: Create Vercel Account**

### Go to Vercel Console
1. Open browser and go to: **https://vercel.com**
2. Click **Sign Up**
3. Choose signup method:
   - GitHub account (recommended)
   - GitLab account
   - Bitbucket account
   - Email address

4. Authorize Vercel to access your GitHub account

✅ **DONE** - You now have a Vercel account

---

## **STEP 2: Import Your GitHub Repository**

1. In Vercel dashboard, click **Add New...** → **Project**
2. Search for your **TaskPilotAI** repository
3. Select the repository and click **Import**
4. Vercel will auto-detect that it's a Next.js project

✅ **DONE** - Repository imported

---

## **STEP 3: Configure Build Settings**

### Vercel should auto-detect these settings:

- **Framework**: Next.js
- **Root Directory**: `./frontend` (may need to set this)
- **Build Command**: `npm run build`
- **Output Directory**: `.next`
- **Install Command**: `npm install`

### If not auto-detected:

1. Click **Settings** during import
2. Set **Root Directory** to `frontend`
3. Keep other settings as default

✅ **DONE** - Build settings configured

---

## **STEP 4: Set Environment Variables**

### In Vercel Dashboard:

1. During import, look for **Environment Variables** section
2. Click **+ Add** and add:

```
NEXT_PUBLIC_API_URL=https://taskpilot-api-xyz123.railway.app
```

### Replace with your actual Railway URL!

Example values:
```
NEXT_PUBLIC_API_URL=https://taskpilot-api-abc123xyz.railway.app
```

**Note**: Only variables starting with `NEXT_PUBLIC_` are available in browser.

✅ **DONE** - Environment variables set

---

## **STEP 5: Deploy to Vercel**

1. Click **Deploy** button
2. Vercel will:
   - Pull code from GitHub
   - Install dependencies (`npm install`)
   - Build the project (`npm run build`)
   - Deploy to Vercel's CDN

⏳ **Wait 2-5 minutes for deployment**

### Expected Output:
```
✓ Production deployment ready
✓ Your app is live at: https://taskpilot-frontend-xyz123.vercel.app
```

✅ **DONE** - Frontend deployed!

---

## **STEP 6: Verify Deployment**

### Visit Your Live Frontend:

1. Vercel will give you a domain: `https://taskpilot-frontend-abc123.vercel.app`
2. Click the link or visit it in your browser
3. You should see the TaskPilotAI signin page

### Test the Frontend:

1. Click **Sign Up**
2. Enter email, password, name
3. If connection succeeds, you should be redirected to dashboard
4. Create a few test tasks
5. Verify all operations work (create, edit, delete, complete, filter)

✅ **Frontend is live and connected to backend!**

---

## **STEP 7: Get Your Vercel URL**

Your frontend URL format:
```
https://taskpilot-frontend-abc123xyz.vercel.app
```

OR if you have a custom domain:
```
https://your-custom-domain.com
```

Save this for hackathon submission!

✅ **DONE** - Vercel URL saved

---

## **STEP 8: Enable Auto-Deploy (Optional)**

By default, Vercel auto-deploys on every push to your GitHub repository.

### To enable/verify:

1. In Vercel dashboard, click **Settings**
2. Go to **Git** section
3. Verify **Auto-redeploy on push** is enabled
4. Select which branch to deploy (usually `phase-2`)

✅ **DONE** - Auto-deploy enabled

---

## **STEP 9: Monitor Deployment**

### In Vercel Dashboard:

1. Click **Deployments** tab
2. See all deployment history
3. Click on a deployment to see:
   - Build logs
   - Deployment status
   - Performance metrics

### If Deployment Fails:

Check logs for:
- **Build errors**: Check `npm run build` output
- **Missing dependencies**: Run `npm install` locally
- **Environment variable errors**: Verify NEXT_PUBLIC_API_URL is set
- **TypeScript errors**: Run `npm run type-check`

---

## **STEP 10: Custom Domain (Optional)**

If you want a custom domain:

1. In Vercel dashboard, click **Settings** → **Domains**
2. Click **Add** and enter your domain
3. Follow DNS configuration instructions
4. Vercel automatically provisions SSL certificate

Example:
```
taskpilot.yourdomain.com
```

✅ **DONE** - Custom domain configured (optional)

---

## **Summary: What You Just Did**

| Step | Action | Status |
|------|--------|--------|
| 1 | Created Vercel account | ✅ |
| 2 | Imported GitHub repo | ✅ |
| 3 | Configured build settings | ✅ |
| 4 | Set environment variables | ✅ |
| 5 | Deployed to Vercel | ✅ |
| 6 | Verified deployment | ✅ |
| 7 | Got Vercel URL | ✅ |
| 8 | Enabled auto-deploy | ✅ |

---

## **Next Steps: Final Submission**

Now that both frontend and backend are deployed:

1. ✅ Backend URL: `https://taskpilot-api-abc123xyz.railway.app`
2. ✅ Frontend URL: `https://taskpilot-frontend-xyz123.vercel.app`
3. **Next**: Record 90-second demo video
4. **Then**: Submit to hackathon form

---

## **Useful Vercel Features**

### Redeploy Anytime:
- Push code to GitHub → auto-deploy
- Click **Redeploy** button in dashboard for manual redeploy

### Environment Variables:
- Add/edit anytime in Settings
- Changes take effect on next deployment

### Analytics:
- View performance metrics
- Monitor page load times
- Check error rates

### Logs:
- Real-time build logs
- Runtime logs
- Error tracking

### Preview Deployments:
- Every pull request gets preview URL
- Test before merging to main

---

## **Troubleshooting**

### ❌ "404 - Not Found"
- Check that you're visiting the correct URL
- Wait 2-3 minutes for deployment to complete
- Refresh the page

### ❌ "Cannot connect to backend"
- Verify NEXT_PUBLIC_API_URL is correct
- Make sure Railway backend is running
- Check CORS settings in backend

### ❌ "Build failed"
- Check `npm run build` locally: `cd frontend && npm run build`
- Fix any build errors
- Push code again

### ❌ "Module not found"
- Run `npm install` locally
- Verify package.json has all dependencies
- Check node_modules are not in .gitignore

### ❌ "TypeScript errors during build"
- Run `npm run type-check` locally
- Fix any type errors
- Push code again

### ✅ Everything working?

Perfect! Your full-stack application is now live! 🎉

---

## **Final Checklist Before Submission**

- [ ] Backend deployed to Railway
- [ ] Frontend deployed to Vercel
- [ ] Frontend can signin/signup
- [ ] Frontend can create tasks
- [ ] Frontend can update/delete tasks
- [ ] Frontend can filter tasks
- [ ] No console errors in browser
- [ ] Both URLs working and accessible

---

## **Quick Reference**

```bash
# Your deployed URLs
Frontend: https://taskpilot-frontend-abc123.vercel.app
Backend: https://taskpilot-api-xyz123.railway.app

# Test frontend locally before deploying
cd frontend
npm run dev
# Visit http://localhost:3000

# Build frontend locally to catch errors
npm run build

# Type check
npm run type-check

# Redeploy from Vercel dashboard anytime
# Just click "Redeploy" button
```

---

**Questions? Check Vercel docs: https://vercel.com/docs**

**Next step: Record demo video and submit to hackathon! 🚀**
