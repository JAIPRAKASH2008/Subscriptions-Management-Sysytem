-- ==============================================================================
-- Brightloop Subscription Management System - Seed Data
-- ==============================================================================

-- -----------------------------------------------------------------------------
-- 1. Users
-- Passwords:
-- Admin:    Admin@1234#
-- Staff:    Staff@1234#
-- Customer: Customer@1234#
-- -----------------------------------------------------------------------------
INSERT INTO users (id, username, email, password_hash, full_name, role, company_name, phone, address, is_active) VALUES
(1, 'admin', 'admin@brightloop.io', 'scrypt:32768:8:1$iv541fJFRi0js5np$f091bf3f5dba4318d1fe256790d2d64b732e56e07f0cd9c5da1c5a50f15990feb9a4cd45084e22c6c4e7509d5c94f24d02cbb49f5184eb2e26eb315521aa4f09', 'Alexandra Vance', 'Admin', 'Brightloop Technologies Inc.', '+1 (555) 019-2834', '548 Market St, Suite 34000, San Francisco, CA', 1),
(2, 'sarah.chen', 'sarah.chen@brightloop.io', 'scrypt:32768:8:1$sEwzv7t3dwVxwaSY$49f74bd795f715d7ed0cae616bec03f278cb8fecfc7754dabbd548dd0a21cfd76887f19661f2a16763418052b1064a7221a5662424d3c080c71b52a1823cb6ff', 'Sarah Chen', 'Staff', 'Brightloop Billing Ops', '+1 (555) 014-9921', '548 Market St, Suite 34000, San Francisco, CA', 1),
(3, 'david.miller', 'david.miller@acmecorp.com', 'scrypt:32768:8:1$kCSzaKWoIF4d5b3s$a92549a9df644541a56308482c173b0e78433cf476b5bd92498c0e06f25155b320b2e656501a85655e4eacc6c365f62fce419f083a5a247c3d6a633513912b62', 'David Miller', 'Customer', 'Acme Corporation', '+1 (555) 234-5678', '100 Enterprise Way, Austin, TX 78701', 1),
(4, 'elena.rostova', 'elena.rostova@novastack.ai', 'scrypt:32768:8:1$kCSzaKWoIF4d5b3s$a92549a9df644541a56308482c173b0e78433cf476b5bd92498c0e06f25155b320b2e656501a85655e4eacc6c365f62fce419f083a5a247c3d6a633513912b62', 'Elena Rostova', 'Customer', 'NovaStack AI Labs', '+1 (555) 872-9102', '450 Silicon Ave, Seattle, WA 98101', 1),
(5, 'marcus.wright', 'marcus.wright@zenithfintech.com', 'scrypt:32768:8:1$kCSzaKWoIF4d5b3s$a92549a9df644541a56308482c173b0e78433cf476b5bd92498c0e06f25155b320b2e656501a85655e4eacc6c365f62fce419f083a5a247c3d6a633513912b62', 'Marcus Wright', 'Customer', 'Zenith Global FinTech', '+44 20 7946 0912', '120 Bishopsgate, London, EC2M 4NR, UK', 1),
(6, 'priya.patel', 'priya.patel@quantumaerospace.com', 'scrypt:32768:8:1$kCSzaKWoIF4d5b3s$a92549a9df644541a56308482c173b0e78433cf476b5bd92498c0e06f25155b320b2e656501a85655e4eacc6c365f62fce419f083a5a247c3d6a633513912b62', 'Priya Patel', 'Customer', 'Quantum Aerospace Inc.', '+91 80 4123 4567', '7th Floor, UB City, Vittal Mallya Rd, Bengaluru, KA', 1);

-- -----------------------------------------------------------------------------
-- 2. Products
-- -----------------------------------------------------------------------------
INSERT INTO products (id, name, code, description, category, icon, is_active) VALUES
(1, 'Brightloop Sentinel', 'PROD-SENTINEL', 'Autonomous multi-cloud security posture monitoring, drift remediation, and compliance auditor.', 'Security & Compliance', 'shield', 1),
(2, 'RevenueMesh Billing', 'PROD-REVMESH', 'Usage-based metering, complex recurring subscription logic, dunning, and invoice orchestration.', 'Financial Infrastructure', 'credit-card', 1),
(3, 'OmniFlow AI Support', 'PROD-OMNIFLOW', 'Autonomous B2B customer success copilot with enterprise context retrieval and real-time triage.', 'AI & Automation', 'cpu', 1),
(4, 'DevShield API Gateway', 'PROD-DEVSHIELD', 'Zero-trust API authorization mesh with distributed rate limiting and cryptographic audit logging.', 'Developer Tools', 'terminal', 1);

