"""
Tests for the Vezgo client.
"""

import pytest
from vezgo import Vezgo, VezgoValidationError


class TestVezgoClient:
    """Tests for the Vezgo client initialization."""

    def test_init_with_valid_credentials(self):
        """Test client initialization with valid credentials."""
        client = Vezgo(client_id="test_client_id", secret="test_secret")
        assert client.client_id == "test_client_id"
        assert client.secret == "test_secret"
        assert client.login_name is None
        client.close()

    def test_init_with_custom_urls(self):
        """Test client initialization with custom URLs."""
        client = Vezgo(
            client_id="test_client_id",
            secret="test_secret",
            base_url="https://custom-api.example.com",
            connect_url="https://custom-connect.example.com",
        )
        assert client.base_url == "https://custom-api.example.com"
        assert client.connect_url == "https://custom-connect.example.com"
        client.close()

    def test_init_without_client_id_raises_error(self):
        """Test that initialization without client_id raises an error."""
        with pytest.raises(VezgoValidationError) as exc_info:
            Vezgo(client_id="", secret="test_secret")
        assert "client_id" in str(exc_info.value)

    def test_init_without_secret_raises_error(self):
        """Test that initialization without secret raises an error."""
        with pytest.raises(VezgoValidationError) as exc_info:
            Vezgo(client_id="test_client_id", secret="")
        assert "secret" in str(exc_info.value)

    def test_init_with_login_name(self):
        """Test client initialization with login_name."""
        client = Vezgo(
            client_id="test_client_id",
            secret="test_secret",
            login_name="user_123",
        )
        assert client.login_name == "user_123"
        assert client.accounts is not None
        assert client.transactions is not None
        client.close()


class TestVezgoLogin:
    """Tests for the login functionality."""

    def test_login_returns_new_instance(self):
        """Test that login returns a new Vezgo instance."""
        client = Vezgo(client_id="test_client_id", secret="test_secret")
        user = client.login("user_123")
        
        assert user is not client
        assert user.login_name == "user_123"
        assert user.client_id == client.client_id
        assert user.secret == client.secret
        
        client.close()
        user.close()

    def test_login_without_login_name_raises_error(self):
        """Test that login without login_name raises an error."""
        client = Vezgo(client_id="test_client_id", secret="test_secret")
        
        with pytest.raises(VezgoValidationError) as exc_info:
            client.login("")
        assert "login_name" in str(exc_info.value)
        
        client.close()

    def test_login_creates_user_resources(self):
        """Test that login creates user-specific resources."""
        client = Vezgo(client_id="test_client_id", secret="test_secret")
        user = client.login("user_123")
        
        assert user.accounts is not None
        assert user.transactions is not None
        assert user.history is not None
        assert user.orders is not None
        
        client.close()
        user.close()


class TestVezgoContextManager:
    """Tests for context manager support."""

    def test_context_manager(self):
        """Test that the client can be used as a context manager."""
        with Vezgo(client_id="test_client_id", secret="test_secret") as client:
            assert client.client_id == "test_client_id"
        # Client should be closed after exiting context

