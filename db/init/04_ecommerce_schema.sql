CREATE TABLE customers (
    customer_id BIGSERIAL PRIMARY KEY,
    customer_key TEXT UNIQUE NOT NULL,

    country TEXT,
    city TEXT,

    acquisition_channel TEXT,

    created_at TIMESTAMPTZ NOT NULL,

    birth_year INTEGER,

    customer_segment TEXT
);

CREATE TABLE products (
    product_id BIGSERIAL PRIMARY KEY,
    sku TEXT UNIQUE NOT NULL,
    product_name TEXT NOT NULL,
    category TEXT NOT NULL,
    subcategory TEXT,
    brand TEXT,
    list_price NUMERIC(12,2) NOT NULL,
    unit_cost NUMERIC(12,2),
    active BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE marketing_channels (
    channel_id SERIAL PRIMARY KEY,

    channel_name TEXT UNIQUE NOT NULL,
    channel_group TEXT NOT NULL
);


CREATE TABLE campaigns (
    campaign_id BIGSERIAL PRIMARY KEY,

    channel_id INTEGER NOT NULL
        REFERENCES marketing_channels(channel_id),

    campaign_name TEXT NOT NULL,

    start_date DATE,
    end_date DATE
);


CREATE TABLE marketing_spend (
    marketing_spend_id BIGSERIAL PRIMARY KEY,

    campaign_id BIGINT NOT NULL
        REFERENCES campaigns(campaign_id),

    spend_date DATE NOT NULL,

    spend_amount NUMERIC(14,2) NOT NULL,

    impressions BIGINT,
    clicks BIGINT
);


CREATE TABLE sessions (
    session_id BIGSERIAL PRIMARY KEY,

    customer_id BIGINT
        REFERENCES customers(customer_id),

    session_started_at TIMESTAMPTZ NOT NULL,

    channel_id INTEGER
        REFERENCES marketing_channels(channel_id),

    campaign_id BIGINT
        REFERENCES campaigns(campaign_id),

    device_category TEXT,

    browser TEXT,
    operating_system TEXT,

    country TEXT,

    landing_page TEXT
);


CREATE TABLE events (
    event_id BIGSERIAL PRIMARY KEY,

    session_id BIGINT NOT NULL
        REFERENCES sessions(session_id),

    customer_id BIGINT
        REFERENCES customers(customer_id),

    event_timestamp TIMESTAMPTZ NOT NULL,

    event_name TEXT NOT NULL,

    product_id BIGINT
        REFERENCES products(product_id),

    page_location TEXT,

    event_value NUMERIC(14,2)
);


CREATE TABLE orders (
    order_id BIGSERIAL PRIMARY KEY,

    customer_id BIGINT
        REFERENCES customers(customer_id),

    session_id BIGINT
        REFERENCES sessions(session_id),

    order_date TIMESTAMPTZ NOT NULL,

    status TEXT NOT NULL,

    subtotal_amount NUMERIC(14,2) NOT NULL,

    discount_amount NUMERIC(14,2) NOT NULL DEFAULT 0,

    shipping_amount NUMERIC(14,2) NOT NULL DEFAULT 0,

    total_amount NUMERIC(14,2) NOT NULL,

    currency TEXT NOT NULL
);


CREATE TABLE order_items (
    order_item_id BIGSERIAL PRIMARY KEY,

    order_id BIGINT NOT NULL
        REFERENCES orders(order_id),

    product_id BIGINT NOT NULL
        REFERENCES products(product_id),

    quantity INTEGER NOT NULL,

    unit_price NUMERIC(12,2) NOT NULL,

    discount_amount NUMERIC(12,2) NOT NULL DEFAULT 0,

    unit_cost NUMERIC(12,2)
);


CREATE TABLE customer_payments (
    customer_payment_id BIGSERIAL PRIMARY KEY,

    order_id BIGINT NOT NULL
        REFERENCES orders(order_id),

    payment_date TIMESTAMPTZ,

    payment_method TEXT,

    amount NUMERIC(14,2) NOT NULL,

    status TEXT NOT NULL,

    failure_reason TEXT
);

CREATE TABLE returns (
    return_id BIGSERIAL PRIMARY KEY,

    order_item_id BIGINT NOT NULL
        REFERENCES order_items(order_item_id),

    return_date DATE NOT NULL,

    quantity INTEGER NOT NULL,

    refund_amount NUMERIC(14,2) NOT NULL,

    return_reason TEXT
);