-- -----------------------------------------------------------------------------
-- 3. Plans
-- -----------------------------------------------------------------------------
INSERT INTO plans (id, product_id, name, code, billing_interval, price, currency, trial_days, features, is_popular, is_active) VALUES
-- Product 1: Brightloop Sentinel
(1, 1, 'Starter Sentinel', 'PLAN-SENT-MO-START', 'Monthly', 79.00, 'USD', 14, 'Up to 5 Cloud Accounts,Daily Compliance Scans,Standard Slack Alerts,Community Support', 0, 1),
(2, 1, 'Sentinel Growth', 'PLAN-SENT-MO-GROWTH', 'Monthly', 249.00, 'USD', 14, 'Up to 25 Cloud Accounts,Real-time Drift Detection,SOC2/ISO27001 Mapping,Priority Email & Chat', 1, 1),
(3, 1, 'Sentinel Enterprise', 'PLAN-SENT-YR-ENT', 'Yearly', 2490.00, 'USD', 30, 'Unlimited Cloud Accounts,Custom Detections Engine,Dedicated Solution Engineer,99.99% SLA Guarantee', 0, 1),

-- Product 2: RevenueMesh Billing
(4, 2, 'Mesh Standard', 'PLAN-REV-MO-STD', 'Monthly', 149.00, 'USD', 14, 'Up to $50k MRR Processed,Multi-currency Support,Automated Invoices,Standard Webhooks', 0, 1),
(5, 2, 'Mesh Scale Pro', 'PLAN-REV-MO-PRO', 'Monthly', 499.00, 'USD', 14, 'Up to $250k MRR Processed,Usage-Based Metering,Custom Dunning Sequences,TaxJar & Avalara Sync', 1, 1),
(6, 2, 'Mesh Global Enterprise', 'PLAN-REV-YR-ENT', 'Yearly', 4990.00, 'USD', 30, 'Unlimited MRR Volume,Multi-entity Billing,Custom ERP & NetSuite Connector,Dedicated Account Manager', 0, 1),

-- Product 3: OmniFlow AI Support
(7, 3, 'OmniFlow Launch', 'PLAN-OMNI-MO-LAUNCH', 'Monthly', 99.00, 'USD', 14, '1,000 AI Conversations/mo,Zendesk & Intercom Integration,Basic Hallucination Guardrails', 0, 1),
(8, 3, 'OmniFlow Pro', 'PLAN-OMNI-MO-PRO', 'Monthly', 349.00, 'USD', 14, '10,000 AI Conversations/mo,Custom Model Fine-tuning,CRM Bi-directional Sync,Multilingual Support', 1, 1),

-- Product 4: DevShield API Gateway
(9, 4, 'DevShield Edge', 'PLAN-SHIELD-MO-EDGE', 'Monthly', 129.00, 'USD', 14, '10M API Requests/mo,mTLS Authorization,Global Edge Caching,Distributed Rate Limiting', 0, 1),
(10, 4, 'DevShield Sovereign', 'PLAN-SHIELD-YR-SOV', 'Yearly', 1290.00, 'USD', 30, '100M API Requests/mo,Self-Hosted Hybrid Deployments,Hardware Key Modules,24/7 Phone Support', 0, 1);

-- -----------------------------------------------------------------------------
-- 4. Discounts
-- -----------------------------------------------------------------------------
INSERT INTO discounts (id, code, discount_type, value, description, valid_from, valid_until, usage_limit, times_used, is_active) VALUES
(1, 'WELCOME20', 'percentage', 20.00, '20% discount on initial billing cycle for new customers', '2026-01-01', '2026-12-31', 500, 42, 1),
(2, 'GROWTH100', 'fixed', 100.00, '$100 flat credit for fast-growing B2B accounts', '2026-01-01', '2026-12-31', 200, 18, 1),
(3, 'ANNUALSAVE15', 'percentage', 15.00, 'Additional 15% off on annual enterprise plans', '2026-01-01', '2026-12-31', 100, 7, 1);

