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

# Example usage
etf_data = fetch_etf_data('VTI')
print(etf_data.head())

etfs = ['VTI', 'VOO', 'QQQ']  # Replace with your portfolio ETFs

for etf in etfs:
    df = fetch_etf_data(etf)
    print(f"ETF: {etf}")
    print(df.isnull().sum())
    print()

