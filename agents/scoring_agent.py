# agents/scoring_agent.py

import yfinance as yf
import pandas as pd

def analyze_stock(stock_symbol):

    try:

        # -----------------------------------
        # DOWNLOAD STOCK DATA
        # -----------------------------------

        data = yf.download(
            stock_symbol,
            period="6mo"
        )

        if data.empty:
            return None

        # -----------------------------------
        # CLOSE PRICE FIX
        # -----------------------------------

        close_prices = data["Close"].squeeze()

        # -----------------------------------
        # MOVING AVERAGE
        # -----------------------------------

        data["MA20"] = close_prices.rolling(
            window=20
        ).mean()

        # -----------------------------------
        # RSI CALCULATION
        # -----------------------------------

        delta = close_prices.diff()

        gain = delta.where(delta > 0, 0)

        loss = -delta.where(delta < 0, 0)

        avg_gain = gain.rolling(
            window=14
        ).mean()

        avg_loss = loss.rolling(
            window=14
        ).mean()

        rs = avg_gain / avg_loss

        data["RSI"] = 100 - (
            100 / (1 + rs)
        )

        # -----------------------------------
        # LATEST VALUES
        # -----------------------------------

        latest_close = close_prices.iloc[-1]

        latest_ma20 = data["MA20"].iloc[-1]

        latest_rsi = data["RSI"].iloc[-1]

        # -----------------------------------
        # VOLATILITY
        # -----------------------------------

        data["Returns"] = close_prices.pct_change()

        volatility = data["Returns"].std()

        # -----------------------------------
        # AI SCORE LOGIC
        # -----------------------------------

        score = 0

        reasons = []

        # Trend Analysis
        if latest_close > latest_ma20:

            score += 30

            reasons.append(
                "Price above 20-day moving average"
            )

        else:

            score -= 10

            reasons.append(
                "Price below moving average"
            )

        # RSI Analysis
        if 40 < latest_rsi < 70:

            score += 30

            reasons.append(
                "Healthy RSI momentum"
            )

        elif latest_rsi >= 70:

            score -= 10

            reasons.append(
                "Stock may be overbought"
            )

        elif latest_rsi <= 30:

            score += 15

            reasons.append(
                "Potential oversold recovery"
            )

        # Volatility Analysis
        if volatility < 0.02:

            score += 25

            reasons.append(
                "Low volatility risk"
            )

        elif volatility < 0.04:

            score += 10

            reasons.append(
                "Moderate volatility"
            )

        else:

            score -= 10

            reasons.append(
                "High volatility risk"
            )

        # -----------------------------------
        # FINAL RECOMMENDATION
        # -----------------------------------

        if score >= 70:

            recommendation = "Strong Buy"

        elif score >= 50:

            recommendation = "Buy"

        elif score >= 30:

            recommendation = "Hold"

        else:

            recommendation = "Avoid"

        # -----------------------------------
        # RETURN RESULTS
        # -----------------------------------

        return {

            "stock": stock_symbol,

            "score": score,

            "recommendation": recommendation,

            "rsi": round(
                float(latest_rsi),
                2
            ),

            "volatility": round(
                float(volatility),
                4
            ),

            "reasons": reasons
        }

    except Exception as e:

        return {
            "stock": stock_symbol,
            "score": 0,
            "recommendation": "Error",
            "rsi": 0,
            "volatility": 0,
            "reasons": [str(e)]
        }