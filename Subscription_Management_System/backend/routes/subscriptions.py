from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from backend.utils.helpers import login_required
from backend.models.subscription import SubscriptionModel
from backend.models.user import UserModel
from backend.models.plan import PlanModel
from backend.models.discount import DiscountModel
from backend.services.billing import BillingService

subscriptions_bp = Blueprint('subscriptions', __name__, url_prefix='/subscriptions')

@subscriptions_bp.route('/')
@login_required()
def list_subscriptions():
    """
    List subscriptions with optional filtering by status (Draft, Quotation, Confirmed, Active, Closed).
    Restricts Customers to only view their own accounts, while Admin & Staff view all.
    """
    user_role = (session.get('role') or '').upper()
    user_id = session.get('user_id')
    status_filter = request.args.get('status', 'All')

    if user_role == 'CUSTOMER':
        subscriptions = SubscriptionModel.get_all(customer_id=user_id, status=status_filter)
    else:
        subscriptions = SubscriptionModel.get_all(status=status_filter)

    # Context data for creating a new subscription via modal
    customers = UserModel.get_all_customers() if user_role in ['ADMIN', 'STAFF'] else []
    plans = PlanModel.get_all()
    metrics = SubscriptionModel.get_metrics()

    return render_template(
        'subscriptions.html',
        subscriptions=subscriptions,
        customers=customers,
        plans=plans,
        metrics=metrics,
        selected_status=status_filter,
        current_page='subscriptions'
    )

@subscriptions_bp.route('/<int:subscription_id>')
@login_required()
def view_subscription(subscription_id):
    """View detailed information for a specific subscription."""
    sub = SubscriptionModel.get_by_id(subscription_id)
    if not sub:
        flash('Subscription not found.', 'error')
        return redirect(url_for('subscriptions.list_subscriptions'))

    # Security check: Customers can only view their own
    if session.get('role') == 'Customer' and sub['customer_id'] != session.get('user_id'):
        flash('Unauthorized access.', 'error')
        return redirect(url_for('subscriptions.list_subscriptions'))

    return render_template('subscription_detail.html', subscription=sub, current_page='subscriptions')

@subscriptions_bp.route('/create', methods=['POST'])
@login_required(role=['Admin', 'Staff'])
def create_subscription():
    """
    Provision a new subscription from the modal or form.
    Calculates subtotal, discounts, and regional taxes automatically.
    """
    customer_id = request.form.get('customer_id')
    plan_id = request.form.get('plan_id')
    status = request.form.get('status', 'Draft')
    discount_code = request.form.get('discount_code', '').strip()
    notes = request.form.get('notes', '')
    start_date = request.form.get('start_date')

    if not customer_id or not plan_id:
        flash('Please select both a customer and a product plan.', 'error')
        return redirect(url_for('subscriptions.list_subscriptions'))

    try:
        # Calculate financial amounts using BillingService & TaxService
        totals = BillingService.calculate_totals(plan_id, discount_code)
        
        # Calculate billing cycle schedule dates
        start_d, end_d, next_bill_d = BillingService.calculate_dates(start_date, totals['billing_cycle'])
        
        sub_number = BillingService.generate_subscription_number()

        # Insert new subscription record
        sub_id = SubscriptionModel.create(
            subscription_number=sub_number,
            customer_id=int(customer_id),
            plan_id=int(plan_id),
            discount_id=totals['discount_id'],
            status=status,
            billing_cycle=totals['billing_cycle'],
            start_date=start_d,
            end_date=end_d,
            next_billing_date=next_bill_d,
            subtotal=totals['subtotal'],
            discount_amount=totals['discount_amount'],
            tax_amount=totals['tax_amount'],
            total_amount=totals['total_amount'],
            currency=totals['currency'],
            notes=notes
        )

        # If discount applied, increment discount counter
        if totals['discount_id']:
            DiscountModel.increment_usage(totals['discount_id'])

        # If status is Confirmed or Active, automatically generate the first invoice
        if status in ['Confirmed', 'Active']:
            new_sub = SubscriptionModel.get_by_id(sub_id)
            inv_id, inv_num = BillingService.generate_invoice_for_subscription(new_sub, status='Unpaid')
            flash(f"Subscription {sub_number} provisioned successfully! Invoice {inv_num} generated.", 'success')
        else:
            flash(f"Subscription {sub_number} created with status '{status}'.", 'success')

    except Exception as e:
        flash(f"Error provisioning subscription: {str(e)}", 'error')

    return redirect(url_for('subscriptions.list_subscriptions'))

@subscriptions_bp.route('/<int:subscription_id>/status/<string:new_status>', methods=['POST', 'GET'])
@login_required(role=['Admin', 'Staff'])
def update_status(subscription_id, new_status):
    """Transition subscription between life-cycle states: Draft, Quotation, Confirmed, Active, Closed."""
    valid_statuses = ['Draft', 'Quotation', 'Confirmed', 'Active', 'Closed']
    if new_status not in valid_statuses:
        flash('Invalid status transition requested.', 'error')
        return redirect(url_for('subscriptions.list_subscriptions'))

    sub = SubscriptionModel.get_by_id(subscription_id)
    if not sub:
        flash('Subscription not found.', 'error')
        return redirect(url_for('subscriptions.list_subscriptions'))

    SubscriptionModel.update_status(subscription_id, new_status)
    
    # If advancing from Quotation or Draft to Confirmed or Active, generate invoice if not yet billed
    if new_status in ['Confirmed', 'Active'] and sub['status'] in ['Draft', 'Quotation']:
        BillingService.generate_invoice_for_subscription(sub, status='Unpaid')
        flash(f"Subscription {sub['subscription_number']} transitioned to {new_status} and invoice created.", 'success')
    else:
        flash(f"Subscription {sub['subscription_number']} status updated to {new_status}.", 'success')

    return redirect(url_for('subscriptions.list_subscriptions'))

