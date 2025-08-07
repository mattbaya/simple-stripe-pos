#!/bin/bash

# Community POS System - Startup Script
# Run this script to start the POS system

set -e

echo "Starting Community POS System..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo "Please copy .env.example to .env and configure your Stripe keys:"
    echo "  cp .env.example .env"
    echo "  nano .env"
    exit 1
fi

# Check if required environment variables are set
source .env

if [ -z "$STRIPE_SECRET_KEY" ] || [ "$STRIPE_SECRET_KEY" = "sk_test_your_secret_key_here" ]; then
    echo "❌ Error: STRIPE_SECRET_KEY not configured in .env file"
    exit 1
fi

if [ -z "$STRIPE_LOCATION_ID" ] || [ "$STRIPE_LOCATION_ID" = "tml_your_location_id_here" ]; then
    echo "❌ Error: STRIPE_LOCATION_ID not configured in .env file"
    exit 1
fi

echo "✅ Configuration looks good"

# Stop any existing containers
echo "🛑 Stopping any existing containers..."
docker compose down --remove-orphans

# Build and start
echo "🔨 Building application..."
docker compose build

echo "🚀 Starting application..."
docker compose up -d

# Wait a moment for startup
sleep 5

# Check health
if curl -f http://localhost:8080/health &>/dev/null; then
    echo "✅ POS System is running successfully!"
    echo "📱 Access the application at: http://bolt.svaha.com:8080"
    echo "📋 Check logs with: docker compose logs -f"
    echo "🛑 Stop with: docker compose down"
else
    echo "❌ Application may not be responding correctly"
    echo "Check logs: docker compose logs -f"
    exit 1
fi