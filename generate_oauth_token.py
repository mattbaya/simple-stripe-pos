#!/usr/bin/env python3
"""
OAuth2 Token Generator for Gmail API

This script helps you generate a refresh token for the POS system to send emails
using Google OAuth2 authentication.

Prerequisites:
1. Google Cloud Console project with Gmail API enabled
2. OAuth2 credentials (client ID and secret)
3. Python with google-auth-oauthlib installed

Usage:
    python3 generate_oauth_token.py
"""

import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow

# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def generate_refresh_token():
    """Generate OAuth2 refresh token for Gmail API"""
    
    # Get client credentials
    client_id = input("Enter your Google Client ID: ").strip()
    client_secret = input("Enter your Google Client Secret: ").strip()
    
    if not client_id or not client_secret:
        print("❌ Client ID and Secret are required!")
        return
    
    # Create client config
    client_config = {
        "installed": {
            "client_id": client_id,
            "client_secret": client_secret,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": ["http://localhost"]
        }
    }
    
    import urllib.parse

# ... (rest of the imports)

# ... (rest of the file until the try block)

    try:
        # Manually construct the authorization URL to ensure correctness
        base_auth_url = "https://accounts.google.com/o/oauth2/auth"
        params = {
            'client_id': client_id,
            'redirect_uri': 'http://localhost',
            'response_type': 'code',
            'scope': ' '.join(SCOPES),
            'access_type': 'offline',
            'prompt': 'consent'
        }
        auth_url = f"{base_auth_url}?{urllib.parse.urlencode(params)}"

        print("\n🔐 Starting OAuth2 flow for headless servers...")
        print("\n1. Open this URL in your browser on any machine:")
        print(f"\n{auth_url}\n")
        print("2. After you grant permissions, your browser will show a 'This site can’t be reached' error. This is expected.")
        print("3. Copy the ENTIRE URL from your browser's address bar (it will start with 'http://localhost').")
        
        # Get the full redirect URL from the user
        redirect_url = input("\n4. Paste the full URL from your browser here: ").strip()
        
        # Extract the authorization code from the redirect URL
        code = urllib.parse.parse_qs(urllib.parse.urlparse(redirect_url).query)['code'][0]

        # Manually exchange the code for a token
        flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
        flow.redirect_uri = 'http://localhost'  # Explicitly set the redirect_uri for the token exchange
        flow.fetch_token(code=code)
        credentials = flow.credentials

        print("\n✅ Authorization successful!")
        print("\n📋 Add these values to your .env file:")
        print("=" * 50)
        print(f"GOOGLE_CLIENT_ID={client_id}")
        print(f"GOOGLE_CLIENT_SECRET={client_secret}")
        print(f"GOOGLE_REFRESH_TOKEN={credentials.refresh_token}")
        
        # Prompt for the email since it's not always in the response
        from_email = input("Enter the Google email address you just authorized: ").strip()
        print(f"FROM_EMAIL={from_email}")
        print("=" * 50)
        
        # Save to file as well
        with open('.env.oauth', 'w') as f:
            f.write(f"# OAuth2 configuration generated on {__import__('datetime').datetime.now()}\n")
            f.write(f"GOOGLE_CLIENT_ID={client_id}\n")
            f.write(f"GOOGLE_CLIENT_SECRET={client_secret}\n")
            f.write(f"GOOGLE_REFRESH_TOKEN={credentials.refresh_token}\n")
            f.write(f"FROM_EMAIL={from_email}\n")
        
        print(f"\n💾 Configuration also saved to .env.oauth")
        print("⚠️  Keep these credentials secure and never commit them to version control!")
        
    except Exception as e:
        print(f"\n❌ Error during OAuth2 flow: {str(e)}")
        print("🔧 Make sure you have:")
        print("   - Enabled Gmail API in Google Cloud Console")
        print("   - Correctly copied the full authorization code")
        print("   - Added http://localhost to authorized redirect URIs")
        print("   - Installed required dependencies: pip install google-auth-oauthlib")

if __name__ == "__main__":
    print("🚀 Gmail OAuth2 Token Generator")
    print("=" * 40)
    generate_refresh_token()