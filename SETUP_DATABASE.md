# Setup Neon Database & Connect to Vercel

## Part 1: Create Database in Neon

### Step 1: Access Neon Console
1. Go to: https://console.neon.tech/app/org-misty-pine-18465080/projects
2. You should see your Neon dashboard

### Step 2: Create New Project
1. Click the **"+ New Project"** button (usually in the top right)
2. A modal will appear asking for project details

### Step 3: Configure Project
1. **Project Name:** Enter `cafe-pos-db`
2. **Select PostgreSQL Version:** Keep default (usually 16)
3. **Region:** Select a region closest to you (e.g., "US East" or "US West")
4. Click **"Create Project"**

### Step 4: Wait for Creation
- Wait about 30-60 seconds for the database to be created
- You'll see a progress indicator
- Once done, you'll see your new project dashboard

### Step 5: Get Connection String
1. On your project dashboard, look for **"Connection Details"** or **"Connection string"**
2. Click to reveal the connection string
3. Copy the full connection string - it looks like:
   ```
   postgresql://neondb_owner:xxxxx@ep-xxxxx.us-east-2.aws.neon.tech/neondb?sslmode=require
   ```
4. **Save this string** - you'll need it for Vercel

---

## Part 2: Initialize Database

### Step 1: Update init_db.py
1. Open the file `init_db.py` in your code editor
2. Find line 7 that says:
   ```python
   DATABASE_URL = "postgresql://user:password@host/dbname?sslmode=require"
   ```
3. Replace it with your Neon connection string from Part 1, Step 5
4. Save the file

### Step 2: Install Dependencies
Open your terminal and run:
```bash
cd /Users/sethy/Desktop/cafe_pos
source venv/bin/activate
pip install psycopg2-binary werkzeug
```

### Step 3: Run Database Initialization
```bash
python init_db.py
```

You should see:
```
✓ Seeded users
✓ Seeded products
✅ Database initialized successfully!
```

### Step 4: Commit Changes
```bash
git add init_db.py
git commit -m "Update DATABASE_URL for Neon"
git push origin main
```

---

## Part 3: Connect to Vercel

### Step 1: Access Vercel Dashboard
1. Go to: https://vercel.com/dashboard
2. Find your project: `cafe-pos-system-python`
3. Click on it

### Step 2: Add Environment Variables
1. Click on the **"Settings"** tab
2. Click on **"Environment Variables"** in the left sidebar
3. Click **"Add New"** button

### Step 3: Add DATABASE_URL
1. **Key:** Enter `DATABASE_URL`
2. **Value:** Paste your Neon connection string from Part 1, Step 5
3. **Environment:** Select all (Production, Preview, Development)
4. Click **"Save"**

### Step 4: Add CAFE_POS_SECRET
1. Click **"Add New"** again
2. **Key:** Enter `CAFE_POS_SECRET`
3. **Value:** Enter a random string (e.g., `cafe-pos-secret-key-2024`)
4. **Environment:** Select all
5. Click **"Save"**

### Step 5: Redeploy
1. Go to the **"Deployments"** tab
2. Click the three dots (⋯) on the latest deployment
3. Click **"Redeploy"**
4. Wait for redeployment to complete (2-3 minutes)

---

## Part 4: Test Your App

### Step 1: Access Your App
1. Go to: https://cafe-pos-system-python.vercel.app
2. You should see the login screen

### Step 2: Login
- **Username:** `admin`
- **Password:** `admin123`
- Click "Login →"

### Step 3: Test Payment
1. Navigate to "Point of Sale"
2. Click on a product (e.g., Americano - $3.00)
3. It should appear in the cart on the right
4. Select payment method (Cash or Card)
5. Click "Complete Order"
6. **If successful:** You'll see a success modal with order details
7. **If it fails:** Check Vercel logs (Settings → Functions → Logs)

---

## Troubleshooting

### Issue: "Database connection failed"
**Solution:**
- Verify DATABASE_URL is correct in Vercel environment variables
- Make sure the connection string includes `?sslmode=require`
- Check Neon dashboard - is the database active?

### Issue: "Table does not exist"
**Solution:**
- Did you run `python init_db.py`?
- Did you update the DATABASE_URL in init_db.py before running it?
- Try running init_db.py again

### Issue: Payment still fails
**Solution:**
- Go to Vercel dashboard → your project → Settings → Functions → Logs
- Look for error messages
- Check that both environment variables are set
- Verify the api/index.py file exists in your repository

### Issue: Can't find Connection Details in Neon
**Solution:**
- In Neon dashboard, click on your project
- Look for "SQL Editor" or "Connection Details" in the sidebar
- Or click the "Connect" button (usually top right of project page)

---

## Need Help?

If you get stuck at any step:
1. **Neon Support:** https://neon.tech/docs
2. **Vercel Support:** https://vercel.com/docs
3. **Check the logs:**
   - Neon: Dashboard → your project → SQL Editor → try running `SELECT 1;`
   - Vercel: Dashboard → your project → Settings → Functions → Logs

---

## Summary Checklist

- [ ] Created new project in Neon
- [ ] Copied connection string from Neon
- [ ] Updated init_db.py with connection string
- [ ] Ran `python init_db.py` successfully
- [ ] Committed and pushed changes to GitHub
- [ ] Added DATABASE_URL to Vercel environment variables
- [ ] Added CAFE_POS_SECRET to Vercel environment variables
- [ ] Redeployed on Vercel
- [ ] Tested login (admin/admin123)
- [ ] Tested payment functionality

Complete all items above and your payments will work on Vercel! ✅
