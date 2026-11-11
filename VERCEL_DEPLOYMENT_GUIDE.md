# Cafe POS - Vercel Deployment Guide

## Overview
This guide will help you deploy the Cafe POS system on Vercel with working payment functionality using serverless functions and PostgreSQL.

## Prerequisites
- GitHub account
- Vercel account (free)
- Neon PostgreSQL database (free)

## Step 1: Set Up PostgreSQL Database

### Option A: Neon (Recommended - Free)
1. Go to https://neon.tech
2. Sign up for free account
3. Create a new project
4. Copy the **Connection String** (looks like: `postgresql://user:password@ep-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require`)

### Option B: Supabase (Also Free)
1. Go to https://supabase.com
2. Create a new project
3. Go to Settings → Database
4. Copy the **Connection String**

## Step 2: Initialize Database

Create a file `init_db.py` to set up your database tables:

```python
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash

# Replace with your DATABASE_URL from Neon/Supabase
DATABASE_URL = "postgresql://user:password@host/dbname?sslmode=require"

def init_db():
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    cur = conn.cursor()
    
    # Create tables
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT NOT NULL,
            role TEXT NOT NULL CHECK (role IN ('admin', 'cashier'))
        );
    """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            cost REAL NOT NULL,
            stock INTEGER NOT NULL DEFAULT 0,
            emoji TEXT NOT NULL DEFAULT ''
        );
    """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL REFERENCES users(id),
            customer TEXT NOT NULL DEFAULT 'Guest',
            total REAL NOT NULL,
            cost REAL NOT NULL,
            payment_method TEXT NOT NULL CHECK (payment_method IN ('Cash', 'Card')),
            created_at TEXT NOT NULL
        );
    """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            id SERIAL PRIMARY KEY,
            order_id INTEGER NOT NULL REFERENCES orders(id),
            product_id INTEGER NOT NULL REFERENCES products(id),
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            unit_cost REAL NOT NULL
        );
    """)
    
    cur.execute("CREATE INDEX IF NOT EXISTS idx_orders_created ON orders(created_at)")
    
    # Seed users if empty
    cur.execute("SELECT COUNT(*) FROM users")
    if cur.fetchone()["count"] == 0:
        cur.execute(
            "INSERT INTO users (username, password_hash, full_name, role) VALUES (%s,%s,%s,%s)",
            ("admin", generate_password_hash("admin123"), "Admin User", "admin")
        )
        cur.execute(
            "INSERT INTO users (username, password_hash, full_name, role) VALUES (%s,%s,%s,%s)",
            ("cashier", generate_password_hash("cashier123"), "Cashier User", "cashier")
        )
    
    # Seed products if empty
    cur.execute("SELECT COUNT(*) FROM products")
    if cur.fetchone()["count"] == 0:
        products = [
            ("Americano", "Coffee", 3.00, 0.90, 50, "☕"),
            ("Cappuccino", "Coffee", 4.00, 1.30, 50, "☕"),
            ("Espresso", "Coffee", 2.50, 0.80, 50, "☕"),
            ("Latte", "Coffee", 4.00, 1.40, 50, "🥛"),
            ("Mocha", "Coffee", 4.50, 1.60, 50, "🍫"),
            ("Iced Coffee", "Cold Drinks", 4.50, 1.50, 50, "🧊"),
            ("Smoothie", "Cold Drinks", 6.00, 2.50, 50, "🥤"),
            ("Lemonade", "Cold Drinks", 3.50, 0.90, 50, "🍋"),
            ("Croissant", "Food", 3.50, 1.20, 50, "🥐"),
            ("Muffin", "Food", 3.00, 1.00, 50, "🧁"),
            ("Sandwich", "Food", 5.50, 2.40, 40, "🥪"),
            ("Cookie", "Food", 2.00, 0.60, 60, "🍪"),
            ("Black Tea", "Tea", 2.50, 0.50, 50, "🍵"),
            ("Chai Latte", "Tea", 4.00, 1.20, 50, "🫖"),
            ("Green Tea", "Tea", 2.50, 0.55, 50, "🍃"),
            ("Milk Tea", "Tea", 3.50, 1.00, 50, "🧋"),
        ]
        cur.executemany(
            "INSERT INTO products (name, category, price, cost, stock, emoji) VALUES (%s,%s,%s,%s,%s,%s)",
            products
        )
    
    conn.commit()
    cur.close()
    conn.close()
    print("Database initialized successfully!")

if __name__ == "__main__":
    init_db()
```

Run this locally to initialize your database:
```bash
pip install psycopg2-binary werkzeug
python init_db.py
```

## Step 3: Deploy to Vercel

### 3.1 Connect GitHub to Vercel
1. Go to https://vercel.com
2. Sign up/login
3. Click "Add New..." → "Project"
4. Import your GitHub repository: `MCSThyCoding/cafe-POS-system-python`

### 3.2 Configure Project
1. **Project Name:** cafe-pos
2. **Framework Preset:** Other
3. **Root Directory:** `./`
4. **Build Command:** Leave empty
5. **Output Directory:** Leave empty

### 3.3 Add Environment Variables
Click "Environment Variables" and add:

| Key | Value |
|-----|-------|
| `DATABASE_URL` | Your PostgreSQL connection string from Step 1 |
| `CAFE_POS_SECRET` | Generate a random string (e.g., use https://randomkeygen.com) |

### 3.4 Deploy
Click "Deploy"

## Step 4: Update Frontend API URLs

The frontend currently calls `/api/...` which will work with Vercel serverless functions. No changes needed!

## Step 5: Test

1. Wait for deployment to complete
2. Visit your Vercel URL (e.g., `https://cafe-pos.vercel.app`)
3. Test login with:
   - Admin: username `admin`, password `admin123`
   - Cashier: username `cashier`, password `cashier123`
4. Test adding items to cart
5. Test completing an order (payment should now work!)

## Troubleshooting

### Payment still fails?
1. Check Vercel logs for errors
2. Verify DATABASE_URL is correct
3. Ensure database tables were created
4. Check that CAFE_POS_SECRET is set

### Database connection error?
1. Verify DATABASE_URL format
2. Ensure SSL is enabled (add `?sslmode=require`)
3. Check database allows connections from your IP

### API returns 404?
1. Check that `api/index.py` exists
2. Verify `vercel.json` is in root
3. Check Vercel deployment logs

## Architecture

**Before (Vercel only):**
- Frontend on Vercel ✅
- No backend ❌
- No database ❌
- Payments fail ❌

**After (Vercel + Serverless + PostgreSQL):**
- Frontend on Vercel ✅
- Serverless functions on Vercel ✅
- PostgreSQL on Neon/Supabase ✅
- Payments work ✅

## Cost

- **Vercel:** Free tier (Hobby plan)
- **Neon/Supabase:** Free tier
- **Total:** $0/month

## Next Steps

After successful deployment:
1. Set up custom domain (optional)
2. Configure automatic database backups
3. Add error monitoring (Sentry, etc.)
4. Set up CI/CD for testing

## Files Modified

- `api/index.py` - Serverless functions
- `vercel.json` - Vercel configuration
- `requirements.txt` - Added psycopg2-binary
- `init_db.py` - Database initialization script

## Support

If you encounter issues:
1. Check Vercel deployment logs
2. Verify environment variables
3. Test database connection locally
4. Check Neon/Supabase dashboard for connection issues
