from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from backend.utils.helpers import login_required
from backend.models.invoice import InvoiceModel
from backend.models.payment import PaymentModel
import random

invoices_bp = Blueprint('invoices', __name__, url_prefix='/invoices')

@invoices_bp.route('/')
@login_required()
def list_invoices():
    user_role = (session.get('role') or '').upper()
    user_id = session.get('user_id')
    status_filter = request.args.get('status', 'All')

    if user_role == 'CUSTOMER':
        invoices = InvoiceModel.get_all(customer_id=user_id, status=status_filter)
    else:
        invoices = InvoiceModel.get_all(status=status_filter)

    metrics = InvoiceModel.get_metrics()

    return render_template(
        'invoices.html',
        invoices=invoices,
        metrics=metrics,
        selected_status=status_filter,
        current_page='invoices'
    )

@invoices_bp.route('/<int:invoice_id>')
@login_required()
def view_invoice(invoice_id):
    invoice = InvoiceModel.get_by_id(invoice_id)
    if not invoice:
        flash('Invoice not found.', 'error')
        return redirect(url_for('invoices.list_invoices'))

    # Security check for Customer
    if session.get('role') == 'Customer' and invoice['customer_id'] != session.get('user_id'):
        flash('Unauthorized access.', 'error')
        return redirect(url_for('invoices.list_invoices'))

    return render_template('invoice_detail.html', invoice=invoice, current_page='invoices')

@invoices_bp.route('/<int:invoice_id>/pay', methods=['POST'])
@login_required()
def pay_invoice(invoice_id):
    invoice = InvoiceModel.get_by_id(invoice_id)
    if not invoice:
        flash('Invoice not found.', 'error')
        return redirect(url_for('invoices.list_invoices'))

    payment_method = request.form.get('payment_method', 'Credit Card')
    amount = float(invoice['total_due'])
    
    # 1. Update invoice to Paid
    InvoiceModel.update_status(invoice_id, 'Paid', amount_paid=amount)

    # 2. Record payment transaction
    pay_ref = f"PAY-TXN-{random.randint(100000, 999999)}"
    PaymentModel.create(
        payment_reference=pay_ref,
        invoice_id=invoice_id,
        amount=amount,
        currency=invoice['currency'],
        payment_method=payment_method,
        transaction_status='Completed',
        notes=f"Payment for {invoice['invoice_number']}"
    )

    flash(f"Invoice {invoice['invoice_number']} settled successfully! Ref: {pay_ref}", 'success')
    return redirect(url_for('invoices.list_invoices'))

