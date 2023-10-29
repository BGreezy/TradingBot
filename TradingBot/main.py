from data_fetching import select_symbols, start_websocket
from trading_strategies import your_trading_strategy_function
from performance_metrics import your_performance_metrics_function

if __name__ == "__main__":
    # Initialize exchange
    exchange = ccxt.binance()

    #Get Pairs
    viable_pairs = select_symbols(exchange)

    # Initialize websocket
    ws = start_websocket()

    # Subscribe to viable pairs
    subscribe_to_websocket(ws, viable_pairs)

    # Start trading bot