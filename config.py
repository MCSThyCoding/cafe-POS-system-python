"""Configuration constants for Cafe POS"""
import os


def load_env_file(path=None):
    """Load KEY=VALUE pairs from a .env file into os.environ (does not override)."""
    env_path = path or os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    try:
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))
    except OSError:
        pass


load_env_file()

# Security
SECRET_KEY = os.environ.get("CAFE_POS_SECRET")
if not SECRET_KEY:
    if os.environ.get("FLASK_ENV") == "production":
        raise ValueError("CAFE_POS_SECRET environment variable must be set in production")

# Business Logic
TOKEN_HOURS = int(os.environ.get("TOKEN_HOURS", "8"))
LOW_STOCK = int(os.environ.get("LOW_STOCK", "10"))
RESTOCK_STEP = int(os.environ.get("RESTOCK_STEP", "10"))

# Validation Limits
MAX_ORDER_QUANTITY = int(os.environ.get("MAX_ORDER_QUANTITY", "100"))
MAX_RESTOCK_QUANTITY = int(os.environ.get("MAX_RESTOCK_QUANTITY", "1000"))
MAX_CUSTOMER_NAME_LENGTH = int(os.environ.get("MAX_CUSTOMER_NAME_LENGTH", "60"))

# Database
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cafe_pos.db")
