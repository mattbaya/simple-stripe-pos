# Community POS System - Project Context

## Overview
This is a Flask-based point-of-sale system for community organizations that enables in-person payment processing for donations and memberships using Stripe Terminal hardware. Features optional fee coverage allowing users to cover Stripe processing fees (2.9% + $0.30) with transparent cost breakdown.

## Technology Stack
- **Backend**: Python Flask web application
- **Payment Processing**: Stripe Terminal API (v8.11.0) with S700 card reader
- **Email**: OAuth2-authenticated Gmail API for receipts and notifications
- **Deployment**: Docker containers with Docker Compose
- **Frontend**: Bootstrap-based web interface with JavaScript
- **Fee Calculation**: Real-time Stripe fee calculations with optional coverage

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
- `INDIVIDUAL_MEMBERSHIP_AMOUNT` - Individual membership price (cents, default: 3500)
- `HOUSEHOLD_MEMBERSHIP_AMOUNT` - Household membership price (cents, default: 5000)
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
1. User selects donation or membership (individual/household) on web interface
2. User enters amount (for donations) and personal details
3. User optionally selects fee coverage (shows transparent breakdown)
4. System creates Stripe PaymentIntent with calculated amount
5. Payment processed on S700 terminal hardware
6. Success triggers automatic email receipt and notification
7. All transaction data stored in Stripe, no local database

## API Endpoints
- `GET /` - Main payment interface
- `GET /health` - Health check endpoint
- `POST /calculate-fees` - Calculate processing fees for given amount/type
- `POST /create-payment-intent` - Create Stripe PaymentIntent with optional fees
- `POST /register-reader` - Register new Stripe terminal (development helper)
- `POST /discover-readers` - Find available Stripe terminals
- `POST /process-payment` - Process payment on selected terminal
- `GET /payment-status/<id>` - Check PaymentIntent status and send emails

## Fee Coverage Feature
- Calculates Stripe fees: 2.9% + $0.30 per transaction
- Optional checkbox with real-time fee display
- Transparent breakdown: base amount + processing fee = total
- Payment metadata tracks fee information for reporting
- Works for both donations and memberships

## Security Notes
- Environment files (.env*) are gitignored
- Uses OAuth2 for secure Gmail authentication
- Stripe handles all sensitive payment data
- Application runs on port 8080 with health checks
- Organization-neutral design with configurable branding