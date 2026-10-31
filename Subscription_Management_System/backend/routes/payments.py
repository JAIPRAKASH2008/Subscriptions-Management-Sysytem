from flask import Blueprint, render_template, session
from backend.utils.helpers import login_required
from backend.models.payment import PaymentModel

payments_bp = Blueprint('payments', __name__, url_prefix='/payments')

@payments_bp.route('/')
@login_required()
def list_payments():
    user_role = (session.get('role') or '').upper()
    user_id = session.get('user_id')

    if user_role == 'CUSTOMER':
        payments = PaymentModel.get_all(customer_id=user_id)
    else:
        payments = PaymentModel.get_all()

    return render_template('payments.html', payments=payments, current_page='payments')

