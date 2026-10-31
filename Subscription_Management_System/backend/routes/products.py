from flask import Blueprint, render_template, request, redirect, url_for, flash
from backend.utils.helpers import login_required
from backend.models.product import ProductModel

products_bp = Blueprint('products', __name__, url_prefix='/products')

@products_bp.route('/')
@login_required()
def list_products():
    products = ProductModel.get_all()
    return render_template('products.html', products=products, current_page='products')

@products_bp.route('/create', methods=['POST'])
@login_required(role=['Admin', 'Staff'])
def create_product():
    name = request.form.get('name')
    code = request.form.get('code')
    description = request.form.get('description')
    category = request.form.get('category', 'SaaS Platform')
    icon = request.form.get('icon', 'cube')

    if not name or not code:
        flash('Product name and code are required.', 'error')
        return redirect(url_for('products.list_products'))

    try:
        ProductModel.create(name, code, description, category, icon)
        flash(f"Product '{name}' added to catalog.", 'success')
    except Exception as e:
        flash(f"Error creating product: {str(e)}", 'error')

    return redirect(url_for('products.list_products'))

