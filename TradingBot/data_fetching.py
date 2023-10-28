import ccxt
import os
import websocket
import json

def fetch_data_from_api(api_function, max_retries=3, delay=1):
    retries = 0
    while retries < max_retries:
        try:
            data = api_function()
            return data
        except Exception as e:
            print(f"An error occurred: {e}. Retrying...")
            retries += 1
            time.sleep(delay)
    raise Exception("Max retries reached. Could not fetch data.")
    logging.error(f'Max retries reached. Exception details: {e}')

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

# Function to fetch available trading pairs

def select_symbols(exchange, num_pairs=5):
    # Fetch available trading pairs
    markets = exchange.load_markets()
    all_pairs = [symbol for symbol in markets.keys()]
    
    # Filter pairs based on liquidity
    sorted_pairs = sorted(all_pairs, key=lambda x: markets[x]['quoteVolume'], reverse=True)[:50]
    
    # Collect historical data and calculate metrics
    metrics = {}
    for pair in sorted_pairs:
        ohlcv = exchange.fetch_ohlcv(pair, '1m', limit=500)  # 1-minute bars, last 500 minutes
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        
        # Calculate volatility
        df['returns'] = df['close'].pct_change()
        volatility = df['returns'].std()
        
        # Calculate momentum
        momentum = df['close'].diff(4)  # Rate of change over last 5 minutes
        
        # Aggregate metrics
        metrics[pair] = {'volatility': volatility, 'momentum': momentum[-1]}
    
    # Select pairs based on volatility and momentum
    selected_pairs = sorted(metrics, key=lambda x: metrics[x]['volatility'] * metrics[x]['momentum'], reverse=True)[:num_pairs]
    
    return selected_pairs

# Function to fetch real-time market data
def fetch_market_data(symbol, timeframe):
    return exchange.fetch_ohlcv(symbol, timeframe)

# Websocket API for Real-time Data
def on_message(ws, message):
    data = json.loads(message)
    # Parse and store the real-time market data here for your high-frequency trading strategy
    
def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("### Connection closed ###")

def start_websocket():
    ws_url = "wss://ws.prod.blockchain.info/"  # Replace with the actual Blockchain.com Websocket URL
    ws = websocket.WebSocketApp(ws_url, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.run_forever()
