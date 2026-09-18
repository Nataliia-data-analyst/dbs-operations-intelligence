CREATE TABLE business_units (
    business_unit_id SERIAL PRIMARY KEY,
    business_unit_name TEXT NOT NULL,
    region TEXT NOT NULL
);

CREATE TABLE cost_centers (
    cost_center_id SERIAL PRIMARY KEY,
    business_unit_id INTEGER NOT NULL
        REFERENCES business_units(business_unit_id),
    cost_center_name TEXT NOT NULL,
    department TEXT NOT NULL
);

CREATE TABLE suppliers (
    supplier_id SERIAL PRIMARY KEY,
    supplier_name TEXT NOT NULL,
    category TEXT NOT NULL,
    country TEXT NOT NULL,
    risk_level TEXT NOT NULL,
    contract_start DATE,
    contract_end DATE
);

CREATE TABLE purchase_orders (
    po_id SERIAL PRIMARY KEY,
    supplier_id INTEGER NOT NULL
        REFERENCES suppliers(supplier_id),
    cost_center_id INTEGER NOT NULL
        REFERENCES cost_centers(cost_center_id),
    po_date DATE NOT NULL,
    approved_amount NUMERIC(14,2) NOT NULL,
    currency TEXT NOT NULL,
    status TEXT NOT NULL
);

CREATE TABLE invoices (
    invoice_id SERIAL PRIMARY KEY,
    supplier_id INTEGER NOT NULL
        REFERENCES suppliers(supplier_id),
    po_id INTEGER REFERENCES purchase_orders(po_id),
    cost_center_id INTEGER NOT NULL
        REFERENCES cost_centers(cost_center_id),
    invoice_number TEXT NOT NULL,
    invoice_date DATE NOT NULL,
    amount NUMERIC(14,2) NOT NULL,
    currency TEXT NOT NULL,
    status TEXT NOT NULL,
    due_date DATE
);

CREATE TABLE payments (
    payment_id SERIAL PRIMARY KEY,
    invoice_id INTEGER NOT NULL
        REFERENCES invoices(invoice_id),
    payment_date DATE,
    amount NUMERIC(14,2) NOT NULL,
    status TEXT NOT NULL
);

CREATE TABLE budgets (
    budget_id SERIAL PRIMARY KEY,
    cost_center_id INTEGER NOT NULL
        REFERENCES cost_centers(cost_center_id),
    budget_month DATE NOT NULL,
    budget_amount NUMERIC(14,2) NOT NULL,
    currency TEXT NOT NULL
);

CREATE TABLE audit_log (
    audit_id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    tool TEXT NOT NULL,
    query TEXT,
    rows_returned INTEGER,
    duration_ms INTEGER,
    status TEXT NOT NULL,
    error TEXT
);