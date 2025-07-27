import os
import argparse
import logging
from binance.client import Client
from binance.exceptions import BinanceAPIException
from dotenv import load_dotenv

# Load credentials
load_dotenv()
api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET")

# Configure logging
logging.basicConfig(
    filename='bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Initialize client
client = Client(api_key, api_secret)
client.FUTURES_URL = "https://testnet.binancefuture.com/fapi"

def place_grid_orders(symbol, side, quantity, min_price, max_price, grids):
    try:
        side = side.upper()
        quantity = float(quantity)
        min_price = float(min_price)
        max_price = float(max_price)
        grids = int(grids)

        if side not in ['BUY', 'SELL']:
            print("Invalid side. Use BUY or SELL.")
            return

        if quantity <= 0 or min_price <= 0 or max_price <= 0 or grids <= 0:
            print("Invalid input values. Must be > 0.")
            return

        if min_price >= max_price:
            print("min_price must be less than max_price.")
            return

        price_step = (max_price - min_price) / grids
        price_levels = [round(min_price + i * price_step, 2) for i in range(grids)]

        print(f"\nPlacing Grid Orders for {symbol} - Side: {side}")
        print(f"Grid Levels: {grids}, Price Range: {min_price} to {max_price}")
        print(f"Quantity per order: {quantity}\n")

        for i, price in enumerate(price_levels):
            try:
                order = client.futures_create_order(
                    symbol=symbol,
                    side=side,
                    type='LIMIT',
                    quantity=quantity,
                    price=str(price),
                    timeInForce='GTC'
                )
                logging.info(f"Grid Order {i+1}/{grids}: {side} {quantity} {symbol} at {price}")
                print(f"Order {i+1}/{grids} placed: {side} {quantity} {symbol} at {price}")
            except BinanceAPIException as e:
                logging.error(f"Grid Order {i+1} Binance error: {str(e)}")
                print(f"Order {i+1} failed: {e.message}")
            except Exception as e:
                logging.error(f"Grid Order {i+1} error: {str(e)}")
                print(f"Order {i+1} error: {str(e)}")

        print("\nGrid orders placed. Monitor your open orders manually.")

    except Exception as e:
        logging.error(f"Grid Strategy Error: {str(e)}")
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Place Grid Orders on Binance Futures")
    parser.add_argument("symbol", help="Trading pair (e.g., BTCUSDT)")
    parser.add_argument("side", help="BUY or SELL")
    parser.add_argument("quantity", help="Quantity per order")
    parser.add_argument("min_price", help="Bottom of price range")
    parser.add_argument("max_price", help="Top of price range")
    parser.add_argument("grids", help="Number of grid levels")

    args = parser.parse_args()

    place_grid_orders(
        args.symbol.upper(),
        args.side.upper(),
        args.quantity,
        args.min_price,
        args.max_price,
        args.grids
    )
