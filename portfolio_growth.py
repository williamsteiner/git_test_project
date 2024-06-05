import requests
import pandas as pd
import matplotlib.pyplot as plt

# Define your Alpha Vantage API key
API_KEY1 = 'N37VYJ2PF36H5BUS' 
API_KEY  ='KE7RYBG7TU0MPRJ6'
# -------------------------------------- #   
   

def fetch_etf_data(symbol, api_key):
    """Fetch ETF data from Alpha Vantage API using the TIME_SERIES_MONTHLY endpoint."""
    try:
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={symbol}&apikey={api_key}'
        response = requests.get(url)
        data = response.json()
        print(data)

        if 'Monthly Time Series' not in data:
            print(f"Error: 'Monthly Time Series' not found in API response for {symbol}.")
            return None

        time_series = data['Monthly Time Series']
        
        df = pd.DataFrame.from_dict(time_series, orient='index')
        df.index = pd.to_datetime(df.index)
        df = df.sort_index()
        df = df.rename(columns={"4. close": "close"})
        df['close'] = pd.to_numeric(df['close'])
        
        return df
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None

def get_current_and_previous_year_data(df):
    """Filter data for the current and previous year."""
    current_year = pd.to_datetime('today').year
    previous_year = current_year - 1
    df_filtered = df[df.index.year.isin([previous_year, current_year])]
    
    return df_filtered

def plot_cumulative_growth(etfs, api_key, combine=True):
    """Fetch data for multiple ETFs and plot their cumulative growth for current and previous year."""
    plt.figure(figsize=(12, 6))
    
    if combine:
        combined_data = None

    for etf in etfs:
        df = fetch_etf_data(etf, api_key)
        if df is None:
            continue
        
        print(f"Fetched data for {etf}:")
        print(df.head())
        
        df_filtered = get_current_and_previous_year_data(df)
        
        # Calculate cumulative growth
        cumulative_growth = df_filtered.groupby(df_filtered.index)['close'].mean().cumsum()
        
        # Plot the cumulative growth for each ETF separately
        if not combine:
            plt.plot(cumulative_growth.index, cumulative_growth.values, marker='o', label=etf)
        
        # Combine the data
        if combine:
            if combined_data is None:
                combined_data = cumulative_growth
            else:
                combined_data += cumulative_growth

    # Plot the combined cumulative growth
    if combine and combined_data is not None:
        plt.plot(combined_data.index, combined_data.values, marker='o', label='Combined')

    # Add a line for comparing to SPY (S&P 500 ETF)
    df_spy = fetch_etf_data('SPY', api_key)
    if df_spy is not None:
        print("Fetched data for SPY:")
        print(df_spy.head())
        
        df_spy_filtered = get_current_and_previous_year_data(df_spy)
        cumulative_growth_spy = df_spy_filtered.groupby(df_spy_filtered.index)['close'].mean().cumsum()
        plt.plot(cumulative_growth_spy.index, cumulative_growth_spy.values, marker='o', label='SPY')

    # Annotate each data point with its value (rounded to whole numbers)
    if combine and combined_data is not None:
        for i, value in enumerate(combined_data.values):
            plt.text(combined_data.index[i], value, f'{int(value):,}', ha='center', va='bottom')

    plt.title('Cumulative ETF Growth for Current and Previous Year')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Close Price')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show(block=True)  # Keeps the plot window open

# Example usage
etfs = ['VTI', 'VOO', 'QQQ']  # Replace with your portfolio ETFs
plot_cumulative_growth(etfs, API_KEY, combine=True)
