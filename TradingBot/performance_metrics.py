
# Performance Metrics: Implementing a simple Sharpe Ratio calculation
def calculate_sharpe_ratio(returns, risk_free_rate=0.01):
    excess_returns = returns - risk_free_rate
    return excess_returns.mean() / excess_returns.std()
    # TODO: Add more performance metrics like Drawdown, Beta, and Alpha
