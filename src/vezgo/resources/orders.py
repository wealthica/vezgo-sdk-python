"""
Orders Resource.

Orders represent trading orders (buy/sell) for a user's connected exchange accounts.
"""

from typing import Any, Dict, List, Optional

from vezgo.exceptions import VezgoValidationError
from vezgo.resources.base import BaseResource


class Orders(BaseResource):
    """
    Orders API resource.

    This resource allows you to retrieve order history for user accounts.

    Note: This resource requires user authentication. Use `vezgo.login(user_id)`
    to create a user-authenticated client first.

    Example:
        ```python
        user = vezgo.login("user_123")

        # Get orders for an account
        orders = user.orders.get_list(account_id="account_id")

        # Get a specific order
        order = user.orders.get_one(account_id="account_id", order_id="order_id")
        ```
    """

    def get_list(
        self,
        account_id: str,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        last: Optional[str] = None,
        limit: Optional[int] = None,
        sort: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Get the list of orders for an account.

        Returns data within the last 1 year by default.

        Args:
            account_id: The Vezgo account ID (required).
            from_date: Start date filter (YYYY-MM-DD format).
            to_date: End date filter (YYYY-MM-DD format).
            last: Last order ID for pagination.
            limit: Maximum number of orders to return.
            sort: Sort order ("asc" or "desc").

        Returns:
            List of order objects.

        Raises:
            VezgoValidationError: If account_id is invalid.

        Example:
            ```python
            # Get all orders for an account
            orders = user.orders.get_list(
                account_id="651538b55e8e333d9c7cdc0d"
            )

            # Get orders from the last month
            orders = user.orders.get_list(
                account_id="651538b55e8e333d9c7cdc0d",
                from_date="2024-01-01",
                to_date="2024-01-31",
                sort="desc",
                limit=50
            )

            for order in orders:
                print(f"Order: {order['side']} {order['base_ticker']}/{order['quote_ticker']}")
                print(f"Status: {order['order_status']}")
            ```
        """
        if not account_id or not isinstance(account_id, str):
            raise VezgoValidationError("Please provide a valid Vezgo account ID.")

        params = {}
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date
        if last is not None:  # Allow empty string for pagination
            params["last"] = last
        if limit:
            params["limit"] = limit
        if sort:
            params["sort"] = sort

        return self._get(
            f"/accounts/{account_id}/orders",
            params=params or None,
            authenticated=True,
        )

    def get_one(
        self,
        account_id: str,
        order_id: str,
    ) -> Dict[str, Any]:
        """
        Get a specific order by ID.

        Args:
            account_id: The Vezgo account ID.
            order_id: The order ID.

        Returns:
            Order object.

        Raises:
            VezgoValidationError: If account_id or order_id is invalid.
            VezgoNotFoundError: If order is not found.

        Example:
            ```python
            order = user.orders.get_one(
                account_id="603522490d2b02001233a5d6",
                order_id="651538b55e8e333d9c7cdc0d"
            )
            print(f"Order: {order['side']} {order['base_ticker']}")
            print(f"Filled: {order['filled_quantity']} @ {order['average_execution_price']}")
            ```
        """
        if not account_id or not isinstance(account_id, str):
            raise VezgoValidationError("Please provide a valid Vezgo account ID.")
        if not order_id or not isinstance(order_id, str):
            raise VezgoValidationError("Please provide a valid Vezgo order ID.")

        return self._get(
            f"/accounts/{account_id}/orders/{order_id}",
            authenticated=True,
        )

