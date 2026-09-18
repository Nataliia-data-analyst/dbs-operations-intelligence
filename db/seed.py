import os
from datetime import date

import psycopg
from dotenv import load_dotenv


load_dotenv()

DATABASE_URL = os.getenv("ADMIN_DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("ADMIN_DATABASE_URL is not configured")


def seed():
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:

            # Clean existing demo data.
            cur.execute("""
                TRUNCATE
                    payments,
                    invoices,
                    purchase_orders,
                    budgets,
                    suppliers,
                    cost_centers,
                    business_units
                RESTART IDENTITY CASCADE
            """)

            # --------------------------------------------------
            # BUSINESS UNITS
            # --------------------------------------------------

            cur.executemany(
                """
                INSERT INTO business_units
                    (business_unit_name, region)
                VALUES (%s, %s)
                """,
                [
                    ("Supply Chain Operations", "Europe"),
                    ("Finance Operations", "Europe"),
                    ("Technology Services", "Global"),
                    ("People Services", "Europe"),
                    ("Facilities & Workplace", "Europe"),
                ],
            )

            # --------------------------------------------------
            # COST CENTERS
            # --------------------------------------------------

            cur.executemany(
                """
                INSERT INTO cost_centers
                    (
                        business_unit_id,
                        cost_center_name,
                        department
                    )
                VALUES (%s, %s, %s)
                """,
                [
                    (1, "Logistics Europe", "Logistics"),
                    (1, "Warehouse Operations", "Operations"),
                    (2, "Accounts Payable", "Finance"),
                    (2, "Financial Reporting", "Finance"),
                    (3, "Cloud Infrastructure", "IT"),
                    (3, "Business Applications", "IT"),
                    (4, "People Operations", "HR"),
                    (5, "Workplace Services", "Facilities"),
                ],
            )

            # --------------------------------------------------
            # SUPPLIERS
            # --------------------------------------------------

            cur.executemany(
                """
                INSERT INTO suppliers
                    (
                        supplier_name,
                        category,
                        country,
                        risk_level,
                        contract_start,
                        contract_end
                    )
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                [
                    (
                        "NorthStar Logistics",
                        "Logistics",
                        "Germany",
                        "medium",
                        date(2024, 1, 1),
                        None,
                    ),
                    (
                        "CloudSphere Technologies",
                        "Technology",
                        "Ireland",
                        "low",
                        date(2024, 3, 1),
                        None,
                    ),
                    (
                        "Vertex Consulting",
                        "Professional Services",
                        "United Kingdom",
                        "low",
                        date(2025, 1, 1),
                        None,
                    ),
                    (
                        "OfficeCore Solutions",
                        "Facilities",
                        "Poland",
                        "low",
                        date(2024, 6, 1),
                        None,
                    ),
                    (
                        "RapidFreight Europe",
                        "Logistics",
                        "Netherlands",
                        "high",
                        date(2025, 4, 1),
                        None,
                    ),
                ],
            )

        conn.commit()

    print("Demo data seeded successfully.")


if __name__ == "__main__":
    seed()