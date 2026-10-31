from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from backend.utils.helpers import login_required
from backend.models.subscription import SubscriptionModel
from backend.models.invoice import InvoiceModel
from backend.models.payment import PaymentModel
from backend.models.user import UserModel
from backend.models.plan import PlanModel

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    role = (session.get('role') or '').upper()
    if role == 'CUSTOMER':
        return redirect(url_for('dashboard.customer_dashboard'))
    elif role == 'STAFF':
        return redirect(url_for('dashboard.staff_dashboard'))
    return redirect(url_for('dashboard.admin_dashboard'))

@dashboard_bp.route('/admin/dashboard')
@login_required(role=['Admin', 'ADMIN'])
def admin_dashboard():
    sub_metrics = SubscriptionModel.get_metrics()
    inv_metrics = InvoiceModel.get_metrics()
    total_customers = UserModel.count(role='Customer')
    
    # Recent items for tables
    recent_subscriptions = SubscriptionModel.get_all()[:8]
    recent_invoices = InvoiceModel.get_all()[:6]
    recent_payments = PaymentModel.get_all()[:6]
    
    # Team & Staff accounts list
    staff_members = UserModel.get_staff_and_admins()
    customers_list = UserModel.get_all_customers()
    plans_list = PlanModel.get_all()

    return render_template(
        'admin_dashboard.html',
        sub_metrics=sub_metrics,
        inv_metrics=inv_metrics,
        total_customers=total_customers,
        recent_subscriptions=recent_subscriptions,
        recent_invoices=recent_invoices,
        recent_payments=recent_payments,
        staff_members=staff_members,
        customers=customers_list,
        plans=plans_list,
        current_page='dashboard'
    )

@dashboard_bp.route('/staff/dashboard')
@login_required(role=['Admin', 'Staff', 'ADMIN', 'STAFF'])
def staff_dashboard():
    sub_metrics = SubscriptionModel.get_metrics()
    inv_metrics = InvoiceModel.get_metrics()
    recent_subscriptions = SubscriptionModel.get_all()[:10]
    recent_invoices = InvoiceModel.get_all()[:10]
    staff_members = UserModel.get_staff_and_admins()

    return render_template(
        'staff_dashboard.html',
        sub_metrics=sub_metrics,
        inv_metrics=inv_metrics,
        recent_subscriptions=recent_subscriptions,
        recent_invoices=recent_invoices,
        staff_members=staff_members,
        current_page='staff_dashboard'
    )

@dashboard_bp.route('/customer/dashboard')
@login_required()
def customer_dashboard():
    """
    Customer portal view.
    Allows logged-in customers to view their subscriptions & invoices.
    Also allows Admins and Staff to inspect a customer's portal by passing ?customer_id=<id>.
    """
    user_role = (session.get('role') or '').upper()
    req_customer_id = request.args.get('customer_id', type=int)

    if req_customer_id and user_role in ['ADMIN', 'STAFF']:
        target_customer_id = req_customer_id
    else:
        target_customer_id = session.get('user_id')

    target_user = UserModel.get_by_id(target_customer_id)
    if not target_user:
        flash('Customer profile not found.', 'error')
        return redirect(url_for('dashboard.admin_dashboard'))

    # Retrieve all subscriptions specifically filtered by the target customer_id
    my_subscriptions = UserModel.get_subscriptions(target_customer_id)
    my_invoices = InvoiceModel.get_all(customer_id=target_customer_id)
    available_plans = PlanModel.get_all()[:4]

    return render_template(
        'customer_dashboard.html',
        customer=target_user,
        subscriptions=my_subscriptions,
        invoices=my_invoices,
        available_plans=available_plans,
        is_admin_view=(user_role in ['ADMIN', 'STAFF'] and target_customer_id != session.get('user_id')),
        current_page='customer_dashboard'
    )

@dashboard_bp.route('/customers/<int:customer_id>')
@dashboard_bp.route('/admin/customers/<int:customer_id>')
@login_required(role=['Admin', 'Staff', 'ADMIN', 'STAFF'])
def view_customer(customer_id):
    """
    Dedicated Customer Detail View for Admins & Staff.
    Shows the customer's profile, full active subscription history, and invoices.
    """
    customer = UserModel.get_by_id(customer_id)
    if not customer:
        flash('Customer profile not found.', 'error')
        return redirect(url_for('dashboard.admin_dashboard'))

    subscriptions = UserModel.get_subscriptions(customer_id)
    invoices = InvoiceModel.get_all(customer_id=customer_id)
    plans = PlanModel.get_all()

    return render_template(
        'customer_detail.html',
        customer=customer,
        subscriptions=subscriptions,
        invoices=invoices,
        plans=plans,
        current_page='customers'
    )
