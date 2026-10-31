from backend.utils.helpers import get_db

class InvoiceModel:
    @staticmethod
    def get_all(customer_id=None, status=None):
        db = get_db()
        query = """
            SELECT inv.*, 
                   u.full_name as customer_name, u.email as customer_email, u.company_name,
                   s.subscription_number, p.name as product_name, pl.name as plan_name
            FROM invoices inv
            JOIN users u ON inv.customer_id = u.id
            JOIN subscriptions s ON inv.subscription_id = s.id
            JOIN plans pl ON s.plan_id = pl.id
            JOIN products p ON pl.product_id = p.id
        """
        clauses = []
        params = []
        if customer_id:
            clauses.append("inv.customer_id = ?")
            params.append(customer_id)
        if status and status != 'All':
            clauses.append("inv.status = ?")
            params.append(status)

        if clauses:
            query += " WHERE " + " AND ".join(clauses)

        query += " ORDER BY inv.issue_date DESC"
        return db.execute(query, params).fetchall()

    @staticmethod
    def get_by_id(invoice_id):
        db = get_db()
        return db.execute(
            """
            SELECT inv.*, 
                   u.full_name as customer_name, u.email as customer_email, u.company_name, u.address as customer_address,
                   s.subscription_number, s.billing_cycle,
                   p.name as product_name, pl.name as plan_name
            FROM invoices inv
            JOIN users u ON inv.customer_id = u.id
            JOIN subscriptions s ON inv.subscription_id = s.id
            JOIN plans pl ON s.plan_id = pl.id
            JOIN products p ON pl.product_id = p.id
            WHERE inv.id = ?
            """,
            (invoice_id,)
        ).fetchone()

    @staticmethod
    def create(invoice_number, subscription_id, customer_id, issue_date, due_date,
               subtotal, tax_amount, discount_amount, total_due, currency='USD', status='Unpaid'):
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            """
            INSERT INTO invoices (
                invoice_number, subscription_id, customer_id, issue_date, due_date,
                subtotal, tax_amount, discount_amount, total_due, currency, status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (invoice_number, subscription_id, customer_id, issue_date, due_date,
             subtotal, tax_amount, discount_amount, total_due, currency, status)
        )
        db.commit()
        return cursor.lastrowid

    @staticmethod
    def update_status(invoice_id, status, amount_paid=None):
        db = get_db()
        if amount_paid is not None:
            db.execute(
                "UPDATE invoices SET status = ?, amount_paid = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (status, amount_paid, invoice_id)
            )
        else:
            db.execute(
                "UPDATE invoices SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (status, invoice_id)
            )
        db.commit()

    @staticmethod
    def get_metrics():
        db = get_db()
        total_collected = db.execute("SELECT SUM(amount_paid) as total FROM invoices WHERE status = 'Paid'").fetchone()['total'] or 0.0
        total_outstanding = db.execute("SELECT SUM(total_due - amount_paid) as total FROM invoices WHERE status IN ('Unpaid', 'Overdue')").fetchone()['total'] or 0.0
        overdue_count = db.execute("SELECT COUNT(*) as count FROM invoices WHERE status = 'Overdue'").fetchone()['count']
        paid_count = db.execute("SELECT COUNT(*) as count FROM invoices WHERE status = 'Paid'").fetchone()['count']
        
        return {
            'total_collected': round(total_collected, 2),
            'total_outstanding': round(total_outstanding, 2),
            'overdue_count': overdue_count,
            'paid_count': paid_count
        }

