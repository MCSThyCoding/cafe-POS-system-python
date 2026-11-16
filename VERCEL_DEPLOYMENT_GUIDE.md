# Cafe POS - Vercel Deployment Guide

## Overview
Cafe POS is a Flask app (`app.py`) backed by PostgreSQL (Neon). Vercel auto-detects
the Flask `app` at the project root and deploys it as a single serverless function —
no `api/` folder or `vercel.json` needed. The same `app.py` serves the frontend,
the REST API, and static files.

## Prerequisites
- GitHub account with this repo pushed
- Vercel account (free Hobby plan)
- Neon PostgreSQL database (already set up — see `init_db.py`)

## Step 1: Database (already done)
The Neon database `coffee-POS-python` is initialized with tables and seed data.
To re-run or reset it locally:

```bash
python init_db.py   # reads DATABASE_URL from .env
```

## Step 2: Deploy to Vercel
1. Go to https://vercel.com → **Add New... → Project**
2. Import `MCSThyCoding/cafe-POS-system-python`
3. Vercel detects **Flask** automatically — leave Framework Preset, Build Command,
   and Output Directory at their defaults. Root Directory: `./`
4. Before clicking Deploy, open **Environment Variables** and add:

   | Key | Value |
   |-----|-------|
   | `DATABASE_URL` | `postgresql://neondb_owner:...@ep-old-cloud-...neon.tech/coffee-POS-python?sslmode=require&channel_binding=require` (same as `.env`) |
   | `CAFE_POS_SECRET` | a long random string (e.g. from https://randomkeygen.com) |

   Apply them to **Production** (and Preview if wanted).

5. Click **Deploy**.

## Step 3: Test
1. Open the deployment URL (e.g. `https://<project>.vercel.app`)
2. Log in:
   - Admin: `admin` / `admin123`
   - Cashier: `cashier` / `cashier123`
3. Place a test order and check the dashboard/reports.

## Notes
- `.env` is gitignored and NOT used on Vercel — env vars must be set in the
  Vercel dashboard (or `vercel env add`).
- The app opens a fresh Neon connection per request; the `-pooler` hostname in
  `DATABASE_URL` is required for serverless workloads (already in use).
- `CAFE_POS_SECRET` signs JWTs — changing it logs everyone out.
- Logs appear in Vercel → Project → Logs (the app falls back to stdout when the
  filesystem is read-only).

## Render alternative
`render.yaml` is also included if you prefer a always-on Flask server:
`python app.py` with the same two env vars set in the Render dashboard.
