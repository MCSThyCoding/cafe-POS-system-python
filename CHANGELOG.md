# Changelog

All notable changes to the Cafe POS project will be documented in this file.

## [Unreleased]

### Added
- Logging system with file and console output
- CORS support for cross-origin requests
- Health check endpoint at `/health`
- Enhanced input validation on API endpoints
- SECRET_KEY validation for production environments
- Centralized configuration in `config.py`
- Environment variable documentation in `.env.example`
- `.gitignore` to prevent committing database files and other sensitive data
- UI Design Specification document (HTML and Markdown versions)
- Vercel serverless functions for cloud deployment
- PostgreSQL support for production deployments
- Daily, monthly, and yearly reports functionality
- Comprehensive project issues report

### Changed
- Removed database file (`cafe_pos.db`) from git tracking
- Fixed Milk Tea initial stock from 0 to 50
- Improved error handling and logging throughout the application
- Enhanced README with deployment instructions

### Security
- Added SECRET_KEY validation to prevent using default key in production
- Added comprehensive logging for security events
- Improved input validation to prevent injection attacks

### Fixed
- Milk Tea showing as "Out of stock" on first run
- Database file being committed to version control

## [1.0.0] - Initial Release
- Basic POS functionality
- JWT authentication
- SQLite database
- Point of Sale, Dashboard, Inventory, Reports screens
- Demo credentials in login form
