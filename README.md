# Vezgo Python SDK

Official Python SDK for the [Vezgo](https://vezgo.com) Cryptocurrency API.

## What is Vezgo?

Vezgo is a unified cryptocurrency API that allows you to connect with cryptocurrency exchanges, wallets, and blockchain protocols. Instead of manually integrating with multiple exchange APIs like Coinbase, Binance, or blockchain APIs - you can simply use Vezgo for them all.

## Features

- 🔐 **Secure Authentication** - JWT-based token authentication
- 📊 **Account Data** - Retrieve balances, positions, and wallet information
- 💸 **Transaction History** - Full transaction history across all connected accounts
- 📈 **Balance History** - Historical balance tracking over time
- 📋 **Order History** - Trading order history from exchanges
- 🏢 **40+ Exchanges** - Support for major cryptocurrency exchanges
- ⛓️ **20+ Blockchains** - Direct blockchain integrations
- 👛 **250+ Wallets** - Wallet connection support

## Installation

```bash
pip install vezgo
```

## Configuration

Copy the example environment file and add your credentials:

```bash
cp env.example .env
```

Edit `.env` with your Vezgo API credentials from the [Vezgo Dashboard](https://vezgo.com/dashboard):

```env
VEZGO_CLIENT_ID=your_client_id_here
VEZGO_CLIENT_SECRET=your_client_secret_here
```

## Quick Start

```python
from vezgo import Vezgo

# Initialize the client with your API credentials
vezgo = Vezgo(
    client_id="your_client_id",
    secret="your_secret"
)

# Get list of supported providers (no user login required)
providers = vezgo.providers.get_list()
print(f"Vezgo supports {len(providers)} providers")

# Get team information
team = vezgo.get_team()
print(f"Team: {team['name']}")
```

## User Authentication

To access user-specific data like accounts and transactions, you need to login as a user:

```python
from vezgo import Vezgo

vezgo = Vezgo(
    client_id="your_client_id",
    secret="your_secret"
)

# Login as a specific user (use your internal user ID)
user = vezgo.login("user_123")

# Now you can access user-specific resources
accounts = user.accounts.get_list()
for account in accounts:
    print(f"Account: {account['provider']['display_name']}")
    for balance in account.get('balances', []):
        print(f"  {balance['ticker']}: {balance['amount']}")
```

## API Reference

### Provider APIs

These APIs don't require user authentication:

#### Get All Providers

```python
providers = vezgo.providers.get_list()

# Each provider includes:
# - name: unique identifier
# - display_name: human-friendly name
# - auth_type: oauth, password, token, or wallet
# - credentials: required credential types
# - features: supported features (positions, transactions, nfts, etc.)
```

#### Get a Specific Provider

```python
coinbase = vezgo.providers.get_one("coinbase")
print(f"Auth type: {coinbase['auth_type']}")
print(f"Credentials: {coinbase['credentials']}")
```

### Account APIs

These APIs require user authentication:

#### List All Accounts

```python
user = vezgo.login("user_123")
accounts = user.accounts.get_list()

for account in accounts:
    print(f"ID: {account['id']}")
    print(f"Provider: {account['provider']['display_name']}")
    print(f"Status: {account['status']}")
    print(f"Total Value: ${account.get('fiat_value', '0')}")
```

#### Get a Specific Account

```python
account = user.accounts.get_one("603522490d2b02001233a5d6")
```

#### Sync an Account

Trigger a refresh to fetch the latest data from the provider:

```python
account = user.accounts.sync("603522490d2b02001233a5d6")
print(f"Sync status: {account['status']}")
```

#### Remove an Account

```python
user.accounts.remove("603522490d2b02001233a5d6")
```

### Transaction APIs

#### List Transactions

```python
user = vezgo.login("user_123")

# Get all transactions for an account
transactions = user.transactions.get_list(
    account_id="603522490d2b02001233a5d6"
)

# With filters
transactions = user.transactions.get_list(
    account_id="603522490d2b02001233a5d6",
    ticker="BTC",                    # Filter by asset
    from_date="2024-01-01",          # Start date
    to_date="2024-06-30",            # End date
    types="trade,deposit",           # Filter by type
    sort="desc",                     # Sort order
    limit=100                        # Max results
)

for tx in transactions:
    print(f"Type: {tx['transaction_type']}")
    for part in tx.get('parts', []):
        print(f"  {part['direction']}: {part['amount']} {part['ticker']}")
```

#### Get a Specific Transaction

```python
tx = user.transactions.get_one(
    account_id="603522490d2b02001233a5d6",
    tx_id="603522490d2b02001233a5d7"
)
```

### Balance History APIs

#### Get Balance History

```python
user = vezgo.login("user_123")

history = user.history.get_list(
    account_id="603522490d2b02001233a5d6",
    from_date="2024-01-01",
    to_date="2024-06-30"
)

for entry in history:
    print(f"Date: {entry['date']}, Value: ${entry['fiat_value']}")
```

### Order APIs

#### List Orders

```python
user = vezgo.login("user_123")

orders = user.orders.get_list(
    account_id="651538b55e8e333d9c7cdc0d",
    from_date="2024-01-01",
    sort="desc"
)

for order in orders:
    print(f"Order: {order['side']} {order['base_ticker']}/{order['quote_ticker']}")
    print(f"Status: {order['order_status']}")
    print(f"Filled: {order['filled_quantity']} @ {order['average_execution_price']}")
```

#### Get a Specific Order

```python
order = user.orders.get_one(
    account_id="603522490d2b02001233a5d6",
    order_id="651538b55e8e333d9c7cdc0d"
)
```

## Error Handling

The SDK provides specific exception classes for different error types:

```python
from vezgo import (
    Vezgo,
    VezgoError,
    VezgoAuthenticationError,
    VezgoAPIError,
    VezgoValidationError,
    VezgoNotFoundError,
    VezgoRateLimitError,
)

try:
    user = vezgo.login("user_123")
    account = user.accounts.get_one("invalid_id")
except VezgoNotFoundError as e:
    print(f"Account not found: {e.message}")
except VezgoAuthenticationError as e:
    print(f"Authentication failed: {e.message}")
except VezgoRateLimitError as e:
    print(f"Rate limit exceeded: {e.message}")
except VezgoAPIError as e:
    print(f"API error [{e.status_code}]: {e.message}")
except VezgoError as e:
    print(f"Vezgo error: {e.message}")
```

## Context Manager Support

The SDK supports context managers for automatic cleanup:

```python
with Vezgo(client_id="...", secret="...") as vezgo:
    providers = vezgo.providers.get_list()
    # Connection is automatically closed when exiting the block
```

## Configuration Options

```python
vezgo = Vezgo(
    client_id="your_client_id",       # Required
    secret="your_secret",             # Required
    base_url="https://api.vezgo.com/v1",  # Optional, default API URL
    connect_url="https://connect.vezgo.com",  # Optional, Connect widget URL
    timeout=30.0,                     # Optional, request timeout in seconds
)
```

## Connecting Users (Frontend Integration)

To connect user accounts, you'll need to use Vezgo Connect in your frontend. Here's how the flow works:

1. **Backend**: Generate a user token

```python
user = vezgo.login("user_123")
token = user.get_token()
# Send this token to your frontend
```

2. **Frontend**: Use the token with Vezgo Connect (JavaScript)

```javascript
// Use the vezgo-sdk-js package or redirect to Connect URL
const { url, token } = await getConnectDataFromYourBackend();

// Redirect to Vezgo Connect or use the SDK widget
window.location.href = `${url}&token=${token}`;
```

3. **Backend**: Handle the callback to receive the connected account

For full frontend integration, see the [JavaScript SDK](https://github.com/wealthica/vezgo-sdk-js).

## Documentation

- [Vezgo API Documentation](https://vezgo.com/docs)
- [API Specification](https://vezgo.com/docs/api/)
- [JavaScript SDK](https://github.com/wealthica/vezgo-sdk-js)

## Support

- Email: [hello@vezgo.com](mailto:hello@vezgo.com)
- Documentation: [https://vezgo.com/docs](https://vezgo.com/docs)

## License

MIT License - see [LICENSE](LICENSE) for details.

