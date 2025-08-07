# Community POS System - Project Context

## Overview
This is a Flask-based point-of-sale system for community organizations that enables in-person payment processing for donations and memberships using Stripe Terminal hardware.

## Technology Stack
- **Backend**: Python Flask web application
- **Payment Processing**: Stripe Terminal API with S700 card reader
- **Email**: OAuth2-authenticated Gmail API for receipts and notifications
- **Deployment**: Docker containers with Docker Compose
- **Frontend**: Bootstrap-based web interface with JavaScript

## Key Files
- `app/main.py` - Main Flask application with payment processing logic
- `templates/index.html` - Web interface for payment collection
- `docker-compose.yml` - Container orchestration
- `requirements.txt` - Python dependencies
- `generate_oauth_token.py` - OAuth2 setup utility

## Environment Configuration
The application requires these environment variables:
- `STRIPE_SECRET_KEY` - Stripe API key
- `STRIPE_LOCATION_ID` - Terminal location ID  
- `MEMBERSHIP_AMOUNT` - Fixed membership price (cents)
- `ORGANIZATION_NAME/LOGO/WEBSITE` - Branding configuration
- `NOTIFICATION_EMAIL` - Organization notification recipient
- `GOOGLE_CLIENT_ID/SECRET/REFRESH_TOKEN` - OAuth2 credentials
- `FROM_EMAIL` - Sender email address

## Development Commands
- Start: `docker compose up -d`
- Logs: `docker compose logs -f` 
- Stop: `docker compose down`
- Health check: `curl http://localhost:8080/health`

## Payment Flow
1. User selects donation or membership on web interface
2. System creates Stripe PaymentIntent
3. Payment processed on S700 terminal hardware
4. Success triggers automatic email receipt and notification
5. All transaction data stored in Stripe, no local database

## Security Notes
- Environment files (.env*) are gitignored
- Uses OAuth2 for secure Gmail authentication
- Stripe handles all sensitive payment data
- Application runs on port 8080 with health checks
- Organization-neutral design with configurable branding