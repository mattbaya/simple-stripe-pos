import os
import logging
import smtplib
import json
import base64
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, render_template, request, jsonify
import stripe
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder='../templates', static_folder='../static')

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
STRIPE_LOCATION_ID = os.getenv('STRIPE_LOCATION_ID')
MEMBERSHIP_AMOUNT = int(os.getenv('MEMBERSHIP_AMOUNT', '2000'))  # $20 in cents

# Email configuration
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
FROM_EMAIL = os.getenv('FROM_EMAIL')
NOTIFICATION_EMAIL = os.getenv('NOTIFICATION_EMAIL')
ORGANIZATION_NAME = os.getenv('ORGANIZATION_NAME', 'Community Organization')
ORGANIZATION_LOGO = os.getenv('ORGANIZATION_LOGO', '/static/logo.png')
ORGANIZATION_WEBSITE = os.getenv('ORGANIZATION_WEBSITE', '')

# OAuth2 configuration
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
GOOGLE_REFRESH_TOKEN = os.getenv('GOOGLE_REFRESH_TOKEN')

# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def get_gmail_credentials():
    """Get valid Gmail credentials using OAuth2"""
    if not all([GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REFRESH_TOKEN]):
        logger.warning("OAuth2 configuration incomplete")
        return None
    
    try:
        # Create credentials from the refresh token
        credentials = Credentials(
            token=None,
            refresh_token=GOOGLE_REFRESH_TOKEN,
            token_uri='https://oauth2.googleapis.com/token',
            client_id=GOOGLE_CLIENT_ID,
            client_secret=GOOGLE_CLIENT_SECRET,
            scopes=SCOPES
        )
        
        # Refresh the token if needed
        if not credentials.valid:
            credentials.refresh(Request())
        
        return credentials
        
    except Exception as e:
        logger.error(f"Failed to get Gmail credentials: {str(e)}")
        return None

def send_email(to_email, subject, body, is_html=False):
    """Send an email using OAuth2 authenticated SMTP"""
    if not FROM_EMAIL:
        logger.warning("FROM_EMAIL not configured - skipping email send")
        return False
    
    credentials = get_gmail_credentials()
    if not credentials:
        logger.warning("Could not get valid credentials - skipping email send")
        return False
    
    try:
        msg = MIMEMultipart('alternative')
        msg['From'] = FROM_EMAIL
        msg['To'] = to_email
        msg['Subject'] = subject
        
        if is_html:
            msg.attach(MIMEText(body, 'html'))
        else:
            msg.attach(MIMEText(body, 'plain'))
        
        # Use OAuth2 for SMTP authentication
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        
        # OAuth2 authentication string
        auth_string = f"user={FROM_EMAIL}\x01auth=Bearer {credentials.token}\x01\x01"
        auth_string = base64.b64encode(auth_string.encode()).decode()
        
        server.docmd('AUTH', 'XOAUTH2 ' + auth_string)
        server.send_message(msg)
        server.quit()
        
        logger.info(f"Email sent successfully to {to_email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {str(e)}")
        return False

def send_receipt_email(payer_email, payer_name, amount, payment_type, transaction_id):
    """Send receipt email to the donor"""
    if not payer_email:
        return False
    
    amount_dollars = amount / 100
    date_str = datetime.now().strftime('%B %d, %Y at %I:%M %p')
    
    subject = f"Receipt for your {payment_type} - {ORGANIZATION_NAME}"
    
    body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
        <div style="text-align: center; margin-bottom: 30px;">
            <h1 style="color: #2c5aa0;">{ORGANIZATION_NAME}</h1>
            <h2 style="color: #666;">Payment Receipt</h2>
        </div>
        
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
            <h3 style="margin-top: 0; color: #28a745;">Thank you for your {payment_type}!</h3>
            <p><strong>Name:</strong> {payer_name}</p>
            <p><strong>Amount:</strong> ${amount_dollars:.2f}</p>
            <p><strong>Type:</strong> {payment_type.title()}</p>
            <p><strong>Date:</strong> {date_str}</p>
            <p><strong>Transaction ID:</strong> {transaction_id}</p>
        </div>
        
        <div style="border-top: 1px solid #ddd; padding-top: 20px; font-size: 14px; color: #666;">
            <p>This receipt serves as confirmation of your payment. Please keep this for your records.</p>
            <p>If you have any questions, please contact us at {NOTIFICATION_EMAIL}</p>
        </div>
        
        <div style="text-align: center; margin-top: 30px; font-size: 12px; color: #999;">
            <p>{ORGANIZATION_NAME}<br>
            Thank you for supporting our community!</p>
        </div>
    </body>
    </html>
    """
    
    return send_email(payer_email, subject, body, is_html=True)

def send_notification_email(payer_name, payer_email, amount, payment_type, transaction_id):
    """Send notification email to the organization"""
    amount_dollars = amount / 100
    date_str = datetime.now().strftime('%B %d, %Y at %I:%M %p')
    
    subject = f"New {payment_type} received - ${amount_dollars:.2f}"
    
    body = f"""
