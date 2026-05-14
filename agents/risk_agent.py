import yfinance as yf
import numpy as np

def calculate_risk(stock_symbol):

    data = yf.download(stock_symbol, period="6mo")

    if data.empty:
        return {
            "volatility": 0,
            "risk_level": "Unknown"
        }

    # Fix Close column issue
    close_prices = data["Close"].squeeze()

    returns = close_prices.pct_change()

    volatility = returns.std()

    if volatility < 0.02:
        risk = "Low"

    elif volatility < 0.04:
        risk = "Medium"

    else:
        risk = "High"

    return {
        "volatility": round(float(volatility), 4),
        "risk_level": risk
    }