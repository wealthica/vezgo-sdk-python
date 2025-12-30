"""
Base Resource class for Vezgo API resources.
"""

from typing import TYPE_CHECKING, Any, Dict, List, Optional
from urllib.parse import urlencode

if TYPE_CHECKING:
    from vezgo.client import Vezgo


class BaseResource:
    """Base class for all API resources."""

    def __init__(self, client: "Vezgo"):
        """
        Initialize the resource.

        Args:
            client: The Vezgo client instance.
        """
        self.client = client

    def _build_query_string(self, params: Optional[Dict[str, Any]] = None) -> str:
        """
        Build a query string from parameters, filtering out None values.

        Args:
            params: Dictionary of query parameters.

        Returns:
            URL-encoded query string.
        """
        if not params:
            return ""

        # Filter out None values
        filtered = {k: v for k, v in params.items() if v is not None}
        if not filtered:
            return ""

        return urlencode(filtered)

    def _get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        authenticated: bool = False,
    ) -> Any:
        """
        Make a GET request.

        Args:
            endpoint: API endpoint.
            params: Query parameters.
            authenticated: Whether to include auth header.

        Returns:
            Response data.
        """
        return self.client._request("GET", endpoint, params=params, authenticated=authenticated)

    def _post(
        self,
        endpoint: str,
        json: Optional[Dict[str, Any]] = None,
        authenticated: bool = False,
    ) -> Any:
        """
        Make a POST request.

        Args:
            endpoint: API endpoint.
            json: JSON body data.
            authenticated: Whether to include auth header.

        Returns:
            Response data.
        """
        return self.client._request("POST", endpoint, json=json, authenticated=authenticated)

    def _put(
        self,
        endpoint: str,
        json: Optional[Dict[str, Any]] = None,
        authenticated: bool = False,
    ) -> Any:
        """
        Make a PUT request.

        Args:
            endpoint: API endpoint.
            json: JSON body data.
            authenticated: Whether to include auth header.

        Returns:
            Response data.
        """
        return self.client._request("PUT", endpoint, json=json, authenticated=authenticated)

    def _delete(
        self,
        endpoint: str,
        authenticated: bool = False,
    ) -> Any:
        """
        Make a DELETE request.

        Args:
            endpoint: API endpoint.
            authenticated: Whether to include auth header.

        Returns:
            Response data.
        """
        return self.client._request("DELETE", endpoint, authenticated=authenticated)

