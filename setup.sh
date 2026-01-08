#!/bin/bash

# Interactive setup script for Telegram X Link Moderator Bot

clear
echo "🤖 ================================================"
echo "   X-Gate: Telegram X Link Moderator Bot Setup"
echo "   ================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed."
    echo ""
    echo "Please install Python 3.11 or higher:"
    echo "  macOS: brew install python@3.11"
    echo "  Ubuntu: sudo apt install python3.11"
    echo "  Windows: Download from python.org"
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"
echo ""

# Check if this is first-time setup
FIRST_TIME=false
if [ ! -f ".env" ] && [ ! -f "config.yml" ]; then
    FIRST_TIME=true
fi

if [ "$FIRST_TIME" = true ]; then
    echo "📋 First-time setup detected!"
    echo ""
    echo "Let's get your bot token first..."
    echo ""
    echo "Steps to get a bot token:"
    echo "  1. Open Telegram and search for @BotFather"
    echo "  2. Send /newbot to BotFather"
    echo "  3. Follow the instructions to create your bot"
    echo "  4. Copy the bot token you receive"
    echo ""
    read -p "Paste your bot token here: " BOT_TOKEN

    if [ -z "$BOT_TOKEN" ]; then
        echo "❌ No token provided. Exiting."
        exit 1
    fi

    # Save to .env file
    echo "TELEGRAM_BOT_TOKEN=$BOT_TOKEN" > .env
    echo ""
    echo "✅ Token saved to .env file"
    echo ""

    # Ask if user wants to customize settings
    echo "⚙️  Configuration (optional)"
    echo ""
    read -p "Customize settings? (y/N): " CUSTOMIZE

    if [[ "$CUSTOMIZE" =~ ^[Yy]$ ]]; then
        echo ""
        read -p "Max X links per user per week [default: 3]: " MAX_LINKS
        MAX_LINKS=${MAX_LINKS:-3}

        read -p "Require context with links? (Y/n): " REQUIRE_CONTEXT
        if [[ "$REQUIRE_CONTEXT" =~ ^[Nn]$ ]]; then
            REQUIRE_CONTEXT=false
        else
            REQUIRE_CONTEXT=true
        fi

        if [ "$REQUIRE_CONTEXT" = true ]; then
            read -p "Minimum context characters [default: 30]: " MIN_CONTEXT
            MIN_CONTEXT=${MIN_CONTEXT:-30}
        else
            MIN_CONTEXT=30
        fi

        # Create config.yml with custom settings
        cat > config.yml << EOF
telegram:
  bot_token: "YOUR_BOT_TOKEN_HERE"  # Token is loaded from .env

rules:
  max_links_per_week: $MAX_LINKS
  require_context: $REQUIRE_CONTEXT
  min_context_length: $MIN_CONTEXT
  count_per_link: true

messages:
  rate_limit: "⚠️ You've hit your weekly limit ({max} X links per week)"
  no_context: "⚠️ X links require context (minimum {min} characters)"
  approaching_limit: "ℹ️ You have {remaining} X link(s) remaining this week"
EOF
        echo ""
        echo "✅ Custom configuration saved to config.yml"
    else
        echo ""
        echo "✅ Using default settings (3 links/week, context required)"
    fi
else
    echo "✅ Configuration found (.env or config.yml exists)"

    # Check if token is set
    if [ -f ".env" ]; then
        source .env
        if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
            echo "⚠️  .env file exists but TELEGRAM_BOT_TOKEN is empty"
            read -p "Enter your bot token: " BOT_TOKEN
            echo "TELEGRAM_BOT_TOKEN=$BOT_TOKEN" > .env
        fi
    fi
fi

echo ""
echo "📦 Installing dependencies..."
echo ""

# Install Python dependencies
pip3 install -q -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    echo "Try running: pip3 install -r requirements.txt"
    exit 1
fi

# Create data directory for database
mkdir -p data
echo "✅ Created data directory for database"

echo ""
echo "🎉 ================================================"
echo "   Setup Complete!"
echo "   ================================================"
echo ""
echo "Next steps:"
echo ""
echo "1️⃣  Start the bot:"
echo "    python3 bot.py"
echo ""
echo "2️⃣  Add the bot to your Telegram group"
echo ""
echo "3️⃣  Make the bot an admin with 'Delete Messages' permission"
echo ""
echo "4️⃣  Test it with /start command in the group"
echo ""
echo "Commands you can use in groups:"
echo "  /start    - View bot rules"
echo "  /stats    - Check your usage"
echo "  /diagnose - Test if bot is configured correctly"
echo ""
echo "================================================"
echo ""

# Ask if user wants to start the bot now
read -p "Start the bot now? (Y/n): " START_NOW

if [[ ! "$START_NOW" =~ ^[Nn]$ ]]; then
    echo ""
    echo "🚀 Starting bot..."
    echo ""
    python3 bot.py
else
    echo ""
    echo "Run 'python3 bot.py' when you're ready to start!"
fi
