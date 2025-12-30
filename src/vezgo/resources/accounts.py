"""
Accounts Resource.

Accounts represent user connections to cryptocurrency exchanges, wallets,
or blockchain addresses through Vezgo.
"""

from typing import Any, Dict, List, Optional

from vezgo.exceptions import VezgoValidationError
from vezgo.resources.base import BaseResource


class Accounts(BaseResource):
    """
    Accounts API resource.

    This resource allows you to manage user accounts (connections to
    cryptocurrency exchanges, wallets, and blockchains).

    Note: This resource requires user authentication. Use `vezgo.login(user_id)`
    to create a user-authenticated client first.

    Example:
        ```python
        user = vezgo.login("user_123")

        # Get all accounts
        accounts = user.accounts.get_list()

        # Get a specific account
        account = user.accounts.get_one("account_id")

        # Sync an account
        user.accounts.sync("account_id")

        # Remove an account
        user.accounts.remove("account_id")
        ```
    """

    def get_list(self, wallet: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get the list of all accounts for the user.

        Args:
            wallet: Optional filter by wallet ID.

        Returns:
            List of account objects with balances and provider info.

        Example:
            ```python
            accounts = user.accounts.get_list()
            for account in accounts:
                print(f"Account: {account['id']}")
                print(f"Provider: {account['provider']['display_name']}")
                for balance in account.get('balances', []):
                    print(f"  {balance['ticker']}: {balance['amount']}")
            ```
        """
        params = {}
        if wallet:
            params["wallet"] = wallet

        return self._get("/accounts", params=params or None, authenticated=True)

    def get_one(
        self,
        account_id: str,
        wallet: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get a specific account by ID.

        Args:
            account_id: The Vezgo account ID.
            wallet: Optional filter by wallet ID.

        Returns:
            Account object with balances and provider info.

        Raises:
            VezgoValidationError: If account_id is invalid.
            VezgoNotFoundError: If account is not found.

        Example:
            ```python
            account = user.accounts.get_one("603522490d2b02001233a5d6")
            print(f"Provider: {account['provider']['display_name']}")
            print(f"Total Value: ${account.get('fiat_value', '0')}")
            ```
        """
        if not account_id or not isinstance(account_id, str):
            raise VezgoValidationError("Please provide a valid Vezgo account ID.")

        params = {}
        if wallet:
            params["wallet"] = wallet

        return self._get(f"/accounts/{account_id}", params=params or None, authenticated=True)

    def sync(self, account_id: str) -> Dict[str, Any]:
        """
        Trigger a sync for an account to fetch latest data.

        This will initiate a refresh of the account's balances and transactions
        from the connected provider.

        Args:
            account_id: The Vezgo account ID.

        Returns:
            Updated account object.

        Raises:
            VezgoValidationError: If account_id is invalid.
            VezgoNotFoundError: If account is not found.

        Example:
            ```python
            # Trigger a sync
            account = user.accounts.sync("603522490d2b02001233a5d6")
            print(f"Status: {account['status']}")
            ```
        """
        if not account_id or not isinstance(account_id, str):
            raise VezgoValidationError("Please provide a valid Vezgo account ID.")

        return self._post(f"/accounts/{account_id}/sync", json={}, authenticated=True)

    def remove(self, account_id: str) -> None:
        """
        Remove an account from the user.

        This will disconnect the account and delete all associated data.

        Args:
            account_id: The Vezgo account ID.

        Raises:
            VezgoValidationError: If account_id is invalid.
            VezgoNotFoundError: If account is not found.

        Example:
            ```python
            user.accounts.remove("603522490d2b02001233a5d6")
            print("Account removed successfully")
            ```
        """
        if not account_id or not isinstance(account_id, str):
            raise VezgoValidationError("Please provide a valid Vezgo account ID.")

        self._delete(f"/accounts/{account_id}", authenticated=True)

