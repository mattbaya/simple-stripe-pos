# Community POS System

A lightweight, containerized point-of-sale application for community organizations to process in-person donations and membership payments using Stripe Terminal hardware.

## Features

- Simple web interface with "Donate" and "Membership" buttons
- Integration with Stripe S700 terminal for card-present transactions
- Collects payer name and optional email
- Preset membership amount ($20 default) or custom donation amounts
- **Automatic email receipts** sent to donors using OAuth2-authenticated Gmail
- **Email notifications** sent to configurable organization email
- Customizable organization branding and logo
- No local database required - all data handled by Stripe
- Containerized with Docker for easy deployment

## Prerequisites

1. **Stripe Account**: You need a Stripe account with Terminal enabled
2. **Stripe S700 Terminal**: Physical card reader device
3. **Docker & Docker Compose**: Installed on your server

## Stripe Setup

### 1. Get API Keys

1. Log in to your [Stripe Dashboard](https://dashboard.stripe.com/)
2. Go to Developers → API keys
3. Copy your **Publishable key** and **Secret key**
4. Make sure you're using the correct keys for your environment (test vs live)

### 2. Create a Location

1. In the Stripe Dashboard, go to Terminal → Locations
2. Click "Create location"
3. Enter your address and business details
4. Copy the **Location ID** (starts with `tml_`)

### 3. Register Your S700 Terminal

1. Power on your Stripe S700 terminal
2. In the Stripe Dashboard, go to Terminal → Readers
3. Click "Register reader"
4. Follow the on-screen instructions to connect your S700 to WiFi
5. The terminal will display a registration code
6. Enter the code in the Stripe Dashboard
7. Assign the reader to the location you created
8. Give the reader a memorable label (e.g., "Donation Table Reader")

### 4. Test the Terminal

1. Use Stripe's test mode first to ensure everything works
2. Test with Stripe's test cards (available in their documentation)
3. Switch to live mode only when ready for actual payments

### 5. Email Setup with OAuth2 (Optional)

The system can automatically send receipt emails to donors and notification emails to your organization using Google OAuth2 authentication.

#### Step 1: Google Cloud Console Setup
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project or select existing project
3. Enable the **Gmail API**:
   - Go to APIs & Services → Library
   - Search for "Gmail API" and enable it
4. Create OAuth2 credentials:
   - Go to APIs & Services → Credentials
   - Click "Create Credentials" → "OAuth 2.0 Client IDs"
   - Application type: "Desktop application"
   - Name: "SWCA POS System"
   - Add `http://localhost` to authorized redirect URIs
   - Save the Client ID and Client Secret

#### Step 2: Generate Refresh Token
Since you have your Client ID and Secret, you need to generate a refresh token:

1. **Install dependencies** (on your local machine):
   ```bash
   pip install google-auth-oauthlib
   ```

2. **Run the token generator script**:
   ```bash
   cd /home/swca/pos-docker
   python3 generate_oauth_token.py
   ```

3. **Follow the prompts**:
   - Enter your Client ID and Secret
   - Browser will open for Google authorization
   - Sign in and grant Gmail send permissions
   - Script will display your refresh token

#### Step 3: Configure Environment
Add the OAuth2 values to your `.env` file:
```env
GOOGLE_CLIENT_ID=your_client_id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your_client_secret
GOOGLE_REFRESH_TOKEN=your_refresh_token
FROM_EMAIL=your_email@domain.com
```

**Email Configuration Notes:**
- OAuth2 is more secure than app passwords and works with Google Workspace
- If OAuth2 isn't configured, the app will still work but won't send emails
- Transaction notifications will always be sent to `info@southwilliamstown.org`
- Receipts are only sent if the donor provides an email address
- Refresh tokens don't expire unless revoked

## Installation & Configuration

### 1. Clone/Copy Files

Ensure all files are in `/home/swca/pos-docker/`:

```
pos-docker/
├── app/
│   └── main.py
├── templates/
│   └── index.html
├── static/
│   └── logo.png          # Your organization logo
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── env-template           # Template for .env file
├── .env                  # Your configuration (create from template)
└── README.md
```

### 2. Configure Environment

Create a `.env` file in the project root:

```bash
cp env-template .env
```

Edit `.env` with your Stripe credentials:

```env
# Stripe API Keys (get from Stripe Dashboard → Developers → API keys)
STRIPE_SECRET_KEY=sk_test_...  # Use sk_live_... for production
STRIPE_PUBLISHABLE_KEY=pk_test_...  # Use pk_live_... for production

# Location ID (get from Stripe Dashboard → Terminal → Locations)
STRIPE_LOCATION_ID=tml_...

# Membership amount in cents (2000 = $20.00)
MEMBERSHIP_AMOUNT=2000

# Email Configuration (for receipts and notifications)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
FROM_EMAIL=payments@yourcommunity.org
NOTIFICATION_EMAIL=treasurer@yourcommunity.org
ORGANIZATION_NAME=Your Community Organization
ORGANIZATION_LOGO=/static/logo.png
ORGANIZATION_WEBSITE=https://yourcommunity.org
```

⚠️ **Security**: Never commit the `.env` file to version control. Keep your API keys secure.

### 3. Start the Application

From the `/home/swca/pos-docker/` directory:

```bash
# Start the application
docker compose up -d

# Check if it's running
docker compose ps

# View logs
docker compose logs -f
```

The application will be available at: `http://localhost:8080`

## Usage

### For Event Volunteers

1. Open the web interface in a browser
2. Click "Find Readers" to detect your Stripe terminal
3. Select your terminal from the list
4. For donations:
   - Click "Make a Donation"
   - Enter payer's name and optional email
   - Enter donation amount
   - Click "Process Payment"
5. For memberships:
   - Click "Pay for Membership" 
   - Enter payer's name and optional email
   - Click "Process Payment" (amount is preset at $20)
6. Follow prompts on the Stripe terminal to complete payment
7. Wait for confirmation message

### Payment Flow

1. Customer inserts, taps, or swipes card on S700 terminal
2. Terminal processes payment through Stripe
3. Success/failure message appears in web interface
4. Receipt email sent to donor (if email provided and configured)
5. Notification email sent to organization (if configured)

## Management Commands

```bash
# Start the application
docker compose up -d

# Stop the application
docker compose down

# View real-time logs
docker compose logs -f

# Restart after configuration changes
docker compose down && docker compose up -d

# Update the application
docker compose build --no-cache
docker compose up -d

# Check application health
curl http://localhost:8080/health
```

## Troubleshooting

### Terminal Not Found

- Ensure S700 is powered on and connected to WiFi
- Check that terminal is registered and assigned to correct location
- Verify `STRIPE_LOCATION_ID` in `.env` file
- Try refreshing the "Find Readers" in the web interface

### Payment Failures

- Check Stripe Dashboard → Payments for error details
- Ensure API keys are correct and for the right environment (test/live)
- Verify terminal has good internet connectivity
- Check application logs: `docker compose logs -f`

### Application Won't Start

- Check environment variables in `.env` file
- Verify Docker and Docker Compose are installed
- Check port 8080 isn't already in use: `ss -tlnp | grep 8080`
- Review logs for specific error messages

### Connection Issues

- Ensure firewall allows traffic on port 8080
- For external access, you may need to configure your router/firewall
- Check if other services are using the same port

### Email Issues

**Emails Not Sending:**
- Check application logs: `docker compose logs -f`
- Verify SMTP credentials in `.env` file
- Ensure email account has app password generated (for Gmail)
- Test SMTP settings with a simple email client first

**OAuth2-Specific Issues:**
- Make sure Gmail API is enabled in Google Cloud Console
- Verify redirect URI `http://localhost` is added to OAuth2 credentials
- Check that refresh token was generated correctly
- Refresh tokens don't expire but can be revoked by user

**Receipt Email Issues:**
- Receipts are only sent if donor provides email address
- Check that `FROM_EMAIL` is configured in `.env`
- Review logs for specific SMTP error messages

**Notification Email Issues:**
- Configure `NOTIFICATION_EMAIL` in `.env` for your organization
- Ensure the SMTP account has permission to send to this address
- Ensure the SMTP account has permission to send to external addresses

## Security Considerations

- Keep Stripe API keys secure and never commit them to version control
- Use test mode during development and switch to live mode only for production
- The application runs on port 8080 - restrict access as needed
- Consider using HTTPS in production (add a reverse proxy like nginx)
- Regularly update dependencies for security patches

## Customization

### Changing Default Amounts

Edit `MEMBERSHIP_AMOUNT` in `.env` file (amount in cents):
```env
MEMBERSHIP_AMOUNT=2500  # $25.00
```

### Modifying the Interface

- Edit `templates/index.html` to change the UI
- Add custom CSS in the `<style>` section
- Modify button text, colors, or layout as needed

### Adding Features

The Flask application (`app/main.py`) can be extended with:
- Email receipts
- Payment reporting
- Custom donation amounts/tiers
- Member information collection
- Integration with other systems

### Environment-Specific Settings

For different environments (development/production):

```env
# Development
FLASK_ENV=development
STRIPE_SECRET_KEY=sk_test_...

# Production  
FLASK_ENV=production
STRIPE_SECRET_KEY=sk_live_...
```

## File Structure

```
pos-docker/
├── app/
│   └── main.py              # Flask application
├── templates/
│   └── index.html           # Web interface
├── static/                  # Static assets (currently empty)
├── docker-compose.yml       # Docker Compose configuration
├── Dockerfile              # Container image definition
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (create this)
└── README.md               # This file
```

## Support

For issues with:
- **Stripe integration**: Check [Stripe Terminal documentation](https://stripe.com/docs/terminal)
- **Application bugs**: Check logs with `docker compose logs -f`
- **Docker issues**: Ensure Docker and Docker Compose are properly installed

## License

This is a simple utility application. Modify and use as needed for your community organization.