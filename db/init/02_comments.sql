-- ============================================================
-- BUSINESS UNITS
-- ============================================================

COMMENT ON TABLE business_units IS
'High-level organizational units used for operational and financial reporting.';

COMMENT ON COLUMN business_units.region IS
'Geographical reporting region of the business unit.';


-- ============================================================
-- COST CENTERS
-- ============================================================

COMMENT ON TABLE cost_centers IS
'Departments or operational areas responsible for costs. Used as the main level for budget vs actual analysis.';

COMMENT ON COLUMN cost_centers.department IS
'Functional department responsible for the cost center, for example Logistics, IT, Finance or Facilities.';


-- ============================================================
-- SUPPLIERS
-- ============================================================

COMMENT ON TABLE suppliers IS
'Master data for external suppliers providing goods or services to the organization.';

COMMENT ON COLUMN suppliers.risk_level IS
'Business-defined supplier risk classification: low, medium or high. This is not an AI-generated risk score.';

COMMENT ON COLUMN suppliers.contract_end IS
'Contract expiration date. NULL means that no contract end date is currently recorded.';


-- ============================================================
-- PURCHASE ORDERS
-- ============================================================

COMMENT ON TABLE purchase_orders IS
'Purchase orders issued to suppliers. Purchase order value represents authorized spend and must not be treated as actual cash outflow.';

COMMENT ON COLUMN purchase_orders.approved_amount IS
'Maximum amount authorized by the purchase order. It is not necessarily the amount actually invoiced or paid.';

COMMENT ON COLUMN purchase_orders.status IS
'Purchase order lifecycle status. Typical values include draft, approved, closed and cancelled. Cancelled purchase orders should not be treated as active commitments.';


-- ============================================================
-- INVOICES
-- ============================================================

COMMENT ON TABLE invoices IS
'Supplier invoices received by the organization. Invoice amounts represent supplier charges, but not necessarily completed cash payments.';

COMMENT ON COLUMN invoices.amount IS
'Gross amount stated on the supplier invoice. Rejected invoices must not be included when calculating approved spend.';

COMMENT ON COLUMN invoices.status IS
'Invoice processing status: pending, approved, paid or rejected. Rejected invoices should be excluded from approved spend calculations.';

COMMENT ON COLUMN invoices.invoice_number IS
'Supplier-provided invoice identifier. Similar invoice numbers, amounts, suppliers and dates may indicate potential duplicate invoices but should not automatically be classified as duplicates.';


-- ============================================================
-- PAYMENTS
-- ============================================================

COMMENT ON TABLE payments IS
'Payments associated with supplier invoices. Use completed payments when calculating actual cash outflow.';

COMMENT ON COLUMN payments.amount IS
'Amount of the payment transaction. This can differ from the invoice amount in cases such as partial payments.';

COMMENT ON COLUMN payments.status IS
'Payment processing status. Only completed payments represent realized cash outflow.';


-- ============================================================
-- BUDGETS
-- ============================================================

COMMENT ON TABLE budgets IS
'Approved monthly budget by cost center. Used as the baseline for budget variance analysis.';

COMMENT ON COLUMN budgets.budget_month IS
'First calendar day of the month represented by the budget record.';

COMMENT ON COLUMN budgets.budget_amount IS
'Approved budget amount for the cost center and month.';


-- ============================================================
-- AUDIT
-- ============================================================

COMMENT ON TABLE audit_log IS
'Audit trail of MCP tool calls made through the analytics agent.';

COMMENT ON COLUMN audit_log.tool IS
'Name of the MCP tool that was called.';

COMMENT ON COLUMN audit_log.status IS
'Execution status of the tool call, for example success or error.';