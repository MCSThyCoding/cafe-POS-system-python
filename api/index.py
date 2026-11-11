"""Vercel Serverless Functions for Cafe POS"""
import os
import json
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime, timedelta, timezone
from functools import wraps
import jwt
from werkzeug.security import check_password_hash, generate_password_hash

# Database connection
DATABASE_URL = os.environ.get("DATABASE_URL")
SECRET_KEY = os.environ.get("CAFE_POS_SECRET", "change-me-in-production-cafe-pos-secret-key")
TOKEN_HOURS = 8
LOW_STOCK = 10
RESTOCK_STEP = 10

def get_db():
    """Get database connection"""
    if DATABASE_URL:
        return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    else:
        raise Exception("DATABASE_URL not set")

def get_db_cursor():
    """Get database cursor"""
    conn = get_db()
    return conn.cursor(), conn

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
        def wrapper(event, context):
            # Get token from Authorization header
            headers = event.get("headers", {})
            auth_header = headers.get("authorization", "")
            
            if not auth_header.startswith("Bearer "):
                return {
                    "statusCode": 401,
                    "body": json.dumps({"error": "Authentication required"})
                }
            
            try:
                claims = jwt.decode(auth_header[7:], SECRET_KEY, algorithms=["HS256"])
            except jwt.ExpiredSignatureError:
                return {
                    "statusCode": 401,
                    "body": json.dumps({"error": "Session expired, please log in again"})
                }
            except jwt.InvalidTokenError:
                return {
                    "statusCode": 401,
                    "body": json.dumps({"error": "Invalid token"})
                }
            
            # Get user from database
            cur, conn = get_db_cursor()
            try:
                cur.execute("SELECT id, username, full_name, role FROM users WHERE id = %s", (claims["sub"],))
                user = cur.fetchone()
                conn.commit()
                
                if user is None:
                    return {
                        "statusCode": 401,
                        "body": json.dumps({"error": "User no longer exists"})
                    }
                
                if roles and user["role"] not in roles:
                    return {
                        "statusCode": 403,
                        "body": json.dumps({"error": "You do not have permission for this action"})
                    }
                
                # Add user to event for use in handler
                event["user"] = user
                return fn(event, context)
            finally:
                cur.close()
                conn.close()
        
        return wrapper
    return decorator

# --------------------------------------------------------------------------- #
# Helper Functions
# --------------------------------------------------------------------------- #
def product_dict(row, include_cost=False):
    d = {
        "id": row["id"],
        "name": row["name"],
        "category": row["category"],
        "price": float(row["price"]),
        "stock": row["stock"],
        "emoji": row["emoji"],
        "low_stock": row["stock"] <= LOW_STOCK
    }
    if include_cost:
        d["cost"] = float(row["cost"])
    return d

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

# --------------------------------------------------------------------------- #
# API Handlers
# --------------------------------------------------------------------------- #
def login_handler(event, context):
    """Handle login requests"""
    try:
        body = json.loads(event.get("body", "{}"))
        username = str(body.get("username", "")).strip()
        password = str(body.get("password", ""))
        
        cur, conn = get_db_cursor()
        try:
            cur.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cur.fetchone()
            conn.commit()
            
            if user is None or not check_password_hash(user["password_hash"], password):
                return {
                    "statusCode": 401,
                    "body": json.dumps({"error": "Invalid username or password"})
                }
            
            return {
                "statusCode": 200,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({
                    "token": make_token(user),
                    "user": {
                        "id": user["id"],
                        "username": user["username"],
                        "full_name": user["full_name"],
                        "role": user["role"]
                    }
                })
            }
        finally:
            cur.close()
            conn.close()
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

@auth_required()
def me_handler(event, context):
    """Get current user info"""
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(dict(event["user"]))
    }

@auth_required()
def list_products_handler(event, context):
    """List all products"""
    cur, conn = get_db_cursor()
    try:
        cur.execute("SELECT * FROM products ORDER BY id")
        rows = cur.fetchall()
        conn.commit()
        
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps([product_dict(r) for r in rows])
        }
    finally:
        cur.close()
        conn.close()

@auth_required()
def inventory_handler(event, context):
    """Get inventory list"""
    cur, conn = get_db_cursor()
    try:
        cur.execute("SELECT * FROM products ORDER BY category, name")
        rows = cur.fetchall()
        conn.commit()
        
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps([product_dict(r) for r in rows])
        }
    finally:
        cur.close()
        conn.close()

