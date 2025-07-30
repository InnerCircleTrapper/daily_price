CREATE VIEW IF NOT EXISTS v_price_sma20 AS
SELECT
  p.*,
  ROUND(AVG(close) OVER (
        PARTITION BY ticker_id
        ORDER BY trade_date
        ROWS BETWEEN 19 PRECEDING AND CURRENT ROW
  ), 4) AS sma_20
FROM price_daily p;
