from backend.utils.helpers import get_db

class ProductModel:
    @staticmethod
    def get_all():
        db = get_db()
        return db.execute(
            """
            SELECT p.*, COUNT(pl.id) as plan_count 
            FROM products p
            LEFT JOIN plans pl ON p.id = pl.product_id
            GROUP BY p.id
            ORDER BY p.name ASC
            """
        ).fetchall()

    @staticmethod
    def get_by_id(product_id):
        db = get_db()
        return db.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()

    @staticmethod
    def create(name, code, description, category='SaaS Platform', icon='cube'):
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            """
            INSERT INTO products (name, code, description, category, icon)
            VALUES (?, ?, ?, ?, ?)
            """,
            (name, code, description, category, icon)
        )
        db.commit()
        return cursor.lastrowid

