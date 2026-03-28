# 🚀 Quick Reference Card

## Setup (One-time)
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up credentials
cp .env.example .env
# Edit .env with your Binance Testnet API keys

# 3. Test connection
python cli.py test
```

## Common Commands

### Check Connection
```bash
python cli.py test
```

### Get Current Price
```bash
python cli.py price BTCUSDT
python cli.py price ETHUSDT
```

### MARKET Orders
```bash
# BUY at market price
python cli.py place -s BTCUSDT -d BUY -t MARKET -q 0.001

# SELL at market price
python cli.py place -s BTCUSDT -d SELL -t MARKET -q 0.001
```

### LIMIT Orders
```bash
# BUY at specific price
python cli.py place -s BTCUSDT -d BUY -t LIMIT -q 0.001 -p 93000

# SELL at specific price
python cli.py place -s BTCUSDT -d SELL -t LIMIT -q 0.001 -p 96000
```

## CLI Options Reference

```
-s, --symbol     Trading pair (e.g., BTCUSDT, ETHUSDT)
-d, --side       BUY or SELL
-t, --type       MARKET or LIMIT
-q, --quantity   Amount to trade (e.g., 0.001)
-p, --price      Price for LIMIT orders (optional for MARKET)
```

## Popular Trading Pairs
- `BTCUSDT` - Bitcoin
- `ETHUSDT` - Ethereum
- `BNBUSDT` - Binance Coin
- `ADAUSDT` - Cardano
- `SOLUSDT` - Solana
- `DOGEUSDT` - Dogecoin

## Typical Quantities (Testnet)
- Bitcoin (BTC): 0.001 - 0.01
- Ethereum (ETH): 0.01 - 0.1
- Others: Adjust based on price

## Log Files Location
```
logs/trading_bot_YYYYMMDD_HHMMSS.log
```

## Quick Troubleshooting

❌ **"API credentials not found"**
→ Edit `.env` file with your keys

❌ **"Invalid symbol"**
→ Use uppercase (BTCUSDT not btcusdt)

❌ **"Insufficient balance"**
→ Get testnet funds from Binance Futures Testnet

❌ **"Connection failed"**
→ Check you're using TESTNET credentials

## Help
```bash
python cli.py --help
python cli.py place --help
```

---

💡 **Pro Tip:** Always check current price before placing LIMIT orders
```bash
python cli.py price BTCUSDT
```
