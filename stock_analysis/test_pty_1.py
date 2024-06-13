import yfinance as yf

# Fetch PTY data from Yahoo Finance
pty = yf.Ticker("PTY")
nav_data = pty.history(period="1mo", start="2020-01-01", end="2020-01-31")

# Print the data
print("NAV Data for January 2020:")
print(nav_data)

# Calculate mean values
mean_close = nav_data["Close"].mean()
mean_high = nav_data["High"].mean()
mean_low = nav_data["Low"].mean()

# Print summary
print("\nSummary:")
print(f"Mean Close: {mean_close}")
print(f"Mean High: {mean_high}")
print(f"Mean Low: {mean_low}")
