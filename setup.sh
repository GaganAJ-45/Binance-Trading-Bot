#!/bin/bash

# Binance Futures Trading Bot - Setup Script
# This script helps you set up the trading bot quickly

echo "🤖 Binance Futures Trading Bot - Setup Script"
echo "=============================================="
echo ""

# Check Python version
echo "📋 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "   Found: Python $python_version"

# Check if Python 3.8+
if ! python3 -c 'import sys; assert sys.version_info >= (3,8)' 2>/dev/null; then
    echo "❌ Error: Python 3.8 or higher is required"
    exit 1
fi
echo "✅ Python version OK"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt --quiet
if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi
echo ""

# Set up .env file
if [ ! -f .env ]; then
    echo "📝 Setting up environment variables..."
    cp .env.example .env
    echo "✅ Created .env file from template"
    echo ""
    echo "⚠️  IMPORTANT: Please edit the .env file and add your Binance Testnet API credentials"
    echo "   1. Open .env file in a text editor"
    echo "   2. Replace 'your_api_key_here' with your actual API key"
    echo "   3. Replace 'your_api_secret_here' with your actual API secret"
    echo ""
else
    echo "ℹ️  .env file already exists, skipping..."
    echo ""
fi

# Create logs directory
if [ ! -d logs ]; then
    mkdir logs
    echo "✅ Created logs directory"
else
    echo "ℹ️  logs directory already exists"
fi
echo ""

# Test installation
echo "🧪 Testing installation..."
python3 -c "from bot import BinanceTestnetClient, OrderManager; print('✅ All modules imported successfully')"
echo ""

echo "=============================================="
echo "✅ Setup complete!"
echo ""
echo "📚 Next steps:"
echo "   1. Get your Binance Testnet API credentials:"
echo "      https://testnet.binancefuture.com/"
echo ""
echo "   2. Edit the .env file with your credentials:"
echo "      nano .env  (or use your preferred editor)"
echo ""
echo "   3. Test the connection:"
echo "      python3 cli.py test"
echo ""
echo "   4. Place your first order:"
echo "      python3 cli.py place -s BTCUSDT -d BUY -t MARKET -q 0.001"
echo ""
echo "🎉 Happy trading!"
echo "=============================================="
