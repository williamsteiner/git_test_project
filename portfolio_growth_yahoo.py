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
        
        return close_price
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None

def get_current_and_previous_year_data(df):
    """Filter data for the current and previous year."""
    current_year = pd.to_datetime('today').year
    previous_year = current_year - 1
    df_filtered = df[df.index.year.isin([previous_year, current_year])]
    
    return df_filtered

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

    # Fetch data for SPY (S&P 500 ETF)
    spy_data = fetch_etf_data('SPY')
    if spy_data is not None:
        spy_filtered = get_current_and_previous_year_data(spy_data)
        average_value_spy = spy_filtered.groupby(pd.Grouper(freq='M')).mean()
        plt.plot(average_value_spy.index, average_value_spy.values, marker='o', label='SPY')
        
        # Annotate each month marker with its value (rounded to whole numbers)
        for i in range(len(average_value_spy)):
            plt.text(average_value_spy.index[i], average_value_spy.values[i], f'{int(average_value_spy.values[i]):,}', ha='center', va='bottom')

    plt.title('Average ETF Value for Current and Previous Year')
    plt.xlabel('Year-Month')
    plt.ylabel('Average Close Price')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show(block=True)  # Keeps the plot window open

# Example usage
etfs = ['VTI', 'VOO', 'QQQ']  # Replace with your portfolio ETFs
plot_cumulative_growth(etfs, combine=False)
