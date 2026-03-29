import yfinance as yf
def opportunity_radar(symbol):
    symbol += ".NS"
    data = yf.Ticker(symbol).history(period="5d")
    if data.empty: return "No data"
    change = ((data["Close"][-1]-data["Close"][-2])/data["Close"][-2])*100
    return "🚀 Momentum" if change>3 else "Stable"
