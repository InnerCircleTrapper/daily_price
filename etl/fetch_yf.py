import yfinance as yf

def get_prices(symbol, period="60d", interval="1d"):
    df = yf.download(symbol, period=period, interval=interval, auto_adjust=False)
    if df.empty:
        return df
    df = df.rename(
        columns={
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Volume": "volume",
        }
    )
    df.index.name = "trade_date"
    return df.reset_index()
