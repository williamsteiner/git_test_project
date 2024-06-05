import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

def fetch_etf_data(symbol):
    """Fetch ETF data from Yahoo Finance."""
    try:
        # Fetch historical data for the symbol
        df = yf.download(symbol, start='2023-01-01', end='2024-12-31')
        
        # Select the 'Close' price
        close_price = df['Close']
        
        # Convert the data to numeric values
        close_price_numeric = pd.to_numeric(close_price, errors='coerce')
        
        return close_price_numeric
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None

def get_current_and_previous_year_data(df):
    """Filter data for the current and previous year."""
    current_year = pd.to_datetime('today').year
    previous_year = current_year - 1
    df_filtered = df[df.index.year.isin([previous_year, current_year])]
    
    return df_filtered

def calculate_combined_growth(etfs):
    """Calculate the combined growth of ETFs."""
    combined_growth = pd.Series(index=pd.date_range(start='2023-01-01', end='2024-12-31', freq='D'), dtype=float)
    
    for etf in etfs:
        df = fetch_etf_data(etf)
        if df is None:
            continue
        
        df_filtered = get_current_and_previous_year_data(df)
        
        # Calculate daily returns
        daily_returns = df_filtered.pct_change()
        
        # Calculate cumulative returns
        cumulative_returns = (1 + daily_returns).cumprod()
        
        # Calculate ETF value
        etf_value = cumulative_returns * 100000  # Initial investment of $100,000
        
        # Add ETF value to combined growth
        combined_growth += etf_value
    
    return combined_growth.fillna(method='ffill').fillna(0)  # Forward fill and replace NaN values with zeros

def calculate_portfolio_growth(etfs, initial_investment=100000):
    """Calculate the cumulative growth of a portfolio based on combined ETFs."""
    combined_growth = calculate_combined_growth(etfs)
    daily_returns = combined_growth.pct_change()
    cumulative_returns = (1 + daily_returns).cumprod()
    portfolio_growth = initial_investment * cumulative_returns
    
    return portfolio_growth.fillna(method='ffill').fillna(0)  # Forward fill and replace NaN values with zeros

def plot_cumulative_growth(etfs, combine=True):
    """Fetch data for multiple ETFs and plot their cumulative growth for current and previous year."""
    plt.figure(figsize=(12, 6))
    
    combined_data = None

    for etf in etfs:
        df = fetch_etf_data(etf)
        if df is None:
            continue
        
        df_filtered = get_current_and_previous_year_data(df)
        
        # Calculate average value
        average_value = df_filtered.groupby(pd.Grouper(freq='M')).mean()
        
        # Combine the data
        if combine:
            if combined_data is None:
                combined_data = average_value
            else:
                combined_data += average_value
                
        # Plot the average value for each ETF separately if combine is False
        if not combine:
            plt.plot(average_value.index, average_value.values, marker='o', label=etf)

    # Plot the combined average value
    if combine and combined_data is not None:
        combined_data /= len(etfs)  # Calculate the average
        plt.plot(combined_data.index, combined_data.values, marker='o', label='Combined')
        
        # Annotate each month marker with its value (rounded to whole numbers)
        for i in range(len(combined_data)):
            plt.text(combined_data.index[i], combined_data.values[i], f'{int(combined_data.values[i]):,}', ha='center', va='bottom')

    # Plot the portfolio growth
    portfolio_growth = calculate_portfolio_growth(etfs)
    plt.plot(portfolio_growth.index, portfolio_growth.values, marker='o', label='Portfolio', linestyle='--')
    
    # Annotate each month marker with its value (rounded to whole numbers)
    for i in range(len(portfolio_growth)):
        plt.text(portfolio_growth.index[i], portfolio_growth.values[i], f'{int(portfolio_growth.values[i]):,}', ha='center', va='bottom')

    plt.title('Portfolio Value for Current and Previous Year')
    plt.xlabel('Year-Month')
    plt.ylabel('Portfolio Value ($)')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show(block=True)  # Keeps the plot window open

# Example usage
etfs = ['VTI', 'VOO', 'QQQ']  # Replace with your portfolio ETFs
plot_cumulative_growth(etfs, combine=True)
