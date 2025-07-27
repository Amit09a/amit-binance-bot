# Binance Futures Order Bot

A modular, CLI-based trading bot for **Binance USDT-M Futures**, built with Python.  
Supports execution of advanced strategies such as **TWAP**, **Stop-Limit**, **OCO (simulated)**, and **Grid Trading** on Binance **Testnet**.

---

## 📌 Key Features

| Strategy        | Description                                                    |
|----------------|----------------------------------------------------------------|
| Market Orders   | Instant buy/sell at current market price                      |
| Limit Orders    | Places orders at a fixed price using GTC (Good Till Cancel)    |
| Stop-Limit      | Triggers a limit order once the stop price is hit              |
| OCO (Simulated) | Simulated Take-Profit + Stop-Loss pair (Futures doesn’t support native OCO) |
| TWAP            | Splits orders evenly over time to reduce slippage              |
| Grid Strategy   | Places multiple limit orders within a price range              |

---

## 🛠 Project Setup

### 1. Clone the repository

```bash
git clone https://github.com/your_username/binance-futures-bot.git
cd binance-futures-bot

2. Create a virtual environment

python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate 

3. Install requirements
pip install -r requirements.txt

4. Set up API credentials

Create a .env file in the root directory:

env

BINANCE_API_KEY=your_testnet_api_key
BINANCE_API_SECRET=your_testnet_secret
🔐 Get your API credentials from: https://testnet.binancefuture.com

🚀 Running Strategies
Market Order

python src/market_orders.py BTCUSDT BUY 0.01
Limit Order

python src/limit_orders.py BTCUSDT SELL 0.01 61000
Stop-Limit Order

python src/advanced/stop_limit.py BTCUSDT SELL 0.01 60000 59000
OCO (Simulated)

python src/advanced/oco.py BTCUSDT BUY 0.01 61000 59000
TWAP Strategy

python src/advanced/twap.py BTCUSDT BUY 0.05 5 10
Grid Strategy

python src/advanced/grid_strategy.py BTCUSDT BUY 0.01 59000 60000 5
📂 Project Structure

binance-futures-bot/
├── src/
│   ├── market_orders.py
│   ├── limit_orders.py
│   └── advanced/
│       ├── stop_limit.py
│       ├── oco.py
│       ├── twap.py
│       └── grid_strategy.py
├── bot.log
├── .env
├── requirements.txt
├── README.md
└── report.pdf


📝 License
This project is for educational/demonstration use only.
Use on real funds is not recommended without further security and risk handling.

Reach out to amitm4148@gmail.com  for any questions

