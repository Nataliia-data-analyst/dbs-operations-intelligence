-- ============================================================
-- E-COMMERCE SEMANTIC LAYER
-- Business descriptions used by the AI analytics agent
-- ============================================================


-- CUSTOMERS

COMMENT ON TABLE customers IS
'Anonymized e-commerce customers. One row represents one known customer. 
Customers may have multiple sessions and orders. Anonymous website visitors 
may appear in sessions without a customer_id.';

COMMENT ON COLUMN customers.acquisition_channel IS
'Original acquisition channel associated with the customer. Do not use this 
instead of session-level channel attribution when analyzing individual orders.';

COMMENT ON COLUMN customers.customer_segment IS
'Business-defined customer segment used for customer and revenue analysis.';


-- PRODUCTS

COMMENT ON TABLE products IS
'Product catalog containing product hierarchy, current list price and current 
unit cost. Historical transaction prices and costs should be taken from 
order_items rather than this table.';

COMMENT ON COLUMN products.list_price IS
'Current standard product price before transaction-level discounts.';

COMMENT ON COLUMN products.unit_cost IS
'Current estimated product cost. For historical profitability analysis use 
order_items.unit_cost when available.';


-- MARKETING CHANNELS

COMMENT ON TABLE marketing_channels IS
'Reference table defining marketing and acquisition channels such as Paid Search, 
Organic Search, Paid Social, Email, Direct and Affiliate.';


-- CAMPAIGNS

COMMENT ON TABLE campaigns IS
'Marketing campaigns associated with acquisition channels. Campaign performance 
should be analyzed together with marketing_spend, sessions, orders and revenue.';


-- MARKETING SPEND

COMMENT ON TABLE marketing_spend IS
'Daily marketing campaign performance and advertising cost. Used to calculate 
metrics such as CPC, ROAS and acquisition efficiency.';

COMMENT ON COLUMN marketing_spend.spend_amount IS
'Advertising spend for the campaign and date. This is a marketing cost, not revenue.';


-- SESSIONS

COMMENT ON TABLE sessions IS
'Website or app sessions representing customer visits. A session may belong to 
a known customer or an anonymous visitor. Sessions contain acquisition, device 
and landing-page context.';

COMMENT ON COLUMN sessions.customer_id IS
'Known customer associated with the session. NULL means the visitor was anonymous 
or could not be identified.';

COMMENT ON COLUMN sessions.channel_id IS
'Session-level acquisition channel. Prefer this field for session and conversion 
analysis rather than customers.acquisition_channel.';

COMMENT ON COLUMN sessions.campaign_id IS
'Marketing campaign associated with the session when attribution is available.';


-- EVENTS

COMMENT ON TABLE events IS
'Behavioral e-commerce events generated during sessions. Used to reconstruct 
customer journeys and conversion funnels.';

COMMENT ON COLUMN events.event_name IS
'Event type such as session_start, view_item, add_to_cart, begin_checkout, 
add_payment_info, purchase or payment_failed.';

COMMENT ON COLUMN events.product_id IS
'Product associated with the event when relevant. May be NULL for events that 
are not product-specific.';


-- ORDERS

COMMENT ON TABLE orders IS
'Customer orders created through the e-commerce platform. One order may contain 
multiple order_items. Order revenue should not automatically be treated as 
profit because product cost, marketing cost, discounts, returns and other costs 
may apply.';

COMMENT ON COLUMN orders.subtotal_amount IS
'Order merchandise value before order-level discounts and shipping charges.';

COMMENT ON COLUMN orders.discount_amount IS
'Order-level discount amount.';

COMMENT ON COLUMN orders.total_amount IS
'Final recorded order amount. Check order status and returns before using it as 
realized net revenue.';

COMMENT ON COLUMN orders.status IS
'Order lifecycle status. Cancelled orders should normally be excluded from 
realized sales analysis.';


-- ORDER ITEMS

COMMENT ON TABLE order_items IS
'Individual products contained in customer orders. Used for product, category, 
basket and gross-margin analysis.';

COMMENT ON COLUMN order_items.unit_price IS
'Actual transaction-level unit selling price before item-level discount.';

COMMENT ON COLUMN order_items.unit_cost IS
'Historical product unit cost captured at the time of the transaction. Prefer 
this value for historical gross-margin calculations.';

COMMENT ON COLUMN order_items.discount_amount IS
'Discount applied to this order item.';


-- CUSTOMER PAYMENTS

COMMENT ON TABLE customer_payments IS
'Payments made by customers for e-commerce orders. This table is separate from 
supplier payments used in the procurement process. Failed payment attempts can 
be analyzed as part of checkout conversion and root-cause analysis.';

COMMENT ON COLUMN customer_payments.status IS
'Payment status such as completed, failed, pending or refunded. Only appropriate 
successful payment statuses should be treated as realized customer payment.';

COMMENT ON COLUMN customer_payments.failure_reason IS
'Recorded reason for a failed customer payment when available. Useful for payment 
failure and checkout conversion analysis.';


-- RETURNS

COMMENT ON TABLE returns IS
'Returned e-commerce order items and associated customer refunds. Returns should 
be considered when calculating net revenue and product profitability.';

COMMENT ON COLUMN returns.refund_amount IS
'Amount refunded to the customer for the returned item quantity.';

COMMENT ON COLUMN returns.return_reason IS
'Business-recorded reason for the return. Useful for product quality and customer 
experience analysis.';