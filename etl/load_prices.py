from time import sleep
import pandas as pd
from etl.fetch_yf import get_prices as yf_prices
from etl.fetch_av import get_prices as av_prices
from etl.db import upsert_dataframe

WATCHLIST = ["AAPL", "MSFT", "TSLA"]  # <-- change tickers if you like

def combined_prices(symbol):
    df_yf = yf_prices(symbol)
    df_av = av_prices(symbol)

    if not df_yf.empty:
        df_yf = df_yf.assign(src="YF")
    if not df_av.empty:
        df_av = df_av.assign(src="AV")

    merged = (
        pd.concat([df_yf, df_av], ignore_index=True)
        .sort_values(["trade_date", "src"])  # Yahoo wins if same day
        .drop_duplicates(subset=["trade_date"], keep="first")
        .drop(columns=["src"])
    )
    merged["trade_date"] = pd.to_datetime(merged["trade_date"])
    return merged

if __name__ == "__main__":
    for sym in WATCHLIST:
        print("Fetching", sym)
        df = combined_prices(sym)
        if not df.empty:
            upsert_dataframe(sym, df)
            print(f"  stored {len(df)} rows.")
        sleep(15)  # stay within Alpha Vantage free limit
