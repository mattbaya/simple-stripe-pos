# Community POS System (Docker Version)

A lightweight, containerized point-of-sale application for community organizations to process in-person donations and membership payments using Stripe Terminal hardware.

**🚀 Alternative Deployment:** For minimal-cost deployment suitable for occasional use, see the [Railway version](https://github.com/mattbaya/simple-stripe-pos-railway) which costs ~$3/year for sporadic events.

## Features

- **Professional web interface** with donation and membership buttons
- **Two membership tiers**: Individual ($35) and Household ($50)
- Integration with Stripe S700 terminal for card-present transactions
- **Optional fee coverage**: Users can choose to cover 2.9% + $0.30 Stripe processing fees
- Real-time fee calculation with transparent breakdown display
- **Required email validation**: Ensures receipt delivery with HTML5 and JavaScript validation
- Custom donation amounts with dynamic fee calculations
- **Professional HTML email receipts** sent to donors with embedded letterhead using Gmail API with OAuth2
- **Tax-compliant receipt format** with 501(c)(3) information and proper documentation
- **Email notifications** sent to your configured organization email
- **Professional success modal** with organization logo and animated confirmation
- **Automatic reader discovery**: Displays connected terminal status on page load
- Customizable organization branding
- **SSL/HTTPS**: Automatic certificate management via Caddy (standard ports 80/443)
- **Domain enforcement**: Configurable primary domain
- No local database required - all data handled by Stripe
- Containerized with Docker for easy deployment

## Requirements Checklist

To deploy this POS system for your organization, you'll need to provide the following:

### 1. Technical Infrastructure
- [ ] **Docker & Docker Compose**: Installed on server
- [ ] **Domain name**: For production deployment (e.g., reader.yourdomain.org)
- [ ] **SSL certificate**: Automatic via Let's Encrypt/Caddy

### 2. Payment Processing (Stripe)
- [ ] **Stripe Account**: Live account with Terminal capability
- [ ] **Stripe API Keys**: Secret and Publishable keys
- [ ] **Stripe Terminal Location**: Physical location ID from Stripe
- [ ] **Stripe S700 Terminal**: Hardware card reader
- [ ] **Terminal Registration**: Reader registered to your Stripe location

### 3. Email System (Gmail API)
- [ ] **Google Cloud Project**: With Gmail API enabled
- [ ] **OAuth2 Credentials**: Client ID and Client Secret
- [ ] **OAuth2 Refresh Token**: Generated via setup script
- [ ] **Gmail Account**: For sending receipts and notifications
- [ ] **Sender Email Address**: For receipt "From" field
- [ ] **Notification Email Address**: Where payment alerts are sent

### 4. Organization Branding & Content
- [ ] **Organization Name**: Full legal name
- [ ] **Organization Website**: URL for receipts and branding
- [ ] **Logo Image**: For web interface (PNG/JPG, ~150x150px)
- [ ] **Letterhead Image**: For email receipts (PNG/JPG, landscape format)
- [ ] **501(c)(3) Tax ID**: For tax-compliant receipts (if applicable)
- [ ] **Donation Acknowledgment Text**: Custom message for donors
- [ ] **Contact Email**: For donor questions and support

### 5. Financial Configuration
- [ ] **Membership Amounts**: Individual and household prices (in cents)
- [ ] **Fee Coverage Policy**: Whether to offer Stripe fee coverage option
- [ ] **Payment Processing Terms**: Legal compliance and policies

### 6. Generic Example Assets (Provided)

For organizations getting started, we provide generic examples:
- [x] **Example Logo**: `static/example-logo.svg` (convert to PNG)
- [x] **Example Letterhead**: `templates/example-letterhead.svg` (convert to PNG)  
- [x] **Generic Email Template**: `templates/donor_acknowledgment_email_template.html`
- [x] **Graphics Setup Guide**: `GRAPHICS_SETUP.md` with detailed instructions
- [x] **Sample Donor Text**: Based on standard 501(c)(3) language

## Prerequisites (SWCA-Specific)

1. **Stripe Account**: Live account with Terminal enabled ✅
2. **Stripe S700 Terminal**: SWCA S700 Reader (tmr_GJIc8gfqlW1SF1) - Online ✅
3. **Docker & Docker Compose**: Installed on server ✅
4. **Domain**: reader.southwilliamstown.org configured ✅

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
- OAuth2 is configured and working ✅
- Gmail API credentials are properly set up
- Transaction notifications are sent to info@southwilliamstown.org
- Receipts are sent to donors who provide email addresses
- OAuth2 refresh tokens don't expire unless revoked

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

### 2. Environment Configuration

The `.env` file is already configured with:

```env
# Stripe Configuration (Live Keys)
STRIPE_SECRET_KEY=sk_live_... # ✅ Configured
STRIPE_PUBLISHABLE_KEY=pk_live_... # ✅ Configured
STRIPE_LOCATION_ID=tml_GJFbNglXXR3JXh # ✅ Configured

# Membership amounts in cents
INDIVIDUAL_MEMBERSHIP_AMOUNT=3500  # $35.00
HOUSEHOLD_MEMBERSHIP_AMOUNT=5000   # $50.00

# Organization Configuration
ORGANIZATION_NAME="South Williamstown Community Association"
ORGANIZATION_WEBSITE=https://southwilliamstown.org
DOMAIN_NAME=reader.southwilliamstown.org

# Email Configuration (OAuth2)
FROM_EMAIL=info@southwilliamstown.org
NOTIFICATION_EMAIL=info@southwilliamstown.org
GOOGLE_CLIENT_ID=... # ✅ Configured
GOOGLE_CLIENT_SECRET=... # ✅ Configured  
GOOGLE_REFRESH_TOKEN=... # ✅ Configured
```

⚠️ **Security**: Never commit the `.env` file to version control. Keep your API keys secure.

### 3. Start the Application

From the `/home/swca/pos-docker/` directory:

**Development:**
```bash
docker compose up -d
```
Available at: `http://localhost:8080`

**Production:**
```bash
docker compose -f docker-compose.prod.yml up -d
```
Available at:
- HTTP: `http://localhost:8080` (redirects to HTTPS)
- HTTPS: `https://localhost:8443`
- Production: `https://reader.southwilliamstown.org` (standard ports 80/443)

**Management:**
```bash
# Check status
docker compose ps

# View logs
docker compose logs -f

# Stop
docker compose down
```

## Usage

### For Event Volunteers

1. Open https://reader.southwilliamstown.org in a browser
2. Page automatically loads and displays "SWCA S700 Reader (stripe_s700) - online" status
3. For donations:
   - Click "Make a Donation"
   - Enter payer's name and **required** email address
   - Enter donation amount
   - Optionally check "Help us cover processing fees" to add Stripe fees
   - Click "Process Payment"
4. For memberships:
   - Click "Individual Membership ($35)" or "Household Membership ($50)"
   - Enter payer's name and **required** email address
   - Optionally check "Help us cover processing fees" to add Stripe fees
   - Click "Process Payment"
5. Follow prompts on the Stripe terminal to complete payment
6. Professional success modal appears with:
   - Organization logo and animated checkmark
   - Payment details (amount, type, name)
   - Thank you message
   - Receipt confirmation note
7. Click "Close" to dismiss modal and reset form

### Payment Flow

1. Customer inserts, taps, or swipes card on S700 terminal
2. Terminal processes payment through Stripe
3. Professional success modal appears with organization branding
4. **Professional HTML receipt email** automatically sent to donor with:
   - Embedded SWCA letterhead image
   - Tax-compliant 501(c)(3) receipt information
   - Transaction details and professional formatting
   - Consistent organization branding
5. Notification email automatically sent to organization

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

**Current Setup:**
- Reader: SWCA S700 Reader (tmr_GJIc8gfqlW1SF1)
- Status: Online ✅
- Location: tml_GJFbNglXXR3JXh ✅

**If issues occur:**
- Ensure S700 is powered on and connected to WiFi
- Refresh the page to reload reader status automatically
- Check Stripe Dashboard → Terminal → Readers for status
- Use `/admin-readers` page for manual reader management

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
- Email address is now required for all transactions
- Using Gmail API instead of SMTP for reliable delivery ✅
- Check that `FROM_EMAIL` is configured in `.env`
- Review logs for Gmail API error messages

**Notification Email Issues:**
- Configure `NOTIFICATION_EMAIL` in `.env` for your organization
- Ensure the SMTP account has permission to send to this address
- Ensure the SMTP account has permission to send to external addresses

## Security Considerations

- Stripe live API keys are properly configured ✅
- Production environment with live payments ✅
- HTTPS enabled with automatic SSL certificates via Caddy ✅
- Security headers and domain enforcement ✅
- OAuth2 authentication for email services ✅
- Environment files (.env) are gitignored ✅
- Regular dependency updates recommended

## Customization

### Changing Default Amounts

Edit membership amounts in `.env` file (amounts in cents):
```env
INDIVIDUAL_MEMBERSHIP_AMOUNT=4000  # $40.00
HOUSEHOLD_MEMBERSHIP_AMOUNT=6000   # $60.00
```

### Fee Coverage Feature

The application automatically calculates Stripe processing fees (2.9% + $0.30 per transaction) and allows users to optionally cover these fees. When enabled:

- Users see a transparent breakdown: base amount, fee amount, and total
- Fee calculation updates dynamically as donation amounts change
- All payment metadata includes fee information for reporting
- Receipts clearly indicate when fees were covered

Examples:
- $20 donation + fees = $20.88 total (covers $0.88 in processing fees)
- $35 individual membership + fees = $36.32 total (covers $1.32 in processing fees)
- $50 household membership + fees = $51.75 total (covers $1.75 in processing fees)

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
│   ├── index.html           # Web interface
│   ├── donor_acknowledgment_email.html # Professional HTML email template
│   └── donor_acknowledgment_email_template.html # Generic template for other orgs
├── static/                  # Static assets (currently empty)
├── docker-compose.yml       # Docker Compose configuration
├── Dockerfile              # Container image definition
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (create this)
├── donor-ack.txt           # Source text for donation acknowledgment
└── README.md               # This file
```

## Support

For issues with:
- **Stripe integration**: Check [Stripe Terminal documentation](https://stripe.com/docs/terminal)
- **Application bugs**: Check logs with `docker compose logs -f`
- **Docker issues**: Ensure Docker and Docker Compose are properly installed

## License

This is a simple utility application. Modify and use as needed for your community organization.