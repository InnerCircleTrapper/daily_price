# etl/db.py
import sqlite3
from pathlib import Path
import pandas as pd       #  ←  NEW (must be here for pd.to_datetime)


DB_PATH = Path("db/prices.sqlite")
SCHEMA_SQL = Path("sql/schema.sql").read_text()


def get_conn() -> sqlite3.Connection:
    """Open SQLite connection and ensure tables exist."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.executescript(SCHEMA_SQL)
    return conn


def ensure_ticker(conn: sqlite3.Connection, symbol: str) -> int:
    """Insert ticker row if missing and return its id."""
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO ticker(symbol) VALUES (?)", (symbol,))
    cur.execute("SELECT id FROM ticker WHERE symbol = ?", (symbol,))
    return cur.fetchone()[0]


def upsert_dataframe(symbol: str, df):
    """Insert / update a DataFrame of daily prices for one symbol."""
    if df.empty:
        return

    conn = get_conn()
    try:
        ticker_id = ensure_ticker(conn, symbol)
        df = df.fillna(0)
        df["trade_date"] = pd.to_datetime(df["trade_date"]).dt.date

        cur = conn.cursor()
        for _, row in df.iterrows():
            cur.execute(
                """
                INSERT OR REPLACE INTO price_daily
                (ticker_id, trade_date, open, high, low, close, volume)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    ticker_id,
                    str(row["trade_date"]),
                    float(row["open"]),
                    float(row["high"]),
                    float(row["low"]),
                    float(row["close"]),
                    int(row["volume"]),
                ),
            )
        conn.commit()
    finally:
        conn.close()
