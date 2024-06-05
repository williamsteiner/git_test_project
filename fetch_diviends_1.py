import yfinance as yf
import pandas as pd
import json
import matplotlib.pyplot as plt

# Function to retrieve and export dividend data to a JSON file
def export_and_plot_dividend_data(csv_file, json_filename):
    # Read CSV file containing stocks
    stocks_df = pd.read_csv(csv_file)
    stocks = stocks_df['Stock'].tolist()
    
    all_data = []
    
    for stock in stocks:
        try:
            ticker = yf.Ticker(stock)
            dividends = ticker.dividends
            
            # Convert dividends to a DataFrame
            dividends_df = dividends.reset_index()
            dividends_df.columns = ['Date', 'Dividend']
            dividends_df['Stock'] = stock
            
            all_data.append(dividends_df)
        except:
            print(f"No dividend data available for stock {stock}.")
    
    if not all_data:
        print("No dividend data available for any stock.")
        return
    
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
    
    # Pivot for plotting
    pivot_data = monthly_data.pivot_table(index=['Month'], columns=['Stock', 'Year'], values='Dividend')
    
    # Export data to JSON file
    pivot_data.to_json(json_filename, orient='index', indent=4)
    
    # Plotting
    plt.figure(figsize=(12, 8))
    
    # Set bar width
    bar_width = 0.35
    
    # Calculate the position of each bar on the X-axis
    r1 = range(1, 13)
    r2 = [x + bar_width for x in r1]
    
    # Plot each stock
    for i, stock in enumerate(stocks):
        if (stock, current_year) in pivot_data.columns:
            plt.bar(r1, pivot_data[stock, current_year].fillna(0), width=bar_width, label=f'{stock} {current_year}')
            for j, value in enumerate(pivot_data[stock, current_year].fillna(0)):
                plt.text(j + 1 - 0.15, value + 0.01, f"{value:.2f}", va='bottom', ha='center')
        if (stock, previous_year) in pivot_data.columns:
            plt.bar(r2, pivot_data[stock, previous_year].fillna(0), width=bar_width, label=f'{stock} {previous_year}', linestyle='--')
            for j, value in enumerate(pivot_data[stock, previous_year].fillna(0)):
                plt.text(j + 1 + 0.2, value + 0.01, f"{value:.2f}", va='bottom', ha='center')
    
    # Customize the plot
    plt.title('Monthly Dividend Values')
    plt.xlabel('Month')
    plt.ylabel('Total Dividend')
    plt.legend()
    plt.grid(True)
    plt.xticks(range(1, 13))
    plt.show()

# Example usage
csv_file = 'stocks.csv'  # Replace with the path to your CSV file containing the list of stocks
json_filename = 'dividend_data.json'  # Output JSON filename
export_and_plot_dividend_data(csv_file, json_filename)
