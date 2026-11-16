"""Configuration constants for Cafe POS"""
import os

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
