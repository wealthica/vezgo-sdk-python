"""
Tests for Vezgo API resources.
"""

import pytest
from vezgo import Vezgo, VezgoValidationError


class TestAccountsResource:
    """Tests for the Accounts resource."""

    @pytest.fixture
    def user(self):
        """Create a user client for testing."""
        client = Vezgo(client_id="test_client_id", secret="test_secret")
        user = client.login("test_user")
        yield user
        user.close()
        client.close()

    def test_get_one_without_account_id_raises_error(self, user):
        """Test that get_one without account_id raises an error."""
        with pytest.raises(VezgoValidationError) as exc_info:
            user.accounts.get_one("")
        assert "account ID" in str(exc_info.value)

    def test_sync_without_account_id_raises_error(self, user):
        """Test that sync without account_id raises an error."""
        with pytest.raises(VezgoValidationError) as exc_info:
            user.accounts.sync("")
        assert "account ID" in str(exc_info.value)

    def test_remove_without_account_id_raises_error(self, user):
        """Test that remove without account_id raises an error."""
        with pytest.raises(VezgoValidationError) as exc_info:
            user.accounts.remove("")
        assert "account ID" in str(exc_info.value)


class TestTransactionsResource:
    """Tests for the Transactions resource."""

    @pytest.fixture
    def user(self):
        """Create a user client for testing."""
        client = Vezgo(client_id="test_client_id", secret="test_secret")
        user = client.login("test_user")
        yield user
        user.close()
        client.close()

    def test_get_list_without_account_id_raises_error(self, user):
        """Test that get_list without account_id raises an error."""
        with pytest.raises(VezgoValidationError) as exc_info:
            user.transactions.get_list(account_id="")
        assert "account ID" in str(exc_info.value)

    def test_get_one_without_account_id_raises_error(self, user):
        """Test that get_one without account_id raises an error."""
        with pytest.raises(VezgoValidationError) as exc_info:
            user.transactions.get_one(account_id="", tx_id="tx123")
        assert "account ID" in str(exc_info.value)

    def test_get_one_without_tx_id_raises_error(self, user):
        """Test that get_one without tx_id raises an error."""
        with pytest.raises(VezgoValidationError) as exc_info:
            user.transactions.get_one(account_id="acc123", tx_id="")
        assert "transaction ID" in str(exc_info.value)


class TestHistoryResource:
    """Tests for the History resource."""

    @pytest.fixture
    def user(self):
        """Create a user client for testing."""
        client = Vezgo(client_id="test_client_id", secret="test_secret")
        user = client.login("test_user")
        yield user
        user.close()
        client.close()

    def test_get_list_without_account_id_raises_error(self, user):
        """Test that get_list without account_id raises an error."""
        with pytest.raises(VezgoValidationError) as exc_info:
            user.history.get_list(account_id="")
        assert "account ID" in str(exc_info.value)


class TestOrdersResource:
    """Tests for the Orders resource."""

    @pytest.fixture
    def user(self):
        """Create a user client for testing."""
        client = Vezgo(client_id="test_client_id", secret="test_secret")
        user = client.login("test_user")
        yield user
        user.close()
        client.close()

    def test_get_list_without_account_id_raises_error(self, user):
        """Test that get_list without account_id raises an error."""
        with pytest.raises(VezgoValidationError) as exc_info:
            user.orders.get_list(account_id="")
        assert "account ID" in str(exc_info.value)

    def test_get_one_without_account_id_raises_error(self, user):
        """Test that get_one without account_id raises an error."""
        with pytest.raises(VezgoValidationError) as exc_info:
            user.orders.get_one(account_id="", order_id="order123")
        assert "account ID" in str(exc_info.value)

    def test_get_one_without_order_id_raises_error(self, user):
        """Test that get_one without order_id raises an error."""
        with pytest.raises(VezgoValidationError) as exc_info:
            user.orders.get_one(account_id="acc123", order_id="")
        assert "order ID" in str(exc_info.value)


class TestProvidersResource:
    """Tests for the Providers resource."""

    @pytest.fixture
    def client(self):
        """Create a client for testing."""
        client = Vezgo(client_id="test_client_id", secret="test_secret")
        yield client
        client.close()

    def test_get_one_without_provider_id_raises_error(self, client):
        """Test that get_one without provider_id raises an error."""
        with pytest.raises(VezgoValidationError) as exc_info:
            client.providers.get_one("")
        assert "provider ID" in str(exc_info.value)

