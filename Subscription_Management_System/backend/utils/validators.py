import re

def validate_password_strength(password):
    """
    Validates that a password satisfies enterprise SaaS security policies:
    - Minimum 8 characters
    - At least one uppercase letter [A-Z]
    - At least one lowercase letter [a-z]
    - At least one special character [^A-Za-z0-9]
    """
    if not password or len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search(r'[A-Z]', password):
        return False, "Password must include at least one uppercase letter (A-Z)."
    if not re.search(r'[a-z]', password):
        return False, "Password must include at least one lowercase letter (a-z)."
    if not re.search(r'[^A-Za-z0-9]', password):
        return False, "Password must contain at least one special character (e.g. !@#$%^&*)."
    return True, ""

def validate_email(email):
    """Basic format verification for user emails."""
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not email or not re.match(pattern, email):
        return False, "Please provide a valid corporate email address."
    return True, ""

