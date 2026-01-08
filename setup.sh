#!/bin/bash

# Setup script for Telegram X Link Moderator Bot

echo "==================================="
echo "X Link Moderator Bot - Quick Setup"
echo "==================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11 or higher."
    exit 1
fi

echo "✓ Python 3 found"

# Check if Docker is installed (optional)
if command -v docker &> /dev/null; then
    echo "✓ Docker found"
    DOCKER_AVAILABLE=true
else
    echo "ℹ Docker not found (optional for local development)"
    DOCKER_AVAILABLE=false
fi

echo ""
echo "Setting up the bot..."
echo ""

# Create data directory
mkdir -p data
echo "✓ Created data directory"

# Check if config.yml exists
if [ ! -f "config.yml" ]; then
    echo "❌ config.yml not found!"
    echo "Please create config.yml and add your bot token."
    echo "You can copy config.example.yml as a template:"
    echo "  cp config.example.yml config.yml"
    echo ""
    exit 1
fi

# Check if bot token is set
if grep -q "YOUR_BOT_TOKEN_HERE" config.yml; then
    echo "⚠️  Bot token not configured!"
    echo "Please edit config.yml and replace YOUR_BOT_TOKEN_HERE with your actual bot token."
    echo "Get your token from: https://t.me/BotFather"
    echo ""
    exit 1
fi

echo "✓ Configuration file found"

# Install dependencies
echo ""
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""
echo "========================================="
echo "✅ Setup complete!"
echo "========================================="
echo ""
echo "To run the bot:"
echo ""
if [ "$DOCKER_AVAILABLE" = true ]; then
    echo "With Docker:"
    echo "  docker-compose up -d"
    echo ""
fi
echo "With Python:"
echo "  python3 bot.py"
echo ""
echo "========================================="