@auth_required("admin")
def restock_handler(event, context):
    """Restock product"""
    try:
        # Get product_id from path
        path = event.get("path", "")
        parts = path.split("/")
        product_id = int(parts[-1]) if parts else None
        
        if not product_id:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Product ID required"})
            }
        
        body = json.loads(event.get("body", "{}"))
        try:
            qty = int(body.get("quantity", RESTOCK_STEP))
        except (TypeError, ValueError):
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Quantity must be a number"})
            }
        
        if qty <= 0 or qty > 1000:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Quantity must be between 1 and 1000"})
            }
        
        cur, conn = get_db_cursor()
        try:
            cur.execute("UPDATE products SET stock = stock + %s WHERE id = %s", (qty, product_id))
            if cur.rowcount == 0:
                conn.rollback()
                return {
                    "statusCode": 404,
                    "body": json.dumps({"error": "Product not found"})
                }
            conn.commit()
            
            cur.execute("SELECT * FROM products WHERE id = %s", (product_id,))
            row = cur.fetchone()
            conn.commit()
            
            return {
                "statusCode": 200,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps(product_dict(row))
            }
        finally:
            cur.close()
            conn.close()
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

@auth_required()
def create_order_handler(event, context):
    """Create a new order"""
    try:
        body = json.loads(event.get("body", "{}"))
        items = body.get("items")
        method = body.get("payment_method")
        customer = (str(body.get("customer") or "Guest").strip() or "Guest")[:60]
        
        if method not in ("Cash", "Card"):
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Payment method must be Cash or Card"})
            }
        
        if not isinstance(items, list) or not items:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Cart is empty"})
            }
        
        # Merge duplicate lines and validate quantities
        wanted = {}
        for it in items:
            try:
                pid, qty = int(it["product_id"]), int(it["quantity"])
            except (KeyError, TypeError, ValueError):
                return {
                    "statusCode": 400,
                    "body": json.dumps({"error": "Invalid cart item"})
                }
            if qty <= 0 or qty > 100:
                return {
                    "statusCode": 400,
                    "body": json.dumps({"error": "Quantity must be between 1 and 100"})
                }
            wanted[pid] = wanted.get(pid, 0) + qty
        
        cur, conn = get_db_cursor()
        try:
            # Check stock and calculate totals
            lines, total, cost = [], 0.0, 0.0
            for pid, qty in wanted.items():
                cur.execute("SELECT * FROM products WHERE id = %s", (pid,))
                p = cur.fetchone()
                
                if p is None:
                    conn.rollback()
                    return {
                        "statusCode": 404,
                        "body": json.dumps({"error": f"Product {pid} not found"})
                    }
                
                if p["stock"] < qty:
                    conn.rollback()
                    return {
                        "statusCode": 409,
                        "body": json.dumps({
                            "error": f"Not enough stock for {p['name']} (only {p['stock']} left)"
                        })
                    }
                
                lines.append((p, qty))
                total += float(p["price"]) * qty
                cost += float(p["cost"]) * qty
            
            # Create order
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cur.execute(
                "INSERT INTO orders (user_id, customer, total, cost, payment_method, created_at) VALUES (%s,%s,%s,%s,%s,%s) RETURNING id",
                (event["user"]["id"], customer, round(total, 2), round(cost, 2), method, now)
            )
            order_id = cur.fetchone()["id"]
            
            # Add order items and update stock
            for p, qty in lines:
                cur.execute(
                    "INSERT INTO order_items (order_id, product_id, name, category, quantity, unit_price, unit_cost) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                    (order_id, p["id"], p["name"], p["category"], qty, p["price"], p["cost"])
                )
                cur.execute("UPDATE products SET stock = stock - %s WHERE id = %s", (qty, p["id"]))
            
            conn.commit()
            
            return {
                "statusCode": 201,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({
                    "order_id": order_id,
                    "total": round(total, 2),
                    "payment_method": method,
                    "created_at": now
                })
            }
        except Exception as e:
            conn.rollback()
            raise
        finally:
            cur.close()
            conn.close()
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

