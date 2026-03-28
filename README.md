# Binance Futures Trading Bot

A Python CLI application for placing orders on **Binance Futures Testnet (USDT-M)** with clean structure, proper logging, and comprehensive error handling.

## 🎯 Features

- ✅ Place **MARKET** and **LIMIT** orders
- ✅ Support for **BUY** and **SELL** sides
- ✅ Input validation and error handling
- ✅ Structured logging to file and console
- ✅ Clean, modular code architecture
- ✅ User-friendly CLI with Click
- ✅ Connection testing utilities

## 📁 Project Structure

```
trading_bot/
├── bot/
│   ├── __init__.py          # Package initialization
│   ├── client.py            # Binance client wrapper
│   ├── orders.py            # Order placement logic
│   ├── validators.py        # Input validation
│   └── logging_config.py    # Logging configuration
├── cli.py                   # CLI entry point
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
├── logs/                   # Log files (auto-created)
└── README.md              # This file
```

## 🚀 Setup Instructions

### 1. Prerequisites

- Python 3.8 or higher
- Binance Futures Testnet account

### 2. Get Binance Testnet API Credentials

1. Visit [Binance Futures Testnet](https://testnet.binancefuture.com/)
2. Register/Login with your email
3. Navigate to API Key Management
4. Generate a new API Key and Secret
5. Save both credentials securely

### 3. Installation

1. **Clone or download this repository**

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   # Copy the example env file
   cp .env.example .env
   
   # Edit .env and add your credentials
   # BINANCE_API_KEY=your_api_key_here
   # BINANCE_API_SECRET=your_api_secret_here
   ```

4. **Test the connection:**
   ```bash
   python cli.py test
   ```

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

**Place a MARKET Order:**
```bash
python cli.py place -s BTCUSDT -d BUY -t MARKET -q 0.001
```

**Place a LIMIT Order:**
```bash
python cli.py place -s BTCUSDT -d SELL -t LIMIT -q 0.001 -p 95000
```

### Command Options

```
Options:
  -s, --symbol TEXT       Trading pair symbol (e.g., BTCUSDT) [required]
  -d, --side TEXT         Order side: BUY or SELL [required]
  -t, --type TEXT         Order type: MARKET or LIMIT [required]
  -q, --quantity FLOAT    Order quantity [required]
  -p, --price FLOAT       Limit price (required for LIMIT orders)
  --help                  Show help message
```

### Example Workflow

1. **Test connection:**
   ```bash
   python cli.py test
   ```

2. **Check current price:**
   ```bash
   python cli.py price BTCUSDT
   ```

3. **Place a MARKET BUY order:**
   ```bash
   python cli.py place -s BTCUSDT -d BUY -t MARKET -q 0.001
   ```
   
4. **Place a LIMIT SELL order:**
   ```bash
   python cli.py place -s ETHUSDT -d SELL -t LIMIT -q 0.01 -p 3500
   ```

## 📊 Logging

All operations are logged to:
- **Console:** Real-time output with colored indicators
- **Log files:** `logs/trading_bot_YYYYMMDD_HHMMSS.log`

Log files include:
- Timestamp for each operation
- Input validation details
- API request/response details
- Error messages with full stack traces
- Order confirmation details

## ✅ Validation & Error Handling

The bot validates:
- ✅ Symbol format (must be valid trading pair)
- ✅ Side (must be BUY or SELL)
- ✅ Order type (must be MARKET or LIMIT)
- ✅ Quantity (must be positive number)
- ✅ Price (required for LIMIT, must be positive)

Error handling covers:
- ❌ Invalid input parameters
- ❌ API authentication errors
- ❌ Network failures
- ❌ Insufficient balance
- ❌ Invalid symbols or trading pairs

## 🧪 Testing Examples

### MARKET Order Test
```bash
# BUY 0.001 BTC at market price
python cli.py place -s BTCUSDT -d BUY -t MARKET -q 0.001
```

**Expected log output:**
- Validation confirmation
- Current market price
- Order request details
- Order execution confirmation
- Order ID and status

### LIMIT Order Test
```bash
# SELL 0.001 BTC at limit price 95000
python cli.py place -s BTCUSDT -d SELL -t LIMIT -q 0.001 -p 95000
```

**Expected log output:**
- Validation confirmation
- Current market price (for reference)
- Limit price confirmation
- Order placement confirmation
- Order ID (order will remain open until filled or cancelled)

## 🔧 Assumptions & Design Decisions

1. **Testnet Only:** Hardcoded to use Binance Futures Testnet URL
2. **USDT-M Futures:** Designed for USDT-margined futures contracts
3. **GTC Time-in-Force:** LIMIT orders use "Good Till Cancelled" by default
4. **Confirmation Prompt:** Added interactive confirmation before placing orders
5. **Logging Strategy:** Dual logging to both file and console for better debugging
6. **Price Display:** Shows current market price before placing orders for context

## 🛡️ Security Notes

- ⚠️ Never commit your `.env` file to version control
- ⚠️ Use testnet credentials only (never mainnet)
- ⚠️ Keep your API keys secure and rotate them regularly
- ⚠️ The `.env` file is included in `.gitignore` by default

## 📝 Dependencies

- `python-binance`: Official Binance API wrapper
- `click`: For building the CLI interface
- `python-dotenv`: For environment variable management
- `requests`: HTTP library (dependency of python-binance)

## 🐛 Troubleshooting

**Connection Issues:**
- Verify your API credentials in `.env`
- Check if you're using Testnet credentials (not mainnet)
- Ensure your IP is whitelisted (if IP restriction is enabled)

**Invalid Symbol Errors:**
- Use uppercase symbols (BTCUSDT, not btcusdt)
- Ensure the symbol exists on Binance Futures
- Check symbol format: base asset + USDT (e.g., BTC**USDT**)

**Insufficient Balance:**
- Check your testnet account balance
- Request testnet funds from Binance Futures Testnet faucet

## 📧 Submission

This project includes:
- ✅ Complete source code with modular structure
- ✅ Comprehensive README with setup and usage
- ✅ requirements.txt for dependencies
- ✅ Example .env file template
- ✅ Logging for all operations
- ✅ Both MARKET and LIMIT order examples

## 👨‍💻 Author

Created as part of the Python Developer Intern assignment.
**[Gagan A J]**

---

**Happy Trading! 🚀**
