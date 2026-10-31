from flask import Blueprint, render_template, request, redirect, url_for, flash
from backend.utils.helpers import login_required
from backend.models.discount import DiscountModel

discounts_bp = Blueprint('discounts', __name__, url_prefix='/discounts')

@discounts_bp.route('/')
@login_required(role=['Admin', 'Staff'])
def list_discounts():
    discounts = DiscountModel.get_all()
    return render_template('discounts.html', discounts=discounts, current_page='discounts')

@discounts_bp.route('/create', methods=['POST'])
@login_required(role=['Admin', 'Staff'])
def create_discount():
    code = request.form.get('code')
    discount_type = request.form.get('discount_type', 'percentage')
    value = request.form.get('value', type=float)
    description = request.form.get('description', '')
    valid_from = request.form.get('valid_from')
    valid_until = request.form.get('valid_until')
    usage_limit = request.form.get('usage_limit', type=int)

    if not code or value is None:
        flash('Coupon code and discount value are required.', 'error')
        return redirect(url_for('discounts.list_discounts'))

    try:
        DiscountModel.create(code, discount_type, value, description, valid_from, valid_until, usage_limit)
        flash(f"Coupon '{code.upper()}' created successfully!", 'success')
    except Exception as e:
        flash(f"Error creating coupon: {str(e)}", 'error')

    return redirect(url_for('discounts.list_discounts'))

