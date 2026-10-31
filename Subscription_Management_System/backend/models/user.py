import sqlite3
from backend.utils.helpers import get_db

class UserModel:
    """User Data Access Object & Relationship Model."""

    @staticmethod
    def get_by_id(user_id):
        if user_id is None:
            return None
        db = get_db()
        return db.execute("SELECT * FROM users WHERE id = ?", (int(user_id),)).fetchone()

    @staticmethod
    def get_by_email(email):
        if not email:
            return None
        db = get_db()
        return db.execute("SELECT * FROM users WHERE email = ? COLLATE NOCASE", (email.strip(),)).fetchone()

    @staticmethod
    def get_by_username(username):
        if not username:
            return None
        db = get_db()
        return db.execute("SELECT * FROM users WHERE username = ? COLLATE NOCASE", (username.strip(),)).fetchone()

    @staticmethod
    def create(username, email, password_hash, full_name, role='Customer', company_name='', phone='', address=''):
        """
        Creates a new user record in the database.
        Supports all roles: 'Admin', 'Staff', 'Customer', 'ADMIN', 'STAFF', 'CUSTOMER'.
        Normalizes role to Title Case to ensure database constraint and display consistency.
        """
        db = get_db()
        cursor = db.cursor()

        # Normalize role
        role_cleaned = (role or 'Customer').strip()
        if role_cleaned.upper() in ['ADMIN', 'STAFF', 'CUSTOMER']:
            role_cleaned = role_cleaned.capitalize()
        else:
            role_cleaned = 'Customer'

        try:
            cursor.execute(
                """
                INSERT INTO users (username, email, password_hash, full_name, role, company_name, phone, address)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (username.strip(), email.strip(), password_hash, full_name.strip(), role_cleaned, company_name.strip(), phone.strip(), address.strip())
            )
            db.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError as e:
            db.rollback()
            err_msg = str(e).lower()
            if 'unique' in err_msg and 'email' in err_msg:
                raise ValueError(f"An account with email '{email}' already exists.")
            elif 'unique' in err_msg and 'username' in err_msg:
                raise ValueError(f"Username '{username}' is already in use.")
            raise ValueError(f"Failed to create user: {str(e)}")

    @staticmethod
    def get_all(role=None):
        db = get_db()
        if role:
            return db.execute("SELECT * FROM users WHERE UPPER(role) = UPPER(?) ORDER BY created_at DESC", (role,)).fetchall()
        return db.execute("SELECT * FROM users ORDER BY created_at DESC").fetchall()

    @staticmethod
    def get_all_customers():
        db = get_db()
        return db.execute("SELECT * FROM users WHERE UPPER(role) = 'CUSTOMER' AND is_active = 1 ORDER BY full_name ASC").fetchall()

    @staticmethod
    def get_staff_and_admins():
        """Returns all staff and administrative accounts for team management."""
        db = get_db()
        return db.execute(
            "SELECT * FROM users WHERE UPPER(role) IN ('ADMIN', 'STAFF') ORDER BY role ASC, full_name ASC"
        ).fetchall()

    @staticmethod
    def get_subscriptions(user_id, status=None):
        """
        Relationship helper: Retrieves all subscriptions linked to this customer account.
        Used by customer dashboard and admin customer inspection.
        """
        if user_id is None:
            return []
        from backend.models.subscription import SubscriptionModel
        return SubscriptionModel.get_all(customer_id=int(user_id), status=status)

    @staticmethod
    def count(role='Customer'):
        db = get_db()
        if role:
            return db.execute("SELECT COUNT(*) as total FROM users WHERE UPPER(role) = UPPER(?)", (role,)).fetchone()['total']
        return db.execute("SELECT COUNT(*) as total FROM users").fetchone()['total']
