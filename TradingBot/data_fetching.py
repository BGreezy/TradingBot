import ccxt
import os
import websocket
import json
import openai
import logging
import pandas as pd
import time

# Initialize ccxt binance object
exchange = ccxt.coinbasepro()

# Your API Keys
api_key = 'TradingBot'
openai_api_key = os.getenv('OpenAISecret')

# Configure API keys
exchange.apiKey = api_key
exchange.secret = os.getenv('TradingBotSecret')

if not api_key or not openai_api_key:
    logging.error("API keys are missing.")
    exit(1)

# TODO: Consider implementing Exponential Moving Averages (EMA) or machine learning models for more robust trading signals.

openai.api_key = openai_api_key

def fetch_markets(exchange):
    return exchange.load_markets()

def sort_pairs_by_liquidity(markets, num=50):
    all_pairs = [symbol for symbol in markets.keys()]
    return sorted(all_pairs, key=lambda x: markets[x].get('quoteVolume', 0), reverse=True)[:num]

def calculate_metrics(df):
    # Calculate volatility
    df['returns'] = df['close'].pct_change()
    volatility = df['returns'].std()
    
    # Calculate Sharpe ratio (assuming risk-free rate is 0)
    sharpe_ratio = df['returns'].mean() / df['returns'].std()
    
    return {'volatility': volatility, 'sharpe_ratio': sharpe_ratio}

def select_top_pairs(metrics, num_pairs=5):
    return sorted(metrics, key=lambda x: metrics[x].get('volatility', 0) * metrics[x].get('momentum', 0), reverse=True)[:num_pairs]

def select_symbols(exchange, num_pairs=5):
    markets = fetch_markets(exchange)
    sorted_pairs = sort_pairs_by_liquidity(markets)
    
    # Fetch historical data and calculate metrics
    metrics = {}
    for pair in sorted_pairs:
        ohlcv = exchange.fetch_ohlcv(pair, '1m', limit=500)  # 1-minute bars, last 500 minutes
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    
        # Corrected function call
        metrics[pair] = calculate_metrics(df)

    selected_pairs = select_top_pairs(metrics, num_pairs)
    logging.info(f"Selected pairs based on advanced metrics: {selected_pairs}")
    return selected_pairs


# Websocket API for Real-time Data
def on_message(ws, message):
    logging.info(f"Received message: {message}")
    print(f"Received message: {message}")
    data = json.loads(message)
    #if data['type'] == 'trade':
    #    process_trade(data)
    # Parse and store the real-time market data here for your high-frequency trading strategy
   
def reconnect(ws):
    # ... existing code
    while True:
        try:
            # ... existing code
            ws.run_forever()
            logging.info("Reconnected successfully.")
            break  # Successfully connected, break the loop
        except Exception as e:
            logging.error(f"Failed to reconnect: {e}")
            time.sleep(delay)
            delay = min(delay * 2, max_delay)

def on_error(ws, error):
    logging.error(f"WebSocket Error: {error}")
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    logging.info("WebSocket connection closed.")
    logging.error(f"WebSocket closed with code: {close_status_code}, message: {close_msg}")
    print("### Connection closed, message: {close_msg} ###")
    ws.close()
    reconnect(ws)

def keep_alive(ws):
    while True:
        if ws.sock and ws.sock.connected:
            ws.send("ping")
            time.sleep(10)  # send a ping every 10 seconds
            logging.info("Sent keep-alive ping.")
        else:
            logging.error("WebSocket connection is closed.")
            break

def subscribe_to_websocket(ws, pairs):
    for pair in pairs:
        if ws.sock and ws.sock.connected:
            ws.send(json.dumps({"type": "subscribe", "symbol": pair}))
            logging.info(f"Subscribed to {pair}.")
        else:
            logging.error("WebSocket connection is closed.")

def start_websocket():
    ws_url = "wss://ws-feed.exchange.coinbase.com"
    ws = websocket.WebSocketApp(ws_url, on_message=on_message, on_error=on_error, on_close=on_close)

    def on_open(ws):
        logging.info("WebSocket connection established.")
        print("WebSocket connection established.")
        
        # Get the top trading pairs
        selected_pairs = select_symbols(exchange)

        # Subscribe to the selected pairs
        subscribe_to_websocket(ws, selected_pairs)
        logging.info(f"Sent subscription message for pairs: {selected_pairs}")
        print(f"Sent subscription message for pairs: {selected_pairs}")
    ws.on_open = on_open
    logging.info("Attempting to start WebSocket.")
    ws.run_forever()
    logging.info("WebSocket has stopped running.")
    return ws