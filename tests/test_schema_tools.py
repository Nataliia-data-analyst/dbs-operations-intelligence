from server.db import open_pool, close_pool
from server.tools.schema import list_tables, describe_table


def test_schema_tools():
    open_pool()

    try:
        # Test list_tables
        tables = list_tables()

        table_names = [
            row["table_name"]
            for row in tables
        ]

        print("\nAvailable tables:")
        print(table_names)

        assert "invoices" in table_names
        assert "suppliers" in table_names
        assert "budgets" in table_names

        # Test describe_table
        result = describe_table("invoices")

        print("\nInvoices metadata:")
        print(result)

        assert result["table"] == "invoices"
        assert len(result["columns"]) > 0
        assert result["description"] is not None

    finally:
        close_pool()