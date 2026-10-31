from flask import Blueprint, render_template, request, redirect, url_for, flash
from backend.utils.helpers import login_required
from backend.models.plan import PlanModel
from backend.models.product import ProductModel

plans_bp = Blueprint('plans', __name__, url_prefix='/plans')

@plans_bp.route('/')
@login_required()
def list_plans():
    product_id = request.args.get('product_id', type=int)
    plans = PlanModel.get_all(product_id=product_id)
    products = ProductModel.get_all()
    
    return render_template(
        'plans.html',
        plans=plans,
        products=products,
        selected_product_id=product_id,
        current_page='plans'
    )

@plans_bp.route('/create', methods=['POST'])
@login_required(role=['Admin', 'Staff'])
def create_plan():
    product_id = request.form.get('product_id')
    name = request.form.get('name')
    code = request.form.get('code')
    billing_interval = request.form.get('billing_interval', 'Monthly')
    price = request.form.get('price', type=float)
    currency = request.form.get('currency', 'USD')
    trial_days = request.form.get('trial_days', default=14, type=int)
    features = request.form.get('features', '')
    is_popular = 1 if request.form.get('is_popular') else 0

    if not product_id or not name or price is None:
        flash('Please fill in all mandatory plan details.', 'error')
        return redirect(url_for('plans.list_plans'))

    try:
        PlanModel.create(
            product_id=int(product_id),
            name=name,
            code=code,
            billing_interval=billing_interval,
            price=price,
            currency=currency,
            trial_days=trial_days,
            features=features,
            is_popular=is_popular
        )
        flash(f"Plan '{name}' successfully created!", 'success')
    except Exception as e:
        flash(f"Error creating plan: {str(e)}", 'error')

    return redirect(url_for('plans.list_plans'))

