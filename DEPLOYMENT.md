# Deployment Guide

## Deploying to Vercel (Full-Stack)

This guide covers deploying both the React frontend and FastAPI backend to Vercel.

### Deployment Steps

#### Option 1: Deploy via Vercel Dashboard (Recommended)

1. **Push your code to Git**
   ```bash
   git add .
   git commit -m "Prepare for Vercel deployment"
   git push origin main
   ```

2. **Import Project to Vercel**
   - Go to [vercel.com/new](https://vercel.com/new)
   - Import your Git repository
   - Vercel will auto-detect the configuration from `vercel.json`

3. **Configure Build Settings**
   - **Framework Preset:** Vite
   - **Build Command:** `npm run vercel-build` (auto-detected)
   - **Output Directory:** `dist` (auto-detected)
   - **Install Command:** `npm install` (auto-detected)

4. **Environment Variables** (Optional)
   - Click "Environment Variables"
   - Add any backend environment variables from `backend/.env.example`
   - Note: Frontend uses relative API paths in production, so no VITE_API_URL needed

5. **Deploy**
   - Click "Deploy"
   - Wait for build to complete (usually 1-2 minutes)
   - Your app will be live at `https://your-project.vercel.app`

#### Option 2: Deploy via Vercel CLI

1. **Install Vercel CLI**
   ```bash
   npm i -g vercel
   ```

2. **Login to Vercel**
   ```bash
   vercel login
   ```

3. **Deploy**
   ```bash
   vercel
   # Follow the prompts
   # First deployment will ask configuration questions
   ```

4. **Deploy to Production**
   ```bash
   vercel --prod
   ```

### How It Works

The `vercel.json` configuration sets up:

1. **Frontend Build**: Vite builds the React app to `dist/`
2. **Backend Serverless**: FastAPI runs as serverless functions via `/api/*` routes
3. **Routing**:
   - `/api/*` → FastAPI backend
   - `/*` → React frontend (SPA)

### API Endpoints

Once deployed, your API will be available at:
- `https://your-project.vercel.app/api/v1/hacker-news/`
- `https://your-project.vercel.app/api/v1/rss/`
- `https://your-project.vercel.app/api/docs` (API documentation)

### Local Development vs Production

**Local Development:**
- Frontend: `http://localhost:5173`
- Backend: `http://localhost:8000`
- API calls use `VITE_API_URL=http://localhost:8000` from `.env`

**Production (Vercel):**
- Frontend: `https://your-project.vercel.app`
- Backend: Same domain at `/api/*`
- API calls use relative paths `/api/v1/*`

### Troubleshooting

#### Build Fails

1. **Check build logs** in Vercel dashboard
2. **Verify dependencies** are in `package.json` and `requirements.txt`
3. **Test build locally**:
   ```bash
   npm run build
   ```

#### API Routes Not Working

1. **Check `vercel.json`** routing configuration
2. **Verify `api/index.py`** exists and imports correctly
3. **Check Python requirements** in root `requirements.txt`

#### CORS Issues

FastAPI backend includes CORS middleware in `backend/main.py`. If you encounter CORS issues:
- Check `ALLOWED_ORIGINS` in `backend/app/core/config.py`
- Add your Vercel domain to allowed origins

### Alternative: Deploy Frontend Only

If you want to deploy only the frontend and host the backend elsewhere:

1. **Update `.env`**:
   ```
   VITE_API_URL=https://your-backend-url.com
   ```

2. **Remove API config from `vercel.json`**:
   ```json
   {
     "builds": [
       {
         "src": "package.json",
         "use": "@vercel/static-build",
         "config": { "distDir": "dist" }
       }
     ]
   }
   ```

3. **Deploy backend to**:
   - [Railway](https://railway.app) (Recommended for Python)
   - [Render](https://render.com)
   - [Fly.io](https://fly.io)
   - AWS Lambda / Google Cloud Functions

### Custom Domain

1. Go to your project in Vercel Dashboard
2. Click "Settings" → "Domains"
3. Add your custom domain
4. Update DNS records as instructed

### Monitoring

- **Logs**: Available in Vercel Dashboard → Deployments → View logs
- **Analytics**: Built-in analytics in Vercel Dashboard
- **Errors**: Check Functions tab for backend errors

---

## Build Commands Summary

For quick reference:

| Command | Description |
|---------|-------------|
| `npm run dev` | Run both frontend & backend locally |
| `npm run build` | Build frontend for production |
| `npm run vercel-build` | Build for Vercel deployment |
| `npm run preview` | Preview production build locally |

---

**Need help?** Check the [Vercel Documentation](https://vercel.com/docs) or open an issue in the repository.
