import requests
from bs4 import BeautifulSoup
from core.financial_metrics_analysis import METRICS


def get_finviz_data(ticker: str) -> dict:
    url = f"https://finviz.com/quote.ashx?t={ticker}&p=d"
    resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    if resp.status_code != 200:
        return {}

    soup = BeautifulSoup(resp.content, "html.parser")
    data: dict[str, str] = {}

    for metric in METRICS:
        if metric == "Dividend %":
            node = soup.find("td", string="Dividend")
            if node:
                txt = node.find_next("td").text.strip()
                data[metric] = "0%" if txt == "-" else txt.split()[-1].strip("()")
            else:
                data[metric] = "0%"
        elif metric == "Payout":
            node = soup.find("td", string="Payout")
            if node:
                txt = node.find_next("td").text.strip()
                data[metric] = "0%" if txt == "-" else txt
            else:
                data[metric] = "0%"
        else:
            cell = soup.find("td", string=lambda t: t and metric in t)
            if cell:
                data[metric] = cell.find_next("td").text.strip()

    return data
