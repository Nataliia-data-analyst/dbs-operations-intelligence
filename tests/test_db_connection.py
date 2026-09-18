from server.db import open_pool, close_pool, run_select


def test_database_connection():
    open_pool()

    try:
        rows = run_select(
            """
            SELECT supplier_id, supplier_name, category
            FROM suppliers
            ORDER BY supplier_id
            """
        )

        assert len(rows) > 0

        print("\nSuppliers returned from PostgreSQL:")

        for row in rows:
            print(row)

    finally:
        close_pool()