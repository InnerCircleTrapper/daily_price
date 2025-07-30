CREATE TABLE IF NOT EXISTS ticker (
    id      INTEGER PRIMARY KEY,
    symbol  TEXT UNIQUE NOT NULL,
    name    TEXT
);

CREATE TABLE IF NOT EXISTS price_daily (
    ticker_id   INTEGER NOT NULL REFERENCES ticker(id),
    trade_date  DATE    NOT NULL,
    open        REAL,
    high        REAL,
    low         REAL,
    close       REAL,
    volume      INTEGER,
    PRIMARY KEY (ticker_id, trade_date)
);
