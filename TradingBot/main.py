import ccxt
import logging
from data_fetching import select_symbols, subscribe_to_websocket, start_websocket
# TODO: Uncomment this line when the trading strategy function is implemented
#from trading_strategies import your_trading_strategy_function
from performance_metrics import calculate_sharpe_ratio, calculate_roi

if __name__ == "__main__":
    # Start logging
    logging.basicConfig(
        filename='log_file.log',  # The name of the log file
        filemode='a',  # Mode to open the file, 'a' will append to the existing file if it exists
        level=logging.INFO,  # Logging level
        format='%(asctime)s - %(levelname)s - %(message)s'  # Log format
    )
    # Initialize exchange
    exchange = ccxt.binance()

    #Get Pairs
    viable_pairs = select_symbols(exchange)

    # Initialize websocket
    ws = start_websocket()

    # Subscribe to viable pairs
    subscribe_to_websocket(ws, viable_pairs)

    # Start trading bot