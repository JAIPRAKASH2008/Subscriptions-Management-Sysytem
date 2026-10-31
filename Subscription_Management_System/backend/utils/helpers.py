import sqlite3
import re
from functools import wraps
from flask import session, redirect, url_for, flash, g
from backend.config import Config

def get_db():
    """Get or reuse a SQLite database connection with row factory enabled."""
    if 'db' not in g:
        # Ensure database directory exists
        Config.DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
        
        conn = sqlite3.connect(Config.DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        g.db = conn
    return g.db

def close_db(e=None):
    """Close the database connection at the end of the request."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db(force_seed=False):
    """Initialize the schema, seed data, and apply self-healing migrations."""
    Config.DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(Config.DATABASE_PATH)
    cursor = conn.cursor()
    
    # Check if users table exists
    cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='users';")
    row = cursor.fetchone()
    
    if not row:
        # Fresh setup: execute schema and seed scripts
        if Config.SCHEMA_PATH.exists():
            with open(Config.SCHEMA_PATH, 'r', encoding='utf-8') as f:
                cursor.executescript(f.read())
        
        if Config.SEED_PATH.exists():
            with open(Config.SEED_PATH, 'r', encoding='utf-8') as f:
                cursor.executescript(f.read())
        conn.commit()
    else:
        # Self-healing migration: Ensure role column allows case-insensitive 'ADMIN', 'STAFF', 'CUSTOMER'
        table_sql = row[0]
        if "UPPER(role)" not in table_sql:
            cursor.execute("PRAGMA foreign_keys = OFF;")
            cursor.execute("""
            CREATE TABLE users_migrated (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                full_name TEXT NOT NULL,
                role TEXT NOT NULL CHECK(UPPER(role) IN ('ADMIN', 'STAFF', 'CUSTOMER')),
                company_name TEXT,
                phone TEXT,
                address TEXT,
                is_active INTEGER NOT NULL DEFAULT 1,
                created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
            """)
            cursor.execute("INSERT INTO users_migrated SELECT * FROM users;")
            cursor.execute("DROP TABLE users;")
            cursor.execute("ALTER TABLE users_migrated RENAME TO users;")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);")
            cursor.execute("PRAGMA foreign_keys = ON;")
            conn.commit()

        if force_seed and Config.SEED_PATH.exists():
            with open(Config.SEED_PATH, 'r', encoding='utf-8') as f:
                cursor.executescript(f.read())
            conn.commit()
            
    conn.close()

def login_required(role=None):
    """Decorator to enforce session authentication and case-insensitive role-based access control."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Please sign in to access this page.', 'error')
                return redirect(url_for('auth.login'))
            
            user_role = session.get('role', '')
            if role:
                allowed_roles = [r.upper() for r in ([role] if isinstance(role, str) else role)]
                if user_role.upper() not in allowed_roles:
                    flash('You do not have permission to access that resource.', 'error')
                    if user_role.upper() == 'CUSTOMER':
                        return redirect(url_for('dashboard.customer_dashboard'))
                    elif user_role.upper() == 'STAFF':
                        return redirect(url_for('dashboard.staff_dashboard'))
                    return redirect(url_for('dashboard.admin_dashboard'))
                    
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def format_currency(value, currency='USD'):
    """Format floating currency values for display."""
    if value is None:
        value = 0.0
    symbol = '$'
    if currency == 'INR':
        symbol = '₹'
    elif currency == 'EUR':
        symbol = '€'
    elif currency == 'GBP':
        symbol = '£'
    return f"{symbol}{value:,.2f}"

def format_date(value):
    """Format SQL dates for user-friendly display."""
    if not value:
        return '—'
    return str(value).split(' ')[0]
