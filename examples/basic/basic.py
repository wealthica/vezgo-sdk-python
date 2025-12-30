#!/usr/bin/env python3
"""
Basic usage example for the Vezgo Python SDK.

This example demonstrates:
1. Initializing the Vezgo client
2. Fetching provider information (no auth required)
3. Logging in as a user
4. Fetching user accounts, transactions, and history

Before running:
1. Set your VEZGO_CLIENT_ID and VEZGO_CLIENT_SECRET environment variables
2. Install the SDK: pip install vezgo

Usage:
    export VEZGO_CLIENT_ID="your_client_id"
    export VEZGO_CLIENT_SECRET="your_secret"
    python basic.py
"""

import os
import sys
from datetime import datetime, timedelta

from vezgo import (
    Vezgo,
    VezgoError,
    VezgoAuthenticationError,
    VezgoNotFoundError,
)


def print_separator(title: str = "") -> None:
    """Print a visual separator."""
    print("\n" + "=" * 60)
    if title:
        print(f"  {title}")
        print("=" * 60)
    print()


def main() -> None:
    # Get credentials from environment variables
    client_id = os.getenv("VEZGO_CLIENT_ID")
    client_secret = os.getenv("VEZGO_CLIENT_SECRET")
    
    if not client_id or not client_secret:
        print("Error: Please set VEZGO_CLIENT_ID and VEZGO_CLIENT_SECRET environment variables")
        print("\nExample:")
        print('  export VEZGO_CLIENT_ID="your_client_id"')
        print('  export VEZGO_CLIENT_SECRET="your_secret"')
        sys.exit(1)
    
    # Initialize the Vezgo client
    print_separator("Initializing Vezgo Client")
    
    with Vezgo(client_id=client_id, secret=client_secret) as vezgo:
        # ============================================================
        # 1. Get Provider Information (No Authentication Required)
        # ============================================================
        print_separator("1. Fetching Providers")
        
        try:
            providers = vezgo.providers.get_list()
            print(f"✓ Found {len(providers)} supported providers\n")
            
            # Show first 5 providers
            print("Sample providers:")
            for provider in providers[:5]:
                print(f"  - {provider['display_name']} ({provider['name']})")
                print(f"    Auth: {provider['auth_type']}, Beta: {provider.get('is_beta', False)}")
            
            if len(providers) > 5:
                print(f"\n  ... and {len(providers) - 5} more providers")
                
        except VezgoError as e:
            print(f"✗ Error fetching providers: {e}")
        
        # Get a specific provider
        print("\nFetching Coinbase provider details...")
        try:
            coinbase = vezgo.providers.get_one("coinbase")
            print(f"✓ Provider: {coinbase['display_name']}")
            print(f"  Auth type: {coinbase['auth_type']}")
            print(f"  Credentials: {coinbase.get('credentials', [])}")
            features = coinbase.get('features', {})
            if features:
                print(f"  Features: {', '.join(k for k, v in features.items() if v)}")
        except VezgoNotFoundError:
            print("✗ Coinbase provider not found")
        except VezgoError as e:
            print(f"✗ Error: {e}")
        
        # ============================================================
        # 2. Get Team Information
        # ============================================================
        print_separator("2. Fetching Team Information")
        
        try:
            team = vezgo.get_team()
            print(f"✓ Team: {team.get('name', 'Unknown')}")
            print(f"  Features: {team.get('features', [])}")
            print(f"  Redirect URIs: {team.get('redirect_uris', [])}")
        except VezgoError as e:
            print(f"✗ Error fetching team info: {e}")
        
        # ============================================================
        # 3. User Operations (Requires User Login)
        # ============================================================
        print_separator("3. User Operations")
        
        # You would use your own user identifier here
        # This could be a user ID from your database
        user_id = os.getenv("VEZGO_TEST_USER_ID", "test_user_123")
        
        print(f"Logging in as user: {user_id}")
        user = vezgo.login(user_id)
        
        # ============================================================
        # 3a. Get User Accounts
        # ============================================================
        print("\n--- User Accounts ---")
        
        try:
            accounts = user.accounts.get_list()
            
            if accounts:
                print(f"✓ Found {len(accounts)} account(s)\n")
                
                for account in accounts:
                    print(f"Account: {account['id']}")
                    print(f"  Provider: {account['provider']['display_name']}")
                    print(f"  Status: {account.get('status', 'unknown')}")
                    print(f"  Fiat Value: ${account.get('fiat_value', '0')}")
                    
                    balances = account.get('balances', [])
                    if balances:
                        print(f"  Balances ({len(balances)}):")
                        for balance in balances[:3]:  # Show first 3 balances
                            print(f"    - {balance['ticker']}: {balance['amount']}")
                        if len(balances) > 3:
                            print(f"    ... and {len(balances) - 3} more")
                    print()
                
                # ============================================================
                # 3b. Get Transactions for First Account
                # ============================================================
                print("--- Recent Transactions ---")
                first_account_id = accounts[0]['id']
                
                # Get transactions from the last 30 days
                thirty_days_ago = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
                
                try:
                    transactions = user.transactions.get_list(
                        account_id=first_account_id,
                        from_date=thirty_days_ago,
                        limit=5,
                        sort="desc"
                    )
                    
                    if transactions:
                        print(f"✓ Found recent transactions\n")
                        
                        for tx in transactions:
                            tx_type = tx.get('transaction_type', 'unknown')
                            initiated = tx.get('initiated_at', 0)
                            
                            # Convert timestamp to readable date
                            if initiated:
                                tx_date = datetime.fromtimestamp(initiated / 1000).strftime("%Y-%m-%d %H:%M")
                            else:
                                tx_date = "Unknown"
                            
                            print(f"Transaction: {tx['id']}")
                            print(f"  Type: {tx_type}")
                            print(f"  Date: {tx_date}")
                            
                            for part in tx.get('parts', []):
                                direction = part.get('direction', 'unknown')
                                amount = part.get('amount', '0')
                                ticker = part.get('ticker', '???')
                                fiat_value = part.get('fiat_value', '0')
                                print(f"  {direction}: {amount} {ticker} (${fiat_value})")
                            
                            print()
                    else:
                        print("No recent transactions found")
                        
                except VezgoError as e:
                    print(f"✗ Error fetching transactions: {e}")
                
                # ============================================================
                # 3c. Get Balance History for First Account
                # ============================================================
                print("--- Balance History ---")
                
                try:
                    history = user.history.get_list(
                        account_id=first_account_id,
                        from_date=thirty_days_ago
                    )
                    
                    if history:
                        print(f"✓ Found {len(history)} history entries\n")
                        
                        # Show last 5 entries
                        for entry in history[-5:]:
                            date = entry.get('date', 0)
                            if date:
                                entry_date = datetime.fromtimestamp(date / 1000).strftime("%Y-%m-%d")
                            else:
                                entry_date = "Unknown"
                            
                            print(f"  {entry_date}: ${entry.get('fiat_value', '0')}")
                    else:
                        print("No history found for this period")
                        
                except VezgoError as e:
                    print(f"✗ Error fetching history: {e}")
                
            else:
                print("No accounts found for this user.")
                print("\nTo connect accounts, you'll need to use Vezgo Connect")
                print("in your frontend. See the README for more information.")
                
        except VezgoAuthenticationError as e:
            print(f"✗ Authentication error: {e}")
            print("\nMake sure your credentials are correct.")
        except VezgoError as e:
            print(f"✗ Error: {e}")
    
    print_separator("Done")
    print("For more examples, see the README and API documentation:")
    print("  https://vezgo.com/docs")


if __name__ == "__main__":
    main()

