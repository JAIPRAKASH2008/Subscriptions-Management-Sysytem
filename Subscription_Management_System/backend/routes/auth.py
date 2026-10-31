import random
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
from backend.models.user import UserModel
from backend.utils.validators import validate_password_strength, validate_email
from backend.utils.helpers import login_required

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        
        user = UserModel.get_by_email(email)
        if not user or not check_password_hash(user['password_hash'], password):
            flash('Invalid email or password. Please verify your credentials.', 'error')
            return render_template('login.html', email=email)
            
        if not user['is_active']:
            flash('This account has been deactivated. Please contact support.', 'error')
            return render_template('login.html', email=email)
            
        # Set session details
        session['user_id'] = user['id']
        session['username'] = user['username']
        session['full_name'] = user['full_name']
        session['email'] = user['email']
        session['role'] = user['role']
        session['company_name'] = user['company_name']
        
        flash(f"Welcome back, {user['full_name']}!", 'success')
        
        # Case-insensitive role-based landing redirects
        role_upper = (user['role'] or '').upper()
        if role_upper == 'CUSTOMER':
            return redirect(url_for('dashboard.customer_dashboard'))
        elif role_upper == 'STAFF':
            return redirect(url_for('dashboard.staff_dashboard'))
        return redirect(url_for('dashboard.admin_dashboard'))

    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        company_name = request.form.get('company_name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # 1. Email format check
        valid_email, err_email = validate_email(email)
        if not valid_email:
            flash(err_email, 'error')
            return render_template('register.html', full_name=full_name, company_name=company_name, email=email, phone=phone)
            
        # 2. Check if email already registered (Friendly UI message instead of crashing)
        if UserModel.get_by_email(email):
            flash(f"An account with email '{email}' already exists. Please sign in or use another email address.", 'error')
            return render_template('register.html', full_name=full_name, company_name=company_name, phone=phone)

        # 3. Password matching
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('register.html', full_name=full_name, company_name=company_name, email=email, phone=phone)

        # 4. Password strength requirement check
        is_strong, err_msg = validate_password_strength(password)
        if not is_strong:
            flash(err_msg, 'error')
            return render_template('register.html', full_name=full_name, company_name=company_name, email=email, phone=phone)

        # 5. Create new Customer user
        username = email.split('@')[0]
        if UserModel.get_by_username(username):
            username = f"{username}{random.randint(100, 999)}"

        hashed_pw = generate_password_hash(password)
        try:
            UserModel.create(
                username=username,
                email=email,
                password_hash=hashed_pw,
                full_name=full_name,
                role='Customer',
                company_name=company_name,
                phone=phone
            )
            flash('Account registered successfully! You can now log in.', 'success')
            return redirect(url_for('auth.login'))
        except ValueError as e:
            flash(str(e), 'error')
            return render_template('register.html', full_name=full_name, company_name=company_name, email=email, phone=phone)

    return render_template('register.html')

@auth_bp.route('/users/create', methods=['POST'])
@auth_bp.route('/staff/create', methods=['POST'])
@login_required(role=['Admin', 'ADMIN'])
def create_user():
    """
    Allows an authenticated Administrator to provision new Admin or Staff user accounts.
    Applies password hashing and friendly unique-email validation.
    """
    full_name = request.form.get('full_name', '').strip()
    email = request.form.get('email', '').strip()
    role = request.form.get('role', 'Staff').strip()
    password = request.form.get('password', '')
    company_name = request.form.get('company_name', '').strip() or 'Brightloop Internal'
    phone = request.form.get('phone', '').strip()

    if not full_name or not email:
        flash('Full name and email address are mandatory.', 'error')
        return redirect(request.referrer or url_for('dashboard.admin_dashboard'))

    # Validate email format
    valid_email, err_email = validate_email(email)
    if not valid_email:
        flash(err_email, 'error')
        return redirect(request.referrer or url_for('dashboard.admin_dashboard'))

    # Check for duplicate email before database insertion
    if UserModel.get_by_email(email):
        flash(f"Cannot create user: An account with email '{email}' already exists. Please use a unique email address.", 'error')
        return redirect(request.referrer or url_for('dashboard.admin_dashboard'))

    # Validate and normalize role (Accepts 'Admin', 'Staff', 'ADMIN', 'STAFF')
    role_upper = role.upper()
    if role_upper not in ['ADMIN', 'STAFF']:
        flash("Invalid role specified. Only 'Admin' or 'Staff' can be created here.", 'error')
        return redirect(request.referrer or url_for('dashboard.admin_dashboard'))
    
    role_normalized = role_upper.capitalize() # 'Admin' or 'Staff'

    # Password validation & Werkzeug hashing
    if not password:
        password = "Staff@1234#" # Secure default if omitted
    
    is_strong, err_pwd = validate_password_strength(password)
    if not is_strong:
        flash(f"Password requirement not met: {err_pwd}", 'error')
        return redirect(request.referrer or url_for('dashboard.admin_dashboard'))

    hashed_pw = generate_password_hash(password)

    # Generate unique username
    base_username = email.split('@')[0]
    username = base_username
    if UserModel.get_by_username(username):
        username = f"{base_username}_{random.randint(100, 999)}"

    try:
        user_id = UserModel.create(
            username=username,
            email=email,
            password_hash=hashed_pw,
            full_name=full_name,
            role=role_normalized,
            company_name=company_name,
            phone=phone
        )
        flash(f"{role_normalized} member '{full_name}' ({email}) created successfully!", 'success')
    except ValueError as e:
        flash(str(e), 'error')
    except Exception as e:
        flash(f"Database error while creating user: {str(e)}", 'error')

    return redirect(request.referrer or url_for('dashboard.admin_dashboard'))

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been signed out safely.', 'success')
    return redirect(url_for('auth.login'))
