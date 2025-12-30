"""
Vezgo SDK Constants.
"""

BASE_API_URL = "https://api.vezgo.com"
CONNECT_URL = "https://connect.vezgo.com"
API_VERSION = "v1"
API_URL = f"{BASE_API_URL}/{API_VERSION}"

# Token lifetime defaults (in seconds)
DEFAULT_TOKEN_MINIMUM_LIFETIME = 10
TOKEN_CONNECT_MINIMUM_LIFETIME = 600  # 10 minutes for connect operations

