"""Initialize PostgreSQL database for Cafe POS on Vercel"""
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash

# Replace this with your DATABASE_URL from Neon or Supabase
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
        print("✓ Seeded users")
    
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
        print("✓ Seeded products")
    
    conn.commit()
    cur.close()
    conn.close()
    print("✅ Database initialized successfully!")

if __name__ == "__main__":
    init_db()
