from datetime import date
from backend.models.discount import DiscountModel

class DiscountService:
    @staticmethod
    def apply_discount(subtotal, code):
        """
        Validates coupon code and returns (is_valid, discount_amount, discount_id, message).
        """
        if not code:
            return True, 0.0, None, "No discount applied."

        discount = DiscountModel.get_by_code(code)
        if not discount:
            return False, 0.0, None, "Invalid or expired promo code."

        # Check expiration date
        today = date.today().isoformat()
        if discount['valid_until'] and discount['valid_until'] < today:
            return False, 0.0, None, "This promo code has expired."

        # Check usage limit
        if discount['usage_limit'] and discount['times_used'] >= discount['usage_limit']:
            return False, 0.0, None, "Promo code usage limit has been reached."

        # Calculate discount amount
        discount_type = discount['discount_type']
        val = float(discount['value'])

        if discount_type == 'percentage':
            discount_amount = round((subtotal * val) / 100.0, 2)
        else: # fixed
            discount_amount = min(subtotal, val)

        return True, discount_amount, discount['id'], f"Coupon applied: {val}{'%' if discount_type == 'percentage' else '$'} off"

