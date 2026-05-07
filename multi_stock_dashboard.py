import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# ==============================
# AI MULTI-STOCK DASHBOARD
# ==============================

print("🚀 Multi-Stock AI Dashboard Started\n")

# ==============================
# STOCK LIST
# ==============================

stocks = ["AAPL", "MSFT", "TSLA", "NVDA"]

# Dictionary to store all stock data
stock_data = {}

# ==============================
# DOWNLOAD STOCK DATA
# ==============================

for stock in stocks:

    print(f"Downloading {stock} data...")

    data = yf.download(stock, period="5y")

    stock_data[stock] = data

    print(data.head())

# ==============================
# DOWNLOAD COMPLETE
# ==============================

print("\n✅ All stock data downloaded successfully")

# ==============================
# MULTI-STOCK VISUALIZATION
# ==============================

plt.figure(figsize=(12, 6))

for stock in stocks:

    data = stock_data[stock]

    close_prices = data["Close"].squeeze()

    plt.plot(
        close_prices.index,
        close_prices,
        label=stock
    )

# Chart Styling
plt.title("Multi-Stock AI Dashboard")
plt.xlabel("Date")
plt.ylabel("Closing Price")
plt.legend()
plt.grid(True)

# Save chart
plt.savefig("multi_stock_chart.png")

print("\n✅ Multi-stock chart saved as multi_stock_chart.png")

# ==============================
# AI STOCK RANKING ENGINE
# ==============================

print("\n🧠 AI STOCK RANKING ENGINE")

stock_scores = []

for stock in stocks:

    data = stock_data[stock]

    # Convert Close column properly
    close_prices = data["Close"].squeeze()

    # Start and End Prices
    start_price = close_prices.iloc[0]

    end_price = close_prices.iloc[-1]

    # Growth %
    growth = ((end_price - start_price) / start_price) * 100

    # Risk (Volatility)
    volatility = close_prices.std()

    # Save Results
    stock_scores.append({

        "Stock": stock,

        "Start Price": round(float(start_price), 2),

        "Current Price": round(float(end_price), 2),

        "Growth %": round(float(growth), 2),

        "Risk": round(float(volatility), 2)

    })

# ==============================
# CREATE RANKING TABLE
# ==============================

ranking_df = pd.DataFrame(stock_scores)

# Sort by Growth %
ranking_df = ranking_df.sort_values(
    by="Growth %",
    ascending=False
)

# Reset index
ranking_df = ranking_df.reset_index(drop=True)

# ==============================
# DISPLAY RANKINGS
# ==============================

print("\n📊 STOCK PERFORMANCE RANKINGS:\n")

print(ranking_df)

# ==============================
# AI INVESTMENT SUGGESTIONS
# ==============================

print("\n💡 AI INVESTMENT SUGGESTIONS:\n")

for index, row in ranking_df.iterrows():

    stock = row["Stock"]

    growth = row["Growth %"]

    risk = row["Risk"]

    # AI Logic
    if growth > 150 and risk < 100:

        suggestion = "🔥 STRONG BUY"

    elif growth > 50:

        suggestion = "✅ BUY"

    elif growth > 0:

        suggestion = "⚠ HOLD"

    else:

        suggestion = "❌ SELL"

    print(f"{stock} → {suggestion}")

# ==============================
# BEST STOCK
# ==============================

best_stock = ranking_df.iloc[0]

print("\n🏆 BEST PERFORMING STOCK:\n")

print(f"Stock: {best_stock['Stock']}")
print(f"Growth: {best_stock['Growth %']}%")

# ==============================
# FINAL MESSAGE
# ==============================

print("\n✅ AI Analysis Complete")
print("📁 Check multi_stock_chart.png for visualization")