import json
import matplotlib.pyplot as plt

# Read portfolio data from JSON file
with open('portfolio_value.json', 'r') as f:
    portfolio_data = json.load(f)

# Initial investment
initial_investment = 100000

# Initialize dictionaries to store the number of shares and dividend totals for each stock
shares = {stock: initial_investment / portfolio_data["My Portfolio"][stock]["2020"]["1"]["Stock Price"] for stock in portfolio_data["My Portfolio"]}
dividend_totals = {stock: [] for stock in portfolio_data["My Portfolio"]}

# Initialize dictionary to store stock growth including dividend reinvestment
stock_growth = {stock: [] for stock in portfolio_data["My Portfolio"]}

# Initialize variables to track the last seen year
last_seen_year = None

# Iterate over each month and calculate stock growth including dividend reinvestment
for stock, years in portfolio_data["My Portfolio"].items():
    for year, months in years.items():
        for month, data in months.items():
            stock_price = data["Stock Price"]
            dividend = data["Dividend"]
            # Check if stock price is not zero to avoid division by zero
            if stock_price != 0:
                # Update number of shares based on dividend reinvestment
                shares[stock] += (dividend * shares[stock]) / stock_price
                # Calculate dividend total as dividend value * shares
                dividend_total = dividend * shares[stock]
                dividend_totals[stock].append(dividend_total)
                # Calculate total value as shares * stock price
                total_value = shares[stock] * stock_price
                # Append total value to stock growth
                stock_growth[stock].append((year, month, total_value))

# Plotting the data
plt.figure(figsize=(10, 6))
for stock, growth in stock_growth.items():
    # Separate the data points and concatenate year and month for x-axis labels
    data_points = [value[2] / 1000 for value in growth]  # Convert to thousands
    x_ticks = [f"{value[0]}-{value[1]}" for value in growth]
    plt.plot(data_points, label=stock)
    # Add line data values for every 3-month interval in thousands
    for i in range(0, len(data_points), 3):
        plt.text(i, data_points[i], f'{data_points[i]:,.0f}K', ha='center', va='bottom', fontsize=8)
    # Set x-axis labels with year and month
    plt.xticks(range(len(data_points)), x_ticks, rotation=45)

plt.xlabel('Year-Month')
plt.ylabel('Portfolio Value (in thousands)')
plt.title('Portfolio Growth including Dividend Reinvestment')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
