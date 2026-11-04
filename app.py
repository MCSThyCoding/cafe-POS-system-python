"""Cafe POS - Coffee Shop Web-Based Management System (Flask + SQLite + JWT)

Roles:
  cashier : login, menu, orders + payment, dashboard, inventory (view only)
  admin   : everything a cashier does + restock, reports, export daily report
"""
import os
import sqlite3
from datetime import datetime, timedelta, timezone
from functools import wraps

import jwt
from flask import Flask, Response, g, jsonify, request, send_from_directory
from werkzeug.security import check_password_hash, generate_password_hash

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "cafe_pos.db")
SECRET_KEY = os.environ.get("CAFE_POS_SECRET", "change-me-in-production-cafe-pos-secret-key")
TOKEN_HOURS = 8
LOW_STOCK = 10
RESTOCK_STEP = 10

app = Flask(__name__, static_folder="static", static_url_path="/static")


# --------------------------------------------------------------------------- #
# Database
# --------------------------------------------------------------------------- #
SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    full_name TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('admin', 'cashier'))
);
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL,
    cost REAL NOT NULL,
    stock INTEGER NOT NULL DEFAULT 0,
    emoji TEXT NOT NULL DEFAULT ''
);
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id),
    customer TEXT NOT NULL DEFAULT 'Guest',
    total REAL NOT NULL,
    cost REAL NOT NULL,
    payment_method TEXT NOT NULL CHECK (payment_method IN ('Cash', 'Card')),
    created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL REFERENCES orders(id),
    product_id INTEGER NOT NULL REFERENCES products(id),
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price REAL NOT NULL,
    unit_cost REAL NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_orders_created ON orders(created_at);
