import yfinance as yf
import json

def fetch_stock_data(symbol, start_date, end_date, interval='1mo'):
    stock = yf.Ticker(symbol)
    hist = stock.history(start=start_date, end=end_date, interval=interval)
    return hist

def save_to_json(data, filename):
    data.reset_index(inplace=True)  # Reset index to move Date from index to column
    data['Date'] = data['Date'].dt.strftime('%Y-%m')  # Format Date as 'YYYY-MM'
    data_dict = data.to_dict(orient='records')  # Convert DataFrame to list of dictionaries
    with open(filename, 'w') as f:
        json.dump(data_dict, f, indent=4)

if __name__ == '__main__':
    stock_symbol = 'PTY'
    start_date = '2020-01-01'
    end_date = '2024-01-01'
    try:
        stock_data = fetch_stock_data(stock_symbol, start_date, end_date)
        filename = f'{stock_symbol}_2020_stock_data.json'
        save_to_json(stock_data, filename)
        print(f'Successfully fetched and saved data to {filename}')
    except Exception as e:
        print(f'Error: {e}')
