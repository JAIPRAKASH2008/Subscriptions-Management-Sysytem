from backend.utils.helpers import get_db

class DiscountModel:
    @staticmethod
    def get_by_code(code):
        db = get_db()
        return db.execute("SELECT * FROM discounts WHERE code = ? AND is_active = 1", (code.upper().strip(),)).fetchone()

    @staticmethod
    def get_by_id(discount_id):
        db = get_db()
        return db.execute("SELECT * FROM discounts WHERE id = ?", (discount_id,)).fetchone()

    @staticmethod
    def get_all():
        db = get_db()
        return db.execute("SELECT * FROM discounts ORDER BY created_at DESC").fetchall()

    @staticmethod
    def increment_usage(discount_id):
        db = get_db()
        db.execute("UPDATE discounts SET times_used = times_used + 1 WHERE id = ?", (discount_id,))
        db.commit()

    @staticmethod
    def create(code, discount_type, value, description='', valid_from=None, valid_until=None, usage_limit=None):
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            """
            INSERT INTO discounts (code, discount_type, value, description, valid_from, valid_until, usage_limit)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (code.upper().strip(), discount_type, value, description, valid_from, valid_until, usage_limit)
        )
        db.commit()
        return cursor.lastrowid

