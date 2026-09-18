from server.tools.schema import list_tables, describe_table


def test_schema_tools():
    tables = list_tables()

    table_names = [row["table_name"] for row in tables]

    assert "suppliers" in table_names
    assert "invoices" in table_names
    assert "orders" in table_names
    assert "sessions" in table_names

    suppliers = describe_table("suppliers")

    assert suppliers["table"] == "suppliers"
    assert len(suppliers["columns"]) > 0