from backend.utils.helpers import get_db

class PlanModel:
    @staticmethod
    def get_all(product_id=None):
        db = get_db()
        query = """
            SELECT pl.*, p.name as product_name, p.category as product_category
            FROM plans pl
            JOIN products p ON pl.product_id = p.id
        """
        params = []
        if product_id:
            query += " WHERE pl.product_id = ?"
            params.append(product_id)
        query += " ORDER BY pl.price ASC"
        return db.execute(query, params).fetchall()

    @staticmethod
    def get_by_id(plan_id):
        db = get_db()
        return db.execute(
            """
            SELECT pl.*, p.name as product_name
            FROM plans pl
            JOIN products p ON pl.product_id = p.id
            WHERE pl.id = ?
            """,
            (plan_id,)
        ).fetchone()

    @staticmethod
    def create(product_id, name, code, billing_interval, price, currency='USD', trial_days=14, features='', is_popular=0):
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            """
            INSERT INTO plans (product_id, name, code, billing_interval, price, currency, trial_days, features, is_popular)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (product_id, name, code, billing_interval, price, currency, trial_days, features, is_popular)
        )
        db.commit()
        return cursor.lastrowid

