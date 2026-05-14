# app.py

import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import datetime

from agents.recommendation_agent import recommend_stock
from agents.risk_agent import calculate_risk
from agents.scoring_agent import analyze_stock
from agents.news_agent import analyze_news_sentiment

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Multi-Agent AI Investment Advisor",
    layout="wide"
)

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------

st.title("🚀 Multi-Agent AI Investment Advisor")

st.markdown("""
This AI-powered platform performs:

✅ Live Stock Analysis  
✅ Technical Indicator Analysis  
✅ AI-Based Stock Scoring  
✅ Risk Assessment  
✅ News Sentiment Analysis  
✅ Portfolio Recommendations  
""")

# ---------------------------------------------------
# LIVE STOCK ANALYSIS
# ---------------------------------------------------

st.header("📈 Live Stock Analysis")

stock = st.text_input(
    "Enter Stock Symbol",
    value="RELIANCE.NS"
).upper()

# ---------------------------------------------------
# DATE INPUTS
# ---------------------------------------------------

today = datetime.date.today()

start_date = st.date_input(
    "Start Date",
    value=today - datetime.timedelta(days=180)
)

end_date = st.date_input(
    "End Date",
    value=today
)

# ---------------------------------------------------
# DATE VALIDATION
# ---------------------------------------------------

if start_date >= end_date:

    st.error(
        "End date must be after start date."
    )

    st.stop()

# ---------------------------------------------------
# ANALYZE STOCK BUTTON
# ---------------------------------------------------

if st.button("Analyze Stock"):

    # Download stock data
    data = yf.download(
        stock,
        start=start_date,
        end=end_date
    )

    # ---------------------------------------------------
    # CHECK DATA
    # ---------------------------------------------------

    if data.empty:

        st.error("No stock data found.")

    else:

        # ---------------------------------------------------
        # SHOW DATA
        # ---------------------------------------------------

        st.subheader(f"📋 {stock} Stock Data")

        st.dataframe(data.tail())

        # ---------------------------------------------------
        # CLOSE PRICES
        # ---------------------------------------------------

        close_prices = data["Close"].squeeze()

        # ---------------------------------------------------
        # MOVING AVERAGE
        # ---------------------------------------------------

        data["MA20"] = close_prices.rolling(
            window=20
        ).mean()

        # ---------------------------------------------------
        # RSI CALCULATION
        # ---------------------------------------------------

        delta = close_prices.diff()

        gain = delta.where(
            delta > 0,
            0
        )

        loss = -delta.where(
            delta < 0,
            0
        )

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

        # ---------------------------------------------------
        # PROFESSIONAL CANDLESTICK CHART
        # ---------------------------------------------------

        st.subheader("📊 Professional Stock Chart")

        fig = go.Figure()

        # Candlestick chart
        fig.add_trace(

            go.Candlestick(

                x=data.index,

                open=data["Open"],

                high=data["High"],

                low=data["Low"],

                close=data["Close"],

                name="Candlestick"
            )
        )

        # Moving Average
        fig.add_trace(

            go.Scatter(

                x=data.index,

                y=data["MA20"],

                line=dict(
                    color="orange",
                    width=2
                ),

                name="20-Day MA"
            )
        )

        # Layout
        fig.update_layout(

            height=600,

            template="plotly_dark",

            xaxis_rangeslider_visible=False,

            title=f"{stock} Candlestick Analysis"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # ---------------------------------------------------
        # RSI CHART
        # ---------------------------------------------------

        st.subheader("📉 RSI Indicator")

        fig2, ax2 = plt.subplots(
            figsize=(12, 3)
        )

        ax2.plot(
            data.index,
            data["RSI"],
            label="RSI"
        )

        ax2.axhline(
            70,
            linestyle="--"
        )

        ax2.axhline(
            30,
            linestyle="--"
        )

        ax2.legend()

        st.pyplot(fig2)

        # ---------------------------------------------------
        # TECHNICAL INSIGHT
        # ---------------------------------------------------

        latest_rsi = data["RSI"].iloc[-1]

        st.subheader("🧠 AI Technical Insight")

        if latest_rsi > 70:

            st.error(
                "⚠️ Stock may be Overbought"
            )

        elif latest_rsi < 30:

            st.success(
                "✅ Stock may be Oversold"
            )

        else:

            st.info(
                "ℹ️ Stock is in Neutral Zone"
            )

        # ---------------------------------------------------
        # RISK ANALYSIS
        # ---------------------------------------------------

        risk_data = calculate_risk(stock)

        st.subheader("⚠️ AI Risk Analysis")

        st.write(
            f"Risk Level: "
            f"{risk_data['risk_level']}"
        )

        st.write(
            f"Volatility Score: "
            f"{risk_data['volatility']}"
        )

        # ---------------------------------------------------
        # AI STOCK ANALYSIS
        # ---------------------------------------------------

        ai_result = analyze_stock(stock)

        if ai_result:

            st.subheader(
                "🤖 AI Stock Intelligence"
            )

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "AI Score",
                    ai_result["score"]
                )

                st.metric(
                    "RSI",
                    ai_result["rsi"]
                )

            with col2:

                st.metric(
                    "Recommendation",
                    ai_result["recommendation"]
                )

                st.metric(
                    "Volatility",
                    ai_result["volatility"]
                )

            # ---------------------------------------------------
            # AI REASONING
            # ---------------------------------------------------

            st.subheader("📌 AI Reasoning")

            for reason in ai_result["reasons"]:

                st.success(reason)

        else:

            st.error(
                "Unable to analyze stock."
            )

        # ---------------------------------------------------
        # NEWS SENTIMENT ANALYSIS
        # ---------------------------------------------------

        news_result = analyze_news_sentiment(stock)

        st.subheader("📰 AI News Sentiment")

        col3, col4 = st.columns(2)

        with col3:

            st.metric(
                "Market Sentiment",
                news_result["sentiment"]
            )

        with col4:

            st.metric(
                "Sentiment Score",
                news_result["score"]
            )

        # ---------------------------------------------------
        # HEADLINES
        # ---------------------------------------------------

        st.subheader("🗞️ Latest Headlines")

        for headline in news_result["headlines"]:

            st.write(f"• {headline}")

