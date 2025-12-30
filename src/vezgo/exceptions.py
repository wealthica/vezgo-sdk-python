"""
Vezgo SDK Exceptions.
"""

from typing import Any, Dict, Optional


class VezgoError(Exception):
    """Base exception for all Vezgo SDK errors."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_data: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.response_data = response_data or {}

    def __str__(self) -> str:
        if self.status_code:
            return f"[{self.status_code}] {self.message}"
        return self.message


class VezgoAuthenticationError(VezgoError):
    """Raised when authentication fails."""

    pass


class VezgoAPIError(VezgoError):
    """Raised when the API returns an error response."""

    pass


class VezgoValidationError(VezgoError):
    """Raised when request validation fails."""

    pass


class VezgoNotFoundError(VezgoError):
    """Raised when a requested resource is not found."""

    pass


class VezgoRateLimitError(VezgoError):
    """Raised when rate limit is exceeded."""

    pass

