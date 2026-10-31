from backend.utils.helpers import get_db

class PaymentModel:
    @staticmethod
    def get_all(customer_id=None):
        db = get_db()
        query = """
            SELECT p.*, inv.invoice_number, u.full_name as customer_name, u.company_name
            FROM payments p
            JOIN invoices inv ON p.invoice_id = inv.id
            JOIN users u ON inv.customer_id = u.id
        """
        params = []
        if customer_id:
            query += " WHERE inv.customer_id = ?"
            params.append(customer_id)
        query += " ORDER BY p.payment_date DESC"
        return db.execute(query, params).fetchall()

    @staticmethod
    def create(payment_reference, invoice_id, amount, currency='USD', payment_method='Credit Card',
               transaction_status='Completed', gateway_transaction_id='', notes=''):
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            """
            INSERT INTO payments (
                payment_reference, invoice_id, amount, currency, payment_method,
                transaction_status, gateway_transaction_id, notes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (payment_reference, invoice_id, amount, currency, payment_method,
             transaction_status, gateway_transaction_id, notes)
        )
        db.commit()
        return cursor.lastrowid

