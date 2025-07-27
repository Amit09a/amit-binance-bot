import os
import argparse
import logging
from binance.client import Client
from binance.exceptions import BinanceAPIException
from dotenv import load_dotenv

# Load API credentials from .env
load_dotenv()
api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET")

# Setup logging
logging.basicConfig(
    filename='bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Initialize Binance Futures Testnet client
client = Client(api_key, api_secret)
client.FUTURES_URL = "https://testnet.binancefuture.com/fapi"

def place_limit_order(symbol, side, quantity, price):
    try:
        # Validate side
        if side not in ['BUY', 'SELL']:
            logging.error(f"Invalid side: {side}")
            print("Error: Side must be either 'BUY' or 'SELL'")
            return

        # Validate quantity and price
        if float(quantity) <= 0 or float(price) <= 0:
            logging.error("Quantity and price must be greater than 0")
            print("Error: Quantity and price must be greater than 0")
            return

        # Place the limit order
        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type='LIMIT',
            quantity=quantity,
            price=price,
            timeInForce='GTC'  # GTC = Good Till Cancelled
        )

        logging.info(f"Limit order placed: {side} {quantity} {symbol} at {price}")
        print(f"Success: Limit {side} order placed for {quantity} {symbol} at {price}")
        return order

    except BinanceAPIException as e:
        logging.error(f"Binance API Error: {str(e)}")
        print(f"Binance API Error: {e.message}")

    except Exception as e:
        logging.error(f"General Error: {str(e)}")
        print(f"Error: {str(e)}")

# Run as CLI
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Place a Binance Futures limit order.')
    parser.add_argument('symbol', help='Trading symbol (e.g., BTCUSDT)')
    parser.add_argument('side', help='BUY or SELL')
    parser.add_argument('quantity', help='Order quantity')
    parser.add_argument('price', help='Order price')

    args = parser.parse_args()
    place_limit_order(args.symbol.upper(), args.side.upper(), args.quantity, args.price)
