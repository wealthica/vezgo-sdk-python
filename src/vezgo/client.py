"""
Vezgo SDK Client.
"""

import time
from typing import Any, Dict, List, Optional

import httpx
import jwt

from vezgo.constants import API_URL, CONNECT_URL, DEFAULT_TOKEN_MINIMUM_LIFETIME
from vezgo.exceptions import (
    VezgoAPIError,
    VezgoAuthenticationError,
    VezgoError,
    VezgoNotFoundError,
    VezgoRateLimitError,
    VezgoValidationError,
)
from vezgo.resources.accounts import Accounts
from vezgo.resources.history import History
from vezgo.resources.orders import Orders
from vezgo.resources.providers import Providers
from vezgo.resources.teams import Teams
from vezgo.resources.transactions import Transactions


class Vezgo:
    """
    Vezgo API Client.

    This is the main entry point for interacting with the Vezgo API.
    Initialize with your client_id and secret, then use the login() method
    to create user-specific instances for accessing user data.

    Example:
        ```python
        from vezgo import Vezgo

        # Initialize the client
        vezgo = Vezgo(client_id="your_client_id", secret="your_secret")

        # Get list of providers (no user login required)
        providers = vezgo.providers.get_list()

        # Login as a specific user
        user = vezgo.login("user_123")

        # Get user's accounts
        accounts = user.accounts.get_list()
        ```
    """

    def __init__(
        self,
        client_id: str,
        secret: str,
        base_url: Optional[str] = None,
        connect_url: Optional[str] = None,
        login_name: Optional[str] = None,
        timeout: float = 30.0,
    ):
        """
        Initialize the Vezgo client.

        Args:
            client_id: Your Vezgo client ID.
            secret: Your Vezgo client secret.
            base_url: Optional custom base URL for the API.
            connect_url: Optional custom URL for the Connect widget.
            login_name: Optional user login name for user-specific operations.
            timeout: Request timeout in seconds (default: 30.0).

        Raises:
            VezgoValidationError: If client_id or secret is invalid.
        """
        if not client_id or not isinstance(client_id, str):
            raise VezgoValidationError("Please provide a valid Vezgo client_id.")
        if not secret or not isinstance(secret, str):
            raise VezgoValidationError("Please provide a valid Vezgo secret.")

        self.client_id = client_id
        self.secret = secret
        self.base_url = base_url or API_URL
        self.connect_url = connect_url or CONNECT_URL
        self.login_name = login_name
        self.timeout = timeout

        # Token cache
        self._token: Optional[str] = None
        self._token_payload: Optional[Dict[str, Any]] = None

        # HTTP client for unauthenticated requests (providers, teams)
        self._client = httpx.Client(
            base_url=self.base_url,
            timeout=timeout,
            headers={"Content-Type": "application/json"},
        )

        # HTTP client for authenticated user requests
        self._user_client: Optional[httpx.Client] = None

        # Initialize resources
        self.providers = Providers(self)
        self.teams = Teams(self)

        # User-specific resources (only available after login)
        self.accounts: Optional[Accounts] = None
        self.transactions: Optional[Transactions] = None
        self.history: Optional[History] = None
        self.orders: Optional[Orders] = None

        # If login_name provided, initialize as logged-in user
        if login_name:
            self._init_user_resources()

    def _init_user_resources(self) -> None:
        """Initialize user-specific resources."""
        self.accounts = Accounts(self)
        self.transactions = Transactions(self)
        self.history = History(self)
        self.orders = Orders(self)

    def login(self, login_name: str) -> "Vezgo":
        """
        Create a new Vezgo instance logged in as a specific user.

        This method returns a new Vezgo instance that can access user-specific
        resources like accounts, transactions, and history.

        Args:
            login_name: The unique identifier for the user in your system.

        Returns:
            A new Vezgo instance configured for the specified user.

        Raises:
            VezgoValidationError: If login_name is invalid.

        Example:
            ```python
            vezgo = Vezgo(client_id="...", secret="...")
            user = vezgo.login("user_123")
            accounts = user.accounts.get_list()
            ```
        """
        if not login_name or not isinstance(login_name, str):
            raise VezgoValidationError("Please provide a valid login_name.")

        return Vezgo(
            client_id=self.client_id,
            secret=self.secret,
            base_url=self.base_url,
            connect_url=self.connect_url,
            login_name=login_name,
            timeout=self.timeout,
        )

    def get_token(self, minimum_lifetime: int = DEFAULT_TOKEN_MINIMUM_LIFETIME) -> str:
        """
        Get an authentication token, fetching a new one if necessary.

        The token is cached and reused until it has less than the specified
        minimum lifetime remaining.

        Args:
            minimum_lifetime: Minimum remaining lifetime in seconds (default: 10).

        Returns:
            A valid authentication token.

        Raises:
            VezgoAuthenticationError: If token fetch fails.
        """
        current_time = time.time()

        # Check if we have a valid cached token
        if self._token and self._token_payload:
            exp = self._token_payload.get("exp", 0)
            if current_time < (exp - minimum_lifetime):
                return self._token

        # Fetch a new token
        return self.fetch_token()

    def fetch_token(self) -> str:
        """
        Fetch a new authentication token from the API.

        Returns:
            A new authentication token.

        Raises:
            VezgoAuthenticationError: If token fetch fails.
        """
        if not self.login_name:
            raise VezgoValidationError(
                "Cannot fetch token without a login_name. Use login() method first."
            )

        try:
            response = self._client.post(
                "/auth/token",
                json={"clientId": self.client_id, "secret": self.secret},
                headers={"loginName": self.login_name},
            )
            self._handle_response_errors(response)

            data = response.json()
            token = data.get("token")

            if not token:
                raise VezgoAuthenticationError("No token received from API")

            # Decode and cache the token
            self._token = token
            self._token_payload = jwt.decode(token, options={"verify_signature": False})

            return self._token

        except httpx.HTTPError as e:
            raise VezgoAuthenticationError(f"Failed to fetch token: {str(e)}")

    def get_team(self) -> Dict[str, Any]:
        """
        Get information about your Vezgo team/application.

        Returns:
            Team information including name, features, and settings.

        Example:
            ```python
            team = vezgo.get_team()
            print(team["name"])
            ```
        """
        return self.teams.info()

    def _get_auth_headers(self) -> Dict[str, str]:
        """Get headers with authentication token."""
        return {"Authorization": f"Bearer {self.get_token()}"}

    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        authenticated: bool = False,
    ) -> Any:
        """
        Make an API request.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE).
            endpoint: API endpoint path.
            params: Query parameters.
            json: JSON body data.
            authenticated: Whether to include authentication header.

        Returns:
            Response data.

        Raises:
            VezgoAPIError: If the API returns an error.
        """
        headers = {}
        if authenticated:
            headers.update(self._get_auth_headers())

        try:
            response = self._client.request(
                method=method,
                url=endpoint,
                params=params,
                json=json,
                headers=headers,
            )
            self._handle_response_errors(response)

            # Return None for 204 No Content
            if response.status_code == 204:
                return None

            return response.json()

        except httpx.HTTPError as e:
            raise VezgoAPIError(f"Request failed: {str(e)}")

    def _handle_response_errors(self, response: httpx.Response) -> None:
        """
        Handle API response errors.

        Args:
            response: The HTTP response object.

        Raises:
            VezgoAuthenticationError: For 401 errors.
            VezgoNotFoundError: For 404 errors.
            VezgoRateLimitError: For 429 errors.
            VezgoAPIError: For other error status codes.
        """
        if response.is_success:
            return

        status_code = response.status_code
        try:
            error_data = response.json()
            message = error_data.get("message", error_data.get("error", response.text))
        except Exception:
            error_data = {}
            message = response.text or f"HTTP {status_code}"

        if status_code == 401:
            raise VezgoAuthenticationError(message, status_code, error_data)
        elif status_code == 404:
            raise VezgoNotFoundError(message, status_code, error_data)
        elif status_code == 429:
            raise VezgoRateLimitError(message, status_code, error_data)
        elif status_code == 400:
            raise VezgoValidationError(message, status_code, error_data)
        else:
            raise VezgoAPIError(message, status_code, error_data)

    def close(self) -> None:
        """Close the HTTP client connections."""
        self._client.close()
        if self._user_client:
            self._user_client.close()

    def __enter__(self) -> "Vezgo":
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.close()

