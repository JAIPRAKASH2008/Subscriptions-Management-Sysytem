-- ==============================================================================
-- Brightloop Subscription Management System - Database Schema
-- Dialect: SQLite 3
-- Description: Core relational schema supporting multi-tenant/B2B SaaS subscriptions,
--              tiered product catalogs, automated billing invoices, tax & discounts.
-- ==============================================================================

PRAGMA foreign_keys = ON;

-- -----------------------------------------------------------------------------
-- 1. Users Table (Admin, Staff, Customer - Case Insensitive Check)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    full_name TEXT NOT NULL,
    role TEXT NOT NULL CHECK(UPPER(role) IN ('ADMIN', 'STAFF', 'CUSTOMER')),
    company_name TEXT,
    phone TEXT,
    address TEXT,
    is_active INTEGER NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);

-- -----------------------------------------------------------------------------
-- 2. Products Table
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    code TEXT NOT NULL UNIQUE,
    description TEXT,
    category TEXT NOT NULL DEFAULT 'SaaS Platform',
    icon TEXT DEFAULT 'cube',
    is_active INTEGER NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_products_code ON products(code);

-- -----------------------------------------------------------------------------
-- 3. Plans Table (Product Tier Plans)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS plans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    code TEXT NOT NULL UNIQUE,
    billing_interval TEXT NOT NULL CHECK(billing_interval IN ('Monthly', 'Quarterly', 'Yearly')),
    price REAL NOT NULL CHECK(price >= 0),
    currency TEXT NOT NULL DEFAULT 'USD',
    trial_days INTEGER NOT NULL DEFAULT 14,
    features TEXT, -- JSON or comma-separated list of plan perks
    is_popular INTEGER NOT NULL DEFAULT 0,
    is_active INTEGER NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_plans_product_id ON plans(product_id);

-- -----------------------------------------------------------------------------
-- 4. Discounts Table (Coupons / Promos)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS discounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT NOT NULL UNIQUE,
    discount_type TEXT NOT NULL CHECK(discount_type IN ('percentage', 'fixed')),
    value REAL NOT NULL CHECK(value > 0),
    description TEXT,
    valid_from DATE,
    valid_until DATE,
    usage_limit INTEGER DEFAULT NULL,
    times_used INTEGER NOT NULL DEFAULT 0,
    is_active INTEGER NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_discounts_code ON discounts(code);

