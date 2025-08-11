# Community POS System (Docker Version)

A lightweight point-of-sale application for community organizations to process in-person donations and membership payments using Stripe Terminal hardware. **Docker deployment with SSL/domain management and enhanced UI features.**

**🚂 Railway Version:** For cost-optimized Railway deployment (~$3/year), see the [Railway version](https://github.com/mattbaya/simple-stripe-pos-railway).

## Docker Deployment Benefits

Perfect for organizations that need reliable, always-available payment processing:
- **Self-hosted control**: Run on your own infrastructure
- **SSL/Domain management**: Automatic HTTPS with Caddy reverse proxy
- **Production ready**: Docker Compose orchestration for stability
- **Local development**: Easy setup for testing and customization

## Features

- **Professional web interface** with donation and membership buttons  
- **Two membership tiers**: Individual ($35) and Household ($50)
- **Renewal donation option**: Members can add additional donations to membership payments
- Integration with Stripe S700 terminal for card-present transactions
- **Conditional fee coverage**: Fee breakdown only shows when users opt to cover 2.9% + $0.30 Stripe processing fees
- **Consistent typography**: All fee text uses 28px font size for better readability
- **Form field reset**: Clean form state when switching between payment types
- **Required email validation**: Ensures receipt delivery with HTML5 and JavaScript validation
- Custom donation amounts with dynamic fee calculations
- **Professional HTML email receipts** sent to donors with embedded letterhead using Gmail API with OAuth2
- **Tax-compliant receipt format** with 501(c)(3) information and proper documentation
- **Email notifications** sent to your configured organization email
- **Professional success modal** with organization logo and animated confirmation
- **Automatic reader discovery**: Displays connected terminal status on page load
- Customizable organization branding
- **Automatic HTTPS**: SSL certificates handled by Caddy reverse proxy
- **Docker orchestration**: Production-ready containerized deployment
- No local database required - all data handled by Stripe

## Quick Docker Deployment

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/simple-stripe-pos.git
cd simple-stripe-pos
```

### 2. Configure Environment Variables
Create a `.env` file with these variables:

```
# Stripe Configuration
STRIPE_SECRET_KEY=sk_live_your_secret_key
STRIPE_LOCATION_ID=tml_your_location_id

# Organization Settings
ORGANIZATION_NAME=Your Community Organization
ORGANIZATION_WEBSITE=https://yourwebsite.org
FROM_EMAIL=contact@yourdomain.org
NOTIFICATION_EMAIL=notifications@yourdomain.org

# Membership Pricing (in cents)
INDIVIDUAL_MEMBERSHIP_AMOUNT=3500  # $35.00
HOUSEHOLD_MEMBERSHIP_AMOUNT=5000   # $50.00

# Gmail OAuth2 (see setup guide below)
GOOGLE_CLIENT_ID=your_client_id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your_client_secret
GOOGLE_REFRESH_TOKEN=your_refresh_token
```

### 3. Set Custom Domain (Optional)
If you want to use your own domain (e.g., pos.yourdomain.org):
1. Update the `DOMAIN_NAME` variable in your `.env` file
2. Point your domain's DNS to your server
3. Caddy will automatically handle SSL certificates

### 4. Deploy with Docker
For **development**:
```bash
docker compose up -d
```

For **production**:
```bash
docker compose -f docker-compose.prod.yml up -d
```

## Quick Start Guide

### Development Setup (localhost:8080)
1. Configure environment variables in `.env`
2. Run: `docker compose up -d`
3. Visit: http://localhost:8080
4. Test with Stripe test terminal

### Production Setup (your-domain.org)
1. Configure environment variables including `DOMAIN_NAME`
2. Run: `docker compose -f docker-compose.prod.yml up -d`
3. Caddy handles SSL automatically
4. Use real Stripe keys and terminal

## Stripe Terminal Setup

### 1. Get API Keys
1. Log in to [Stripe Dashboard](https://dashboard.stripe.com/)
2. Go to Developers → API keys
3. Copy your **Secret key**
4. Switch to live mode for real payments

### 2. Create Location & Register Terminal
1. Terminal → Locations → Create location
2. Terminal → Readers → Register reader
3. Connect S700 to WiFi and enter registration code
4. Copy Location ID (starts with `tml_`)

### 3. Test Connection
1. Deploy to Railway with test keys first
2. Verify terminal shows as "online" in your app
3. Process a test payment
4. Switch to live keys when ready

## Gmail Email Setup

The system sends professional HTML receipts and notifications via Gmail API:

### 1. Google Cloud Setup
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create project and enable Gmail API
3. Create OAuth2 credentials (Desktop application type)
4. Add `http://localhost` to redirect URIs

### 2. Generate Refresh Token
```bash
# Install on your local machine
pip install google-auth-oauthlib

# Run the OAuth flow
python3 generate_oauth_token.py
```

### 3. Add to Railway Environment
Add the generated values to Railway environment variables.

## Cost Management

### Usage Monitoring
- **Railway Dashboard**: Shows exact usage hours and costs
- **Billing**: Monthly billing with per-minute precision
- **Estimates**: ~$0.10-0.20/hour depending on usage

### Cost Examples
| Usage Pattern | Annual Cost |
|--------------|-------------|
| 4 events/year, 4 hours each | ~$2-4/year |
| 12 events/year, 2 hours each | ~$3-6/year |
| Always-on development | ~$15-30/month |

### Optimization Tips
1. **Sleep when not needed**: Railway auto-sleeps after 30 min
2. **Manual control**: Stop service between events
3. **Monitor usage**: Check Railway dashboard monthly
4. **Development**: Use local Docker for development to save Railway costs

## File Structure
```
simple-stripe-pos-railway/
├── app/
│   └── main.py              # Flask application  
├── templates/
│   ├── index.html           # Web interface
│   └── *.html               # Email templates
├── static/                  # Organization assets
├── requirements.txt         # Python dependencies
├── railway.json             # Railway deployment config
├── generate_oauth_token.py  # OAuth2 setup utility
└── README.md               # This file
```

## Management Commands

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export STRIPE_SECRET_KEY=sk_test_...
export STRIPE_LOCATION_ID=tml_...
# ... other variables

# Run locally
python app/main.py
```

### Railway Management
- **Dashboard**: Monitor usage, logs, and costs
- **CLI**: `railway login` and `railway logs` for advanced management
- **Scaling**: Manually start/stop services as needed

## Troubleshooting

### Payment Issues
1. Check Stripe dashboard for detailed error messages
2. Verify terminal is online and connected to WiFi  
3. Ensure you're using live (not test) API keys for real payments
4. Check Railway logs in dashboard

### Email Issues
1. Verify Gmail API is enabled in Google Cloud Console
2. Check OAuth2 credentials and refresh token
3. Test email sending with a small transaction first
4. Review Railway application logs

### Railway-Specific Issues
1. **App won't start**: Check environment variables are set correctly
2. **Timeouts**: Railway has request timeout limits for idle connections
3. **Domain issues**: DNS propagation can take 24-48 hours
4. **Costs higher than expected**: Check if app is sleeping properly

## Security Notes
- Never commit API keys to git
- Use Railway's built-in environment variable encryption
- Enable 2FA on Stripe and Google Cloud accounts  
- Regularly rotate API keys and refresh tokens
- Railway provides HTTPS automatically

## Support Resources
- **Stripe**: [Terminal Documentation](https://stripe.com/docs/terminal)
- **Railway**: [Documentation](https://docs.railway.app)
- **Gmail API**: [Python Quickstart](https://developers.google.com/gmail/api/quickstart/python)

---

**Perfect for**: Community organizations, nonprofits, and small businesses that need occasional payment processing with minimal ongoing costs.