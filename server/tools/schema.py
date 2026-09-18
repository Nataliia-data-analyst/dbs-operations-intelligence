from server.db import run_select


def list_tables() -> list[dict]:
    """
    Return all user tables available in the public schema.
    """

    query = """
        SELECT
            table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
          AND table_type = 'BASE TABLE'
        ORDER BY table_name
    """

    return run_select(query)


def describe_table(table_name: str) -> dict:
    """
    Return columns and business description for a table.
    """

    columns_query = """
        SELECT
            column_name,
            data_type,
            is_nullable
        FROM information_schema.columns
        WHERE table_schema = 'public'
          AND table_name = %s
        ORDER BY ordinal_position
    """

    description_query = """
        SELECT obj_description(
            to_regclass(%s),
            'pg_class'
        ) AS description
    """

    columns = run_select(columns_query, (table_name,))
    description_rows = run_select(
        description_query,
        (f"public.{table_name}",)
    )

    description = None

    if description_rows:
        description = description_rows[0]["description"]

    return {
        "table": table_name,
        "description": description,
        "columns": columns,
    }