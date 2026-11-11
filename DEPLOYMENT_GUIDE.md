# Cafe POS - Deployment Guide

## Current Issue
Your app is deployed on Vercel, but **Vercel cannot host Flask applications with databases**. This is why:
- The frontend loads (HTML/CSS/JS)
- API calls fail (no Flask backend)
- Payments don't work (no database)

## Solution: Deploy on Render

Render is a hosting service that supports Flask + PostgreSQL with a free tier.

### Step 1: Create a Render Account
1. Go to https://render.com
2. Sign up with GitHub
3. Connect your GitHub repository

### Step 2: Deploy Web Service
1. Click "New +" → "Web Service"
2. Select your repository: `MCSThyCoding/cafe-POS-system-python`
3. Configure:
   - **Name:** cafe-pos
   - **Region:** Oregon (or closest to you)
   - **Branch:** main
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python app.py`
4. Click "Advanced"
5. Add Environment Variable:
   - Key: `PORT`
   - Value: `10000`
   - Key: `CAFE_POS_SECRET`
   - Value: Generate a random string
6. Click "Create Web Service"

### Step 3: Deploy PostgreSQL Database
1. Click "New +" → "PostgreSQL"
2. Name: cafe-pos-db
3. Click "Create Database"
4. Copy the **Internal Database URL** from the database page

### Step 4: Update Environment Variables
1. Go to your web service on Render
2. Click "Environment"
3. Add these variables:
   - `DATABASE_URL`: (paste the Internal Database URL from step 3)
   - `PORT`: `10000`
   - `CAFE_POS_SECRET`: (generate a random string)

### Step 5: Update app.py for PostgreSQL
The current app uses SQLite. For production, you need to switch to PostgreSQL.

**Modify app.py:**
```python
# Replace SQLite with PostgreSQL
import os
import psycopg2
from psycopg2.extras import RealDictCursor

# Use DATABASE_URL from environment
DATABASE_URL = os.environ.get("DATABASE_URL")
if DATABASE_URL:
    # PostgreSQL for production
    def get_db():
        if "db" not in g:
            g.db = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
        return g.db
else:
    # SQLite for local development
    DB_PATH = os.path.join(BASE_DIR, "cafe_pos.db")
    def get_db():
        if "db" not in g:
            g.db = sqlite3.connect(DB_PATH)
            g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
        return g.db
```

**Update requirements.txt:**
```
Flask>=3.0
PyJWT>=2.8
psycopg2-binary>=2.9
```

### Step 6: Push Changes to GitHub
```bash
git add .
git commit -m "Add PostgreSQL support for production deployment"
git push origin main
```

Render will automatically redeploy with the new code.

### Step 7: Access Your App
1. Wait for deployment to complete (check Render dashboard)
2. Your app will be available at: `https://cafe-pos.onrender.com`
3. Test login and payment functionality

## Alternative: Railway

If you prefer Railway:
1. Go to https://railway.app
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Railway will detect Flask and set up PostgreSQL automatically
5. Click "Deploy"

## Alternative: PythonAnywhere

1. Go to https://www.pythonanywhere.com
2. Create a free account
3. Create a new Web app
4. Upload your files
5. Install requirements
6. Configure WSGI file
7. Set up PostgreSQL database

## Why Not Vercel?

Vercel is designed for:
- Static sites (HTML/CSS/JS) ✅
- Serverless functions (short-lived API calls) ✅
- **NOT** persistent Flask servers ❌
- **NOT** file-based databases (SQLite) ❌

Your Cafe POS needs:
- Persistent Flask server ✅
- Database for orders/products ✅

## Local Testing

Before deploying, test locally:
```bash
cd /Users/sethy/Desktop/cafe_pos
source venv/bin/activate
python app.py
```

Then open http://localhost:3000 and test:
- Login with admin/admin123
- Add items to cart
- Complete order (this should work locally)

## Summary

**To fix the payment issue:**
1. Deploy on Render (free tier available)
2. Add PostgreSQL database
3. Update app.py to use PostgreSQL
4. Push changes to GitHub
5. Test on the deployed URL

The payment functionality will work once the Flask backend and database are properly hosted.
