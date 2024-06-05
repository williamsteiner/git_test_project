import pandas as pd
import matplotlib.pyplot as plt

# Function to fetch ETF data from Yahoo Finance
def fetch_etf_data(etf, start_date, end_date):
    try:
        data = pd.read_csv(f'https://query1.finance.yahoo.com/v7/finance/download/{etf}?period1={start_date}&period2={end_date}&interval=1d&events=history')
        data['Date'] = pd.to_datetime(data['Date'])
        data.set_index('Date', inplace=True)
        
        # Fetch dividend data
        dividends = pd.read_csv(f'https://query1.finance.yahoo.com/v7/finance/download/{etf}?period1={start_date}&period2={end_date}&interval=1d&events=div')
        dividends['Date'] = pd.to_datetime(dividends['Date'])
        dividends.set_index('Date', inplace=True)
        
        # Calculate dividend per share
        dividend_per_share = dividends['Dividends'].fillna(0).sum() / len(data)
        
        return data, dividend_per_share
    except Exception as e:
        print(f"Error fetching data for {etf}: {e}")
        return None, None

# Function to calculate cumulative growth of ETF including dividends
def calculate_cumulative_growth(data, initial_investment, dividend_per_share):
    """Calculate the cumulative growth of an ETF including dividends."""
    # Calculate daily returns
    daily_returns = data['Close'].pct_change()
    
    # Calculate cumulative returns
    cumulative_returns = (1 + daily_returns).cumprod()
    
    # Calculate number of shares based on initial investment
    initial_price = data.iloc[0]['Close']
    num_shares = initial_investment / initial_price
    
    # Calculate dividends
    dividends = num_shares * dividend_per_share
    
    # Include dividends
    cumulative_returns = cumulative_returns * (1 + dividends / data.shift(1)['Close'].fillna(method='ffill').fillna(0))
    
    # Calculate ETF value
    etf_value = num_shares * data['Close']
    
    return etf_value

def plot_cumulative_growth(portfolio, etf2, start_date, end_date, initial_investment=100000):
    """Fetch data for a portfolio of ETFs and plot their cumulative growth compared to ETF2 from start_date to end_date."""
    # Fetch data for ETFs in the portfolio including dividends
    portfolio_data = {}
    portfolio_dividends = {}
    for etf in portfolio:
        etf_data, dividend_per_share = fetch_etf_data(etf, start_date, end_date)
        if etf_data is not None:
            portfolio_data[etf] = etf_data
            portfolio_dividends[etf] = dividend_per_share
    
    # Fetch data for ETF2 (PTY) including dividends
    etf2_data, etf2_dividends = fetch_etf_data(etf2, start_date, end_date)
    if etf2_data is None:
        return
    
    # Calculate initial investment for each ETF in the portfolio
    num_etfs = len(portfolio)
    initial_investment_per_etf = initial_investment / num_etfs
    
    # Calculate cumulative growth for the portfolio and ETF2 including dividends
    portfolio_growth = pd.DataFrame()
    for etf in portfolio_data:
        portfolio_growth[etf] = calculate_cumulative_growth(portfolio_data[etf], initial_investment_per_etf, portfolio_dividends[etf])
    
    # Total portfolio value
    total_portfolio_value = portfolio_growth.sum(axis=1)
    
    # Calculate cumulative growth for ETF2
    etf2_growth = calculate_cumulative_growth(etf2_data, initial_investment, etf2_dividends)
    
    # Adjust portfolio value for the first month
    total_portfolio_value.iloc[0] = initial_investment
    
    # Plot cumulative growth of portfolio and ETF2
    plt.figure(figsize=(12, 6))
    plt.plot(total_portfolio_value.index, total_portfolio_value.values / 1000, label='Portfolio Total', linestyle='-', color='green')  # Display total portfolio as solid line
    plt.plot(etf2_growth.index, etf2_growth.values / 1000, label=etf2, linestyle='--', color='black')  # Display ETF2 as dashed line
    
    # Add monthly values for portfolio
    for date, value in total_portfolio_value.items():
        if date.is_month_end:
            plt.text(date, value / 1000, f'{int(value / 1000):,}', ha='center', va='bottom')
    
    # Add monthly values for ETF2
    for date, value in etf2_growth.items():
        if date.is_month_end:
            plt.text(date, value / 1000, f'{int(value / 1000):,}', ha='center', va='bottom')
    
    plt.title('Cumulative Growth of ETF Portfolio vs. ETF')
    plt.xlabel('Date')
    plt.ylabel('Portfolio Value (Thousands of $)')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Example usage
portfolio = ['VTI', 'VOO']  # Portfolio of ETFs
etf2 = 'PTY'  # ETF to compare
start_date = '2023-01-01'
end_date = '2024-12-31'
plot_cumulative_growth(portfolio, etf2, start_date, end_date)
