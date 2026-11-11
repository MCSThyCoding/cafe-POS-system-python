# Quick Start: Add PostgreSQL Database

## Step 1: Create Free PostgreSQL Database (Neon)

1. Go to https://neon.tech
2. Click "Sign up" (free, no credit card required)
3. Sign up with GitHub or Google
4. Click "Create a project"
5. Enter project name: `cafe-pos-db`
6. Select a region (choose closest to you)
7. Click "Create project"
8. Wait for database to be created (about 30 seconds)
9. Click "Connection details"
10. Copy the **Connection string** (it looks like):
   ```
   postgresql://neondb_owner:xxxxx@ep-xxxxx.us-east-2.aws.neon.tech/neondb?sslmode=require
   ```

## Step 2: Initialize Database

1. Open the file `init_db.py` in your project
2. Replace line 7 with your connection string:
   ```python
   DATABASE_URL = "postgresql://neondb_owner:xxxxx@ep-xxxxx.us-east-2.aws.neon.tech/neondb?sslmode=require"
   ```
3. Save the file
4. Install required packages:
   ```bash
   pip install psycopg2-binary werkzeug
   ```
5. Run the initialization script:
   ```bash
   python init_db.py
   ```
6. You should see:
   ```
   ✓ Seeded users
   ✓ Seeded products
   ✅ Database initialized successfully!
   ```

## Step 3: Deploy to Vercel with Database

1. Go to https://vercel.com
2. Sign up/login with GitHub
3. Click "Add New..." → "Project"
4. Click "Import" next to your repository: `MCSThyCoding/cafe-POS-system-python`
5. Configure:
   - **Project Name:** cafe-pos
   - **Framework Preset:** Other
   - **Root Directory:** `./`
   - Leave Build and Output directories empty
6. Click "Environment Variables"
7. Add two variables:
   
   **Variable 1:**
   - Key: `DATABASE_URL`
   - Value: (paste your Neon connection string from Step 1)
   
   **Variable 2:**
   - Key: `CAFE_POS_SECRET`
   - Value: (generate a random string, e.g., `abc123xyz789`)
   
8. Click "Add" for each variable
9. Click "Deploy"
10. Wait for deployment to complete (about 2-3 minutes)

## Step 4: Test Your App

1. Once deployment finishes, click the deployed URL
2. You should see the login screen
3. Login with:
   - Username: `admin`
   - Password: `admin123`
4. Go to Point of Sale
5. Add an item to cart
6. Select payment method (Cash or Card)
7. Click "Complete Order"
8. **Payment should now work!** ✅

## Troubleshooting

### "Database connection failed"
- Check that DATABASE_URL is correct in Vercel environment variables
- Ensure the connection string includes `?sslmode=require`
- Verify your Neon database is active

### "Table does not exist"
- Make sure you ran `python init_db.py` with the correct DATABASE_URL
- Check that the script completed successfully

### "Payment still fails"
- Check Vercel deployment logs (click your project → Logs)
- Verify both environment variables are set
- Ensure `api/index.py` was deployed (check Build logs)

### Get help:
- Check Neon dashboard: https://console.neon.tech
- Check Vercel dashboard: https://vercel.com/dashboard
- Read full guide: `VERCEL_DEPLOYMENT_GUIDE.md`

## Summary

After completing these steps:
- ✅ PostgreSQL database created (Neon, free)
- ✅ Database initialized with users and products
- ✅ App deployed to Vercel with database connection
- ✅ Payment functionality working

**Total cost:** $0/month (both Neon and Vercel have free tiers)
