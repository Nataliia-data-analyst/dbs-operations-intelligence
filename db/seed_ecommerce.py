import os
import random
from datetime import datetime, timedelta, timezone
from decimal import Decimal

import psycopg
from dotenv import load_dotenv


load_dotenv()

DATABASE_URL = os.getenv("ADMIN_DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("ADMIN_DATABASE_URL is not configured")


random.seed(42)

START_DATE = datetime(2025, 1, 1, tzinfo=timezone.utc)
END_DATE = datetime(2026, 6, 30, 23, 59, tzinfo=timezone.utc)

COUNTRIES = [
    ("Poland", "Krakow"),
    ("Poland", "Warsaw"),
    ("Germany", "Berlin"),
    ("Germany", "Munich"),
    ("France", "Paris"),
    ("Netherlands", "Amsterdam"),
]

CHANNELS = [
    ("Google Ads", "Paid Search"),
    ("Google Organic", "Organic Search"),
    ("Meta Ads", "Paid Social"),
    ("Email", "CRM"),
    ("Direct", "Direct"),
    ("Affiliate", "Affiliate"),
]

PRODUCT_DEFINITIONS = [
    ("Electronics", "Headphones", 89, 35),
    ("Electronics", "Accessories", 39, 14),
    ("Home", "Kitchen", 79, 31),
    ("Home", "Lighting", 59, 22),
    ("Beauty", "Skincare", 49, 17),
    ("Beauty", "Hair Care", 35, 12),
    ("Sports", "Fitness", 69, 27),
    ("Sports", "Outdoor", 95, 39),
]

PAYMENT_METHODS = ["card", "paypal", "apple_pay"]

RETURN_REASONS = [
    "changed_mind",
    "wrong_size",
    "damaged",
    "not_as_expected",
    "defective",
]


def random_datetime(start, end):
    seconds = int((end - start).total_seconds())
    return start + timedelta(seconds=random.randint(0, seconds))


def money(value):
    return Decimal(str(round(value, 2)))


def main():
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:

            print("Cleaning e-commerce tables...")

            cur.execute("""
                TRUNCATE TABLE
                    returns,
                    customer_payments,
                    order_items,
                    orders,
                    events,
                    sessions,
                    marketing_spend,
                    campaigns,
                    marketing_channels,
                    products,
                    customers
                RESTART IDENTITY CASCADE
            """)

            # -------------------------------------------------
            # MARKETING CHANNELS
            # -------------------------------------------------

            channel_ids = {}

            for channel_name, channel_group in CHANNELS:
                cur.execute(
                    """
                    INSERT INTO marketing_channels (
                        channel_name,
                        channel_group
                    )
                    VALUES (%s, %s)
                    RETURNING channel_id
                    """,
                    (channel_name, channel_group),
                )

                channel_ids[channel_name] = cur.fetchone()[0]

            # -------------------------------------------------
            # CAMPAIGNS
            # -------------------------------------------------

            campaign_ids = []

            campaign_definitions = [
                ("Google Brand", "Google Ads"),
                ("Google Generic", "Google Ads"),
                ("Google Shopping", "Google Ads"),
                ("Meta Prospecting", "Meta Ads"),
                ("Meta Retargeting", "Meta Ads"),
                ("Affiliate Partners", "Affiliate"),
                ("Email Newsletter", "Email"),
                ("Email Retention", "Email"),
            ]

            for campaign_name, channel_name in campaign_definitions:
                cur.execute(
                    """
                    INSERT INTO campaigns (
                        channel_id,
                        campaign_name,
                        start_date,
                        end_date
                    )
                    VALUES (%s, %s, %s, %s)
                    RETURNING campaign_id
                    """,
                    (
                        channel_ids[channel_name],
                        campaign_name,
                        START_DATE.date(),
                        END_DATE.date(),
                    ),
                )

                campaign_ids.append(
                    (
                        cur.fetchone()[0],
                        campaign_name,
                        channel_name,
                    )
                )

            # -------------------------------------------------
            # PRODUCTS
            # -------------------------------------------------

            product_ids = []

            for i in range(1, 81):
                category, subcategory, base_price, base_cost = (
                    PRODUCT_DEFINITIONS[(i - 1) % len(PRODUCT_DEFINITIONS)]
                )

                price = money(base_price * random.uniform(0.85, 1.25))
                cost = money(base_cost * random.uniform(0.90, 1.15))

                sku = f"SKU-{i:04d}"
                product_name = f"{subcategory} Product {i:02d}"
                brand = f"Brand-{((i - 1) % 10) + 1}"

                cur.execute(
                    """
                    INSERT INTO products (
                        sku,
                        product_name,
                        category,
                        subcategory,
                        brand,
                        list_price,
                        unit_cost,
                        active
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, TRUE)
                    RETURNING product_id
                    """,
                    (
                        sku,
                        product_name,
                        category,
                        subcategory,
                        brand,
                        price,
                        cost,
                    ),
                )

                product_ids.append(
                    (
                        cur.fetchone()[0],
                        category,
                        price,
                        cost,
                    )
                )

            # -------------------------------------------------
            # CUSTOMERS
            # -------------------------------------------------

            customer_ids = []

            acquisition_choices = [
                "Google Ads",
                "Google Organic",
                "Meta Ads",
                "Email",
                "Direct",
                "Affiliate",
            ]

            segments = [
                "new",
                "regular",
                "high_value",
            ]

            for i in range(1, 12001):
                country, city = random.choice(COUNTRIES)

                created_at = random_datetime(
                    START_DATE - timedelta(days=365),
                    END_DATE,
                )

                acquisition_channel = random.choices(
                    acquisition_choices,
                    weights=[28, 25, 18, 8, 15, 6],
                )[0]

                segment = random.choices(
                    segments,
                    weights=[45, 45, 10],
                )[0]

                birth_year = random.randint(1965, 2005)

                cur.execute(
                    """
                    INSERT INTO customers (
                        customer_key,
                        country,
                        city,
                        acquisition_channel,
                        created_at,
                        birth_year,
                        customer_segment
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    RETURNING customer_id
                    """,
                    (
                        f"CUST-{i:06d}",
                        country,
                        city,
                        acquisition_channel,
                        created_at,
                        birth_year,
                        segment,
                    ),
                )

                customer_ids.append(cur.fetchone()[0])

            # -------------------------------------------------
            # MARKETING SPEND
            # -------------------------------------------------

            current_date = START_DATE.date()

            while current_date <= END_DATE.date():

                for campaign_id, campaign_name, channel_name in campaign_ids:

                    if channel_name == "Google Ads":
                        spend = random.uniform(350, 750)

                    elif channel_name == "Meta Ads":
                        spend = random.uniform(250, 600)

                    elif channel_name == "Affiliate":
                        spend = random.uniform(80, 180)

                    else:
                        spend = random.uniform(20, 80)

                    # ANOMALY #1
                    # Google Generic spend rises in May-June 2026
                    # without proportional business improvement.
                    if (
                        campaign_name == "Google Generic"
                        and current_date.year == 2026
                        and current_date.month in (5, 6)
                    ):
                        spend *= 1.65

                    impressions = int(spend * random.uniform(80, 160))
                    clicks = int(impressions * random.uniform(0.015, 0.045))

                    cur.execute(
                        """
                        INSERT INTO marketing_spend (
                            campaign_id,
                            spend_date,
                            spend_amount,
                            impressions,
                            clicks
                        )
                        VALUES (%s, %s, %s, %s, %s)
                        """,
                        (
                            campaign_id,
                            current_date,
                            money(spend),
                            impressions,
                            clicks,
                        ),
                    )

                current_date += timedelta(days=1)

            # -------------------------------------------------
            # SESSIONS + EVENTS + ORDERS
            # -------------------------------------------------

            total_sessions = 40000

            for session_number in range(1, total_sessions + 1):

                session_date = random_datetime(
                    START_DATE,
                    END_DATE,
                )

                known_customer = random.random() < 0.72

                customer_id = (
                    random.choice(customer_ids)
                    if known_customer
                    else None
                )

                channel_name = random.choices(
                    acquisition_choices,
                    weights=[28, 25, 18, 8, 15, 6],
                )[0]

                channel_id = channel_ids[channel_name]

                matching_campaigns = [
                    item
                    for item in campaign_ids
                    if item[2] == channel_name
                ]

                campaign_id = (
                    random.choice(matching_campaigns)[0]
                    if matching_campaigns
                    else None
                )

                device = random.choices(
                    ["mobile", "desktop", "tablet"],
                    weights=[62, 32, 6],
                )[0]

                if device == "mobile":
                    browser = random.choices(
                        ["Safari", "Chrome", "Firefox"],
                        weights=[45, 50, 5],
                    )[0]
                else:
                    browser = random.choices(
                        ["Chrome", "Safari", "Firefox", "Edge"],
                        weights=[55, 18, 12, 15],
                    )[0]

                operating_system = (
                    "iOS"
                    if device == "mobile" and browser == "Safari"
                    else random.choice(
                        ["Windows", "macOS", "Android", "iOS"]
                    )
                )

                country, _ = random.choice(COUNTRIES)

                landing_page = random.choice(
                    [
                        "/",
                        "/products",
                        "/sale",
                        "/electronics",
                        "/beauty",
                        "/sports",
                    ]
                )

                cur.execute(
                    """
                    INSERT INTO sessions (
                        customer_id,
                        session_started_at,
                        channel_id,
                        campaign_id,
                        device_category,
                        browser,
                        operating_system,
                        country,
                        landing_page
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING session_id
                    """,
                    (
                        customer_id,
                        session_date,
                        channel_id,
                        campaign_id,
                        device,
                        browser,
                        operating_system,
                        country,
                        landing_page,
                    ),
                )

                session_id = cur.fetchone()[0]

                # session_start
                cur.execute(
                    """
                    INSERT INTO events (
                        session_id,
                        customer_id,
                        event_timestamp,
                        event_name,
                        page_location
                    )
                    VALUES (%s, %s, %s, 'session_start', %s)
                    """,
                    (
                        session_id,
                        customer_id,
                        session_date,
                        landing_page,
                    ),
                )

                # Not every session reaches a product page.
                if random.random() >= 0.78:
                    continue

                product_id, category, price, cost = random.choice(
                    product_ids
                )

                view_time = session_date + timedelta(
                    seconds=random.randint(10, 120)
                )

                cur.execute(
                    """
                    INSERT INTO events (
                        session_id,
                        customer_id,
                        event_timestamp,
                        event_name,
                        product_id,
                        page_location,
                        event_value
                    )
                    VALUES (%s, %s, %s, 'view_item', %s, %s, %s)
                    """,
                    (
                        session_id,
                        customer_id,
                        view_time,
                        product_id,
                        "/product",
                        price,
                    ),
                )

                # Add to cart
                if random.random() >= 0.30:
                    continue

                cart_time = view_time + timedelta(
                    seconds=random.randint(20, 300)
                )

                cur.execute(
                    """
                    INSERT INTO events (
                        session_id,
                        customer_id,
                        event_timestamp,
                        event_name,
                        product_id,
                        page_location,
                        event_value
                    )
                    VALUES (%s, %s, %s, 'add_to_cart', %s, '/cart', %s)
                    """,
                    (
                        session_id,
                        customer_id,
                        cart_time,
                        product_id,
                        price,
                    ),
                )

                # Checkout
                if random.random() >= 0.62:
                    continue

                checkout_time = cart_time + timedelta(
                    seconds=random.randint(30, 300)
                )

                cur.execute(
                    """
                    INSERT INTO events (
                        session_id,
                        customer_id,
                        event_timestamp,
                        event_name,
                        product_id,
                        page_location,
                        event_value
                    )
                    VALUES (%s, %s, %s, 'begin_checkout', %s, '/checkout', %s)
                    """,
                    (
                        session_id,
                        customer_id,
                        checkout_time,
                        product_id,
                        price,
                    ),
                )

                payment_failure_probability = 0.04

                # ANOMALY #2
                # Mobile Safari payment failures spike in June 2026.
                if (
                    session_date.year == 2026
                    and session_date.month == 6
                    and device == "mobile"
                    and browser == "Safari"
                ):
                    payment_failure_probability = 0.22

                payment_time = checkout_time + timedelta(
                    seconds=random.randint(10, 180)
                )

                if random.random() < payment_failure_probability:

                    cur.execute(
                        """
                        INSERT INTO events (
                            session_id,
                            customer_id,
                            event_timestamp,
                            event_name,
                            product_id,
                            page_location,
                            event_value
                        )
                        VALUES (
                            %s, %s, %s, 'payment_failed',
                            %s, '/checkout/payment', %s
                        )
                        """,
                        (
                            session_id,
                            customer_id,
                            payment_time,
                            product_id,
                            price,
                        ),
                    )

                    continue

                cur.execute(
                    """
                    INSERT INTO events (
                        session_id,
                        customer_id,
                        event_timestamp,
                        event_name,
                        product_id,
                        page_location,
                        event_value
                    )
                    VALUES (
                        %s, %s, %s, 'add_payment_info',
                        %s, '/checkout/payment', %s
                    )
                    """,
                    (
                        session_id,
                        customer_id,
                        payment_time,
                        product_id,
                        price,
                    ),
                )

                # Additional normal checkout abandonment
                if random.random() >= 0.88:
                    continue

                quantity = random.choices(
                    [1, 2, 3],
                    weights=[82, 15, 3],
                )[0]

                discount_rate = 0

                if random.random() < 0.22:
                    discount_rate = random.choice(
                        [0.05, 0.10, 0.15]
                    )

                # ANOMALY #4
                # Heavy discounting in June 2026.
                if (
                    session_date.year == 2026
                    and session_date.month == 6
                    and random.random() < 0.55
                ):
                    discount_rate = random.choice(
                        [0.15, 0.20, 0.25]
                    )

                subtotal = float(price) * quantity
                discount = subtotal * discount_rate
                shipping = 0 if subtotal >= 80 else 5.99
                total = subtotal - discount + shipping

                order_time = payment_time + timedelta(
                    seconds=random.randint(5, 90)
                )

                cur.execute(
                    """
                    INSERT INTO orders (
                        customer_id,
                        session_id,
                        order_date,
                        status,
                        subtotal_amount,
                        discount_amount,
                        shipping_amount,
                        total_amount,
                        currency
                    )
                    VALUES (
                        %s, %s, %s, 'completed',
                        %s, %s, %s, %s, 'EUR'
                    )
                    RETURNING order_id
                    """,
                    (
                        customer_id,
                        session_id,
                        order_time,
                        money(subtotal),
                        money(discount),
                        money(shipping),
                        money(total),
                    ),
                )

                order_id = cur.fetchone()[0]

                cur.execute(
                    """
                    INSERT INTO order_items (
                        order_id,
                        product_id,
                        quantity,
                        unit_price,
                        discount_amount,
                        unit_cost
                    )
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING order_item_id
                    """,
                    (
                        order_id,
                        product_id,
                        quantity,
                        price,
                        money(discount),
                        cost,
                    ),
                )

                order_item_id = cur.fetchone()[0]

                payment_method = random.choice(PAYMENT_METHODS)

                cur.execute(
                    """
                    INSERT INTO customer_payments (
                        order_id,
                        payment_date,
                        payment_method,
                        amount,
                        status,
                        failure_reason
                    )
                    VALUES (%s, %s, %s, %s, 'completed', NULL)
                    """,
                    (
                        order_id,
                        order_time,
                        payment_method,
                        money(total),
                    ),
                )

                purchase_time = order_time + timedelta(seconds=1)

                cur.execute(
                    """
                    INSERT INTO events (
                        session_id,
                        customer_id,
                        event_timestamp,
                        event_name,
                        product_id,
                        page_location,
                        event_value
                    )
                    VALUES (
                        %s, %s, %s, 'purchase',
                        %s, '/order-confirmation', %s
                    )
                    """,
                    (
                        session_id,
                        customer_id,
                        purchase_time,
                        product_id,
                        money(total),
                    ),
                )

                # Normal return rate.
                return_probability = 0.07

                # ANOMALY #3
                # Beauty returns increase in Apr-Jun 2026.
                if (
                    category == "Beauty"
                    and session_date.year == 2026
                    and session_date.month in (4, 5, 6)
                ):
                    return_probability = 0.24

                if random.random() < return_probability:
                    return_quantity = 1

                    refund = (
                        float(price)
                        * return_quantity
                        * (1 - discount_rate)
                    )

                    return_date = (
                        order_time
                        + timedelta(days=random.randint(3, 25))
                    ).date()

                    cur.execute(
                        """
                        INSERT INTO returns (
                            order_item_id,
                            return_date,
                            quantity,
                            refund_amount,
                            return_reason
                        )
                        VALUES (%s, %s, %s, %s, %s)
                        """,
                        (
                            order_item_id,
                            return_date,
                            return_quantity,
                            money(refund),
                            random.choice(RETURN_REASONS),
                        ),
                    )

            conn.commit()

    print("E-commerce seed completed successfully.")


if __name__ == "__main__":
    main()