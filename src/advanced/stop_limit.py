import os
import argparse
import logging
from binance.client import Client
from binance.exceptions import BinanceAPIException
from dotenv import load_dotenv

# Load environment
load_dotenv()
api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET")

# Configure logging
logging.basicConfig(
    filename='bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

client = Client(api_key, api_secret)
client.FUTURES_URL = "https://testnet.binancefuture.com/fapi"

def place_stop_limit_order(symbol, side, quantity, price, stop_price, working_type="MARK_PRICE"):
    try:
        # Basic validations
        side = side.upper()
        if side not in ("BUY", "SELL"):
            logging.error(f"Invalid side: {side}")
            print("Error: Side must be BUY or SELL")
            return

        quantity = float(quantity)
        price = float(price)
        stop_price = float(stop_price)
        if quantity <= 0 or price <= 0 or stop_price <= 0:
            logging.error("Quantity, price, and stop_price must be > 0")
            print("Error: Quantity, price, and stop_price must all be > 0")
            return

        # STOP == Stop-Limit (needs price + stopPrice)
        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type='STOP',            # <— this is the key change
            quantity=quantity,
            price=str(price),
            stopPrice=str(stop_price),
            timeInForce='GTC',
            workingType=working_type  # MARK_PRICE or CONTRACT_PRICE
        )

        logging.info(f"STOP (stop-limit) order placed: {side} {quantity} {symbol} @ {price} (stop {stop_price})")
        print(f"Success: Stop-Limit order placed for {symbol}")
        return order

    except BinanceAPIException as e:
        logging.error(f"Binance API error: {str(e)}")
        print(f"Binance API error: {e.message}")
    except Exception as e:
        logging.error(f"General error: {str(e)}")
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Place a Binance Futures Stop-Limit order (type=STOP).")
    parser.add_argument("symbol", help="e.g., BTCUSDT")
    parser.add_argument("side", help="BUY or SELL")
    parser.add_argument("quantity", help="Order quantity")
    parser.add_argument("price", help="Limit price (the order you want to place once triggered)")
    parser.add_argument("stop_price", help="Trigger price")
    parser.add_argument("--working_type", default="MARK_PRICE", choices=["MARK_PRICE", "CONTRACT_PRICE"],
                        help="Trigger source price (default MARK_PRICE)")

    args = parser.parse_args()

    place_stop_limit_order(
        args.symbol.upper(),
        args.side.upper(),
        args.quantity,
        args.price,
        args.stop_price,
        args.working_type
    )
