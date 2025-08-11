#!/usr/bin/env python3
"""
Test script to send a raffle purchase confirmation email
Usage: python3 test_raffle_email.py
"""
import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from main import send_raffle_email

# Test with 5 tickets ($5 total, $1.00 per ticket)
payer_email = "info@southwilliamstown.org"
payer_name = "Test Customer"
amount = 500  # $5.00 in cents
raffle_quantity = 5
transaction_id = "test_payment_intent_12345"

print("Sending test raffle email...")
try:
    result = send_raffle_email(payer_email, payer_name, amount, raffle_quantity, transaction_id)
    if result:
        print("✅ Test raffle email sent successfully!")
        print(f"Sent to: {payer_email}")
        print(f"Tickets: {raffle_quantity}")
        print(f"Amount: ${amount/100:.2f}")
        print(f"Price per ticket: $1.00")
    else:
        print("❌ Failed to send test raffle email")
except Exception as e:
    print(f"❌ Error sending test raffle email: {str(e)}")

print("\nTo test other quantities:")
print("- Change raffle_quantity to 12 (should show $0.83 per ticket)")
print("- Change raffle_quantity to 25 (should show $0.80 per ticket)")
print("- Change raffle_quantity to 30 (should show $0.80 per ticket)")