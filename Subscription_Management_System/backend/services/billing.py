import random
from datetime import date, datetime, timedelta
from backend.services.tax import TaxService
from backend.services.discount import DiscountService
from backend.models.invoice import InvoiceModel
from backend.models.plan import PlanModel

class BillingService:
    @staticmethod
    def generate_subscription_number():
        year = datetime.now().year
        rand_num = random.randint(1000, 9999)
        return f"SUB-{year}-{rand_num}"

    @staticmethod
    def generate_invoice_number():
        year = datetime.now().year
        rand_num = random.randint(1000, 9999)
        return f"INV-{year}-{rand_num}"

    @staticmethod
    def calculate_dates(start_date=None, cycle='Monthly'):
        if not start_date:
            start_date = date.today()
        elif isinstance(start_date, str):
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()

        if cycle == 'Yearly':
            end_date = start_date + timedelta(days=365)
            next_bill = end_date
        elif cycle == 'Quarterly':
            end_date = start_date + timedelta(days=90)
            next_bill = end_date
        else: # Monthly
            end_date = start_date + timedelta(days=30)
            next_bill = end_date

        return start_date.isoformat(), end_date.isoformat(), next_bill.isoformat()

    @staticmethod
    def calculate_totals(plan_id, discount_code=None):
        plan = PlanModel.get_by_id(plan_id)
        if not plan:
            raise ValueError("Plan not found.")

        subtotal = float(plan['price'])
        valid_discount, discount_amount, discount_id, msg = DiscountService.apply_discount(subtotal, discount_code)

        taxable_amount = max(0.0, subtotal - discount_amount)
        tax_amount = TaxService.calculate_tax(taxable_amount)
        total_amount = round(taxable_amount + tax_amount, 2)

        return {
            'subtotal': subtotal,
            'discount_amount': discount_amount,
            'discount_id': discount_id,
            'tax_amount': tax_amount,
            'total_amount': total_amount,
            'currency': plan['currency'],
            'billing_cycle': plan['billing_interval'],
            'discount_message': msg
        }

    @staticmethod
    def generate_invoice_for_subscription(subscription, status='Unpaid'):
        inv_num = BillingService.generate_invoice_number()
        issue_date = date.today().isoformat()
        due_date = (date.today() + timedelta(days=10)).isoformat()

        invoice_id = InvoiceModel.create(
            invoice_number=inv_num,
            subscription_id=subscription['id'],
            customer_id=subscription['customer_id'],
            issue_date=issue_date,
            due_date=due_date,
            subtotal=subscription['subtotal'],
            tax_amount=subscription['tax_amount'],
            discount_amount=subscription['discount_amount'],
            total_due=subscription['total_amount'],
            currency=subscription['currency'],
            status=status
        )
        return invoice_id, inv_num