-- -----------------------------------------------------------------------------
-- 5. Subscriptions
-- Statuses: Draft, Quotation, Confirmed, Active, Closed
-- -----------------------------------------------------------------------------
INSERT INTO subscriptions (id, subscription_number, customer_id, plan_id, discount_id, status, billing_cycle, start_date, end_date, next_billing_date, subtotal, discount_amount, tax_amount, total_amount, currency, auto_renew, notes) VALUES
-- Active subscription for Acme Corp (Sentinel Growth)
(1, 'SUB-2026-0010', 3, 2, 1, 'Active', 'Monthly', '2026-01-15', '2027-01-14', '2026-11-15', 249.00, 49.80, 15.94, 215.14, 'USD', 1, 'Acme tier upgraded from Starter with WELCOME20 promo.'),

-- Active subscription for NovaStack AI (Mesh Scale Pro)
(2, 'SUB-2026-0011', 4, 5, NULL, 'Active', 'Monthly', '2026-02-01', '2027-01-31', '2026-11-01', 499.00, 0.00, 39.92, 538.92, 'USD', 1, 'High API usage volume anticipated in Q4.'),

-- Active annual subscription for Zenith FinTech (Sentinel Enterprise)
(3, 'SUB-2026-0012', 5, 3, 3, 'Active', 'Yearly', '2026-03-01', '2027-02-28', '2027-03-01', 2490.00, 373.50, 169.32, 2285.82, 'USD', 1, 'Enterprise annual contract with dedicated solution architect.'),

-- Confirmed subscription for Quantum Aerospace (DevShield Sovereign)
(4, 'SUB-2026-0013', 6, 10, NULL, 'Confirmed', 'Yearly', '2026-11-05', '2027-11-04', '2026-11-05', 1290.00, 0.00, 103.20, 1393.20, 'USD', 1, 'Purchase order PO-QA-901 received and confirmed by billing ops.'),

-- Confirmed subscription for Acme Corp (OmniFlow Pro)
(5, 'SUB-2026-0014', 3, 8, 2, 'Confirmed', 'Monthly', '2026-11-10', '2027-11-09', '2026-11-10', 349.00, 100.00, 19.92, 268.92, 'USD', 1, 'Add-on module for customer service operations.'),

-- Quotation state subscription for NovaStack AI (Sentinel Enterprise)
(6, 'SUB-2026-0015', 4, 3, 3, 'Quotation', 'Yearly', '2026-11-15', '2027-11-14', '2026-11-15', 2490.00, 373.50, 169.32, 2285.82, 'USD', 0, 'Quotation provided with 15% annual enterprise discount.'),

-- Draft subscription for Zenith FinTech (DevShield Edge)
(7, 'SUB-2026-0016', 5, 9, NULL, 'Draft', 'Monthly', '2026-11-20', '2027-11-19', '2026-11-20', 129.00, 0.00, 10.32, 139.32, 'USD', 1, 'Draft proposal awaiting network team approval.'),

-- Closed subscription (Historical churn / expired)
(8, 'SUB-2025-0004', 6, 1, NULL, 'Closed', 'Monthly', '2025-05-01', '2026-05-01', NULL, 79.00, 0.00, 6.32, 85.32, 'USD', 0, 'Customer completed migration to Sovereign dedicated tier.');

-- -----------------------------------------------------------------------------
-- 6. Quotations
-- -----------------------------------------------------------------------------
INSERT INTO quotations (id, quotation_number, customer_id, plan_id, subscription_id, proposed_amount, discount_amount, tax_amount, total_amount, currency, valid_until, status, terms) VALUES
(1, 'QUO-2026-0101', 4, 3, 6, 2490.00, 373.50, 169.32, 2285.82, 'USD', '2026-11-30', 'Sent', 'Annual agreement including 30 days money-back guarantee, Net 30 payment terms.'),
(2, 'QUO-2026-0102', 6, 10, 4, 1290.00, 0.00, 103.20, 1393.20, 'USD', '2026-11-15', 'Accepted', 'Sovereign cluster deployment on AWS GovCloud with ITAR compliance terms.'),
(3, 'QUO-2026-0103', 3, 6, NULL, 4990.00, 748.50, 339.32, 4580.82, 'USD', '2026-12-15', 'Draft', 'High-volume Mesh billing enterprise contract proposal with NetSuite integration.');

