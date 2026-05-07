import yfinance as yf
import pandas as pd

stocks = ["AAPL", "MSFT", "GOOGL", "TSLA"]

for stock in stocks:
    print(f"Downloading {stock}...")

    data = yf.download(stock, period="5y")

    print(data.head())

    data.to_csv(f"{stock}.csv")

    print(f"{stock}.csv saved successfully\n")