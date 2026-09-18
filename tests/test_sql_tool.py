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
    rows = run_sql("SELECT 1 AS value")

    assert rows[0]["value"] == 1