-- -----------------------------------------------------------------------------
-- 7. Invoices
-- Statuses: Draft, Unpaid, Paid, Overdue, Cancelled
-- -----------------------------------------------------------------------------
INSERT INTO invoices (id, invoice_number, subscription_id, customer_id, issue_date, due_date, subtotal, tax_amount, discount_amount, total_due, amount_paid, currency, status, pdf_path) VALUES
-- Paid invoice (Acme Corp October)
(1, 'INV-2026-0891', 1, 3, '2026-10-15', '2026-10-25', 249.00, 15.94, 49.80, 215.14, 215.14, 'USD', 'Paid', '/static/invoices/INV-2026-0891.pdf'),

-- Paid invoice (NovaStack October)
(2, 'INV-2026-0892', 2, 4, '2026-10-01', '2026-10-11', 499.00, 39.92, 0.00, 538.92, 538.92, 'USD', 'Paid', '/static/invoices/INV-2026-0892.pdf'),

-- Unpaid invoice (Acme Corp Upcoming November)
(3, 'INV-2026-0920', 1, 3, '2026-10-30', '2026-11-10', 249.00, 15.94, 49.80, 215.14, 0.00, 'USD', 'Unpaid', '/static/invoices/INV-2026-0920.pdf'),

-- Overdue invoice (NovaStack September auxiliary adjustments)
(4, 'INV-2026-0780', 2, 4, '2026-09-01', '2026-09-15', 499.00, 39.92, 0.00, 538.92, 0.00, 'USD', 'Overdue', '/static/invoices/INV-2026-0780.pdf'),

-- Paid Annual Invoice (Zenith FinTech Sentinel)
(5, 'INV-2026-0410', 3, 5, '2026-03-01', '2026-03-31', 2490.00, 169.32, 373.50, 2285.82, 2285.82, 'USD', 'Paid', '/static/invoices/INV-2026-0410.pdf'),

-- Confirmed/Unpaid Invoice for Quantum Aerospace
(6, 'INV-2026-0935', 4, 6, '2026-10-28', '2026-11-28', 1290.00, 103.20, 0.00, 1393.20, 0.00, 'USD', 'Unpaid', '/static/invoices/INV-2026-0935.pdf'),

-- Draft Invoice for upcoming cycle
(7, 'INV-2026-0950', 5, 3, '2026-10-31', '2026-11-15', 349.00, 19.92, 100.00, 268.92, 0.00, 'USD', 'Draft', NULL);

-- -----------------------------------------------------------------------------
-- 8. Payments
-- -----------------------------------------------------------------------------
INSERT INTO payments (id, payment_reference, invoice_id, amount, currency, payment_method, transaction_status, gateway_transaction_id, payment_date, notes) VALUES
(1, 'PAY-TXN-2026-0091', 1, 215.14, 'USD', 'Credit Card', 'Completed', 'ch_3N89z02eZvKYlo2C1g', '2026-10-16 14:22:10', 'Stripe automated card charge (Mastercard ending in 4242)'),
(2, 'PAY-TXN-2026-0092', 2, 538.92, 'USD', 'Bank Transfer', 'Completed', 'ach_wire_992140', '2026-10-03 09:15:44', 'Fedwire clearing confirmed via Silicon Valley Bank account'),
(3, 'PAY-TXN-2026-0041', 5, 2285.82, 'USD', 'Stripe', 'Completed', 'ch_3M47b11eBvKYlo1X9k', '2026-03-05 11:40:02', 'Annual enterprise contract payment processed successfully'),
(4, 'PAY-TXN-2026-0099', 4, 538.92, 'USD', 'Credit Card', 'Failed', 'ch_3P11x90eZvKYlo3W2r', '2026-09-16 04:02:19', 'Card expired or insufficient credit limit, dunning notice dispatched');

