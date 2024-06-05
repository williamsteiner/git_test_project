import json
import pandas as pd
import matplotlib.pyplot as plt

def plot_dividend_data(json_file):
    # Read JSON file containing dividend data
    with open(json_file, 'r') as file:
        dividend_data = json.load(file)
    
    # Convert JSON data to DataFrame
    df = pd.DataFrame(dividend_data)
    
    # Plotting
    plt.figure(figsize=(12, 8))
    
    # Iterate over each stock
    for stock, years_data in df.items():
        has_2024_data = '2024' in years_data.keys()
        
        # Iterate over each year
        for year, months_data in years_data.items():
            months = list(map(int, months_data.keys())) # Extract months as integers
            dividends = list(months_data.values())
            
            # Exclude 2023 months if there is no associated 2024 data
            if year == '2023' and not has_2024_data:
                continue
            
            plt.plot(months, dividends, label=f'{stock} {year}')
            
            # Display dividend values on the line chart
            for month, dividend in zip(months, dividends):
                plt.text(month, dividend, f'{dividend:.3f}', ha='center', va='bottom')
    
    # Customize the plot
    plt.title('Year-wise Dividend Values by Month')
    plt.xlabel('Month')
    plt.ylabel('Dividend')
    plt.legend()
    plt.grid(True)
    plt.xticks(range(1, 13))
    plt.show()

# Example usage
json_file = 'dividend_data.json'  # Replace with the path to your JSON file containing the dividend data
plot_dividend_data(json_file)
