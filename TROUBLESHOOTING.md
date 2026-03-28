# 🔧 Troubleshooting Guide

Common issues and their solutions for the Binance Futures Trading Bot.

---

## 🔌 Connection Issues

### Problem: "API credentials not found"
**Error Message:**
```
ValueError: API credentials not found. Please set BINANCE_API_KEY and BINANCE_API_SECRET in .env file
```

**Solution:**
1. Ensure `.env` file exists in the project root
2. Check that it contains both variables:
   ```
   BINANCE_API_KEY=your_actual_key
   BINANCE_API_SECRET=your_actual_secret
   ```
3. No quotes needed around the values
4. No spaces around the `=` sign

---

### Problem: "Connection test failed"
**Possible Causes:**
- Wrong API credentials
- Using mainnet credentials instead of testnet
- Network/firewall issues
- IP whitelist restrictions

**Solutions:**
1. **Verify credentials are from Testnet:**
   - Go to https://testnet.binancefuture.com/
   - Check you're on the TESTNET, not mainnet
   - Regenerate API keys if needed

2. **Check API key permissions:**
   - Ensure "Enable Futures" is checked
   - Ensure "Enable Reading" is checked

3. **Test internet connection:**
   ```bash
   ping testnet.binancefuture.com
   ```

4. **Disable IP restrictions** (for testnet testing):
   - In Binance Testnet, edit your API key
   - Remove IP whitelist restrictions temporarily

---

## ❌ Order Placement Errors

### Problem: "Invalid symbol"
**Error Message:**
```
BinanceAPIException: Invalid symbol
```

**Solutions:**
1. Use uppercase: `BTCUSDT` not `btcusdt`
2. Ensure symbol exists on Binance Futures
3. Check correct format: `BASEUSDT` (e.g., BTC**USDT**, ETH**USDT**)
4. Use futures symbols, not spot symbols

**Common Valid Symbols:**
- `BTCUSDT`
- `ETHUSDT`
- `BNBUSDT`
- `ADAUSDT`
- `SOLUSDT`

---

### Problem: "Insufficient balance"
**Error Message:**
```
BinanceAPIException: Balance insufficient
```

**Solutions:**
1. **Check your testnet balance:**
   ```bash
   python cli.py test
   ```

2. **Get testnet funds:**
   - Log into https://testnet.binancefuture.com/
   - Navigate to "Get Test Funds" or faucet
   - Request USDT for testing

3. **Reduce order quantity:**
   - Try smaller amounts (e.g., 0.001 instead of 1.0)

---

### Problem: "Precision error"
**Error Message:**
```
BinanceAPIException: Precision is over the maximum defined for this asset
```

**Solutions:**
1. **Check symbol's precision requirements:**
   - Different symbols have different precision
   - BTC usually allows 3 decimal places (0.001)
   - Some coins need less precision

2. **Adjust your quantity:**
   ```bash
   # Instead of 0.0001
   python cli.py place -s BTCUSDT -d BUY -t MARKET -q 0.001
   ```

---

### Problem: "Price filter error" (LIMIT orders)
**Error Message:**
```
BinanceAPIException: Filter failure: PRICE_FILTER
```

**Solutions:**
1. **Check current market price first:**
   ```bash
   python cli.py price BTCUSDT
   ```

2. **Ensure your limit price is reasonable:**
   - Not too far from current price
   - Follows tick size rules
   - For BTC, usually increments of 0.1 or 0.01

3. **Round to appropriate decimals:**
   ```bash
   # Good: 95000
   # Good: 95000.5
   # Bad: 95000.123456
   ```

---

## 🐍 Python/Installation Issues

### Problem: "Module not found"
**Error Message:**
```
ModuleNotFoundError: No module named 'binance'
```

**Solution:**
```bash
# Install dependencies
pip install -r requirements.txt

# Or install individually
pip install python-binance click python-dotenv requests
```

---

### Problem: "Permission denied" on Linux/Mac
**Error Message:**
```
bash: ./setup.sh: Permission denied
```

**Solution:**
```bash
# Make script executable
chmod +x setup.sh
./setup.sh

# Or run with bash directly
bash setup.sh
```

---

### Problem: Python version issues
**Solution:**
```bash
# Check Python version
python --version
python3 --version

# Use Python 3.8+
python3 cli.py test
```

---

## 📝 Validation Errors

### Problem: "Side must be BUY or SELL"
**Solution:**
- Use exact uppercase: `BUY` or `SELL`
- Not: `buy`, `Buy`, `LONG`, `SHORT`

---

### Problem: "Order type must be MARKET or LIMIT"
**Solution:**
- Use exact uppercase: `MARKET` or `LIMIT`
- Not: `market`, `limit`, `STOP`, `STOP_LIMIT`

---

### Problem: "Price is required for LIMIT orders"
**Error Message:**
```
ValidationError: Price is required for LIMIT orders
```

**Solution:**
```bash
# Always include -p flag for LIMIT orders
python cli.py place -s BTCUSDT -d BUY -t LIMIT -q 0.001 -p 94500
```

---

## 📊 Logging Issues

### Problem: "Logs not being created"
**Solution:**
1. **Check logs directory exists:**
   ```bash
   mkdir -p logs
   ```

2. **Check permissions:**
   ```bash
   ls -la logs/
   chmod 755 logs/
   ```

3. **Manually check if logging works:**
   ```python
   from bot import setup_logging
   logger = setup_logging()
   logger.info("Test message")
   ```

---

## 🔐 Security Warnings

### Problem: ".env file in git repository"
**Solution:**
```bash
# Remove from git
git rm --cached .env

# Ensure .gitignore includes it
echo ".env" >> .gitignore

# Commit changes
git add .gitignore
git commit -m "Remove .env from tracking"
```

---

## 🆘 Still Having Issues?

### Debug Steps:
1. **Enable verbose logging:**
   - Check the logs directory for detailed error info
   - Look for the latest log file

2. **Test connection separately:**
   ```bash
   python cli.py test
   ```

3. **Try a minimal order:**
   ```bash
   python cli.py place -s BTCUSDT -d BUY -t MARKET -q 0.001
   ```

4. **Check Binance status:**
   - Visit https://testnet.binancefuture.com/
   - Ensure testnet is operational
   - Check if you can log in via web interface

5. **Test with example script:**
   ```bash
   python examples.py
   ```

---

## 📞 Getting Help

If you're still stuck:
1. Check the log files in `logs/` directory
2. Look for the specific error message
3. Search Binance API documentation
4. Check python-binance GitHub issues
5. Verify all requirements in SUBMISSION_CHECKLIST.md

---

**Remember:** This is a testnet environment, so don't worry about breaking anything. Experiment and learn! 🚀
