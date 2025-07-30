"""
reports/plot_close_vs_sma.py
Draw a bar‑chart of Close price vs. 20‑day SMA and save it.

Prereqs (inside .venv):
    pip install matplotlib pandas
"""
from pathlib import Path
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# ------------------------------------------------------------------
# 1.  Load latest data from SQLite
# ------------------------------------------------------------------
DB_PATH = "db/prices.sqlite"
QUERY = """
SELECT t.symbol,
       trade_date,
       close,
       sma_20
FROM   v_price_sma20 v
JOIN   ticker t ON t.id = v.ticker_id
WHERE  trade_date = (SELECT MAX(trade_date) FROM price_daily)
"""

with sqlite3.connect(DB_PATH) as conn:
    df = pd.read_sql(QUERY, conn)

if df.empty:
    raise SystemExit("No data found. Run the ETL first (python -m etl.load_prices).")

latest_date = df["trade_date"].iloc[0]  # same for all rows

# ------------------------------------------------------------------
# 2.  Plot
# ------------------------------------------------------------------
ax = df.set_index("symbol")[["close", "sma_20"]].plot(
    kind="bar", figsize=(7, 4)
)
ax.set_title(f"Close vs 20‑Day SMA — {latest_date}")
ax.set_ylabel("Price")
plt.tight_layout()

# ------------------------------------------------------------------
# 3.  Save figure
# ------------------------------------------------------------------
out_dir = Path("reports/img")
out_dir.mkdir(parents=True, exist_ok=True)

png_file = out_dir / f"close_vs_sma_{latest_date}.png"
pdf_file = out_dir / f"close_vs_sma_{latest_date}.pdf"

plt.savefig(png_file, dpi=300, bbox_inches="tight")
plt.savefig(pdf_file, bbox_inches="tight")  # vector version
print(f"Chart saved to:\n • {png_file}\n • {pdf_file}")

# ------------------------------------------------------------------
# 4.  Show window (optional)
# ------------------------------------------------------------------
plt.show()
