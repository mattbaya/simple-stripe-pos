# Community POS System (Railway Version)

A lightweight point-of-sale application for community organizations to process in-person donations and membership payments using Stripe Terminal hardware. **Optimized for Railway deployment with ~$3/year operating costs for sporadic use.**

**🐳 Docker Version:** For full-featured Docker deployment with SSL/domain management, see the [Docker version](https://github.com/mattbaya/simple-stripe-pos).

## Cost-Effective Deployment

Perfect for organizations that use their POS system **several times per year**:
- **Railway.app**: Pay only when running (~$0.10/hour)
- **Annual cost**: ~$3/year for 28 hours of usage (7 events × 4 hours each)
- **Auto-sleep**: Automatically stops when inactive to minimize costs
- **Instant activation**: Scale up 30 minutes before your event

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
- **Automatic HTTPS**: SSL certificates handled by Railway
- No local database required - all data handled by Stripe

## Quick Railway Deployment

### 1. Fork this Repository
1. Click "Fork" on this GitHub repo
2. This gives you your own copy to deploy

### 2. Connect to Railway
1. Go to [railway.app](https://railway.app) and sign up
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your forked repository
4. Railway automatically detects Flask and deploys

### 3. Configure Environment Variables
In Railway dashboard, add these variables:

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

### 4. Set Custom Domain (Optional)
- In Railway settings, add your custom domain (e.g., pos.yourdomain.org)
- Or use the provided Railway URL

### 5. Configure Auto-Sleep
- **Default**: Railway automatically sleeps after inactivity
- **Manual Control**: Use Railway dashboard to start/stop as needed
- **Cost**: $0/month when sleeping, ~$0.10/hour when active

## Pre-Event Checklist

**30 minutes before your event:**
1. Open Railway dashboard
2. Ensure app is running (wake from sleep if needed)
3. Test payment flow with a small amount
4. Confirm Stripe terminal is online
5. Share payment URL with volunteers

**After your event:**
1. App automatically sleeps after ~30 minutes of inactivity
2. Check Railway dashboard to confirm it's sleeping
3. Review payments in Stripe dashboard

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