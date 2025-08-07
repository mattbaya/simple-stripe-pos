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
    
    try:
        # Run OAuth2 flow
        flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
        
        print("\n🔐 Starting OAuth2 flow for headless servers...")
        print("Please follow these instructions:")
        print("1. The script will now print a URL.")
        print("2. Open that URL in a web browser on any machine (e.g., your laptop).")
        print("3. Log in to your Google account and grant the requested permissions.")
        print("4. After authorization, Google will provide you with a code.")
        print("5. Copy that code and paste it back here when prompted.\n")

        credentials = flow.run_console()
        
        print("\n✅ Authorization successful!")
        print("\n📋 Add these values to your .env file:")
        print("=" * 50)
        print(f"GOOGLE_CLIENT_ID={client_id}")
        print(f"GOOGLE_CLIENT_SECRET={client_secret}")
        print(f"GOOGLE_REFRESH_TOKEN={credentials.refresh_token}")
        print(f"FROM_EMAIL={credentials.token.get('email', 'your_email@domain.com')}")
        print("=" * 50)
        
        # Save to file as well
        with open('.env.oauth', 'w') as f:
            f.write(f"# OAuth2 configuration generated on {__import__('datetime').datetime.now()}\n")
            f.write(f"GOOGLE_CLIENT_ID={client_id}\n")
            f.write(f"GOOGLE_CLIENT_SECRET={client_secret}\n")
            f.write(f"GOOGLE_REFRESH_TOKEN={credentials.refresh_token}\n")
            f.write(f"# FROM_EMAIL=your_email@domain.com\n")
        
        print(f"\n💾 Configuration also saved to .env.oauth")
        print("⚠️  Keep these credentials secure and never commit them to version control!")
        
    except Exception as e:
        print(f"\n❌ Error during OAuth2 flow: {str(e)}")
        print("🔧 Make sure you have:")
        print("   - Enabled Gmail API in Google Cloud Console")
        print("   - Added http://localhost to authorized redirect URIs")
        print("   - Installed required dependencies: pip install google-auth-oauthlib")

if __name__ == "__main__":
    print("🚀 Gmail OAuth2 Token Generator")
    print("=" * 40)
    generate_refresh_token()