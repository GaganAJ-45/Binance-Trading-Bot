#!/usr/bin/env python3
"""
CLI entry point for the Binance Futures Trading Bot.
"""

import click
import sys
from bot import (
    BinanceTestnetClient, 
    OrderManager, 
    validate_order_params,
    ValidationError,
    setup_logging,
    get_logger
)

# Set up logging
setup_logging()
logger = get_logger(__name__)


@click.group()
def cli():
    """Binance Futures Trading Bot - Place orders on Binance Futures Testnet"""
    pass


@cli.command()
@click.option('--symbol', '-s', required=True, help='Trading pair symbol (e.g., BTCUSDT)')
@click.option('--side', '-d', required=True, type=click.Choice(['BUY', 'SELL', 'buy', 'sell'], case_sensitive=False), 
              help='Order side: BUY or SELL')
@click.option('--type', '-t', 'order_type', required=True, 
              type=click.Choice(['MARKET', 'LIMIT', 'market', 'limit'], case_sensitive=False),
              help='Order type: MARKET or LIMIT')
@click.option('--quantity', '-q', required=True, type=float, help='Order quantity')
@click.option('--price', '-p', type=float, default=None, help='Limit price (required for LIMIT orders)')
def place(symbol, side, order_type, quantity, price):
    """
    Place an order on Binance Futures Testnet.
    
    Examples:
    
    \b
    # Place a MARKET BUY order
    python cli.py place -s BTCUSDT -d BUY -t MARKET -q 0.001
    
    \b
    # Place a LIMIT SELL order
    python cli.py place -s BTCUSDT -d SELL -t LIMIT -q 0.001 -p 95000
    """
    logger.info("="*60)
    logger.info("Starting order placement process")
    logger.info("="*60)
    
    try:
        # Validate inputs
        click.echo("\n🔍 Validating order parameters...")
        validated = validate_order_params(symbol, side, order_type, quantity, price)
        
        click.echo("✅ Validation successful!")
        
        # Print order summary
        click.echo("\n" + "="*60)
        click.echo("ORDER REQUEST SUMMARY")
        click.echo("="*60)
        click.echo(f"Symbol:         {validated['symbol']}")
        click.echo(f"Side:           {validated['side']}")
        click.echo(f"Type:           {validated['order_type']}")
        click.echo(f"Quantity:       {validated['quantity']}")
        if validated['price']:
            click.echo(f"Price:          {validated['price']}")
        click.echo("="*60 + "\n")
        
        # Confirm with user
        if not click.confirm("Do you want to proceed with this order?"):
            click.echo("❌ Order cancelled by user")
            logger.info("Order cancelled by user")
            return
        
        # Initialize client
        click.echo("\n🔌 Connecting to Binance Futures Testnet...")
        client = BinanceTestnetClient()
        
        # Test connection
        if not client.test_connection():
            click.echo("❌ Failed to connect to Binance Futures Testnet")
            logger.error("Connection test failed")
            sys.exit(1)
        
        click.echo("✅ Connected successfully!")
        
        # Get current price for reference
        try:
            current_price = client.get_current_price(validated['symbol'])
            click.echo(f"📊 Current market price: {current_price}")
        except Exception as e:
            logger.warning(f"Could not fetch current price: {str(e)}")
        
        # Initialize order manager and place order
        click.echo(f"\n📤 Placing {validated['order_type']} order...")
        order_manager = OrderManager(client)
        
        order = order_manager.place_order(
            symbol=validated['symbol'],
            side=validated['side'],
            order_type=validated['order_type'],
            quantity=validated['quantity'],
            price=validated['price']
        )
        
        # Display order response
        click.echo("\n✅ SUCCESS!")
        formatted_output = OrderManager.format_order_response(order)
        click.echo(formatted_output)
        
        logger.info("Order placement completed successfully")
        
    except ValidationError as e:
        click.echo(f"\n❌ Validation Error: {str(e)}", err=True)
        logger.error(f"Validation error: {str(e)}")
        sys.exit(1)
        
    except Exception as e:
        click.echo(f"\n❌ Error: {str(e)}", err=True)
        logger.error(f"Order placement failed: {str(e)}")
        sys.exit(1)


@cli.command()
def test():
    """Test connection to Binance Futures Testnet"""
    click.echo("\n🔍 Testing connection to Binance Futures Testnet...\n")
    
    try:
        client = BinanceTestnetClient()
        
        if client.test_connection():
            click.echo("✅ Connection successful!")
            
            # Try to get account info
            try:
                account = client.get_account_info()
                click.echo(f"\n📊 Account Information:")
                click.echo(f"   Total Wallet Balance: {account.get('totalWalletBalance', 'N/A')} USDT")
                click.echo(f"   Available Balance: {account.get('availableBalance', 'N/A')} USDT")
            except Exception as e:
                logger.warning(f"Could not fetch account info: {str(e)}")
                
        else:
            click.echo("❌ Connection failed!")
            sys.exit(1)
            
    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)
        logger.error(f"Connection test failed: {str(e)}")
        sys.exit(1)


@cli.command()
@click.argument('symbol')
def price(symbol):
    """Get current price for a symbol (e.g., BTCUSDT)"""
    try:
        client = BinanceTestnetClient()
        current_price = client.get_current_price(symbol.upper())
        click.echo(f"\n💰 Current price for {symbol.upper()}: {current_price} USDT\n")
    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)
        logger.error(f"Failed to get price: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    cli()