-- -----------------------------------------------------------------------------
-- 5. Subscriptions Table
-- Statuses: Draft, Quotation, Confirmed, Active, Closed (Case Insensitive)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS subscriptions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subscription_number TEXT NOT NULL UNIQUE,
    customer_id INTEGER NOT NULL,
    plan_id INTEGER NOT NULL,
    discount_id INTEGER,
    status TEXT NOT NULL CHECK(UPPER(status) IN ('DRAFT', 'QUOTATION', 'CONFIRMED', 'ACTIVE', 'CLOSED')),
    billing_cycle TEXT NOT NULL CHECK(billing_cycle IN ('Monthly', 'Quarterly', 'Yearly')),
    start_date DATE,
    end_date DATE,
    next_billing_date DATE,
    subtotal REAL NOT NULL DEFAULT 0.00,
    discount_amount REAL NOT NULL DEFAULT 0.00,
    tax_amount REAL NOT NULL DEFAULT 0.00,
    total_amount REAL NOT NULL DEFAULT 0.00,
    currency TEXT NOT NULL DEFAULT 'USD',
    auto_renew INTEGER NOT NULL DEFAULT 1,
    notes TEXT,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES users(id) ON DELETE RESTRICT,
    FOREIGN KEY (plan_id) REFERENCES plans(id) ON DELETE RESTRICT,
    FOREIGN KEY (discount_id) REFERENCES discounts(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_subscriptions_number ON subscriptions(subscription_number);
CREATE INDEX IF NOT EXISTS idx_subscriptions_customer ON subscriptions(customer_id);
CREATE INDEX IF NOT EXISTS idx_subscriptions_status ON subscriptions(status);

-- -----------------------------------------------------------------------------
-- 6. Quotations Table (Pre-subscription quotes & enterprise proposals)
-- Statuses: Draft, Sent, Accepted, Rejected, Converted
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS quotations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quotation_number TEXT NOT NULL UNIQUE,
    customer_id INTEGER NOT NULL,
    plan_id INTEGER NOT NULL,
    subscription_id INTEGER,
    proposed_amount REAL NOT NULL,
    discount_amount REAL DEFAULT 0.00,
    tax_amount REAL DEFAULT 0.00,
    total_amount REAL NOT NULL,
    currency TEXT NOT NULL DEFAULT 'USD',
    valid_until DATE NOT NULL,
    status TEXT NOT NULL CHECK(UPPER(status) IN ('DRAFT', 'SENT', 'ACCEPTED', 'REJECTED', 'CONVERTED')),
    terms TEXT,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES users(id) ON DELETE RESTRICT,
    FOREIGN KEY (plan_id) REFERENCES plans(id) ON DELETE RESTRICT,
    FOREIGN KEY (subscription_id) REFERENCES subscriptions(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_quotations_number ON quotations(quotation_number);
CREATE INDEX IF NOT EXISTS idx_quotations_customer ON quotations(customer_id);

-- -----------------------------------------------------------------------------
-- 7. Invoices Table
-- Statuses: Draft, Unpaid, Paid, Overdue, Cancelled
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS invoices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_number TEXT NOT NULL UNIQUE,
    subscription_id INTEGER NOT NULL,
    customer_id INTEGER NOT NULL,
    issue_date DATE NOT NULL,
    due_date DATE NOT NULL,
    subtotal REAL NOT NULL,
    tax_amount REAL NOT NULL DEFAULT 0.00,
    discount_amount REAL NOT NULL DEFAULT 0.00,
    total_due REAL NOT NULL,
    amount_paid REAL NOT NULL DEFAULT 0.00,
    currency TEXT NOT NULL DEFAULT 'USD',
    status TEXT NOT NULL CHECK(UPPER(status) IN ('DRAFT', 'UNPAID', 'PAID', 'OVERDUE', 'CANCELLED')),
    pdf_path TEXT,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (subscription_id) REFERENCES subscriptions(id) ON DELETE CASCADE,
    FOREIGN KEY (customer_id) REFERENCES users(id) ON DELETE RESTRICT
);

CREATE INDEX IF NOT EXISTS idx_invoices_number ON invoices(invoice_number);
CREATE INDEX IF NOT EXISTS idx_invoices_subscription ON invoices(subscription_id);
CREATE INDEX IF NOT EXISTS idx_invoices_customer ON invoices(customer_id);
CREATE INDEX IF NOT EXISTS idx_invoices_status ON invoices(status);

-- -----------------------------------------------------------------------------
-- 8. Payments Table
-- Statuses: Pending, Completed, Failed, Refunded
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    payment_reference TEXT NOT NULL UNIQUE,
    invoice_id INTEGER NOT NULL,
    amount REAL NOT NULL CHECK(amount > 0),
    currency TEXT NOT NULL DEFAULT 'USD',
    payment_method TEXT NOT NULL CHECK(payment_method IN ('Credit Card', 'Bank Transfer', 'Stripe', 'UPI', 'PayPal')),
    transaction_status TEXT NOT NULL CHECK(UPPER(transaction_status) IN ('PENDING', 'COMPLETED', 'FAILED', 'REFUNDED')),
    gateway_transaction_id TEXT,
    payment_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    notes TEXT,
    FOREIGN KEY (invoice_id) REFERENCES invoices(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_payments_reference ON payments(payment_reference);
CREATE INDEX IF NOT EXISTS idx_payments_invoice ON payments(invoice_id);
CREATE INDEX IF NOT EXISTS idx_payments_status ON payments(transaction_status);
