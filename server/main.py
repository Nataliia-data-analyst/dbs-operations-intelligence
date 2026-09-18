import os

from dotenv import load_dotenv
from mcp.server.mcpserver import MCPServer

from server.db import open_pool, close_pool
from server.tools.schema import (
    list_tables as db_list_tables,
    describe_table as db_describe_table,
)
from server.tools.sql import run_sql as db_run_sql


load_dotenv()


mcp = MCPServer(
    "DBS Operations Intelligence",
    description="AI-powered operations analytics server",
    version="0.1.0",
)


@mcp.tool()
def list_tables() -> list[dict]:
    """
    List all business-data tables available to the analyst.

    Use this tool first when you need to understand what data
    is available in the database.
    """
    return db_list_tables()


@mcp.tool()
def describe_table(table_name: str) -> dict:
    """
    Describe a database table.

    Returns its business description and column structure.

    Use this tool before writing SQL against an unfamiliar table.
    """
    return db_describe_table(table_name)


@mcp.tool()
def run_sql(query: str) -> list[dict]:
    """
    Execute a read-only analytical SQL query.

    Use this tool to aggregate, filter, join, and analyze business data.
    Only SELECT and WITH queries are allowed.
    """
    return db_run_sql(query)


def main() -> None:
    transport = os.getenv("MCP_TRANSPORT", "stdio")

    open_pool()

    try:
        mcp.run(transport=transport)
    finally:
        close_pool()


if __name__ == "__main__":
    main()