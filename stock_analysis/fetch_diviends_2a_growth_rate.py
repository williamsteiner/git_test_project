import json

def calculate_growth_rate(data, portfolio_name):
    growth_data = {}
    if portfolio_name in data and "Stocks" in data[portfolio_name]:
        for stock, years_data in data[portfolio_name]["Stocks"].items():
            growth_data[stock] = {}
            for year, months_data in years_data.items():
                growth_data[stock][year] = {}
                previous_dividend = None
                previous_price = None
                for month, values in sorted(months_data.items(), key=lambda x: int(x[0])):
                    dividend = values.get("Dividend", 0)
                    price = values.get("Stock Price", 0)
                    if previous_dividend is not None and previous_dividend != 0:
                        dividend_growth_rate = (dividend - previous_dividend) / previous_dividend
                    else:
                        dividend_growth_rate = 0
                    if previous_price is not None and previous_price != 0:
                        price_growth_rate = (price - previous_price) / previous_price
                    else:
                        price_growth_rate = 0
                    growth_data[stock][year][month] = {
                        "Dividend Growth Rate": round(dividend_growth_rate, 4),
                        "Price Growth Rate": round(price_growth_rate, 4)
                    }
                    previous_dividend = dividend
                    previous_price = price
    else:
        print(f"Portfolio '{portfolio_name}' not found in the input file or missing stocks data.")
    return growth_data

def main():
    input_file = 'dividend_stock_data.json'
    output_file = 'growth_rates.json'
    portfolio_name = 'My Portfolio'  # Specify the portfolio name here

    with open(input_file, 'r') as file:
        data = json.load(file)

    growth_data = calculate_growth_rate(data, portfolio_name)

    if growth_data:
        # Add the portfolio name as a parent-level element
        output_data = {
            portfolio_name: {
                "Stocks": growth_data
            }
        }

        with open(output_file, 'w') as file:
            json.dump(output_data, file, indent=4)

        print("Growth rates calculated and saved to", output_file)

if __name__ == "__main__":
    main()
