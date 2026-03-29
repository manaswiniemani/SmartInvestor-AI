import yfinance as yf, numpy as np
def backtest_accuracy(symbol):
    symbol += ".NS"
    data = yf.Ticker(symbol).history(period="3mo")
    if data.empty: return "No data"
    prices = data["Close"].values
    correct=0; total=0
    for i in range(5,len(prices)-1):
        trend = np.polyfit(range(5), prices[i-5:i],1)[0]
        actual = prices[i+1]-prices[i]
        if (trend>0 and actual>0) or (trend<0 and actual<0):
            correct+=1
        total+=1
    return f"{round((correct/total)*100,2)}%" if total else "No data"
