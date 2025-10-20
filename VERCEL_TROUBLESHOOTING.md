# Vercel Deployment Troubleshooting

## Quick Fixes Applied

### Issue: API routes returning 404 or errors

**Fixed by:**
1. Updated `vercel.json` to point to correct serverless function (`api/index.py`)
2. Fixed API path configuration in `src/config/api.js` to avoid double `/api/api` paths
3. Updated `.gitignore` to exclude build artifacts

## After Making Changes

**Redeploy to Vercel:**

```bash
# Commit changes
git add .
git commit -m "Fix Vercel API routing"
git push origin main
```

Vercel will automatically redeploy on push.

## How to Check if Backend is Working

Visit these URLs in your browser (replace `your-app` with your Vercel app name):

1. **Health check**: `https://your-app.vercel.app/api/health`
   - Should return: `{"status": "healthy"}`

2. **Root endpoint**: `https://your-app.vercel.app/api/`
   - Should return API welcome message

3. **API docs**: `https://your-app.vercel.app/api/docs`
   - Should show FastAPI Swagger UI

4. **Test Hacker News**: `https://your-app.vercel.app/api/v1/hacker-news/?limit=5`
   - Should return JSON with articles

## Common Errors and Solutions

### Error: "Failed to fetch" or CORS errors

**Solution:**
Check that `backend/app/core/config.py` includes your Vercel domain in `ALLOWED_ORIGINS`:

```python
ALLOWED_ORIGINS: list = ["*"]  # or ["https://your-app.vercel.app"]
```

### Error: "500 Internal Server Error" from API

**Check Vercel Function Logs:**
1. Go to Vercel Dashboard → Your Project
2. Click "Functions" tab
3. Click on `/api/index` function
4. View error logs

**Common causes:**
- Missing Python dependencies
- Import errors in backend code
- Timeout (Vercel has 10s limit on Hobby plan)

### Error: API routes return 404

**Verify routing:**
1. Check `vercel.json` routes section
2. Ensure `api/index.py` exists
3. Check Vercel build logs for Python build errors

### Frontend shows but API doesn't work

**Check browser console:**
1. Open DevTools (F12)
2. Check Network tab
3. Look for failed API requests
4. Verify the URL being called is `/api/v1/...` (not `http://localhost:8000/...`)

## Environment Variables on Vercel

If you need to add environment variables:

1. Go to Vercel Dashboard → Your Project → Settings
2. Click "Environment Variables"
3. Add variables (they'll be available in your backend)
4. Redeploy for changes to take effect

## Rebuild and Redeploy

If nothing works, try a fresh deployment:

```bash
# Using Vercel CLI
vercel --prod --force

# Or via Dashboard
# Go to Deployments → Click three dots → Redeploy
```

## Still Having Issues?

1. **Check build logs** in Vercel Dashboard → Deployments → [Latest] → View Build Logs
2. **Check function logs** in Vercel Dashboard → Functions → `/api/index`
3. **Test locally first**:
   ```bash
   npm run build
   npm run preview
   ```
4. **Verify all files are committed**:
   ```bash
   git status
   ```

## Expected Behavior After Fix

✅ Frontend loads at `https://your-app.vercel.app`
✅ API health check works at `/api/health`
✅ Hacker News articles load in the UI
✅ RSS feeds load in the UI
✅ Article modals open and display content
✅ No CORS errors in browser console
