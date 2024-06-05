import json

def calculate_portfolio_value(data, shares_data, adjustments_data):
    portfolio_value = {}
    for portfolio_name, portfolio_stocks in data.items():
        portfolio_value[portfolio_name] = {}
        for stock, years_data in portfolio_stocks["Stocks"].items():
            portfolio_value[portfolio_name][stock] = {}
            for year, months_data in years_data.items():
                portfolio_value[portfolio_name][stock][year] = {}
                for month, values in sorted(months_data.items(), key=lambda x: int(x[0])):
                    dividend = values.get("Dividend", 0)
                    price = values.get("Stock Price", 0)

                    # Check for adjustments and apply them if present
                    ##if adjustments_data.get(portfolio_name, {}).get(stock, {}).get(year, {}).get(month):
                    if adjustments_data.get(portfolio_name, {}).get("Stocks", {}).get(stock, {}).get(year, {}).get(month):
                        ##adjustment = adjustments_data[portfolio_name][stock][year][month]
                        adjustment = adjustments_data.get(portfolio_name, {}).get("Stocks", {}).get(stock, {}).get(year, {}).get(month)
                        dividend = adjustment.get("Dividend", dividend)
                        price = adjustment.get("Stock Price", price)

                    portfolio_value[portfolio_name][stock][year][month] = {
                        "Dividend": dividend,
                        "Stock Price": price
                    }

    return portfolio_value

def main():
    input_file = 'dividend_stock_data.json'
    shares_file = 'portfolio_stocks.json'
    adjustments_file = 'stock_data_adjustments.json'
    portfolio_value_file = 'portfolio_value.json'

    with open(input_file, 'r') as file:
        data = json.load(file)

    with open(shares_file, 'r') as file:
        shares_data = json.load(file)

    with open(adjustments_file, 'r') as file:
        adjustments_data = json.load(file)

    portfolio_value = calculate_portfolio_value(data, shares_data, adjustments_data)

    with open(portfolio_value_file, 'w') as file:
        json.dump(portfolio_value, file, indent=4)

    print("Portfolio value calculated and saved to", portfolio_value_file)

if __name__ == "__main__":
    main()
