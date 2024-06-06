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
                stock_growth[stock].append(total_value)

# Plotting the data
plt.figure(figsize=(10, 6))
for stock, growth in stock_growth.items():
    plt.plot(growth, label=stock)

# Annotate value for every 3 months
for stock in stock_growth.keys():
    for i in range(0, len(stock_growth[stock]), 3):
        plt.annotate(f'{stock_growth[stock][i] / 1000:.1f}K', (i, stock_growth[stock][i]), textcoords="offset points", xytext=(0,10), ha='center')

plt.xlabel('Month')
plt.ylabel('Portfolio Value (Thousands)')
plt.title('Portfolio Growth including Dividend Reinvestment')
plt.legend()
plt.grid(True)
plt.show()
