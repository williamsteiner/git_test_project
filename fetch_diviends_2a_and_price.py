import yfinance as yf
import pandas as pd
import json
from datetime import datetime

# Function to retrieve dividend and stock price data for the last five years and export it to a JSON file
def export_dividend_stock_data(json_file, json_output_file):
    # Read JSON file containing stocks
    with open(json_file, 'r') as f:
        stocks_data = json.load(f)
    
    dividend_stock_data = {}
    
    # Get the current date
    current_date = datetime.now()
    
    # Iterate through each stock
    for stock_info in stocks_data:
        stock = stock_info['Stock']
        shares = stock_info.get('Shares', 1)  # Default to 1 if Shares field not provided
        
        try:
            # Fetch dividend data
            ticker = yf.Ticker(stock)
            dividends = ticker.dividends
            
            # Fetch historical stock prices
            history = ticker.history(period='5y')  # Fetch last 5 years of historical data
            
            # Filter dividend and stock price data for the last five years
            dividends_last_5_years = dividends[(dividends.index.year >= current_date.year - 5) & (dividends.index.year <= current_date.year)]
            prices_last_5_years = history[(history.index.year >= current_date.year - 5) & (history.index.year <= current_date.year)]
            
            # Combine dividend and stock price data by year and month
            data = {}
            for year in range(current_date.year - 4, current_date.year + 1):
                data[str(year)] = {}
                for month in range(1, 13):
                    monthly_dividends = dividends_last_5_years[(dividends_last_5_years.index.year == year) & (dividends_last_5_years.index.month == month)]
                    monthly_prices = prices_last_5_years[(prices_last_5_years.index.year == year) & (prices_last_5_years.index.month == month)]['Close']
                    data[str(year)][str(month)] = {
                        'Dividend': monthly_dividends.sum() * shares,
                        'Stock Price': monthly_prices.mean() * shares if not monthly_prices.empty else 0
                    }
            
            dividend_stock_data[stock] = data
        except Exception as e:
            print(f"Error fetching data for stock {stock}: {e}")
    
    # Export data to JSON file
    with open(json_output_file, 'w') as file:
        json.dump(dividend_stock_data, file, indent=4)
    
    print("Data exported successfully.")

# Example usage
json_file = 'stocks.json'  # Replace with the path to your JSON file containing the list of stocks
json_output_file = 'dividend_stock_data.json'  # Output JSON filename
export_dividend_stock_data(json_file, json_output_file)
