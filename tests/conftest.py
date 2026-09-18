import pytest

from server.db import open_pool, close_pool


@pytest.fixture(scope="session", autouse=True)
def database_pool():
    open_pool()

    yield

    close_pool()