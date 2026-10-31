# Brightloop — Enterprise Subscription Management System

Brightloop is a next-generation **B2B SaaS Subscription & Recurring Billing Infrastructure** web application designed to orchestrate complex product plans, proposals, subscription lifecycles, and automated tax-compliant invoicing.

Crafted with a **Soft Teal / Aqua (`#0e7490`, `#06b6d4`) and White gradient theme**, modern CSS Flexbox/Grid, smooth hover interactions, rounded corners (`border-radius: 12px`), and soft multi-layer drop shadows inspired by Stripe, Linear, and Vercel.

---

## 🚀 Key Features

1. **B2B Executive UI/UX Design System**:
   - **Split-Screen Public Auth**: Left side features an expansive Teal/Cyan gradient with glassmorphism KPI simulation cards; right side features high-converting auth cards with password visibility toggles and real-time password requirement checklists.
   - **Dark Slate Fixed Sidebar (`260px`)**: Featuring glyph branding, grouped operational navigation, active gradient state indicators, and user account status.
   - **Modern Frosted Topbar (`70px`)**: Global search (`⌘K`), quick notifications, and role pill tags.
   - **Clean Relational Tables**: Zero vertical borders, subtle hover transitions, and pulse-ready status pills.
   - **KPI Metric Telemetry**: Executive overview of MRR, active licenses, settled receivables, and overdue alerts.

2. **Full Subscription Lifecycle**:
   - Status transitions: `Draft` &rarr; `Quotation` &rarr; `Confirmed` &rarr; `Active` &rarr; `Closed`.
   - Automatic invoice generation upon transitioning to `Confirmed` or `Active`.
   - Multi-cycle billing options: `Monthly`, `Quarterly`, `Yearly`.

3. **Invoicing & Payments Engine**:
   - Automated subtotal, discount, and 8% tax calculations.
   - Invoices across `Paid`, `Unpaid`, `Overdue`, and `Draft` states.
   - One-click invoice settlement and payment transaction generation.
   - Printable tax invoice layout with company and customer addresses.

4. **Role-Based Access Control (RBAC)**:
   - **Admin**: Full catalog, subscription, discount, and financial oversight.
   - **Staff**: Operational queue, customer proposal conversions, and dunning follow-ups.
   - **Customer**: Dedicated self-service portal, active subscriptions view, invoice payments, and plan upgrades.

---

## 🛠 Tech Stack

- **Backend**: Python 3 (Flask), Werkzeug Security (`scrypt` password hashing)
- **Frontend**: HTML5, Vanilla CSS3 (Custom design system, No Bootstrap, No Tailwind), Vanilla JavaScript
- **Typography**: Google Font **Inter** & JetBrains Mono for codes
- **Database**: SQLite 3 with strict foreign key constraints & relational indices

---

## 📂 Strict Folder Structure

```
Subscription_Management_System/
│
├── backend/
│   ├── app.py                     # Main Flask application & factory
│   ├── config.py                  # Environment & path configurations
│   ├── __init__.py
│   ├── routes/
│   │   ├── auth.py                # Sign in, registration, session RBAC
│   │   ├── dashboard.py           # Admin, staff, customer dashboards
│   │   ├── subscriptions.py       # Subscription lifecycle operations
│   │   ├── products.py            # Software catalog management
│   │   ├── plans.py               # Tiered pricing plans
│   │   ├── quotations.py          # Enterprise contract quotes
│   │   ├── invoices.py            # Invoicing and payment settlement
│   │   ├── discounts.py           # Promo code & coupon engine
│   │   └── payments.py            # Settled transaction logs
│   ├── models/
│   │   ├── user.py                # Users & RBAC
│   │   ├── product.py             # Product catalog model
│   │   ├── plan.py                # Pricing plan model
│   │   ├── subscription.py        # Subscription contracts model
│   │   ├── invoice.py             # Invoices & receivables model
│   │   ├── payment.py             # Payment transactions model
│   │   └── discount.py            # Coupons & discount rules model
│   ├── services/
│   │   ├── billing.py             # Billing cycle & invoice generators
│   │   ├── tax.py                 # Sales tax / VAT calculators
│   │   └── discount.py            # Coupon validation & deductions
│   └── utils/
│       ├── validators.py          # Password strength & email validators
│       └── helpers.py             # DB connection pool, currency & date filters
│
├── frontend/
│   ├── templates/
│   │   ├── base.html              # Core SaaS shell with sidebar & topbar
│   │   ├── login.html             # Split-screen login with demo quick-pills
│   │   ├── register.html          # Registration with live password checklist
│   │   ├── admin_dashboard.html   # Executive revenue operations overview
│   │   ├── staff_dashboard.html   # Staff queue & quotation conversions
│   │   ├── customer_dashboard.html# Customer self-service portal
│   │   ├── subscriptions.html     # Subscriptions management & modal
│   │   ├── subscription_detail.html# Comprehensive contract breakdown
│   │   ├── plans.html             # Pricing tiers catalog
│   │   ├── products.html          # Product module definitions
│   │   ├── quotations.html        # Quotes & proposals view
│   │   ├── invoices.html          # Invoices ledger with filters
│   │   ├── invoice_detail.html    # Printable clean invoice receipt
│   │   ├── discounts.html         # Coupons & promotions manager
│   │   ├── payments.html          # Payment transactions log
│   │   ├── reports.html           # Revenue & cohort intelligence
│   │   └── 404.html               # Custom 404 error page
│   └── static/
│       ├── css/style.css          # Premium modern vanilla CSS design system
│       ├── js/script.js           # Client-side validation, filters, modals
│       └── images/                # SVG branding assets
│
├── database/
│   ├── schema.sql                 # Complete relational DDL schema
│   └── seed_data.sql              # Rich enterprise B2B seed data
│
├── requirements.txt
├── README.md
├── .env
└── .gitignore
```

---

## ⚡ Quick Start & Run Instructions

### 1. Prerequisites
Ensure Python 3.10+ is installed:
```bash
python --version
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
From the `Subscription_Management_System` folder:
```bash
python backend/app.py
```
Open your browser and navigate to:
👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

*Note: On first startup, SQLite will automatically create the database and seed the tables from `database/schema.sql` and `database/seed_data.sql`.*

---

## 🔑 Demo Login Accounts

| Role | Email | Password | Access Highlights |
| :--- | :--- | :--- | :--- |
| **Admin** | `admin@brightloop.io` | `Admin@1234#` | Full Executive revenue dashboard, create plans, provision subscriptions, manage coupons |
| **Staff** | `sarah.chen@brightloop.io` | `Staff@1234#` | Operational queue, quote approvals, overdue invoice monitoring |
| **Customer** | `david.miller@acmecorp.com` | `Customer@1234#` | Self-service portal, view active subscriptions, settle invoices |

*(Tip: On the Login screen, click any of the **Admin**, **Staff**, or **Customer** chips to autofill credentials instantly!)*

---

## 🔒 Enterprise Password Validation Rule
When registering an account via `register.html`, passwords must strictly fulfill:
1. Minimum **8 characters**
2. At least one **uppercase letter** (`A-Z`)
3. At least one **lowercase letter** (`a-z`)
4. At least one **special character** (`!@#$%^&*`, etc.)

The UI features a dynamic, real-time checklist that verifies each criterion as you type before enabling the submit button.
