import yfinance as yf
import json
from datetime import datetime
import matplotlib.pyplot as plt

# Function to retrieve dividend and stock price data for the last five years and export it to a JSON file
def export_dividend_stock_data(json_file, json_output_file):
    # Read JSON file containing stocks
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    # Get portfolio name
    portfolio_name = list(data.keys())[0]

    # Get stock data
    stocks_data = data.get(portfolio_name, {}).get('Stocks', [])
    
    combined_data = {}
    
    # Get the current date
    current_date = datetime.now()
    
    # Iterate through each stock
    for stock_info in stocks_data:
        stock = stock_info['Stock']
        shares = stock_info.get('Shares', 0)
        
        try:
            # Fetch dividend data
            ticker = yf.Ticker(stock)
            dividends = ticker.dividends
            
            # Fetch historical stock prices
            history = ticker.history(period='5y', interval='1mo')  # Fetch last 5 years of monthly historical data
            
            # Filter dividend and stock price data for the last five years
            dividends_last_5_years = dividends[(dividends.index.year >= current_date.year - 5) & (dividends.index.year <= current_date.year)]
            prices_last_5_years = history[(history.index.year >= current_date.year - 5) & (history.index.year <= current_date.year)]
            
            # Combine dividend and stock price data by year and month
            for year in range(current_date.year - 4, current_date.year + 1):
                for month in range(1, 13):
                    monthly_dividends = dividends_last_5_years[(dividends_last_5_years.index.year == year) & (dividends_last_5_years.index.month == month)]
                    monthly_prices = prices_last_5_years[(prices_last_5_years.index.year == year) & (prices_last_5_years.index.month == month)]['Close']
                    
                    if str(year) not in combined_data:
                        combined_data[str(year)] = {}
                    if str(month) not in combined_data[str(year)]:
                        combined_data[str(year)][str(month)] = {'Dividend': 0, 'Total Value': 0}
                    
                    combined_data[str(year)][str(month)]['Dividend'] += monthly_dividends.sum()
                    combined_data[str(year)][str(month)]['Total Value'] += shares * (monthly_prices.iloc[0] if not monthly_prices.empty else 0)
                    
        except Exception as e:
            print(f"Error fetching data for stock {stock}: {e}")
    
    # Export data to JSON file
    with open(json_output_file, 'w') as file:
        json.dump({portfolio_name: {'Stocks': {'All Stocks': combined_data}}}, file, indent=4)
    
    print("Data exported successfully.")

# Function to plot the combined data of dividends and total values
def plot_combined_data(json_file):
    # Load data from JSON file
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    # Get combined data for all stocks
    combined_data = data[list(data.keys())[0]]['Stocks']['All Stocks']
    
    months = []
    combined_values = []
    for year, year_data in combined_data.items():
        for month, month_data in year_data.items():
            value = month_data['Dividend'] + month_data['Total Value']
            if value != 0:
                months.append(f"{year}-{month}")
                combined_values.append(value)
    
    # Calculate percentage growth year over year
    growth_rates = [100 * ((combined_values[i] - combined_values[i-12]) / combined_values[i-12]) for i in range(12, len(combined_values))]
    total_growth = (combined_values[-1] - combined_values[0]) / combined_values[0] * 100
    
    # Plotting
    fig, ax = plt.subplots()
    ax.plot(months, combined_values, label='Combined Data')
    
    # Add dollar amounts for each new year
    last_year = None
    for i, year_month in enumerate(months):
        year = year_month.split('-')[0]
        if year != last_year:
            ax.text(i, combined_values[i], f"${combined_values[i]:,.0f}", ha='right', va='bottom', rotation=45)
            last_year = year
    
    ax.set_xlabel('Year-Month')
    ax.set_ylabel('Combined Value')
    ax.set_title(f'Combined Dividend and Total Value by Year/Month\nTotal Growth: {total_growth:.2f}%')
    ax.set_xticks(months[::12])
    ax.tick_params(axis='x', rotation=45)
    ax.legend()
    plt.tight_layout()
    plt.show()

# Example usage
json_file = 'portfolio_stocks.json'  # Replace with the path to your JSON file containing the list of stocks
json_output_file = 'dividend_stock_data.json'  # Output JSON filename
export_dividend_stock_data(json_file, json_output_file)
plot_combined_data(json_output_file)
