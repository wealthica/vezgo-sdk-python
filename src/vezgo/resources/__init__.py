"""
Vezgo API Resources.
"""

from vezgo.resources.accounts import Accounts
from vezgo.resources.history import History
from vezgo.resources.orders import Orders
from vezgo.resources.providers import Providers
from vezgo.resources.teams import Teams
from vezgo.resources.transactions import Transactions

__all__ = [
    "Accounts",
    "History",
    "Orders",
    "Providers",
    "Teams",
    "Transactions",
]

