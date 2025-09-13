from collectors.finviz import get_finviz_data
from collectors.loader import write_raw_to_postgres

tickers = ["AAPL", "MSFT", "AMZN", "GOOGL"]

for t in tickers:
    rows = write_raw_to_postgres(t, get_finviz_data(t))
    print(f"{t}: {rows} rows")
