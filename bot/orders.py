from binance.exceptions import BinanceAPIException, BinanceRequestException
from bot.logging_config import get_logger

logger = get_logger(__name__)


class OrderManager:
    """
    Handles order placement and management on Binance Futures Testnet.
    """
    
    def __init__(self, client):
        """
        Initialize OrderManager with a Binance client.
        
        Args:
            client (BinanceTestnetClient): Initialized Binance client
        """
        self.client = client.client  # Access the underlying binance.client.Client
        logger.info("OrderManager initialized")
    
    def place_market_order(self, symbol, side, quantity):
        """
        Place a market order on Binance Futures.
        
        Args:
            symbol (str): Trading pair (e.g., BTCUSDT)
            side (str): BUY or SELL
            quantity (float): Order quantity
        
        Returns:
            dict: Order response from Binance
        """
        logger.info(f"Attempting to place MARKET order: {side} {quantity} {symbol}")
        
        try:
            # Prepare order parameters
            order_params = {
                'symbol': symbol,
                'side': side,
                'type': 'MARKET',
                'quantity': quantity,
            }
            
            logger.info(f"Order request: {order_params}")
            
            # Place the order
            order = self.client.futures_create_order(**order_params)
            
            logger.info(f"MARKET order placed successfully. Order ID: {order.get('orderId')}")
            logger.info(f"Order response: {order}")
            
            return order
            
        except BinanceAPIException as e:
            logger.error(f"Binance API Exception: {e.status_code} - {e.message}")
            raise
        except BinanceRequestException as e:
            logger.error(f"Binance Request Exception: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error placing market order: {str(e)}")
            raise
    
    def place_limit_order(self, symbol, side, quantity, price):
        """
        Place a limit order on Binance Futures.
        
        Args:
            symbol (str): Trading pair (e.g., BTCUSDT)
            side (str): BUY or SELL
            quantity (float): Order quantity
            price (float): Limit price
        
        Returns:
            dict: Order response from Binance
        """
        logger.info(f"Attempting to place LIMIT order: {side} {quantity} {symbol} @ {price}")
        
        try:
            # Prepare order parameters
            order_params = {
                'symbol': symbol,
                'side': side,
                'type': 'LIMIT',
                'quantity': quantity,
                'price': price,
                'timeInForce': 'GTC'  # Good Till Cancelled
            }
            
            logger.info(f"Order request: {order_params}")
            
            # Place the order
            order = self.client.futures_create_order(**order_params)
            
            logger.info(f"LIMIT order placed successfully. Order ID: {order.get('orderId')}")
            logger.info(f"Order response: {order}")
            
            return order
            
        except BinanceAPIException as e:
            logger.error(f"Binance API Exception: {e.status_code} - {e.message}")
            raise
        except BinanceRequestException as e:
            logger.error(f"Binance Request Exception: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error placing limit order: {str(e)}")
            raise
    
    def place_order(self, symbol, side, order_type, quantity, price=None):
        """
        Place an order (MARKET or LIMIT) on Binance Futures.
        
        Args:
            symbol (str): Trading pair (e.g., BTCUSDT)
            side (str): BUY or SELL
            order_type (str): MARKET or LIMIT
            quantity (float): Order quantity
            price (float, optional): Limit price (required for LIMIT orders)
        
        Returns:
            dict: Order response from Binance
        """
        if order_type == 'MARKET':
            return self.place_market_order(symbol, side, quantity)
        elif order_type == 'LIMIT':
            if price is None:
                raise ValueError("Price is required for LIMIT orders")
            return self.place_limit_order(symbol, side, quantity, price)
        else:
            raise ValueError(f"Unsupported order type: {order_type}")
    
    def get_order_status(self, symbol, order_id):
        """
        Get the status of a specific order.
        
        Args:
            symbol (str): Trading pair
            order_id (int): Order ID
        
        Returns:
            dict: Order status
        """
        try:
            order = self.client.futures_get_order(symbol=symbol, orderId=order_id)
            logger.info(f"Retrieved order status for Order ID {order_id}: {order.get('status')}")
            return order
        except BinanceAPIException as e:
            logger.error(f"API Exception getting order status: {e.message}")
            raise
        except Exception as e:
            logger.error(f"Error getting order status: {str(e)}")
            raise
    
    def cancel_order(self, symbol, order_id):
        """
        Cancel a specific order.
        
        Args:
            symbol (str): Trading pair
            order_id (int): Order ID to cancel
        
        Returns:
            dict: Cancellation response
        """
        try:
            result = self.client.futures_cancel_order(symbol=symbol, orderId=order_id)
            logger.info(f"Order {order_id} cancelled successfully")
            return result
        except BinanceAPIException as e:
            logger.error(f"API Exception cancelling order: {e.message}")
            raise
        except Exception as e:
            logger.error(f"Error cancelling order: {str(e)}")
            raise
    
    @staticmethod
    def format_order_response(order):
        """
        Format order response for display.
        
        Args:
            order (dict): Order response from Binance
        
        Returns:
            str: Formatted order information
        """
        output = "\n" + "="*60 + "\n"
        output += "ORDER PLACED SUCCESSFULLY\n"
        output += "="*60 + "\n"
        output += f"Order ID:       {order.get('orderId')}\n"
        output += f"Symbol:         {order.get('symbol')}\n"
        output += f"Side:           {order.get('side')}\n"
        output += f"Type:           {order.get('type')}\n"
        output += f"Status:         {order.get('status')}\n"
        output += f"Quantity:       {order.get('origQty')}\n"
        output += f"Executed Qty:   {order.get('executedQty', 'N/A')}\n"
        
        if order.get('avgPrice'):
            output += f"Avg Price:      {order.get('avgPrice')}\n"
        
        if order.get('price') and order.get('price') != '0':
            output += f"Limit Price:    {order.get('price')}\n"
        
        output += f"Time:           {order.get('updateTime', order.get('transactTime', 'N/A'))}\n"
        output += "="*60 + "\n"
        
        return output
