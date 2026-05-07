import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np

print("🚀 AI Stock Analyst Started\n")

# -----------------------------------
# STOCK TO ANALYZE
# -----------------------------------

stock_name = "AAPL"

print(f"Downloading {stock_name} data...\n")

# -----------------------------------
# DOWNLOAD DATA
# -----------------------------------

data = yf.download(stock_name, period="5y")

print("Dataset Preview:\n")
print(data.head())

# -----------------------------------
# FIX MULTI-INDEX COLUMNS (IMPORTANT)
# -----------------------------------

if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.get_level_values(0)

# -----------------------------------
# MOVING AVERAGES
# -----------------------------------

data["MA50"] = data["Close"].rolling(window=50).mean()
data["MA200"] = data["Close"].rolling(window=200).mean()

# -----------------------------------
# VISUALIZATION
# -----------------------------------

plt.figure(figsize=(12, 6))

plt.plot(data.index, data["Close"], label="Closing Price")
plt.plot(data.index, data["MA50"], label="50 Day Moving Average")
plt.plot(data.index, data["MA200"], label="200 Day Moving Average")

plt.title(f"{stock_name} Stock Analysis")
plt.xlabel("Date")
plt.ylabel("Price")

plt.legend()

plt.savefig("stock_chart.png")

print("\n✅ Chart saved as stock_chart.png")

# -----------------------------------
# PREPARE DATA FOR AI MODEL
# -----------------------------------

data = data.dropna()

# Predict next day's closing price
data["Prediction"] = data["Close"].shift(-1)

# Remove last row because prediction becomes NaN
data = data[:-1]

# Features (X)
X = np.array(data["Close"]).reshape(-1, 1)

# Target (y)
y = np.array(data["Prediction"])

# -----------------------------------
# TRAIN AI MODEL
# -----------------------------------

model = LinearRegression()

model.fit(X, y)

print("\n✅ AI Model Trained Successfully")

# -----------------------------------
# FUTURE PRICE PREDICTION
# -----------------------------------

latest_price = float(data["Close"].iloc[-1])

future_price = model.predict([[latest_price]])

predicted_price = float(future_price[0])

print("\n🧠 AI PREDICTION:")
print(f"Current Price: ${latest_price:.2f}")
print(f"Predicted Next Price: ${predicted_price:.2f}")

# -----------------------------------
# BUY / SELL SIGNAL
# -----------------------------------

print("\n📈 INVESTMENT SUGGESTION:")

if predicted_price > latest_price:
    print("✅ BUY SIGNAL")
    print("Stock may rise in next trading session.")
else:
    print("❌ SELL SIGNAL")
    print("Stock may decline in next trading session.")

# -----------------------------------
# EXTRA ANALYSIS
# -----------------------------------

average_close = data["Close"].mean()
highest_price = data["High"].max()
lowest_price = data["Low"].min()

print("\n📊 STOCK INSIGHTS:")

print(f"Average Closing Price: ${average_close:.2f}")
print(f"Highest Price in 5 Years: ${highest_price:.2f}")
print(f"Lowest Price in 5 Years: ${lowest_price:.2f}")

# -----------------------------------
# FINAL MESSAGE
# -----------------------------------

print("\n✅ ANALYSIS COMPLETE")
print("📁 Check stock_chart.png for visualization")