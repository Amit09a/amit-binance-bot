import os
import time
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

def twap_order(symbol, side, total_quantity, chunks, interval):
    try:
        side = side.upper()

        if side not in ['BUY', 'SELL']:
            print("Invalid side. Must be BUY or SELL.")
            return

        total_quantity = float(total_quantity)
        chunks = int(chunks)
        interval = int(interval)

        if total_quantity <= 0 or chunks <= 0 or interval <= 0:
            print("Total quantity, chunks, and interval must be greater than 0.")
            return

        chunk_quantity = round(total_quantity / chunks, 6)

        print(f"\nStarting TWAP Strategy for {symbol} — {side}")
        print(f"Total Quantity: {total_quantity}")
        print(f"Chunks: {chunks}")
        print(f"Quantity per Chunk: {chunk_quantity}")
        print(f"Interval: {interval} seconds\n")

        for i in range(chunks):
            try:
                order = client.futures_create_order(
                    symbol=symbol,
                    side=side,
                    type='MARKET',
                    quantity=chunk_quantity
                )
                logging.info(f"TWAP chunk {i+1}/{chunks}: {side} {chunk_quantity} {symbol}")
                print(f"Chunk {i+1}/{chunks} placed: {side} {chunk_quantity} {symbol}")
            except BinanceAPIException as e:
                logging.error(f"Chunk {i+1} Binance API error: {str(e)}")
                print(f"Chunk {i+1} failed: {e.message}")
            except Exception as e:
                logging.error(f"Chunk {i+1} General error: {str(e)}")
                print(f"Chunk {i+1} error: {str(e)}")

            if i < chunks - 1:
                time.sleep(interval)

        print("\nTWAP execution completed.")

    except Exception as e:
        logging.error(f"TWAP Error: {str(e)}")
        print(f"TWAP strategy failed: {str(e)}")

# CLI Entry
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TWAP (Time-Weighted Average Price) strategy execution")
    parser.add_argument("symbol", help="Trading pair (e.g., BTCUSDT)")
    parser.add_argument("side", help="BUY or SELL")
    parser.add_argument("total_quantity", help="Total quantity to trade")
    parser.add_argument("chunks", help="Number of chunks to split the order")
    parser.add_argument("interval", help="Interval in seconds between each chunk")

    args = parser.parse_args()

    twap_order(
        symbol=args.symbol.upper(),
        side=args.side.upper(),
        total_quantity=args.total_quantity,
        chunks=args.chunks,
        interval=args.interval
    )
