# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.1] - 2025-12-31

### Added

- `accounts.add()` method for Direct API integration (Enterprise only)
- Add account endpoint in Flask example (`POST /api/accounts`)
- UI form for adding accounts in demo page
- Support for all credential types: wallet, network, code, username, password, user_id, key, secret

### Changed

- Updated documentation with add account examples

## [1.0.0] - 2025-12-31

### Added

- Initial release of the Vezgo Python SDK
- Authentication with JWT tokens
- Providers API - list and get provider information
- Teams API - get team/application information
- Accounts API - list, get, sync, and remove user accounts
- Transactions API - list and get transaction history
- History API - get balance history
- Orders API - list and get order history
- Comprehensive error handling with specific exception types
- Context manager support for automatic cleanup
- Full type hints for IDE support
- Extensive documentation and examples

