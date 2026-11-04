# Cafe POS – Coffee Shop Web-Based Management System

Python (Flask) + SQLite + JWT login, with a plain HTML/CSS/JS front end.

## Run
```bash
pip install -r requirements.txt
python app.py
```
Open http://localhost:3000 (the database `cafe_pos.db` is created and seeded on first run).

| Role    | Username | Password   |
|---------|----------|------------|
| Admin   | admin    | admin123   |
| Cashier | cashier  | cashier123 |

## Flow (from the slides)
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

Set `CAFE_POS_SECRET` to your own secret before real use; `PORT` changes the port.
