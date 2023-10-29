# Data Parsing and Storage
# Global dictionary to store parsed market data
parsed_market_data = {}

def parse_and_store_data(data):
    global parsed_market_data
    
    # Extract relevant fields (Assuming data is a dictionary)
    if 'symbol' in data and 'price' in data and 'volume' in data:
        symbol = data['symbol']
        price = float(data['price'])
        volume = float(data['volume'])
        
        # Calculate momentum (price change per unit volume)
        if symbol in parsed_market_data:
            previous_price = parsed_market_data[symbol]['price']
            previous_volume = parsed_market_data[symbol]['volume']
            momentum = (price - previous_price) / (volume - previous_volume)
        else:
            momentum = 0  # Initialize with zero for the first data point
        
        # Store the parsed data
        parsed_market_data[symbol] = {'price': price, 'volume': volume, 'momentum': momentum}

    else:
        print("Data missing relevant fields, could not parse.")
