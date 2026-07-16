from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


import pytest


@pytest.fixture
def test_client():
    return client