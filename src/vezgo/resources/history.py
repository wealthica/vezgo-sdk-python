"""
History Resource.

History represents the balance history over time for a user's connected accounts.
"""

from typing import Any, Dict, List, Optional

from vezgo.exceptions import VezgoValidationError
from vezgo.resources.base import BaseResource


class History(BaseResource):
    """
    History API resource.

    This resource allows you to retrieve balance history for user accounts.

    Note: This resource requires user authentication. Use `vezgo.login(user_id)`
    to create a user-authenticated client first.

    Example:
        ```python
        user = vezgo.login("user_123")

        # Get balance history for an account
        history = user.history.get_list(account_id="account_id")
        ```
    """

    def get_list(
        self,
        account_id: str,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        wallet: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Get the balance history for an account.

        Returns data within the last 1 year by default.

        Args:
            account_id: The Vezgo account ID (required).
            from_date: Start date filter (YYYY-MM-DD format).
            to_date: End date filter (YYYY-MM-DD format).
            wallet: Filter by wallet ID.

        Returns:
            List of history entry objects with date and fiat_value.

        Raises:
            VezgoValidationError: If account_id is invalid.

        Example:
            ```python
            # Get all history for an account
            history = user.history.get_list(
                account_id="603522490d2b02001233a5d6"
            )

            # Get history for a specific date range
            history = user.history.get_list(
                account_id="603522490d2b02001233a5d6",
                from_date="2024-01-01",
                to_date="2024-06-30"
            )

            for entry in history:
                print(f"Date: {entry['date']}, Value: ${entry['fiat_value']}")
            ```
        """
        if not account_id or not isinstance(account_id, str):
            raise VezgoValidationError("Please provide a valid Vezgo account ID.")

        params = {}
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date
        if wallet:
            params["wallet"] = wallet

        return self._get(
            f"/accounts/{account_id}/history",
            params=params or None,
            authenticated=True,
        )

