import pytest

from server.db import open_pool, close_pool
from server.tools.sql import run_sql, validate_sql


def test_sql_validation():
    # Valid queries
    assert validate_sql(
        "SELECT * FROM suppliers"
    ) == "SELECT * FROM suppliers"

    assert validate_sql(
        """
        WITH supplier_totals AS (
            SELECT supplier_id, COUNT(*) AS invoice_count
            FROM invoices
            GROUP BY supplier_id
        )
        SELECT *
        FROM supplier_totals
        """
    )

    # Dangerous queries
    with pytest.raises(ValueError):
        validate_sql(
            "DELETE FROM invoices"
        )

    with pytest.raises(ValueError):
        validate_sql(
            "UPDATE suppliers SET risk_level = 'low'"
        )

    with pytest.raises(ValueError):
        validate_sql(
            "DROP TABLE suppliers"
        )

    # Multiple statements
    with pytest.raises(ValueError):
        validate_sql(
            "SELECT * FROM suppliers; DROP TABLE suppliers"
        )


def test_run_sql():
    open_pool()

    try:
        rows = run_sql(
            """
            SELECT
                supplier_id,
                supplier_name,
                category,
                risk_level
            FROM suppliers
            ORDER BY supplier_id
            """
        )

        print("\nSQL result:")

        for row in rows:
            print(row)

        assert len(rows) > 0
        assert "supplier_name" in rows[0]

    finally:
        close_pool()