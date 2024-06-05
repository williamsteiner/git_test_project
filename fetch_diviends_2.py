import yfinance as yf
import pandas as pd
import json

# Function to retrieve and export dividend data to a JSON file
def export_dividend_data(csv_file, filename):
    # Read CSV file containing stocks
    stocks_df = pd.read_csv(csv_file)
    stocks = stocks_df['Stock'].tolist()
    
    all_data = []
    
    for stock in stocks:
        ticker = yf.Ticker(stock)
        dividends = ticker.dividends
        
        # Convert dividends to a DataFrame
        dividends_df = dividends.reset_index()
        dividends_df.columns = ['Date', 'Dividend']
        dividends_df['Stock'] = stock
        
        all_data.append(dividends_df)
    
    # Combine all dividend data
    df = pd.concat(all_data)
    
    # Extract year and month for grouping
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    
    # Get current and previous year
    current_year = pd.Timestamp.now().year
    previous_year = current_year - 1
    
    # Filter data for the current and previous year
    filtered_data = df[df['Year'].isin([current_year, previous_year])]
    
    # Group by Stock, Year, and Month, then calculate sum of dividends
    monthly_data = filtered_data.groupby(['Stock', 'Year', 'Month'])['Dividend'].sum().reset_index()
    
    # Convert data to dictionary
    dividend_dict = {}
    for index, row in monthly_data.iterrows():
        stock = row['Stock']
        year = row['Year']
        month = row['Month']
        dividend = row['Dividend']
        
        if stock not in dividend_dict:
            dividend_dict[stock] = {}
        if year not in dividend_dict[stock]:
            dividend_dict[stock][year] = {}
        
        dividend_dict[stock][year][month] = dividend
    
    # Export data to JSON file
    with open(filename, 'w') as json_file:
        json.dump(dividend_dict, json_file, indent=4)

# Example usage
csv_file = 'stocks.csv'  # Replace with the path to your CSV file containing the list of stocks
filename = 'dividend_data.json'
export_dividend_data(csv_file, filename)
print("Done")