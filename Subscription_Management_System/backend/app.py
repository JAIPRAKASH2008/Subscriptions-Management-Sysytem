import sys
from pathlib import Path

# Add project root to sys.path so backend modules import cleanly
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from flask import Flask, render_template, session
from backend.config import Config
from backend.utils.helpers import close_db, init_db, format_currency, format_date

# Import route blueprints
from backend.routes.auth import auth_bp
from backend.routes.dashboard import dashboard_bp
from backend.routes.subscriptions import subscriptions_bp
from backend.routes.plans import plans_bp
from backend.routes.products import products_bp
from backend.routes.invoices import invoices_bp
from backend.routes.payments import payments_bp
from backend.routes.quotations import quotations_bp
from backend.routes.discounts import discounts_bp

def create_app(config_class=Config):
    """Application factory for Brightloop Subscription Management System."""
    app = Flask(
        __name__,
        template_folder=config_class.TEMPLATE_FOLDER,
        static_folder=config_class.STATIC_FOLDER
    )
    app.config.from_object(config_class)

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(subscriptions_bp)
    app.register_blueprint(plans_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(invoices_bp)
    app.register_blueprint(payments_bp)
    app.register_blueprint(quotations_bp)
    app.register_blueprint(discounts_bp)

    # Teardown database request handles
    app.teardown_appcontext(close_db)

    # Template filters
    @app.template_filter('currency')
    def filter_currency(value, currency='USD'):
        return format_currency(value, currency)

    @app.template_filter('date')
    def filter_date(value):
        return format_date(value)

    # Global context variables
    @app.context_processor
    def inject_global_vars():
        return {
            'app_name': 'Brightloop',
            'current_user': session.get('full_name'),
            'current_role': session.get('role'),
            'current_email': session.get('email'),
            'current_company': session.get('company_name'),
        }

    # Custom 404 handler
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    # Ensure database is prepared
    with app.app_context():
        init_db()

    return app

app = create_app()

if __name__ == '__main__':
    print("=" * 70)
    print(" Brightloop Subscription Management System starting...")
    print(f" Access URL: http://127.0.0.1:{Config.PORT}")
    print(" Demo Logins:")
    print("   Admin:    admin@brightloop.io      | Password: Admin@1234#")
    print("   Staff:    sarah.chen@brightloop.io | Password: Staff@1234#")
    print("   Customer: david.miller@acmecorp.com | Password: Customer@1234#")
    print("=" * 70)
    app.run(host='0.0.0.0', port=Config.PORT, debug=Config.DEBUG)

