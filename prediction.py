import yfinance as yf, numpy as np
def predict_trend(symbol):
    if "." not in symbol:
        symbol += ".NS"
    data = yf.Ticker(symbol).history(period="1mo")["Close"].values
    if len(data)<2: return "No data"
    trend = np.polyfit(range(len(data)), data,1)
    return "📈 Buy" if trend[0]>0 else "📉 Sell"

def detect_pattern(symbol):
    symbol += ".NS"
    data = yf.Ticker(symbol).history(period="1mo")
    if data.empty: return "No pattern"
    high = data["High"].max()
    current = data["Close"][-1]
    if current >= high*0.98:
        return "📈 Breakout"
    return "No strong pattern"
