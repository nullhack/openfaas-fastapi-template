"""Coverage test for auth module."""
import json

import pytest
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


@pytest.mark.parametrize(
    ("user_id", "password", "status_code"),
    [
        ("user_id", "password", 200),
        ("", "", 403),
        ("", "password", 403),
        ("user_id", "", 403),
    ],
)
def test_auth(user_id: str, password: str, status_code: int) -> None:
    """Test valid access token.

    Arguments:
        user_id (str): User id used to login.
        password (str): Password used to login.
        status_code (int): Expected status code.
    """
    payload = json.dumps(
        {
            "user_id": user_id,
            "password": password,
        }
    )
    response = client.post("/auth", data=payload)
    assert response.status_code == status_code


@pytest.mark.parametrize(
    ("authorization", "status_code"),
    [
        ("Bearer eyJhbGciOiJB", 403),
        ("Bearer", 403),
        ("Not eyJhbGciOiJB", 403),
        ("", 403),
    ],
)
def test_handle(authorization: str, status_code: int) -> None:
    """Test handle and authentication.

    Arguments:
        authorization (str): Authorization string.
        status_code (int): Expected status code returned.
    """
    payload = json.dumps({"data": ""})
    h = {
        "Authorization": authorization,
        "accept": "application/json",
        "Content-Type": "application/json",
    }
    response = client.post("/handle", data=payload, headers=h)
    assert response.status_code == status_code


def test_valid_handle() -> None:
    """Test docs generation."""
    payload = json.dumps(
        {
            "user_id": "user_id",
            "password": "password",
        }
    )
    response = client.post("/auth", data=payload)
    assert response.status_code == 200
    assert response.__dict__ == "test"
