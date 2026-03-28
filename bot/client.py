import os
import time
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException
from dotenv import load_dotenv
from bot.logging_config import get_logger

logger = get_logger(__name__)


class BinanceTestnetClient:
    """
    Wrapper class for Binance Futures Testnet API client.
    Handles authentication and provides methods for trading operations.
    """
    
    TESTNET_BASE_URL = "https://testnet.binancefuture.com"
    
    def __init__(self):
        """Initialize the Binance Futures Testnet client."""
        load_dotenv()
        
        self.api_key = os.getenv('BINANCE_API_KEY')
        self.api_secret = os.getenv('BINANCE_API_SECRET')
        
        if not self.api_key or not self.api_secret:
            error_msg = "API credentials not found. Please set BINANCE_API_KEY and BINANCE_API_SECRET in .env file"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        try:
            # Initialize client with testnet URL
            self.client = Client(self.api_key, self.api_secret, testnet=True)
            # Set the futures base URL to testnet
            self.client.FUTURES_URL = self.TESTNET_BASE_URL
            self.sync_time_offset()
            
            logger.info("Binance Testnet client initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Binance client: {str(e)}")
            raise

    def sync_time_offset(self):
        """
        Sync the local request timestamp against Binance Futures server time.
        """
        try:
            server_time = self.client.futures_time()["serverTime"]
            local_time = int(time.time() * 1000)
            self.client.timestamp_offset = server_time - local_time
            logger.info(
                "Synchronized Binance server time. Offset set to %sms",
                self.client.timestamp_offset
            )
        except Exception as e:
            logger.warning(f"Could not sync Binance server time: {str(e)}")

    @staticmethod
    def _is_timestamp_error(error):
        """
        Check whether an API error was caused by timestamp drift.
        """
        message = getattr(error, "message", str(error))
        return "outside of the recvwindow" in message.lower()

    def execute_signed_request(self, request_fn, *args, **kwargs):
        """
        Execute a signed Binance request with a timestamp resync retry on drift.
        """
        kwargs.setdefault("recvWindow", 10000)

        try:
            return request_fn(*args, **kwargs)
        except BinanceAPIException as e:
            if self._is_timestamp_error(e):
                logger.warning("Timestamp drift detected. Re-syncing Binance server time and retrying once.")
                self.sync_time_offset()
                return request_fn(*args, **kwargs)
            raise
    
    def test_connection(self):
        """
        Test the connection to Binance Futures Testnet.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            # Try to fetch futures account balance
            self.execute_signed_request(self.client.futures_account_balance)
            logger.info("Connection test successful")
            return True
        except BinanceAPIException as e:
            logger.error(f"API Exception during connection test: {e.message}")
            return False
        except BinanceRequestException as e:
            logger.error(f"Request Exception during connection test: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during connection test: {str(e)}")
            return False
    
    def get_account_info(self):
        """
        Get futures account information.
        
        Returns:
            dict: Account information
        """
        try:
            account_info = self.execute_signed_request(self.client.futures_account)
            logger.info("Successfully retrieved account information")
            return account_info
        except BinanceAPIException as e:
            logger.error(f"API Exception getting account info: {e.message}")
            raise
        except Exception as e:
            logger.error(f"Error getting account info: {str(e)}")
            raise
    
    def get_symbol_info(self, symbol):
        """
        Get information about a specific trading symbol.
        
        Args:
            symbol (str): Trading pair symbol (e.g., BTCUSDT)
        
        Returns:
            dict: Symbol information
        """
        try:
            exchange_info = self.client.futures_exchange_info()
            for s in exchange_info['symbols']:
                if s['symbol'] == symbol:
                    logger.info(f"Retrieved info for symbol: {symbol}")
                    return s
            
            logger.warning(f"Symbol {symbol} not found in exchange info")
            return None
            
        except BinanceAPIException as e:
            logger.error(f"API Exception getting symbol info: {e.message}")
            raise
        except Exception as e:
            logger.error(f"Error getting symbol info: {str(e)}")
            raise
    
    def get_current_price(self, symbol):
        """
        Get current price for a symbol.
        
        Args:
            symbol (str): Trading pair symbol
        
        Returns:
            float: Current price
        """
        try:
            ticker = self.client.futures_symbol_ticker(symbol=symbol)
            price = float(ticker['price'])
            logger.info(f"Current price for {symbol}: {price}")
            return price
        except BinanceAPIException as e:
            logger.error(f"API Exception getting current price: {e.message}")
            raise
        except Exception as e:
            logger.error(f"Error getting current price: {str(e)}")
            raise
