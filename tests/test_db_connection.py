from server.db import run_select


def test_database_connection():
    result = run_select("SELECT 1 AS value")

    assert result[0]["value"] == 1