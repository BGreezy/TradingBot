import ccxt
import os
import websocket
import json
import openai
import logging

def configure_logging():
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s',filename='websocket_log_file.log')


def fetch_data_from_api(api_function, max_retries=3, delay=1):
    retries = 0
    while retries < max_retries:
        try:
            data = api_function()
            return data
        except Exception as e:
            logging.error(f"An error occurred: {e}. Retrying...")
            print(f"An error occurred: {e}. Retrying...")
            retries += 1
            time.sleep(delay)
    logging.error(f'Max retries reached. Exception details: {e}')
    raise Exception("Max retries reached. Could not fetch data.")


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
# Implement a simple moving average crossover strategy
def moving_average_crossover(short_window, long_window, price_data):
    short_mavg = price_data.rolling(window=short_window).mean()
    long_mavg = price_data.rolling(window=long_window).mean()

    signal = 0.0
    if short_mavg[-1] > long_mavg[-1]:
        signal = 1.0  # Buy
    elif short_mavg[-1] < long_mavg[-1]:
        signal = -1.0  # Sell
    
    return signal

openai.api_key = openai_api_key

def fetch_markets(exchange):
    return exchange.load_markets()

def sort_pairs_by_liquidity(markets, num=50):
    all_pairs = [symbol for symbol in markets.keys()]
    return sorted(all_pairs, key=lambda x: markets[x]['quoteVolume'], reverse=True)[:num]

def calculate_metrics(exchange, sorted_pairs):
    metrics = {}
    for pair in sorted_pairs:
        ohlcv = exchange.fetch_ohlcv(pair, '1m', limit=500)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        
        df['returns'] = df['close'].pct_change()
        volatility = df['returns'].std()
        momentum = df['close'].diff(4)
        
        metrics[pair] = {'volatility': volatility, 'momentum': momentum[-1]}
    return metrics

def select_top_pairs(metrics, num_pairs=5):
    return sorted(metrics, key=lambda x: metrics[x]['volatility'] * metrics[x]['momentum'], reverse=True)[:num_pairs]

def select_symbols(exchange, num_pairs=5):
    markets = fetch_markets(exchange)
    sorted_pairs = sort_pairs_by_liquidity(markets)
    metrics = calculate_metrics(exchange, sorted_pairs)
    selected_pairs = select_top_pairs(metrics, num_pairs)
    return selected_pairs


# Websocket API for Real-time Data
def on_message(ws, message):
    logging.info(f"Received message: {message}")
    print(f"Received message: {message}")
    data = json.loads(message)
    if data['type'] == 'trade':
        process_trade(data)
    # Parse and store the real-time market data here for your high-frequency trading strategy
    
def on_error(ws, error):
    logging.error(f"Error: {error}")
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    logging.info("WebSocket connection closed.")
    print("### Connection closed ###")

def start_websocket():
    ws_url = "wss://ws.blockchain.info/inv"
    ws = websocket.WebSocketApp(ws_url, on_message=on_message, on_error=on_error, on_close=on_close)

    def on_open(ws):
        logging.info("WebSocket connection established.")
        print("WebSocket connection established.")
        
        # Subscribe to unconfirmed transactions
        sub_msg = json.dumps({"op": "unconfirmed_sub"})
        ws.send(sub_msg)
        logging.info(f"Sent subscription message: {sub_msg}")
        print(f"Sent subscription message: {sub_msg}")

    ws.on_open = on_open
    ws.run_forever()