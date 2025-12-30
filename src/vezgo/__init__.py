"""
Vezgo Python SDK - Official Python client for the Vezgo Cryptocurrency API.

Vezgo is a unified API for connecting with cryptocurrency exchanges, wallets,
and blockchain protocols.
"""

from vezgo.client import Vezgo
from vezgo.exceptions import (
    VezgoError,
    VezgoAuthenticationError,
    VezgoAPIError,
    VezgoValidationError,
    VezgoNotFoundError,
    VezgoRateLimitError,
)

__version__ = "1.0.0"
__all__ = [
    "Vezgo",
    "VezgoError",
    "VezgoAuthenticationError",
    "VezgoAPIError",
    "VezgoValidationError",
    "VezgoNotFoundError",
    "VezgoRateLimitError",
]

