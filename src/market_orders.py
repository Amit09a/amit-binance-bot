import os
import argparse
import logging
from binance.client import Client
from binance.exceptions import BinanceAPIException
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET")

# Configure logging
logging.basicConfig(
    filename='bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Initialize Binance Futures client
client = Client(api_key, api_secret)
client.FUTURES_URL = "https://testnet.binancefuture.com/fapi"

def place_market_order(symbol, side, quantity):
    try:
        # Validate order side
        if side not in ['BUY', 'SELL']:
            logging.error(f"Invalid side: {side}")
            print("Error: Order side must be either 'BUY' or 'SELL'")
            return

        # Validate quantity
        if float(quantity) <= 0:
            logging.error("Invalid quantity: must be greater than 0")
            print("Error: Quantity must be greater than 0")
            return

        # Place market order
        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type='MARKET',
            quantity=quantity
        )

        logging.info(f"Market order placed: {side} {quantity} {symbol}")
        print(f"Success: Market {side} order placed for {quantity} {symbol}")
        return order

    except BinanceAPIException as e:
        logging.error(f"Binance API Error: {str(e)}")
        print(f"Binance API Error: {e.message}")

    except Exception as e:
        logging.error(f"General Error: {str(e)}")
        print(f"Error: {str(e)}")

# Run as script from CLI
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Place a Binance Futures market order.')
    parser.add_argument('symbol', help='Trading pair symbol (e.g., BTCUSDT)')
    parser.add_argument('side', help='Order side: BUY or SELL')
    parser.add_argument('quantity', help='Quantity to trade')

    args = parser.parse_args()

    place_market_order(args.symbol.upper(), args.side.upper(), args.quantity)
