"""
Transactions Resource.

Transactions represent cryptocurrency movements (deposits, withdrawals, trades, etc.)
for a user's connected accounts.
"""

from typing import Any, Dict, List, Optional

from vezgo.exceptions import VezgoValidationError
from vezgo.resources.base import BaseResource


class Transactions(BaseResource):
    """
    Transactions API resource.

    This resource allows you to retrieve transaction history for user accounts.

    Note: This resource requires user authentication. Use `vezgo.login(user_id)`
    to create a user-authenticated client first.

    Example:
        ```python
        user = vezgo.login("user_123")

        # Get transactions for an account
        transactions = user.transactions.get_list(account_id="account_id")

        # Get a specific transaction
        tx = user.transactions.get_one(account_id="account_id", tx_id="tx_id")
        ```
    """

    def get_list(
        self,
        account_id: str,
        ticker: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        wallet: Optional[str] = None,
        last: Optional[str] = None,
        limit: Optional[int] = None,
        sort: Optional[str] = None,
        types: Optional[str] = None,
        exclude_fields: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Get the list of transactions for an account.

        Returns data within the last 1 year by default.

        Args:
            account_id: The Vezgo account ID (required).
            ticker: Filter by asset ticker (e.g., "BTC").
            from_date: Start date filter (YYYY-MM-DD format).
            to_date: End date filter (YYYY-MM-DD format).
            wallet: Filter by wallet ID.
            last: Last transaction ID for pagination.
            limit: Maximum number of transactions to return.
            sort: Sort order ("asc" or "desc").
            types: Comma-separated list of transaction types to include
                   (e.g., "trade,deposit,withdrawal").
            exclude_fields: Comma-separated list of fields to exclude
                           (e.g., "other_parties,transaction_hash").

        Returns:
            List of transaction objects.

        Raises:
            VezgoValidationError: If account_id is invalid.

        Example:
            ```python
            # Get all transactions for an account
            transactions = user.transactions.get_list(
                account_id="603522490d2b02001233a5d6"
            )

            # Get BTC transactions from the last month
            transactions = user.transactions.get_list(
                account_id="603522490d2b02001233a5d6",
                ticker="BTC",
                from_date="2024-01-01",
                to_date="2024-01-31",
                sort="desc"
            )

            # Get only trades and deposits
            transactions = user.transactions.get_list(
                account_id="603522490d2b02001233a5d6",
                types="trade,deposit"
            )
            ```
        """
        if not account_id or not isinstance(account_id, str):
            raise VezgoValidationError("Please provide a valid Vezgo account ID.")

        params = {}
        if ticker:
            params["ticker"] = ticker
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date
        if wallet:
            params["wallet"] = wallet
        if last is not None:  # Allow empty string for pagination
            params["last"] = last
        if limit:
            params["limit"] = limit
        if sort:
            params["sort"] = sort
        if types:
            params["types"] = types
        if exclude_fields:
            params["exclude_fields"] = exclude_fields

        return self._get(
            f"/accounts/{account_id}/transactions",
            params=params or None,
            authenticated=True,
        )

    def get_one(
        self,
        account_id: str,
        tx_id: str,
    ) -> Dict[str, Any]:
        """
        Get a specific transaction by ID.

        Args:
            account_id: The Vezgo account ID.
            tx_id: The transaction ID.

        Returns:
            Transaction object.

        Raises:
            VezgoValidationError: If account_id or tx_id is invalid.
            VezgoNotFoundError: If transaction is not found.

        Example:
            ```python
            tx = user.transactions.get_one(
                account_id="603522490d2b02001233a5d6",
                tx_id="603522490d2b02001233a5d7"
            )
            print(f"Type: {tx['transaction_type']}")
            print(f"Amount: {tx['parts'][0]['amount']} {tx['parts'][0]['ticker']}")
            ```
        """
        if not account_id or not isinstance(account_id, str):
            raise VezgoValidationError("Please provide a valid Vezgo account ID.")
        if not tx_id or not isinstance(tx_id, str):
            raise VezgoValidationError("Please provide a valid Vezgo transaction ID.")

        return self._get(
            f"/accounts/{account_id}/transactions/{tx_id}",
            authenticated=True,
        )

