from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from backend.utils.helpers import login_required, get_db
from backend.models.user import UserModel
from backend.models.plan import PlanModel

quotations_bp = Blueprint('quotations', __name__, url_prefix='/quotations')

@quotations_bp.route('/')
@login_required()
def list_quotations():
    db = get_db()
    user_role = (session.get('role') or '').upper()
    user_id = session.get('user_id')

    query = """
        SELECT q.*, u.full_name as customer_name, u.company_name, pl.name as plan_name, p.name as product_name
        FROM quotations q
        JOIN users u ON q.customer_id = u.id
        JOIN plans pl ON q.plan_id = pl.id
        JOIN products p ON pl.product_id = p.id
    """
    params = []
    if user_role == 'CUSTOMER':
        query += " WHERE q.customer_id = ?"
        params.append(user_id)
    query += " ORDER BY q.created_at DESC"
    
    quotations = db.execute(query, params).fetchall()
    customers = UserModel.get_all_customers()
    plans = PlanModel.get_all()

    return render_template(
        'quotations.html',
        quotations=quotations,
        customers=customers,
        plans=plans,
        current_page='quotations'
    )

