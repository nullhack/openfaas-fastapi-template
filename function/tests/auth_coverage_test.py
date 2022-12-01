"""Coverage test for auth module."""
from handler.server.auth import auth_bearer, auth_handler


def test_auth_handler_token_response_output() -> None:
    """Test if token response has the correct format."""
    token_response = auth_handler.token_response("test")
    assert token_response == {"access_token": "test"}


def test_encrypt_and_decrypt() -> None:
    """Test if encryption and decryption of token works."""
    encrypted_token_response = auth_handler.encrypt_jwe()
    decrypted_token = auth_handler.decrypt_jwe(
        encrypted_token_response["access_token"]
    )
    assert isinstance(decrypted_token, dict)


def test_bearer_verify_invalid_jwe() -> None:
    """Test invalid JWE token."""
    jwe_bearer = auth_bearer.JWEBearer()
    assert not jwe_bearer.verify_jwe("Invalid token!")
