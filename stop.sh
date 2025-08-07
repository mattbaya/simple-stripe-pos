#!/bin/bash

# Community POS System - Stop Script
# Run this script to stop the POS system

echo "🛑 Stopping Community POS System..."

docker compose down

echo "✅ POS System stopped successfully"
echo "🚀 Start again with: ./start.sh or docker compose up -d"