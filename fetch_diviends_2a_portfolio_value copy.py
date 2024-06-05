import json

def calculate_portfolio_value(data, shares_data):
    portfolio_value = {}
    for stock_info in shares_data:
        stock = stock_info["Stock"]
        shares = stock_info["Shares"]
        if stock in data:
            portfolio_value[stock] = {}
            for year, months_data in data[stock].items():
                portfolio_value[stock][year] = {}
                for month, values in sorted(months_data.items(), key=lambda x: int(x[0])):
                    dividend = values.get("Dividend", 0)
                    price = values.get("Stock Price", 0)
                    dividend_income = shares * dividend
                    stock_value = shares * price
                    portfolio_value[stock][year][month] = {
                        "Dividend Income": round(dividend_income, 4),
                        "Stock Value": round(stock_value, 4)
                    }
    return portfolio_value

def main():
    input_file = 'dividend_stock_data.json'
    shares_file = 'stocks.json'
    portfolio_value_file = 'portfolio_value.json'

    with open(input_file, 'r') as file:
        data = json.load(file)

    with open(shares_file, 'r') as file:
        shares_data = json.load(file)

    portfolio_value = calculate_portfolio_value(data, shares_data)

    with open(portfolio_value_file, 'w') as file:
        json.dump(portfolio_value, file, indent=4)

    print("Portfolio value calculated and saved to", portfolio_value_file)

if __name__ == "__main__":
    main()
