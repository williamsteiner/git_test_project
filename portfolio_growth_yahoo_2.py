import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

def fetch_etf_data(symbol, start_date, end_date):
    """Fetch ETF data from Yahoo Finance."""
    try:
        # Fetch historical data for the symbol
        df = yf.download(symbol, start=start_date, end=end_date)
        
        # Select the 'Close' price
        close_price = df['Close']
        
        return close_price
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None

def calculate_cumulative_growth(data, initial_investment):
    """Calculate the cumulative growth of an ETF."""
    # Calculate daily returns
    daily_returns = data.pct_change()
    
    # Calculate cumulative returns
    cumulative_returns = (1 + daily_returns).cumprod()
    
    # Calculate ETF value
    etf_value = initial_investment * cumulative_returns
    
    return etf_value

def plot_cumulative_growth(etf1, etf2, start_date, end_date, initial_investment=100000):
    """Fetch data for two ETFs and plot their cumulative growth from start_date to end_date."""
    # Fetch data for ETF1 (VTI)
    etf1_data = fetch_etf_data(etf1, start_date, end_date)
    if etf1_data is None:
        return
    
    # Fetch data for ETF2 (SPY)
    etf2_data = fetch_etf_data(etf2, start_date, end_date)
    if etf2_data is None:
        return
    
    # Calculate cumulative growth for ETF1 and ETF2
    etf1_growth = calculate_cumulative_growth(etf1_data, initial_investment)
    etf2_growth = calculate_cumulative_growth(etf2_data, initial_investment)
    
    # Plot cumulative growth
    plt.figure(figsize=(12, 6))
    plt.plot(etf1_growth.index, etf1_growth.values / 1000, label=etf1)  # Display in thousands
    plt.plot(etf2_growth.index, etf2_growth.values / 1000, label=etf2)  # Display in thousands
    
    # Annotate each month with portfolio value and plot vertical lines
    for date in pd.date_range(start=start_date, end=end_date, freq='M'):
        try:
            month_end_value_etf1 = etf1_growth.loc[date]
            month_end_value_etf2 = etf2_growth.loc[date]
            
            # Show only the integer value for each month
            plt.text(date, int(month_end_value_etf1) / 1000, f'{int(month_end_value_etf1 / 1000):,}', ha='center', va='bottom', color='blue')
            plt.text(date, int(month_end_value_etf2) / 1000, f'{int(month_end_value_etf2 / 1000):,}', ha='center', va='bottom', color='orange')
        except KeyError:
            pass
        
        # Plot vertical lines at the beginning of each month
        plt.axvline(date, color='gray', linestyle='--', alpha=0.5)
    
    plt.title('Cumulative Growth of ETFs')
    plt.xlabel('Date')
    plt.ylabel('Portfolio Value (Thousands of $)')
    plt.legend()
    plt.grid(True)
    plt.show()

# Specify parameters
etf1 = 'VTI'  # VTI ETF
etf2 = 'PTY'  # SPY ETF
start_date = '2023-01-01'
end_date = '2024-12-31'

# Plot cumulative growth of ETFs
plot_cumulative_growth(etf1, etf2, start_date, end_date)