# ---------------------------------------------------
# AI RECOMMENDATION AGENT
# ---------------------------------------------------

st.header(
    "🤖 AI Investment Recommendation Agent"
)

investment_amount = st.number_input(
    "Enter Investment Amount (₹)",
    min_value=1000,
    step=1000
)

risk_level = st.selectbox(
    "Select Risk Level",
    ["Low", "Medium", "High"]
)

duration = st.selectbox(
    "Investment Duration",
    ["Short Term", "Long Term"]
)

# ---------------------------------------------------
# RECOMMENDATION BUTTON
# ---------------------------------------------------

if st.button("Get AI Recommendation"):

    recommended_stocks = recommend_stock(
        risk_level,
        duration
    )

    st.subheader("📌 Recommended Stocks")

    for stock_name in recommended_stocks:

        st.success(f"✅ {stock_name}")

    # ---------------------------------------------------
    # PORTFOLIO ALLOCATION
    # ---------------------------------------------------

    allocation = (
        investment_amount /
        len(recommended_stocks)
    )

    st.subheader(
        "💰 Suggested Portfolio Allocation"
    )

    for stock_name in recommended_stocks:

        st.write(
            f"₹ {allocation:.2f} "
            f"→ {stock_name}"
        )

    # ---------------------------------------------------
    # PIE CHART
    # ---------------------------------------------------

    st.subheader("📊 Portfolio Distribution")

    fig3, ax3 = plt.subplots()

    ax3.pie(
        [allocation] * len(recommended_stocks),
        labels=recommended_stocks,
        autopct='%1.1f%%'
    )

    st.pyplot(fig3)

    # ---------------------------------------------------
    # STOCK INTELLIGENCE
    # ---------------------------------------------------

    st.subheader(
        "🧠 Recommended Stock Intelligence"
    )

    for stock_name in recommended_stocks:

        st.markdown(f"## {stock_name}")

        ai_analysis = analyze_stock(stock_name)

        if ai_analysis:

            st.write(
                f"AI Score: "
                f"{ai_analysis['score']}"
            )

            st.write(
                f"Recommendation: "
                f"{ai_analysis['recommendation']}"
            )

            st.write(
                f"RSI: "
                f"{ai_analysis['rsi']}"
            )

            st.write(
                f"Volatility: "
                f"{ai_analysis['volatility']}"
            )

            st.write("Reasons:")

            for reason in ai_analysis["reasons"]:

                st.success(reason)

        else:

            st.error(
                "Unable to analyze this stock."
            )

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.markdown("---")

st.markdown("""

# 🚀 Multi-Agent AI System Features

## AI Agents Included

✅ Technical Analysis Agent  
✅ Risk Analysis Agent  
✅ AI Scoring Agent  
✅ News Sentiment Agent  
✅ Portfolio Recommendation Agent  

## Technologies Used

- Python
- Streamlit
- Plotly
- Pandas
- Matplotlib
- yFinance
- Multi-Agent AI Architecture
- Financial Intelligence System

""")