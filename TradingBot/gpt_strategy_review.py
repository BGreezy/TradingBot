# Function to prepare data for ChatGPT analysis
def prepare_data_for_chatgpt(data):
    # Convert the data into a JSON string
    data_str = json.dumps(data)
    return data_str

# Function to analyze data with ChatGPT
def analyze_with_chatgpt(data, model="text-davinci-002"):
    # Validate the data
    if not data or not isinstance(data, dict):
        return "Invalid data format"
    
    # Prepare the data
    prepared_data = prepare_data_for_chatgpt(data)
    
    # Create specific questions for high-frequency momentum trading
    specific_question = f"What are the buy/sell signals based on the current momentum indicators in this market data: {prepared_data}?"
    
    # Create a conversation with ChatGPT
    try:
        conversation = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a financial analysis expert specialized in high-frequency momentum trading."},
                {"role": "user", "content": specific_question},
                {"role": "assistant", "content": "Analyzing the data..."}
            ]
        )
    except Exception as e:
        return f"Error in ChatGPT interaction: {e}"
    
    # Extract and return the assistant's reply
    assistant_reply = conversation['choices'][0]['message']['content']
    return assistant_reply
