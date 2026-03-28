# 🤖 Binance Futures Trading Bot

> A Python CLI application for automated trading on Binance Futures Testnet with comprehensive logging and error handling.

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-PEP8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)

---

## 📋 Table of Contents

- [Features](#-features)
- [Demo](#-demo)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Documentation](#-documentation)
- [Examples](#-examples)
- [Testing](#-testing)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

- ✅ **MARKET & LIMIT Orders** - Full support for both order types
- ✅ **BUY/SELL Operations** - Complete trading functionality
- ✅ **Input Validation** - Comprehensive parameter checking
- ✅ **Error Handling** - Robust handling of API errors, network failures, and invalid inputs
- ✅ **Structured Logging** - Detailed logs to both file and console
- ✅ **Clean Architecture** - Modular, maintainable, and testable code
- ✅ **CLI Interface** - User-friendly command-line interface built with Click
- ✅ **Type Safety** - Clear parameter validation and type checking
- ✅ **Testnet Safe** - Hardcoded to use Binance Futures Testnet only

---

## 🎬 Demo

### MARKET Order
```bash
$ python cli.py place -s BTCUSDT -d BUY -t MARKET -q 0.001

🔍 Validating order parameters...
✅ Validation successful!

============================================================
ORDER REQUEST SUMMARY
============================================================
Symbol:         BTCUSDT
Side:           BUY
Type:           MARKET
Quantity:       0.001
============================================================

Do you want to proceed with this order? [y/N]: y

🔌 Connecting to Binance Futures Testnet...
✅ Connected successfully!
📊 Current market price: 94523.50

📤 Placing MARKET order...

✅ SUCCESS!
============================================================
ORDER PLACED SUCCESSFULLY
============================================================
Order ID:       12345678901
Symbol:         BTCUSDT
Side:           BUY
Type:           MARKET
Status:         FILLED
Quantity:       0.001
Executed Qty:   0.001
Avg Price:      94523.50
Time:           1711616124892
============================================================
```

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Binance Futures Testnet account

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/binance-futures-bot.git
   cd binance-futures-bot
   ```

2. **Run setup script** (Linux/Mac)
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

   Or manually:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API credentials**
   ```bash
   cp .env.example .env
   # Edit .env and add your Binance Testnet API credentials
   ```

4. **Test connection**
   ```bash
   python cli.py test
   ```

### Getting Testnet Credentials

1. Visit [Binance Futures Testnet](https://testnet.binancefuture.com/)
2. Sign up or log in
3. Navigate to API Management
4. Create a new API key
5. Copy both API Key and Secret Key
6. Add them to your `.env` file

---

## 💻 Usage

### Basic Commands

**Test Connection:**
```bash
python cli.py test
```

**Get Current Price:**
```bash
python cli.py price BTCUSDT
```

**Place MARKET Order:**
```bash
python cli.py place -s BTCUSDT -d BUY -t MARKET -q 0.001
```

**Place LIMIT Order:**
```bash
python cli.py place -s BTCUSDT -d SELL -t LIMIT -q 0.001 -p 95000
```

### Command Options

| Option | Short | Description | Required |
|--------|-------|-------------|----------|
| `--symbol` | `-s` | Trading pair (e.g., BTCUSDT) | Yes |
| `--side` | `-d` | BUY or SELL | Yes |
| `--type` | `-t` | MARKET or LIMIT | Yes |
| `--quantity` | `-q` | Order quantity | Yes |
| `--price` | `-p` | Limit price | For LIMIT only |

### Examples

```bash
# Buy 0.001 BTC at market price
python cli.py place -s BTCUSDT -d BUY -t MARKET -q 0.001

# Sell 0.01 ETH at $3500
python cli.py place -s ETHUSDT -d SELL -t LIMIT -q 0.01 -p 3500

# Check current BTC price
python cli.py price BTCUSDT

# Test your API connection
python cli.py test
```

---

## 📁 Project Structure

```
trading_bot/
├── bot/
│   ├── __init__.py           # Package initialization
│   ├── client.py             # Binance testnet client wrapper
│   ├── orders.py             # Order placement & management
│   ├── validators.py         # Input validation logic
│   └── logging_config.py     # Logging configuration
├── cli.py                    # CLI entry point (Click)
├── examples.py               # Programmatic usage examples
├── requirements.txt          # Python dependencies
├── setup.sh                  # Setup automation script
├── .env.example             # API credentials template
├── .gitignore               # Git ignore rules
├── README.md                # This file
├── QUICK_REFERENCE.md       # Command cheat sheet
├── TROUBLESHOOTING.md       # Common issues & solutions
├── SUBMISSION_CHECKLIST.md  # Pre-submission checklist
└── logs/                    # Log files (auto-generated)
    ├── example_market_order.log
    └── example_limit_order.log
```

---

## 📚 Documentation

- **[Quick Reference](QUICK_REFERENCE.md)** - Command cheat sheet
- **[Troubleshooting Guide](TROUBLESHOOTING.md)** - Common issues and solutions
- **[Submission Checklist](SUBMISSION_CHECKLIST.md)** - Pre-submission verification

---

## 📝 Examples

See `examples.py` for programmatic usage:

```python
from bot import BinanceTestnetClient, OrderManager, validate_order_params

# Initialize client
client = BinanceTestnetClient()

# Validate parameters
params = validate_order_params(
    symbol='BTCUSDT',
    side='BUY',
    order_type='MARKET',
    quantity=0.001
)

# Place order
order_manager = OrderManager(client)
order = order_manager.place_market_order(
    symbol=params['symbol'],
    side=params['side'],
    quantity=params['quantity']
)

print(f"Order placed! ID: {order['orderId']}")
```

---

## 🧪 Testing

Run the example log generation:

```bash
# Test MARKET order
python cli.py place -s BTCUSDT -d BUY -t MARKET -q 0.001

# Test LIMIT order
python cli.py place -s BTCUSDT -d SELL -t LIMIT -q 0.001 -p 95000

# Check logs
ls -l logs/
```

Logs include:
- Timestamp for each operation
- Input validation details
- API request/response payloads
- Error messages with stack traces
- Order confirmation details

---

## 🔧 Troubleshooting

**Common Issues:**

| Issue | Solution |
|-------|----------|
| API credentials not found | Edit `.env` file with your keys |
| Invalid symbol error | Use uppercase (BTCUSDT not btcusdt) |
| Connection failed | Verify testnet credentials |
| Insufficient balance | Get funds from testnet faucet |

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for detailed solutions.

---

## 🤝 Contributing

This is a submission project for an internship application. However, suggestions and feedback are welcome!

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- Built using [python-binance](https://github.com/sammchardy/python-binance)
- CLI powered by [Click](https://click.palletsprojects.com/)
- Created as part of Python Developer Intern application

---

## 📧 Contact

For questions or feedback about this submission:
- **Application:** Python Developer Intern @ Anything.ai
- **Submitted to:** joydip@anything.ai, chetan@anything.ai, hello@anything.ai

---

**⚠️ Disclaimer:** This bot is for educational purposes and testnet use only. Never use testnet code with mainnet credentials.

---

Made with ❤️ for learning and growth
