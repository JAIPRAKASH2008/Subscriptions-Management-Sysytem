from backend.utils.helpers import get_db

class SubscriptionModel:
    """Subscription Data Access Object & Relationship Model."""

    @staticmethod
    def get_all(customer_id=None, status=None):
        """
        Retrieves subscriptions with optional filtering by customer_id and status.
        Ensures strict integer casting for customer_id and case-insensitive status matching.
        """
        db = get_db()
        query = """
            SELECT s.*, 
                   u.full_name as customer_name, u.email as customer_email, u.company_name, u.phone as customer_phone,
                   pl.name as plan_name, pl.billing_interval as plan_interval, pl.price as plan_price, pl.features as plan_features,
                   p.name as product_name, p.code as product_code
            FROM subscriptions s
            JOIN users u ON s.customer_id = u.id
            JOIN plans pl ON s.plan_id = pl.id
            JOIN products p ON pl.product_id = p.id
        """
        clauses = []
        params = []
        if customer_id is not None:
            clauses.append("s.customer_id = ?")
            params.append(int(customer_id))
            
        if status and status != 'All':
            clauses.append("UPPER(s.status) = UPPER(?)")
            params.append(status.strip())

        if clauses:
            query += " WHERE " + " AND ".join(clauses)

        query += " ORDER BY s.created_at DESC"
        return db.execute(query, params).fetchall()

    @staticmethod
    def get_for_customer(customer_id, status=None):
        """Relationship helper to retrieve all subscriptions for a specific customer."""
        return SubscriptionModel.get_all(customer_id=customer_id, status=status)

    @staticmethod
    def get_customer(subscription):
        """Relationship helper to retrieve the User model for a given subscription."""
        if not subscription or 'customer_id' not in subscription:
            return None
        from backend.models.user import UserModel
        return UserModel.get_by_id(subscription['customer_id'])

    @staticmethod
    def get_by_id(subscription_id):
        if subscription_id is None:
            return None
        db = get_db()
        return db.execute(
            """
            SELECT s.*, 
                   u.full_name as customer_name, u.email as customer_email, u.company_name, u.phone as customer_phone, u.address as customer_address,
                   pl.name as plan_name, pl.price as plan_price, pl.features as plan_features,
                   p.name as product_name, p.code as product_code,
                   d.code as discount_code, d.discount_type, d.value as discount_val
            FROM subscriptions s
            JOIN users u ON s.customer_id = u.id
            JOIN plans pl ON s.plan_id = pl.id
            JOIN products p ON pl.product_id = p.id
            LEFT JOIN discounts d ON s.discount_id = d.id
            WHERE s.id = ?
            """,
            (int(subscription_id),)
        ).fetchone()

    @staticmethod
    def create(subscription_number, customer_id, plan_id, discount_id, status, billing_cycle,
               start_date, end_date, next_billing_date, subtotal, discount_amount, tax_amount,
               total_amount, currency='USD', auto_renew=1, notes=''):
        db = get_db()
        cursor = db.cursor()
        
        # Normalize status to Title Case ('Active', 'Confirmed', 'Quotation', 'Draft', 'Closed')
        status_clean = (status or 'Draft').strip().capitalize()

        cursor.execute(
            """
            INSERT INTO subscriptions (
                subscription_number, customer_id, plan_id, discount_id, status,
                billing_cycle, start_date, end_date, next_billing_date, subtotal,
                discount_amount, tax_amount, total_amount, currency, auto_renew, notes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (subscription_number, int(customer_id), int(plan_id), discount_id, status_clean,
             billing_cycle, start_date, end_date, next_billing_date, subtotal,
             discount_amount, tax_amount, total_amount, currency, auto_renew, notes)
        )
        db.commit()
        return cursor.lastrowid

    @staticmethod
    def update_status(subscription_id, new_status):
        db = get_db()
        status_clean = new_status.strip().capitalize()
        db.execute(
            "UPDATE subscriptions SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (status_clean, int(subscription_id))
        )
        db.commit()

    @staticmethod
    def get_metrics():
        db = get_db()
        total_active = db.execute("SELECT COUNT(*) as count FROM subscriptions WHERE UPPER(status) = 'ACTIVE'").fetchone()['count']
        total_confirmed = db.execute("SELECT COUNT(*) as count FROM subscriptions WHERE UPPER(status) = 'CONFIRMED'").fetchone()['count']
        total_quotation = db.execute("SELECT COUNT(*) as count FROM subscriptions WHERE UPPER(status) = 'QUOTATION'").fetchone()['count']
        total_draft = db.execute("SELECT COUNT(*) as count FROM subscriptions WHERE UPPER(status) = 'DRAFT'").fetchone()['count']
        
        # Monthly Recurring Revenue (MRR) calculation:
        active_subs = db.execute(
            "SELECT subtotal, billing_cycle FROM subscriptions WHERE UPPER(status) = 'ACTIVE'"
        ).fetchall()
        
        mrr = 0.0
        for sub in active_subs:
            cycle = sub['billing_cycle']
            amount = float(sub['subtotal'])
            if cycle == 'Yearly':
                mrr += (amount / 12.0)
            elif cycle == 'Quarterly':
                mrr += (amount / 3.0)
            else:
                mrr += amount

        return {
            'active_count': total_active,
            'confirmed_count': total_confirmed,
            'quotation_count': total_quotation,
            'draft_count': total_draft,
            'mrr': round(mrr, 2)
        }