@auth_required()
def dashboard_handler(event, context):
    """Get dashboard data"""
    cur, conn = get_db_cursor()
    try:
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Get today's stats
        cur.execute(
            "SELECT COALESCE(SUM(total),0) AS revenue, COUNT(*) AS orders FROM orders WHERE DATE(created_at) = %s",
            (today,)
        )
        day = cur.fetchone()
        revenue, orders = round(float(day["revenue"]), 2), day["orders"]
        
        # Sales by category
        cur.execute(
            "SELECT oi.category AS name, ROUND(SUM(oi.quantity*oi.unit_price),2) AS value FROM order_items oi JOIN orders o ON o.id = oi.order_id WHERE DATE(o.created_at) = %s GROUP BY oi.category ORDER BY value DESC",
            (today,)
        )
        by_cat = cur.fetchall()
        
        # Top products
        cur.execute(
            "SELECT oi.name AS name, SUM(oi.quantity) AS value FROM order_items oi JOIN orders o ON o.id = oi.order_id WHERE DATE(o.created_at) = %s GROUP BY oi.name ORDER BY value DESC LIMIT 5",
            (today,)
        )
        top = cur.fetchall()
        
        # Recent orders
        cur.execute("SELECT id, customer, total, payment_method, created_at FROM orders ORDER BY id DESC LIMIT 8")
        recent = cur.fetchall()
        
        # Total products
        cur.execute("SELECT COUNT(*) AS count FROM products")
        total_products = cur.fetchone()["count"]
        
        # Low stock
        cur.execute("SELECT name, stock FROM products WHERE stock <= %s ORDER BY stock", (LOW_STOCK,))
        low = cur.fetchall()
        
        conn.commit()
        
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "revenue": revenue,
                "orders": orders,
                "average_order": round(revenue / orders, 2) if orders else 0,
                "total_products": total_products,
                "sales_by_category": [dict(r) for r in by_cat],
                "top_products": [dict(r) for r in top],
                "recent_orders": [dict(r) for r in recent],
                "low_stock": [dict(r) for r in low]
            })
        }
    finally:
        cur.close()
        conn.close()

@auth_required("admin")
def reports_handler(event, context):
    """Get reports data"""
    try:
        period_type = event.get("queryStringParameters", {}).get("type", "daily")
        date_value = event.get("queryStringParameters", {}).get("date")
        
        if period_type == "daily":
            day = parse_date(date_value or datetime.now().strftime("%Y-%m-%d"))
            if day is None:
                return {"statusCode": 400, "body": json.dumps({"error": "Date must be YYYY-MM-DD"})}
            # Build daily report (simplified for now)
            cur, conn = get_db_cursor()
            try:
                cur.execute(
                    "SELECT COALESCE(SUM(total),0) AS revenue, COALESCE(SUM(cost),0) AS cost, COUNT(*) AS orders FROM orders WHERE DATE(created_at) = %s",
                    (day,)
                )
                summary = cur.fetchone()
                conn.commit()
                
                return {
                    "statusCode": 200,
                    "headers": {"Content-Type": "application/json"},
                    "body": json.dumps({
                        "date": day,
                        "revenue": round(float(summary["revenue"]), 2),
                        "cost": round(float(summary["cost"]), 2),
                        "profit": round(float(summary["revenue"]) - float(summary["cost"]), 2),
                        "orders": summary["orders"],
                        "products": [],
                        "categories": [],
                        "trend": []
                    })
                }
            finally:
                cur.close()
                conn.close()
        else:
            return {"statusCode": 400, "body": json.dumps({"error": "Only daily reports supported for now"})}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}

# --------------------------------------------------------------------------- #
# Main Handler
# --------------------------------------------------------------------------- #
def handler(event, context):
    """Route to appropriate handler based on path"""
    path = event.get("path", "")
    method = event.get("httpMethod", "GET")
    
    # Route mapping
    routes = {
        "POST /api/login": login_handler,
        "GET /api/me": me_handler,
        "GET /api/products": list_products_handler,
        "GET /api/inventory": inventory_handler,
        "POST /api/orders": create_order_handler,
        "GET /api/dashboard": dashboard_handler,
        "GET /api/reports": reports_handler,
    }
    
    # Check for dynamic routes
    if path.startswith("/api/inventory/") and method == "POST":
        return restock_handler(event, context)
    
    key = f"{method} {path}"
    handler_func = routes.get(key)
    
    if handler_func:
        return handler_func(event, context)
    else:
        return {
            "statusCode": 404,
            "body": json.dumps({"error": "Not found"})
        }
