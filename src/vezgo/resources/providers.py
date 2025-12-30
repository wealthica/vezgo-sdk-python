"""
Providers Resource.

Providers represent cryptocurrency exchanges, wallets, and blockchain protocols
that users can connect to through Vezgo.
"""

from typing import Any, Dict, List, Optional

from vezgo.exceptions import VezgoValidationError
from vezgo.resources.base import BaseResource


class Providers(BaseResource):
    """
    Providers API resource.

    This resource allows you to retrieve information about supported
    cryptocurrency providers (exchanges, wallets, blockchains).

    Example:
        ```python
        # Get all providers
        providers = vezgo.providers.get_list()

        # Get a specific provider
        coinbase = vezgo.providers.get_one("coinbase")
        ```
    """

    def get_list(
        self,
        category: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Get the list of all supported providers.

        Args:
            category: Optional filter by category (exchanges, wallets, blockchains).

        Returns:
            List of provider objects.

        Example:
            ```python
            providers = vezgo.providers.get_list()
            for provider in providers:
                print(f"{provider['name']}: {provider['display_name']}")
            ```
        """
        params = {}
        if category:
            params["category"] = category

        return self._get("/providers", params=params or None)

    def get_one(self, provider_id: str) -> Dict[str, Any]:
        """
        Get a specific provider by ID/name.

        Args:
            provider_id: The provider's unique name (e.g., "coinbase", "bitcoin").

        Returns:
            Provider object.

        Raises:
            VezgoValidationError: If provider_id is invalid.
            VezgoNotFoundError: If provider is not found.

        Example:
            ```python
            coinbase = vezgo.providers.get_one("coinbase")
            print(f"Auth type: {coinbase['auth_type']}")
            ```
        """
        if not provider_id or not isinstance(provider_id, str):
            raise VezgoValidationError("Please provide a valid provider ID.")

        return self._get(f"/providers/{provider_id}")

