import os
import pandas as pd
from dotenv import load_dotenv
from alpha_vantage.timeseries import TimeSeries

load_dotenv()  # reads .env so we get ALPHA_KEY


def get_prices(symbol: str) -> pd.DataFrame:
    """
    Fetch ~100 days of daily OHLCV from Alpha Vantage (free tier).
    Returns DataFrame: trade_date | open | high | low | close | volume
    """
    ts = TimeSeries(
        key=os.getenv("ALPHA_KEY"),
        output_format="pandas",
        indexing_type="date",
    )

    try:
        raw, _ = ts.get_daily(symbol, outputsize="compact")
    except ValueError as exc:
        print(f"Alpha Vantage error for {symbol}: {exc}")
        return pd.DataFrame()

    if raw.empty:
        return raw

    raw = raw.rename(
        columns={
            "1. open": "open",
            "2. high": "high",
            "3. low": "low",
            "4. close": "close",
            "5. volume": "volume",
        }
    )
    raw.index.name = "trade_date"
    df = raw.reset_index()[["trade_date", "open", "high", "low", "close", "volume"]]
    df = df.fillna(0)  # replace any NaNs (e.g., missing volume) with 0
    return df
