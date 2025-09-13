from collectors.finviz import get_finviz_data
from core.financial_metrics_analysis import assess_financial_health

tickers = ["AAPL", "MSFT"]

for t in tickers:
    data = get_finviz_data(t)
    result = assess_financial_health(data)
    print(t, result["overall_health"])
