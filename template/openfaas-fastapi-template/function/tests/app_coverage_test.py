"""Coverage test for auth module."""
import json

from fastapi.testclient import TestClient

from handler.server import api

client = TestClient(api.app)


def test_get_root() -> None:
    """Test root access."""
    response = client.get("/")
    assert response.status_code == 200


def test_docs() -> None:
    """Test docs generation."""
    response = client.get("/docs")
    assert response.status_code == 200


def test_handle() -> None:
    """Test invalid handle and authentication."""
    payload = json.dumps({"data": ""})
    response = client.post("/handle", data=payload)
    assert response.status_code == 200
