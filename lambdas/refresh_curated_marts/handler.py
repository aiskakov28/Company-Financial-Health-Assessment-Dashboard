import os
import json
import time

from collectors.finviz import get_finviz_data

TICKERS = [t.strip().upper() for t in os.getenv("TICKERS", "AAPL,MSFT").split(",")]

def handler(event, context):
    started = time.time()
    results = {}
    for t in TICKERS:
        try:
            results[t] = get_finviz_data(t)
        except Exception as e:
            results[t] = {"error": str(e)}
    return {
        "statusCode": 200,
        "body": json.dumps({"ok": True, "elapsed_sec": round(time.time() - started, 2), "tickers": list(results.keys())})
    }
