# Daily‑Price Mini‑Warehouse

Small Python + SQLite project that:
1. Fetches daily OHLCV data (yfinance / Alpha Vantage)
2. Stores it in a relational schema
3. Computes 20‑day simple moving averages (SQL window functions)
4. Generates a Close vs SMA bar chart every night (matplotlib)

<p align="center">
  <img src="docs/screenshot.png" width="600">
</p>

## Folder layout