New payment received through the POS system:

PAYMENT DETAILS:
- Type: {payment_type.title()}
- Amount: ${amount_dollars:.2f}
- Donor: {payer_name}
- Email: {payer_email or 'Not provided'}
- Date: {date_str}
- Transaction ID: {transaction_id}

This payment was processed through Stripe Terminal at your community event.

---
{ORGANIZATION_NAME} POS System
    """
    
    return send_email(NOTIFICATION_EMAIL, subject, body)

@app.route('/')
def index():
    return render_template('index.html', 
                         organization_name=ORGANIZATION_NAME,
                         organization_logo=ORGANIZATION_LOGO,
                         organization_website=ORGANIZATION_WEBSITE)

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

@app.route('/create-payment-intent', methods=['POST'])
def create_payment_intent():
    try:
        data = request.json
        payment_type = data.get('payment_type')
        amount = data.get('amount')
        payer_name = data.get('payer_name', '')
        payer_email = data.get('payer_email', '')
        
        if payment_type == 'membership':
            amount = MEMBERSHIP_AMOUNT
            description = f"Membership payment from {payer_name}"
        else:
            description = f"Donation from {payer_name}"
        
        metadata = {
            'payment_type': payment_type,
            'payer_name': payer_name,
        }
        
        if payer_email:
            metadata['payer_email'] = payer_email
        
        payment_intent = stripe.PaymentIntent.create(
            amount=amount,
            currency='usd',
            payment_method_types=['card_present'],
            capture_method='automatic',
            description=description,
            metadata=metadata
        )
        
        logger.info(f"Created PaymentIntent {payment_intent.id} for {payment_type} amount {amount}")
        
        return jsonify({
            'client_secret': payment_intent.client_secret,
            'id': payment_intent.id
        })
        
    except Exception as e:
        logger.error(f"Error creating payment intent: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/discover-readers', methods=['POST'])
def discover_readers():
    try:
        readers = stripe.terminal.Reader.list(
            location=STRIPE_LOCATION_ID
        )
        
        logger.info(f"Found {len(readers.data)} readers")
        
        return jsonify({
            'readers': [
                {
                    'id': reader.id,
                    'label': reader.label or 'Stripe Reader',
                    'status': reader.status
                } for reader in readers.data
            ]
        })
        
    except Exception as e:
        logger.error(f"Error discovering readers: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/process-payment', methods=['POST'])
def process_payment():
    try:
        data = request.json
        payment_intent_id = data.get('payment_intent_id')
        reader_id = data.get('reader_id')
        
        if not payment_intent_id or not reader_id:
            return jsonify({'error': 'Missing payment_intent_id or reader_id'}), 400
        
        payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        
        reader = stripe.terminal.Reader.process_payment_intent(
            reader_id,
            payment_intent=payment_intent_id
        )
        
        logger.info(f"Processing payment {payment_intent_id} on reader {reader_id}")
        
        return jsonify({
            'status': 'processing',
            'payment_intent_id': payment_intent_id
        })
        
    except Exception as e:
        logger.error(f"Error processing payment: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/payment-status/<payment_intent_id>')
def payment_status(payment_intent_id):
    try:
        payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        
        # If payment succeeded and we haven't sent emails yet, send them now
        if payment_intent.status == 'succeeded' and not payment_intent.metadata.get('emails_sent'):
            payer_name = payment_intent.metadata.get('payer_name', 'Unknown')
            payer_email = payment_intent.metadata.get('payer_email')
            payment_type = payment_intent.metadata.get('payment_type', 'payment')
            
            # Send emails
            receipt_sent = False
            notification_sent = False
            
            if payer_email:
                receipt_sent = send_receipt_email(
                    payer_email, payer_name, payment_intent.amount, 
                    payment_type, payment_intent.id
                )
            
            notification_sent = send_notification_email(
                payer_name, payer_email, payment_intent.amount,
                payment_type, payment_intent.id
            )
            
            # Mark emails as sent to avoid duplicate sends
            try:
                stripe.PaymentIntent.modify(
                    payment_intent_id,
                    metadata={
                        **payment_intent.metadata,
                        'emails_sent': 'true',
                        'receipt_sent': str(receipt_sent),
                        'notification_sent': str(notification_sent)
                    }
                )
            except Exception as e:
                logger.error(f"Error updating payment intent metadata: {str(e)}")
        
        return jsonify({
            'status': payment_intent.status,
            'amount': payment_intent.amount,
            'metadata': payment_intent.metadata
        })
        
    except Exception as e:
        logger.error(f"Error checking payment status: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    required_vars = ['STRIPE_SECRET_KEY', 'STRIPE_LOCATION_ID']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        exit(1)
    
    logger.info("Starting POS application")
    app.run(host='0.0.0.0', port=5000, debug=False)