import os
import argparse
import logging
from binance.client import Client
from binance.exceptions import BinanceAPIException
from dotenv import load_dotenv

# Load API keys
load_dotenv()
api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET")

# Setup logging
logging.basicConfig(
    filename='bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Initialize Binance Testnet Futures
client = Client(api_key, api_secret)
client.FUTURES_URL = "https://testnet.binancefuture.com/fapi"

def get_mark_price(symbol):
    try:
        response = client.futures_mark_price(symbol=symbol)
        return float(response['markPrice'])
    except Exception as e:
        logging.error(f"Failed to fetch mark price: {str(e)}")
        print(f"Error: Unable to fetch current market price")
        return None

def place_oco(symbol, side, quantity, take_profit_price, stop_loss_price, buffer=50):
    try:
        side = side.upper()
        opposite_side = "SELL" if side == "BUY" else "BUY"
        take_profit_price = float(take_profit_price)
        stop_loss_price = float(stop_loss_price)
        quantity = float(quantity)

        # ✅ Step 1: Get current mark price
        current_price = get_mark_price(symbol)
        if not current_price:
            return

        # ✅ Step 2: Check if stop-loss or TP are too close to trigger
        if opposite_side == "SELL":
            if stop_loss_price >= current_price - buffer:
                print(f"❌ Stop-Loss ({stop_loss_price}) is too close to or above current price ({current_price}).")
                print("➡️ Adjust it at least 50 USDT below.")
                return
        elif opposite_side == "BUY":
            if stop_loss_price <= current_price + buffer:
                print(f"❌ Stop-Loss ({stop_loss_price}) is too close to or below current price ({current_price}).")
                print("➡️ Adjust it at least 50 USDT above.")
                return

        # ✅ Step 3: Place TP (LIMIT)
        tp_order = client.futures_create_order(
            symbol=symbol,
            side=opposite_side,
            type='LIMIT',
            quantity=quantity,
            price=str(take_profit_price),
            timeInForce='GTC'
        )

        # ✅ Step 4: Place SL (STOP_MARKET)
        sl_order = client.futures_create_order(
            symbol=symbol,
            side=opposite_side,
            type='STOP_MARKET',
            stopPrice=str(stop_loss_price),
            quantity=quantity,
            timeInForce='GTC',
            workingType='MARK_PRICE'
        )

        logging.info(f"OCO Simulated — TP: {take_profit_price}, SL: {stop_loss_price}, Side: {opposite_side}")
        print(f"✅ OCO Orders Placed on Testnet:")
        print(f"   Take-Profit (LIMIT) at {take_profit_price}")
        print(f"   Stop-Loss (MARKET) at {stop_loss_price}")
        print("⚠️ Monitor manually — not auto-cancelling on Binance Futures.")

    except BinanceAPIException as e:
        logging.error(f"Binance API error: {str(e)}")
        print(f"Binance API error: {e.message}")
    except Exception as e:
        logging.error(f"General error: {str(e)}")
        print(f"Error: {str(e)}")

# CLI
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simulated OCO (TP + SL) for Binance Futures")
    parser.add_argument("symbol", help="Trading pair (e.g., BTCUSDT)")
    parser.add_argument("side", help="Your position direction: BUY or SELL")
    parser.add_argument("quantity", help="Amount to protect")
    parser.add_argument("take_profit_price", help="Profit target")
    parser.add_argument("stop_loss_price", help="Stop loss trigger")
    parser.add_argument("--buffer", help="Min distance from market price (default 50)", default=50)

    args = parser.parse_args()

    place_oco(
        symbol=args.symbol.upper(),
        side=args.side.upper(),
        quantity=args.quantity,
        take_profit_price=args.take_profit_price,
        stop_loss_price=args.stop_loss_price,
        buffer=float(args.buffer)
    )
