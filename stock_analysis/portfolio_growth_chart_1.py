import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MaxNLocator

# Provided data
data = {
    "PTY": {
        "2020": {
            "1": {"Dividend": 0.13, "Stock Price": 12.577540942600795},
            "2": {"Dividend": 0.13, "Stock Price": 12.511583077280145},
            "3": {"Dividend": 0.13, "Stock Price": 9.497751517729325},
            "4": {"Dividend": 0.13, "Stock Price": 8.966304642813546},
            "5": {"Dividend": 0.13, "Stock Price": 9.643408727645873},
            "6": {"Dividend": 0.13, "Stock Price": 10.520112081007523},
            "7": {"Dividend": 0.13, "Stock Price": 10.60601212761619},
            "8": {"Dividend": 0.13, "Stock Price": 10.930207343328567},
            "9": {"Dividend": 0.13, "Stock Price": 11.172965503874279},
            "10": {"Dividend": 0.13, "Stock Price": 11.451901912689209},
            "11": {"Dividend": 0.13, "Stock Price": 11.906722021102905},
            "12": {"Dividend": 0.13, "Stock Price": 12.614972244609486}
        },
        "2021": {
            "1": {"Dividend": 0.13, "Stock Price": 12.805470717580695},
            "2": {"Dividend": 0.13, "Stock Price": 12.9233701103612},
            "3": {"Dividend": 0.13, "Stock Price": 13.049247161201809},
            "4": {"Dividend": 0.13, "Stock Price": 13.664055460975284},
            "5": {"Dividend": 0.13, "Stock Price": 14.159770298004151},
            "6": {"Dividend": 0.13, "Stock Price": 14.727139082821934},
            "7": {"Dividend": 0.13, "Stock Price": 15.037842932201567},
            "8": {"Dividend": 0.13, "Stock Price": 15.667173125527121},
            "9": {"Dividend": 0.119, "Stock Price": 14.08751119886126},
            "10": {"Dividend": 0.119, "Stock Price": 13.813362711951847},
            "11": {"Dividend": 0.119, "Stock Price": 13.940853255135673},
            "12": {"Dividend": 0.119, "Stock Price": 13.041592251170766}
        },
        "2022": {
            "1": {"Dividend": 0.119, "Stock Price": 12.498227882385255},
            "2": {"Dividend": 0.119, "Stock Price": 11.984162932948061},
            "3": {"Dividend": 0.119, "Stock Price": 11.596313393634299},
            "4": {"Dividend": 0.119, "Stock Price": 11.848458623886108},
            "5": {"Dividend": 0.119, "Stock Price": 11.363729931059337},
            "6": {"Dividend": 0.119, "Stock Price": 11.08860833304269},
            "7": {"Dividend": 0.119, "Stock Price": 10.374450635910033},
            "8": {"Dividend": 0.119, "Stock Price": 11.494903066883916},
            "9": {"Dividend": 0.119, "Stock Price": 10.634654499235607},
            "10": {"Dividend": 0.119, "Stock Price": 10.02611001332601},
            "11": {"Dividend": 0.119, "Stock Price": 10.632943743751163},
            "12": {"Dividend": 0.269, "Stock Price": 10.947834832327706}
        },
        "2023": {
            "1": {"Dividend": 0.119, "Stock Price": 11.448599052429199},
            "2": {"Dividend": 0.119, "Stock Price": 12.080903404637388},
            "3": {"Dividend": 0.119, "Stock Price": 11.221695070681365},
            "4": {"Dividend": 0.119, "Stock Price": 11.421469136288291},
            "5": {"Dividend": 0.119, "Stock Price": 11.461936300451105},
            "6": {"Dividend": 0.119, "Stock Price": 12.126239776611328},
            "7": {"Dividend": 0.119, "Stock Price": 13.07817063331604},
            "8": {"Dividend": 0.119, "Stock Price": 13.148896880771803},
            "9": {"Dividend": 0.119, "Stock Price": 12.868331336975098},
            "10": {"Dividend": 0.119, "Stock Price": 11.716158780184658},
            "11": {"Dividend": 0.119, "Stock Price": 12.800392060052781},
            "12": {"Dividend": 0.119, "Stock Price": 12.91375799179077}
        },
         "2024": {
                "1": {
                    "Dividend": 0.119,
                    "Stock Price": 13.164775348844982
                },
                "2": {
                    "Dividend": 0.119,
                    "Stock Price": 13.685339164733886
                },
                "3": {
                    "Dividend": 0.119,
                    "Stock Price": 14.29465627670288
                },
                "4": {
                    "Dividend": 0.119,
                    "Stock Price": 14.124295841563832
                },
                "5": {
                    "Dividend": 0.119,
                    "Stock Price": 14.229925805872137
                },
                "6": {
                    "Dividend": 0.0,
                    "Stock Price": 14.478274822235107
                },
                "7": {
                    "Dividend": 0.0,
                    "Stock Price": 0
                },
                "8": {
                    "Dividend": 0.0,
                    "Stock Price": 0
                },
                "9": {
                    "Dividend": 0.0,
                    "Stock Price": 0
                },
                "10": {
                    "Dividend": 0.0,
                    "Stock Price": 0
                },
                "11": {
                    "Dividend": 0.0,
                    "Stock Price": 0
                },
                "12": {
                    "Dividend": 0.0,
                    "Stock Price": 0
                }}
    }
}

# Initialize variables
initial_investment = 100000
current_value = initial_investment
total_shares = initial_investment / data["PTY"]["2020"]["1"]["Stock Price"]

# Dataframe to store the portfolio value over time
portfolio_values = []

# Iterate through each year and month
for year in data["PTY"]:
    for month in data["PTY"][year]:
        stock_price = data["PTY"][year][month]["Stock Price"]
        dividend = data["PTY"][year][month]["Dividend"]
        
        # Calculate dividends received
        dividends_received = total_shares * dividend
        
        # Reinvest dividends by purchasing more shares if stock price is not zero
        if stock_price > 0:
            total_shares += dividends_received / stock_price
        
        # Calculate the current value of the investment
        current_value = total_shares * stock_price
        
        # Append the current value to the list
        portfolio_values.append({
            "Year": int(year),
            "Month": int(month),
            "Portfolio Value": current_value
        })

# Create DataFrame
df = pd.DataFrame(portfolio_values)

# Convert Year and Month to datetime for better plotting
df["Date"] = pd.to_datetime(df[["Year", "Month"]].assign(DAY=1))

# Plot the line chart
plt.figure(figsize=(12, 6))
plt.plot(df["Date"], df["Portfolio Value"], marker='o')
plt.title('5-Year Growth of PTY Investment with Dividends Reinvested')
plt.xlabel('Date')
plt.ylabel('Portfolio Value ($)')
plt.grid(True)
plt.xticks(rotation=45)

# Format x-axis labels to include the month name
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
plt.gca().xaxis.set_major_locator(MaxNLocator(nbins=10))  # Reduce the number of x-axis ticks

# Add value annotations to the data points
for i, row in df.iterrows():
    plt.annotate(f'{int(row["Portfolio Value"])}', (row["Date"], row["Portfolio Value"]),
                 textcoords="offset points", xytext=(0, 5), ha='center')

plt.tight_layout()

# Show the plot
plt.show()
