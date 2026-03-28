from bot.logging_config import get_logger

logger = get_logger(__name__)


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


def validate_symbol(symbol):
    """
    Validate the trading symbol.
    
    Args:
        symbol (str): Trading pair symbol (e.g., BTCUSDT)
    
    Returns:
        str: Uppercase symbol
    
    Raises:
        ValidationError: If symbol is invalid
    """
    if not symbol or not isinstance(symbol, str):
        raise ValidationError("Symbol must be a non-empty string")
    
    symbol = symbol.upper()
    
    # Basic validation - symbol should end with USDT for futures
    if not symbol.endswith('USDT'):
        logger.warning(f"Symbol '{symbol}' doesn't end with USDT. Common format is like BTCUSDT")
    
    logger.info(f"Symbol validated: {symbol}")
    return symbol


def validate_side(side):
    """
    Validate the order side.
    
    Args:
        side (str): Order side (BUY or SELL)
    
    Returns:
        str: Uppercase side
    
    Raises:
        ValidationError: If side is invalid
    """
    if not side or not isinstance(side, str):
        raise ValidationError("Side must be a non-empty string")
    
    side = side.upper()
    
    if side not in ['BUY', 'SELL']:
        raise ValidationError(f"Invalid side: {side}. Must be 'BUY' or 'SELL'")
    
    logger.info(f"Side validated: {side}")
    return side


def validate_order_type(order_type):
    """
    Validate the order type.
    
    Args:
        order_type (str): Order type (MARKET or LIMIT)
    
    Returns:
        str: Uppercase order type
    
    Raises:
        ValidationError: If order type is invalid
    """
    if not order_type or not isinstance(order_type, str):
        raise ValidationError("Order type must be a non-empty string")
    
    order_type = order_type.upper()
    
    if order_type not in ['MARKET', 'LIMIT']:
        raise ValidationError(f"Invalid order type: {order_type}. Must be 'MARKET' or 'LIMIT'")
    
    logger.info(f"Order type validated: {order_type}")
    return order_type


def validate_quantity(quantity):
    """
    Validate the order quantity.
    
    Args:
        quantity (float): Order quantity
    
    Returns:
        float: Validated quantity
    
    Raises:
        ValidationError: If quantity is invalid
    """
    try:
        quantity = float(quantity)
    except (ValueError, TypeError):
        raise ValidationError(f"Quantity must be a number, got: {quantity}")
    
    if quantity <= 0:
        raise ValidationError(f"Quantity must be positive, got: {quantity}")
    
    logger.info(f"Quantity validated: {quantity}")
    return quantity


def validate_price(price, order_type):
    """
    Validate the order price.
    
    Args:
        price (float): Order price
        order_type (str): Order type (MARKET or LIMIT)
    
    Returns:
        float or None: Validated price (None for MARKET orders)
    
    Raises:
        ValidationError: If price is invalid
    """
    if order_type == 'LIMIT':
        if price is None:
            raise ValidationError("Price is required for LIMIT orders")
    elif order_type == 'MARKET':
        if price is not None:
            raise ValidationError("Price should NOT be provided for MARKET orders")
        return None
    
    try:
        price = float(price)
    except (ValueError, TypeError):
        raise ValidationError(f"Price must be a number, got: {price}")
    
    if price <= 0:
        raise ValidationError(f"Price must be positive, got: {price}")
    
    logger.info(f"Price validated: {price}")
    return price


def validate_order_params(symbol, side, order_type, quantity, price=None):
    """
    Validate all order parameters at once.
    
    Args:
        symbol (str): Trading pair symbol
        side (str): Order side (BUY or SELL)
        order_type (str): Order type (MARKET or LIMIT)
        quantity (float): Order quantity
        price (float, optional): Order price (required for LIMIT)
    
    Returns:
        dict: Dictionary with validated parameters
    
    Raises:
        ValidationError: If any parameter is invalid
    """
    logger.info("Validating order parameters...")
    
    validated_order_type = validate_order_type(order_type)
    validated = {
        'symbol': validate_symbol(symbol),
        'side': validate_side(side),
        'order_type': validated_order_type,
        'quantity': validate_quantity(quantity),
        'price': validate_price(price, validated_order_type)
    }
    
    logger.info("All parameters validated successfully")
    return validated
