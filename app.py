import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from ta.momentum import RSIIndicator
from ta.trend import MACD

# -----------------------------
# PAGE CONFIG
# -----------------------------

st.set_page_config(
    page_title="AI Stock Dashboard",
    layout="wide"
)

st.title("🚀 AI Advanced Stock Dashboard")

# -----------------------------
# STOCK SELECTION
# -----------------------------

stocks = ["AAPL", "MSFT", "TSLA", "NVDA", "GOOGL"]

selected_stock = st.selectbox(
    "Select Stock",
    stocks
)

# -----------------------------
# DOWNLOAD DATA
# -----------------------------

data = yf.download(
    selected_stock,
    period="5y"
)

# -----------------------------
# FIX MULTIINDEX COLUMNS
# -----------------------------

if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.get_level_values(0)

# -----------------------------
# TECHNICAL INDICATORS
# -----------------------------

data["50_MA"] = data["Close"].rolling(50).mean()
data["200_MA"] = data["Close"].rolling(200).mean()

# RSI
rsi_indicator = RSIIndicator(close=data["Close"])
data["RSI"] = rsi_indicator.rsi()

# MACD
macd = MACD(close=data["Close"])

data["MACD"] = macd.macd()
data["Signal"] = macd.macd_signal()

# -----------------------------
# PRICE METRICS
# -----------------------------

start_price = float(data["Close"].iloc[0])
current_price = float(data["Close"].iloc[-1])

growth = ((current_price - start_price) / start_price) * 100

risk = data["Close"].std()

# -----------------------------
# AI SUGGESTION ENGINE
# -----------------------------

latest_rsi = data["RSI"].iloc[-1]
latest_macd = data["MACD"].iloc[-1]
latest_signal = data["Signal"].iloc[-1]

suggestion = "HOLD"

if growth > 100 and latest_macd > latest_signal:
    suggestion = "BUY"

if growth > 200 and latest_macd > latest_signal:
    suggestion = "STRONG BUY"

if latest_rsi > 80:
    suggestion = "OVERBOUGHT"

# -----------------------------
# CANDLESTICK CHART
# -----------------------------

fig = go.Figure()

fig.add_trace(go.Candlestick(
    x=data.index,
    open=data["Open"],
    high=data["High"],
    low=data["Low"],
    close=data["Close"],
    name="Candlestick"
))

# Moving averages
fig.add_trace(go.Scatter(
    x=data.index,
    y=data["50_MA"],
    line=dict(color="orange"),
    name="50 Day MA"
))

fig.add_trace(go.Scatter(
    x=data.index,
    y=data["200_MA"],
    line=dict(color="green"),
    name="200 Day MA"
))

fig.update_layout(
    title=f"{selected_stock} Professional Trading Chart",
    xaxis_title="Date",
    yaxis_title="Price",
    height=700
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# RSI CHART
# -----------------------------

st.subheader("📈 RSI Indicator")

rsi_fig = go.Figure()

rsi_fig.add_trace(go.Scatter(
    x=data.index,
    y=data["RSI"],
    line=dict(color="purple"),
    name="RSI"
))

rsi_fig.add_hline(y=70, line_dash="dash", line_color="red")
rsi_fig.add_hline(y=30, line_dash="dash", line_color="green")

rsi_fig.update_layout(
    height=300
)

st.plotly_chart(rsi_fig, use_container_width=True)

# -----------------------------
# MACD CHART
# -----------------------------

st.subheader("📉 MACD Indicator")

macd_fig = go.Figure()

macd_fig.add_trace(go.Scatter(
    x=data.index,
    y=data["MACD"],
    line=dict(color="blue"),
    name="MACD"
))

macd_fig.add_trace(go.Scatter(
    x=data.index,
    y=data["Signal"],
    line=dict(color="orange"),
    name="Signal Line"
))

macd_fig.update_layout(
    height=300
)

st.plotly_chart(macd_fig, use_container_width=True)

# -----------------------------
# METRICS
# -----------------------------

st.subheader("📊 AI Analysis")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Start Price", f"${start_price:.2f}")
col2.metric("Current Price", f"${current_price:.2f}")
col3.metric("Growth %", f"{growth:.2f}%")
col4.metric("Risk", f"{risk:.2f}")

# -----------------------------
# AI SUGGESTION
# -----------------------------

st.subheader("💡 AI Investment Suggestion")

if suggestion == "STRONG BUY":
    st.success("🔥 STRONG BUY")

elif suggestion == "BUY":
    st.success("✅ BUY")

elif suggestion == "OVERBOUGHT":
    st.warning("⚠ OVERBOUGHT")

else:
    st.info("⏳ HOLD")

# -----------------------------
# RSI INTERPRETATION
# -----------------------------

st.subheader("📈 RSI Interpretation")

if latest_rsi > 70:
    st.warning(f"RSI = {latest_rsi:.2f} → Stock may be OVERBOUGHT")

elif latest_rsi < 30:
    st.success(f"RSI = {latest_rsi:.2f} → Stock may be OVERSOLD")

else:
    st.info(f"RSI = {latest_rsi:.2f} → Normal Range")

# -----------------------------
# MACD INTERPRETATION
# -----------------------------

st.subheader("📉 MACD Interpretation")

if latest_macd > latest_signal:
    st.success("MACD is above Signal Line → Bullish Momentum")

else:
    st.error("MACD is below Signal Line → Bearish Momentum")

# -----------------------------
# DATA TABLE
# -----------------------------

st.subheader("📋 Raw Stock Data")

st.dataframe(data.tail())