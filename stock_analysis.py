import yfinance as yf
def get_stock_data(symbol):
    if "." not in symbol:
        symbol += ".NS"
    info = yf.Ticker(symbol).info
    return {"name": info.get("longName","N/A"), "price": info.get("currentPrice",0)}
