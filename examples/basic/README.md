# Vezgo Python SDK Examples

This directory contains example scripts demonstrating how to use the Vezgo Python SDK.

## Prerequisites

1. Install the Vezgo SDK:

```bash
pip install vezgo
```

2. Get your API credentials from [Vezgo Dashboard](https://vezgo.com/dashboard)

3. Set up environment variables:

```bash
# Copy the example env file
cp env.example .env

# Edit .env and fill in your credentials
# Then load them (or use python-dotenv)
export $(cat .env | xargs)
```

Or set them directly:

```bash
export VEZGO_CLIENT_ID="your_client_id"
export VEZGO_CLIENT_SECRET="your_secret"
```

## Examples

### Basic Example (`basic.py`)

A command-line script demonstrating core SDK functionality:

- Fetching provider information
- Getting team details
- User authentication
- Listing accounts and balances
- Fetching transactions and history

```bash
python basic.py
```

### Flask Server Example (`flask_server.py`)

A web server demonstrating how to integrate Vezgo into a backend application:

- REST API endpoints for all Vezgo operations
- Token generation for frontend authentication
- Interactive web interface for testing

```bash
# Install Flask
pip install flask python-dotenv

# Run the server
python flask_server.py
```

Then open http://localhost:3001 in your browser.

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `VEZGO_CLIENT_ID` | Your Vezgo client ID | Yes |
| `VEZGO_CLIENT_SECRET` | Your Vezgo client secret | Yes |
| `VEZGO_TEST_USER_ID` | User ID for testing (default: "test_user_123") | No |

## Connecting User Accounts

To connect user accounts to your application, you need to use **Vezgo Connect** in your frontend. The flow is:

1. **Backend**: Generate an auth token for your user:

```python
user = vezgo.login("user_id_from_your_database")
token = user.get_token()
# Return this token to your frontend
```

2. **Frontend**: Use the token with Vezgo Connect (JavaScript):

```javascript
import Vezgo from 'vezgo-sdk-js';

const vezgo = Vezgo.init({
    clientId: 'YOUR_CLIENT_ID',
    authEndpoint: '/api/auth/token',  // Your backend endpoint
});

const user = vezgo.login();
user.connect()
    .onConnection((account) => {
        console.log('Account connected:', account);
    })
    .onError((error) => {
        console.error('Connection error:', error);
    });
```

3. **Backend**: Once connected, fetch the account data:

```python
user = vezgo.login("user_id")
accounts = user.accounts.get_list()
```

For full frontend integration, see the [JavaScript SDK](https://github.com/wealthica/vezgo-sdk-js).

## More Information

- [Vezgo Documentation](https://vezgo.com/docs)
- [API Reference](https://vezgo.com/docs/api/)
- [JavaScript SDK](https://github.com/wealthica/vezgo-sdk-js)

