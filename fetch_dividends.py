import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import json
from datetime import datetime

# Function to fetch dividend data for an ETF
def fetch_dividend_data(etf, start_date, end_date):
    try:
        ticker = yf.Ticker(etf)
        dividends = ticker.dividends
        dividends = dividends.loc[start_date:end_date]
        dividends.index = pd.to_datetime(dividends.index)
        return dividends
    except Exception as e:
        print(f"Error fetching data for {etf}: {e}")
        return pd.Series()

# Function to process ETF list from CSV and fetch dividend data
def process_etfs(etf_list, start_date, end_date):
    dividend_dict = {}
    for etf in etf_list:
        dividends = fetch_dividend_data(etf, start_date, end_date)
        if not dividends.empty:
            dividend_dict[etf] = dividends
    return dividend_dict

# Function to compare dividends this year versus last year
def compare_dividends(dividend_dict):
    this_year = datetime.now().year
    last_year = this_year - 1

    comparison_dict = {}
    for etf, dividends in dividend_dict.items():
        this_year_dividends = dividends[dividends.index.year == this_year].sum()
        last_year_dividends = dividends[dividends.index.year == last_year].sum()
        comparison_dict[etf] = {
            "this_year": this_year_dividends,
            "last_year": last_year_dividends
        }
    return comparison_dict

# Function to plot dividend comparison as a bar chart
def plot_dividend_comparison_bar(comparison_dict):
    etfs = list(comparison_dict.keys())
    this_year_values = [comparison_dict[etf]['this_year'] for etf in etfs]
    last_year_values = [comparison_dict[etf]['last_year'] for etf in etfs]

    x = range(len(etfs))
    
    fig, ax = plt.subplots()
    bar_width = 0.4

    bars1 = ax.bar(x, this_year_values, width=bar_width, label='This Year', align='center')
    bars2 = ax.bar([i + bar_width for i in x], last_year_values, width=bar_width, label='Last Year', align='center')
    
    ax.set_xlabel('ETFs')
    ax.set_ylabel('Total Dividends (Thousands)')
    ax.set_title('Dividends This Year vs Last Year')
    ax.set_xticks([i + bar_width / 2 for i in x])
    ax.set_xticklabels(etfs, rotation=45)
    ax.legend()
    
    # Add values on top of bars
    for bar in bars1:
        height = bar.get_height()
        ax.annotate(f'{height / 1000:.1f}k', xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords='offset points', ha='center', va='bottom')

    for bar in bars2:
        height = bar.get_height()
        ax.annotate(f'{height / 1000:.1f}k', xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords='offset points', ha='center', va='bottom')
    
    plt.tight_layout()
    plt.show()

# Function to plot dividend comparison as a line chart
def plot_dividend_comparison_line(dividend_dict):
    fig, ax = plt.subplots()

    this_year = datetime.now().year
    last_year = this_year - 1

    for etf, dividends in dividend_dict.items():
        dividends_this_year = dividends[dividends.index.year == this_year].resample('M').sum()
        dividends_last_year = dividends[dividends.index.year == last_year].resample('M').sum()

        if not dividends_this_year.empty:
            ax.plot(dividends_this_year.index, dividends_this_year.cumsum(), label=f'{etf} This Year')
        if not dividends_last_year.empty:
            ax.plot(dividends_last_year.index, dividends_last_year.cumsum(), label=f'{etf} Last Year')

    ax.set_xlabel('Date')
    ax.set_ylabel('Cumulative Dividends (Thousands)')
    ax.set_title('Cumulative Dividends This Year vs Last Year')
    ax.legend()

    # Add values at each month
    for etf, dividends in dividend_dict.items():
        dividends_this_year = dividends[dividends.index.year == this_year].resample('M').sum().cumsum()
        dividends_last_year = dividends[dividends.index.year == last_year].resample('M').sum().cumsum()

        if not dividends_this_year.empty:
            for date, value in dividends_this_year.items():
                ax.annotate(f'{value / 1000:.1f}k', xy=(date, value), xytext=(0, 3), textcoords='offset points', ha='center', va='bottom')

        if not dividends_last_year.empty:
            for date, value in dividends_last_year.items():
                ax.annotate(f'{value / 1000:.1f}k', xy=(date, value), xytext=(0, 3), textcoords='offset points', ha='center', va='bottom')

    plt.tight_layout()
    plt.show()

# Function to save dividend data to JSON
def save_to_json(dividend_dict, filename):
    dividend_dict_json = {etf: dividends.to_dict() for etf, dividends in dividend_dict.items()}
    with open(filename, 'w') as json_file:
        json.dump(dividend_dict_json, json_file, indent=4)

def main(chart_type='line'):
    # Read ETF list from CSV
    etf_csv = 'etf_list.csv'
    etf_list = pd.read_csv(etf_csv)['ETF'].tolist()

    # Define date range
    start_date = '2023-01-01'
    end_date = '2024-12-31'
    
    # Fetch and process dividend data
    dividend_dict = process_etfs(etf_list, start_date, end_date)
    
    # Compare dividends this year versus last year
    comparison_dict = compare_dividends(dividend_dict)
    
    # Plot dividend comparison based on the chart type
    if chart_type == 'bar':
        plot_dividend_comparison_bar(comparison_dict)
    else:
        plot_dividend_comparison_line(dividend_dict)
    
    # Save dividend data to JSON
    json_filename = 'dividend_data.json'
    save_to_json(dividend_dict, json_filename)
    print(f"Dividend data saved to {json_filename}")

if __name__ == "__main__":
    main('line')  # Change 'line' to 'bar' to plot bar chart
