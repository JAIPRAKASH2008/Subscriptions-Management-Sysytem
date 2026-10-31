from backend.config import Config

class TaxService:
    @staticmethod
    def calculate_tax(taxable_amount, tax_rate=None):
        """
        Calculate sales tax / VAT based on taxable amount (subtotal - discount).
        """
        if tax_rate is None:
            tax_rate = Config.DEFAULT_TAX_RATE
            
        if taxable_amount <= 0:
            return 0.0
            
        tax = round(taxable_amount * tax_rate, 2)
        return tax

