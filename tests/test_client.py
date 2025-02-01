import pytest
from a1base import A1BaseClient, AuthenticationError, ValidationError
from a1base.models import MessageRequest

def test_basic_initialization():
    """Test that client can be initialized with API credentials."""
    client = A1BaseClient(api_key="fake_key", api_secret="fake_secret")
    assert client is not None
    assert client.headers["x-api-key"] == "fake_key"
    assert client.headers["x-api-secret"] == "fake_secret"
    assert client.base_url == "https://api.a1base.com/v1"

def test_auth_failure():
    """Test that authentication errors are raised appropriately."""
    client = A1BaseClient(api_key="", api_secret="")
    message = MessageRequest(
        content="test message",
        from_="+1234567890",
        to="+0987654321",
        service="whatsapp"
    )
    with pytest.raises(AuthenticationError):
        client.send_individual_message("123", message)

def test_invalid_account_id():
    """Test that empty account_id raises ValueError."""
    client = A1BaseClient(api_key="fake_key", api_secret="fake_secret")
    message = MessageRequest(
        content="test message",
        from_="+1234567890",
        to="+0987654321",
        service="whatsapp"
    )
    with pytest.raises(ValueError, match="Account ID cannot be empty"):
        client.send_individual_message("", message)
