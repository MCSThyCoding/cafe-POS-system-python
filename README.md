# Cafe POS – Coffee Shop Web-Based Management System

Python (Flask) + SQLite + JWT login, with a plain HTML/CSS/JS front end.

## Local Development

### Run
```bash
pip install -r requirements.txt
python app.py
```
Open http://localhost:3000 (the database `cafe_pos.db` is created and seeded on first run).

### Test Account Credentials
| Role    | Username | Password   |
|---------|----------|------------|
| Admin   | admin    | admin123   |
| Cashier | cashier  | cashier123 |

## Features
- **Point of Sale**: Process orders with real-time inventory tracking
- **Dashboard**: Revenue analytics, sales by category, top products, recent orders
- **Inventory Management**: View stock levels (all users), restock (admin only)
- **Reports**: Daily, monthly, and yearly sales reports with profit analysis (admin only)
- **Export**: Download sales reports as text files

## Flow
1. **Login**: JWT token; the menu depends on the role.
2. **Cashier, take order**: pick category, tap product, adjust quantity, total updates.
3. **Cashier, payment**: Cash or Card, Complete Order, confirmation. Stock is deducted and the order saved in one transaction.
4. **Cashier, dashboard**: revenue, orders, average order, sales by category, top products, recent orders, low-stock alert. Inventory is view-only.
5. **Admin, inventory**: restock with "+ Add 10".
6. **Admin, reports**: pick a date to see revenue, cost, profit, orders, monthly revenue trend, profit by product and decision-support advice.
7. **Admin, export**: downloads `report-YYYY-MM-DD.txt`.

## Files
- `app.py`: database, JWT auth, role checks, REST API (`/api/...`)
- `static/index.html`, `style.css`, `app.js`: the front end (Chart.js is bundled in `static/vendor`)
- `api/index.py`: Vercel serverless functions (for Vercel deployment)
- `init_db.py`: Database initialization script for PostgreSQL

## Environment Variables
- `CAFE_POS_SECRET`: Secret key for JWT tokens (required in production)
- `PORT`: Server port (default: 3000)
- `FLASK_DEBUG`: Set to "1" for debug mode

## Deployment

### Vercel Deployment
See `VERCEL_DEPLOYMENT_GUIDE.md` for detailed instructions.

**Quick Start:**
1. Create a free PostgreSQL database on Neon (https://neon.tech)
2. Update `init_db.py` with your DATABASE_URL
3. Run `python init_db.py` to initialize the database
4. Deploy to Vercel and add environment variables:
   - `DATABASE_URL`: Your Neon connection string
   - `CAFE_POS_SECRET`: Generate a random secret key

### Other Deployment Options
- **Render**: Free tier available, supports Flask + PostgreSQL
- **Railway**: Auto-detects Flask, easy setup
- **PythonAnywhere**: Designed for Python web apps

See `DEPLOYMENT_GUIDE.md` for more deployment options.

## Health Check
The application includes a health check endpoint at `/health` for monitoring.

## Important Notes
- **Change the default passwords** before deploying to production
- **Set `CAFE_POS_SECRET`** environment variable in production
- **Database file (`cafe_pos.db`) is not tracked in git (see `.gitignore`)
- **API endpoints require JWT authentication**