"""

SEED_USERS = [
    ("admin", "admin123", "Admin User", "admin"),
    ("cashier", "cashier123", "Cashier User", "cashier"),
]

# name, category, price, cost, stock, emoji
SEED_PRODUCTS = [
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
    ("Milk Tea", "Tea", 3.50, 1.00, 0, "🧋"),
]


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


@app.teardown_appcontext
def close_db(_exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = sqlite3.connect(DB_PATH)
    db.executescript(SCHEMA)
    if db.execute("SELECT COUNT(*) FROM users").fetchone()[0] == 0:
        db.executemany(
            "INSERT INTO users (username, password_hash, full_name, role) VALUES (?,?,?,?)",
            [(u, generate_password_hash(p), n, r) for u, p, n, r in SEED_USERS],
        )
    if db.execute("SELECT COUNT(*) FROM products").fetchone()[0] == 0:
        db.executemany(
            "INSERT INTO products (name, category, price, cost, stock, emoji) VALUES (?,?,?,?,?,?)",
            SEED_PRODUCTS,
        )
    db.commit()
    db.close()


# --------------------------------------------------------------------------- #
# Auth (JWT)
# --------------------------------------------------------------------------- #
def make_token(user):
    payload = {
        "sub": str(user["id"]),
        "username": user["username"],
        "role": user["role"],
        "exp": datetime.now(timezone.utc) + timedelta(hours=TOKEN_HOURS),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def auth_required(*roles):
    """Require a valid JWT; optionally restrict to the given roles."""

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            header = request.headers.get("Authorization", "")
            if not header.startswith("Bearer "):
                return jsonify(error="Authentication required"), 401
            try:
                claims = jwt.decode(header[7:], SECRET_KEY, algorithms=["HS256"])
            except jwt.ExpiredSignatureError:
                return jsonify(error="Session expired, please log in again"), 401
            except jwt.InvalidTokenError:
                return jsonify(error="Invalid token"), 401
            user = get_db().execute(
                "SELECT id, username, full_name, role FROM users WHERE id = ?", (claims["sub"],)
            ).fetchone()
            if user is None:
                return jsonify(error="User no longer exists"), 401
            if roles and user["role"] not in roles:
                return jsonify(error="You do not have permission for this action"), 403
            g.user = user
            return fn(*args, **kwargs)

        return wrapper

    return decorator


@app.post("/api/login")
def login():
    data = request.get_json(silent=True) or {}
    username = str(data.get("username", "")).strip()
    password = str(data.get("password", ""))
    user = get_db().execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    if user is None or not check_password_hash(user["password_hash"], password):
        return jsonify(error="Invalid username or password"), 401
    return jsonify(
        token=make_token(user),
        user={"id": user["id"], "username": user["username"],
              "full_name": user["full_name"], "role": user["role"]},
    )


@app.get("/api/me")
@auth_required()
def me():
    return jsonify(dict(g.user))


# --------------------------------------------------------------------------- #
# Products & inventory
# --------------------------------------------------------------------------- #
def product_dict(row, include_cost=False):
    d = {"id": row["id"], "name": row["name"], "category": row["category"],
         "price": row["price"], "stock": row["stock"], "emoji": row["emoji"],
         "low_stock": row["stock"] <= LOW_STOCK}
    if include_cost:
        d["cost"] = row["cost"]
    return d


@app.get("/api/products")
@auth_required()
def list_products():
    rows = get_db().execute("SELECT * FROM products ORDER BY id").fetchall()
    return jsonify([product_dict(r) for r in rows])


@app.get("/api/inventory")
@auth_required()
def inventory():
    rows = get_db().execute("SELECT * FROM products ORDER BY category, name").fetchall()
    return jsonify([product_dict(r) for r in rows])


@app.post("/api/inventory/<int:product_id>/restock")
@auth_required("admin")
def restock(product_id):
    data = request.get_json(silent=True) or {}
    try:
        qty = int(data.get("quantity", RESTOCK_STEP))
    except (TypeError, ValueError):
        return jsonify(error="Quantity must be a number"), 400
    if qty <= 0 or qty > 1000:
        return jsonify(error="Quantity must be between 1 and 1000"), 400
    db = get_db()
    cur = db.execute("UPDATE products SET stock = stock + ? WHERE id = ?", (qty, product_id))
    if cur.rowcount == 0:
        return jsonify(error="Product not found"), 404
    db.commit()
    row = db.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
    return jsonify(product_dict(row))


# --------------------------------------------------------------------------- #
# Orders & payment
# --------------------------------------------------------------------------- #
@app.post("/api/orders")
@auth_required()
def create_order():
    data = request.get_json(silent=True) or {}
    items = data.get("items")
    method = data.get("payment_method")
    customer = (str(data.get("customer") or "Guest").strip() or "Guest")[:60]
    if method not in ("Cash", "Card"):
        return jsonify(error="Payment method must be Cash or Card"), 400
    if not isinstance(items, list) or not items:
        return jsonify(error="Cart is empty"), 400

    # merge duplicate lines and validate quantities
    wanted = {}
    for it in items:
        try:
            pid, qty = int(it["product_id"]), int(it["quantity"])
        except (KeyError, TypeError, ValueError):
            return jsonify(error="Invalid cart item"), 400
        if qty <= 0 or qty > 100:
            return jsonify(error="Quantity must be between 1 and 100"), 400
        wanted[pid] = wanted.get(pid, 0) + qty

    db = get_db()
    try:
        db.execute("BEGIN IMMEDIATE")  # lock so concurrent sales can't oversell
        lines, total, cost = [], 0.0, 0.0
        for pid, qty in wanted.items():
            p = db.execute("SELECT * FROM products WHERE id = ?", (pid,)).fetchone()
            if p is None:
                db.rollback()
                return jsonify(error=f"Product {pid} not found"), 404
            if p["stock"] < qty:
                db.rollback()
                return jsonify(error=f"Not enough stock for {p['name']} (only {p['stock']} left)"), 409
            lines.append((p, qty))
            total += p["price"] * qty
            cost += p["cost"] * qty

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cur = db.execute(
            "INSERT INTO orders (user_id, customer, total, cost, payment_method, created_at) "
            "VALUES (?,?,?,?,?,?)",
            (g.user["id"], customer, round(total, 2), round(cost, 2), method, now),
        )
        order_id = cur.lastrowid
        for p, qty in lines:
            db.execute(
                "INSERT INTO order_items (order_id, product_id, name, category, quantity, unit_price, unit_cost) "
                "VALUES (?,?,?,?,?,?,?)",
                (order_id, p["id"], p["name"], p["category"], qty, p["price"], p["cost"]),
            )
            db.execute("UPDATE products SET stock = stock - ? WHERE id = ?", (qty, p["id"]))  # deduct stock
        db.commit()
    except Exception:
        db.rollback()
        raise
    return jsonify(order_id=order_id, total=round(total, 2), payment_method=method, created_at=now), 201


# --------------------------------------------------------------------------- #
# Dashboard (cashier + admin) - price analysis
# --------------------------------------------------------------------------- #
@app.get("/api/dashboard")
@auth_required()
def dashboard():
    db = get_db()
    today = datetime.now().strftime("%Y-%m-%d")
    day = db.execute(
        "SELECT COALESCE(SUM(total),0) AS revenue, COUNT(*) AS orders FROM orders "
        "WHERE date(created_at) = ?", (today,)).fetchone()
    revenue, orders = round(day["revenue"], 2), day["orders"]
    by_cat = db.execute(
        "SELECT oi.category AS name, ROUND(SUM(oi.quantity*oi.unit_price),2) AS value "
        "FROM order_items oi JOIN orders o ON o.id = oi.order_id "
        "WHERE date(o.created_at) = ? GROUP BY oi.category ORDER BY value DESC", (today,)).fetchall()
    top = db.execute(
        "SELECT oi.name AS name, SUM(oi.quantity) AS value "
        "FROM order_items oi JOIN orders o ON o.id = oi.order_id "
        "WHERE date(o.created_at) = ? GROUP BY oi.name ORDER BY value DESC LIMIT 5", (today,)).fetchall()
    recent = db.execute(
        "SELECT id, customer, total, payment_method, created_at FROM orders "
        "ORDER BY id DESC LIMIT 8").fetchall()
    total_products = db.execute("SELECT COUNT(*) FROM products").fetchone()[0]
    low = db.execute(
        "SELECT name, stock FROM products WHERE stock <= ? ORDER BY stock", (LOW_STOCK,)).fetchall()
    return jsonify(
        revenue=revenue, orders=orders,
        average_order=round(revenue / orders, 2) if orders else 0,
        total_products=total_products,
        sales_by_category=[dict(r) for r in by_cat],
        top_products=[dict(r) for r in top],
        recent_orders=[dict(r) for r in recent],
        low_stock=[dict(r) for r in low],
    )


# --------------------------------------------------------------------------- #
# Reports (admin only)
# --------------------------------------------------------------------------- #
def parse_date(value):
    try:
        return datetime.strptime(value, "%Y-%m-%d").strftime("%Y-%m-%d")
    except (TypeError, ValueError):
        return None


def parse_month(value):
    try:
        return datetime.strptime(value, "%Y-%m").strftime("%Y-%m")
    except (TypeError, ValueError):
        return None


def parse_year(value):
    try:
        return datetime.strptime(value, "%Y").strftime("%Y")
    except (TypeError, ValueError):
        return None


def build_report(db, day):
    summary = db.execute(
        "SELECT COALESCE(SUM(total),0) AS revenue, COALESCE(SUM(cost),0) AS cost, COUNT(*) AS orders "
        "FROM orders WHERE date(created_at) = ?", (day,)).fetchone()
    revenue, cost = round(summary["revenue"], 2), round(summary["cost"], 2)

    rows = db.execute(
        "SELECT oi.name AS name, oi.category AS category, SUM(oi.quantity) AS units, "
        "SUM(oi.quantity*oi.unit_price) AS revenue, SUM(oi.quantity*oi.unit_cost) AS cost "
        "FROM order_items oi JOIN orders o ON o.id = oi.order_id "
        "WHERE date(o.created_at) = ? GROUP BY oi.name, oi.category", (day,)).fetchall()
    products = []
    for r in rows:
        rev, cst = r["revenue"], r["cost"]
        profit = rev - cst
        margin = round(profit / rev * 100, 2) if rev else 0
        products.append({"name": r["name"], "category": r["category"], "units": r["units"],
                         "revenue": round(rev, 2), "cost": round(cst, 2),
                         "profit": round(profit, 2), "margin": margin})
    products.sort(key=lambda p: p["profit"], reverse=True)

    # Decision support: simple rule-based advice per product
    for i, p in enumerate(products):
        if p["margin"] >= 65 and i < 3:
            p["advice"] = "Promote - high profit margin"
        elif p["margin"] < 50:
            p["advice"] = "Review price or ingredient cost"
        elif p["units"] <= 1:
            p["advice"] = "Slow seller - consider a combo deal"
        else:
            p["advice"] = "Keep as is"

    by_cat = {}
    for p in products:
        c = by_cat.setdefault(p["category"], {"category": p["category"], "revenue": 0, "profit": 0})
        c["revenue"] += p["revenue"]
        c["profit"] += p["profit"]
    categories = [{"category": c["category"], "revenue": round(c["revenue"], 2),
                   "profit": round(c["profit"], 2)} for c in by_cat.values()]
    categories.sort(key=lambda c: c["profit"], reverse=True)

    # revenue trend: each day of the selected month
    month = day[:7]
    trend_rows = db.execute(
        "SELECT strftime('%d', created_at) AS d, ROUND(SUM(total),2) AS revenue FROM orders "
        "WHERE strftime('%Y-%m', created_at) = ? GROUP BY d ORDER BY d", (month,)).fetchall()
    return {
        "date": day, "revenue": revenue, "cost": cost, "profit": round(revenue - cost, 2),
        "orders": summary["orders"], "products": products, "categories": categories,
        "trend": [{"day": int(r["d"]), "revenue": r["revenue"]} for r in trend_rows],
    }


def build_monthly_report(db, month):
    summary = db.execute(
        "SELECT COALESCE(SUM(total),0) AS revenue, COALESCE(SUM(cost),0) AS cost, COUNT(*) AS orders "
        "FROM orders WHERE strftime('%Y-%m', created_at) = ?", (month,)).fetchone()
    revenue, cost = round(summary["revenue"], 2), round(summary["cost"], 2)

    rows = db.execute(
        "SELECT oi.name AS name, oi.category AS category, SUM(oi.quantity) AS units, "
        "SUM(oi.quantity*oi.unit_price) AS revenue, SUM(oi.quantity*oi.unit_cost) AS cost "
        "FROM order_items oi JOIN orders o ON o.id = oi.order_id "
        "WHERE strftime('%Y-%m', o.created_at) = ? GROUP BY oi.name, oi.category", (month,)).fetchall()
    products = []
    for r in rows:
        rev, cst = r["revenue"], r["cost"]
        profit = rev - cst
        margin = round(profit / rev * 100, 2) if rev else 0
        products.append({"name": r["name"], "category": r["category"], "units": r["units"],
                         "revenue": round(rev, 2), "cost": round(cst, 2),
                         "profit": round(profit, 2), "margin": margin})
    products.sort(key=lambda p: p["profit"], reverse=True)

    # Decision support
    for i, p in enumerate(products):
        if p["margin"] >= 65 and i < 3:
            p["advice"] = "Promote - high profit margin"
        elif p["margin"] < 50:
            p["advice"] = "Review price or ingredient cost"
        elif p["units"] <= 1:
            p["advice"] = "Slow seller - consider a combo deal"
        else:
            p["advice"] = "Keep as is"

    by_cat = {}
    for p in products:
        c = by_cat.setdefault(p["category"], {"category": p["category"], "revenue": 0, "profit": 0})
        c["revenue"] += p["revenue"]
        c["profit"] += p["profit"]
    categories = [{"category": c["category"], "revenue": round(c["revenue"], 2),
                   "profit": round(c["profit"], 2)} for c in by_cat.values()]
    categories.sort(key=lambda c: c["profit"], reverse=True)

    # revenue trend: each day of the selected month
    trend_rows = db.execute(
        "SELECT strftime('%d', created_at) AS d, ROUND(SUM(total),2) AS revenue FROM orders "
        "WHERE strftime('%Y-%m', created_at) = ? GROUP BY d ORDER BY d", (month,)).fetchall()
    return {
        "date": month, "revenue": revenue, "cost": cost, "profit": round(revenue - cost, 2),
        "orders": summary["orders"], "products": products, "categories": categories,
        "trend": [{"day": int(r["d"]), "revenue": r["revenue"]} for r in trend_rows],
    }


def build_yearly_report(db, year):
    summary = db.execute(
        "SELECT COALESCE(SUM(total),0) AS revenue, COALESCE(SUM(cost),0) AS cost, COUNT(*) AS orders "
        "FROM orders WHERE strftime('%Y', created_at) = ?", (year,)).fetchone()
    revenue, cost = round(summary["revenue"], 2), round(summary["cost"], 2)

    rows = db.execute(
        "SELECT oi.name AS name, oi.category AS category, SUM(oi.quantity) AS units, "
        "SUM(oi.quantity*oi.unit_price) AS revenue, SUM(oi.quantity*oi.unit_cost) AS cost "
        "FROM order_items oi JOIN orders o ON o.id = oi.order_id "
        "WHERE strftime('%Y', o.created_at) = ? GROUP BY oi.name, oi.category", (year,)).fetchall()
    products = []
    for r in rows:
        rev, cst = r["revenue"], r["cost"]
        profit = rev - cst
        margin = round(profit / rev * 100, 2) if rev else 0
        products.append({"name": r["name"], "category": r["category"], "units": r["units"],
                         "revenue": round(rev, 2), "cost": round(cst, 2),
                         "profit": round(profit, 2), "margin": margin})
    products.sort(key=lambda p: p["profit"], reverse=True)

    # Decision support
    for i, p in enumerate(products):
        if p["margin"] >= 65 and i < 3:
            p["advice"] = "Promote - high profit margin"
        elif p["margin"] < 50:
            p["advice"] = "Review price or ingredient cost"
        elif p["units"] <= 1:
            p["advice"] = "Slow seller - consider a combo deal"
        else:
            p["advice"] = "Keep as is"

    by_cat = {}
    for p in products:
        c = by_cat.setdefault(p["category"], {"category": p["category"], "revenue": 0, "profit": 0})
        c["revenue"] += p["revenue"]
        c["profit"] += p["profit"]
    categories = [{"category": c["category"], "revenue": round(c["revenue"], 2),
                   "profit": round(c["profit"], 2)} for c in by_cat.values()]
    categories.sort(key=lambda c: c["profit"], reverse=True)

    # revenue trend: each month of the selected year
    trend_rows = db.execute(
        "SELECT strftime('%m', created_at) AS d, ROUND(SUM(total),2) AS revenue FROM orders "
        "WHERE strftime('%Y', created_at) = ? GROUP BY d ORDER BY d", (year,)).fetchall()
    return {
        "date": year, "revenue": revenue, "cost": cost, "profit": round(revenue - cost, 2),
        "orders": summary["orders"], "products": products, "categories": categories,
        "trend": [{"day": int(r["d"]), "revenue": r["revenue"]} for r in trend_rows],
    }


@app.get("/api/reports")
@auth_required("admin")
def reports():
    period_type = request.args.get("type", "daily")
    date_value = request.args.get("date")
    
    if period_type == "daily":
        day = parse_date(date_value or datetime.now().strftime("%Y-%m-%d"))
        if day is None:
            return jsonify(error="Date must be YYYY-MM-DD"), 400
        return jsonify(build_report(get_db(), day))
    elif period_type == "monthly":
        month = parse_month(date_value or datetime.now().strftime("%Y-%m"))
        if month is None:
            return jsonify(error="Date must be YYYY-MM"), 400
        return jsonify(build_monthly_report(get_db(), month))
    elif period_type == "yearly":
        year = parse_year(date_value or datetime.now().strftime("%Y"))
        if year is None:
            return jsonify(error="Date must be YYYY"), 400
        return jsonify(build_yearly_report(get_db(), year))
    else:
        return jsonify(error="Invalid report type. Use: daily, monthly, or yearly"), 400


@app.get("/api/reports/export")
@auth_required("admin")
def export_report():
    period_type = request.args.get("type", "daily")
    date_value = request.args.get("date")
    
    if period_type == "daily":
        day = parse_date(date_value or datetime.now().strftime("%Y-%m-%d"))
        if day is None:
            return jsonify(error="Date must be YYYY-MM-DD"), 400
        r = build_report(get_db(), day)
        title = f"Daily Sales Report - {day}"
        filename = f"report-daily-{day}.txt"
    elif period_type == "monthly":
        month = parse_month(date_value or datetime.now().strftime("%Y-%m"))
        if month is None:
            return jsonify(error="Date must be YYYY-MM"), 400
        r = build_monthly_report(get_db(), month)
        title = f"Monthly Sales Report - {month}"
        filename = f"report-monthly-{month}.txt"
    elif period_type == "yearly":
        year = parse_year(date_value or datetime.now().strftime("%Y"))
        if year is None:
            return jsonify(error="Date must be YYYY"), 400
        r = build_yearly_report(get_db(), year)
        title = f"Yearly Sales Report - {year}"
        filename = f"report-yearly-{year}.txt"
    else:
        return jsonify(error="Invalid report type. Use: daily, monthly, or yearly"), 400
    
    lines = [title, "=" * 32,
             f"Total Revenue: ${r['revenue']:.2f}", f"Total Cost: ${r['cost']:.2f}",
             f"Profit: ${r['profit']:.2f}", f"Total Orders: {r['orders']}", "",
             "Top Products by Profit:"]
    if r["products"]:
        for i, p in enumerate(r["products"][:10], 1):
            lines.append(f"{i}. {p['name']}: ${p['profit']:.2f} ({p['margin']:g}%)")
    else:
        lines.append("(no sales data)")
    return Response("\n".join(lines) + "\n", mimetype="text/plain",
                    headers={"Content-Disposition": f'attachment; filename="{filename}"'})


# --------------------------------------------------------------------------- #
# Frontend
# --------------------------------------------------------------------------- #
@app.get("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


init_db()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host="127.0.0.1", port=port, debug=os.environ.get("FLASK_DEBUG") == "1")
