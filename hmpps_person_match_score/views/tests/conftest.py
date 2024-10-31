import pytest


@pytest.fixture(scope="module")
def client(app):
    return app.test_client()
