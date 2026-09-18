import os
from typing import Any

from dotenv import load_dotenv
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool


load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")
SQL_TIMEOUT_SECONDS = int(os.getenv("SQL_TIMEOUT_SECONDS", "15"))
SQL_MAX_ROWS = int(os.getenv("SQL_MAX_ROWS", "1000"))


if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not configured")


pool = ConnectionPool(
    conninfo=DATABASE_URL,
    min_size=1,
    max_size=5,
    kwargs={
        "row_factory": dict_row,
        "autocommit": False,
    },
    open=False,
)


def open_pool() -> None:
    """Open the PostgreSQL connection pool."""
    pool.open()
    pool.wait()


def close_pool() -> None:
    """Close all PostgreSQL connections."""
    pool.close()


def run_select(query: str, params: tuple[Any, ...] | None = None) -> list[dict]:
    """
    Execute a read-only SQL query and return rows as dictionaries.
    """

    query = query.strip()

    if not query:
        raise ValueError("SQL query cannot be empty")

    limited_query = f"""
        SELECT *
        FROM (
            {query.rstrip(';')}
        ) AS agent_query
        LIMIT {SQL_MAX_ROWS}
    """

    with pool.connection() as conn:
        with conn.transaction():
            conn.execute("SET TRANSACTION READ ONLY")
            conn.execute(
                f"SET LOCAL statement_timeout = '{SQL_TIMEOUT_SECONDS}s'"
            )

            with conn.cursor() as cur:
                cur.execute(limited_query, params)
                rows = cur.fetchall()

    return rows