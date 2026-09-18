import re

from server.db import run_select


FORBIDDEN_SQL = re.compile(
    r"\b("
    r"INSERT|UPDATE|DELETE|DROP|ALTER|TRUNCATE|CREATE|"
    r"GRANT|REVOKE|COPY|CALL|DO|MERGE|VACUUM|ANALYZE"
    r")\b",
    re.IGNORECASE,
)


def validate_sql(query: str) -> str:
    """
    Validate SQL before sending it to PostgreSQL.

    Only SELECT queries and WITH ... SELECT queries are allowed.
    """

    query = query.strip()

    if not query:
        raise ValueError("SQL query cannot be empty")

    # Remove one optional trailing semicolon.
    query = query.rstrip(";").strip()

    # Do not allow multiple SQL statements.
    if ";" in query:
        raise ValueError("Multiple SQL statements are not allowed")

    if FORBIDDEN_SQL.search(query):
        raise ValueError("Only read-only SQL queries are allowed")

    first_word = query.split(None, 1)[0].upper()

    if first_word not in {"SELECT", "WITH"}:
        raise ValueError(
            "Query must start with SELECT or WITH"
        )

    return query


def run_sql(query: str) -> list[dict]:
    """
    Execute a validated read-only analytical SQL query.

    The result is limited by SQL_MAX_ROWS configured in the environment.
    """

    safe_query = validate_sql(query)

    return run_select(safe_query)