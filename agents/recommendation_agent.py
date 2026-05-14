def recommend_stock(risk_level, duration):

    if risk_level == "Low":

        return [
            "TCS.NS",
            "HDFCBANK.NS",
            "INFY.NS"
        ]

    elif risk_level == "Medium":

        return [
            "RELIANCE.NS",
            "ICICIBANK.NS",
            "LT.NS"
        ]

    else:

        return [
            "NVDA",
            "TSLA",
            "AMD"
        ]