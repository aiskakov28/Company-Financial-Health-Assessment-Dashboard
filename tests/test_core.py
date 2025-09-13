import math
import pytest
from core.financial_metrics_analysis import (
    METRIC_CATEGORIES,
    parse_metric_value,
    assess_metric,
    assess_financial_health,
)

@pytest.mark.parametrize("raw,expected", [
    ("12", 12.0),
    ("12.5", 12.5),
    ("10%", 10.0),
    ("2.5B", 2.5e9),
    ("3m", 3e6),
    ("7k", 7000.0),
    ("-", 0.0),
    ("N/A", 0.0),
    ("junk", 0.0),
])
def test_parse_metric_value(raw, expected):
    assert parse_metric_value(raw) == expected

@pytest.mark.parametrize("metric,val,label", [
    ("P/E", 10, "Excellent"),
    ("P/E", 20, "Good"),
    ("P/E", 30, "OK"),
    ("P/E", 40, "Bad"),
    ("Quick Ratio", 1.6, "Excellent"),
    ("Quick Ratio", 1.1, "Good"),
    ("Quick Ratio", 0.7, "OK"),
])
def test_assess_metric_branches(metric, val, label):
    assert assess_metric(metric, val) == label

def test_metric_categories_have_content():
    assert isinstance(METRIC_CATEGORIES, dict)
    assert all(len(v) > 0 for v in METRIC_CATEGORIES.values())

def test_assess_financial_health_integration():
    metrics = {
        "P/E": "10",
        "Forward P/E": "11",
        "PEG": "0.9",
        "Quick Ratio": "2.0",
        "Current Ratio": "2.0",
        "Debt/Eq": "0.2",
        "LT Debt/Eq": "0.2",
        "ROA": "12",
        "ROE": "22",
        "ROI": "18",
        "Gross Margin": "45",
        "Oper. Margin": "22",
        "Profit Margin": "18",
        "Payout": "35%",
        "Dividend %": "1.5%",
        "EPS Q/Q": "30%",
        "EPS Y/Y": "28%",
        "Sales Q/Q": "15%",
        "EPS next 5Y": "18%",
        "Sales past 5Y": "12%",
        "EPS past 5Y": "14%",
        "Insider Own": "20%",
        "Insider Trans": "1%",
        "Inst Own": "70%",
        "Inst Trans": "2%",
        "Float Short": "3%",
    }
    res = assess_financial_health(metrics)
    assert "overall_health" in res
    assert "overall_score" in res
    assert "category_scores" in res
    assert res["overall_score"] >= 0
    assert all(0 <= s <= 100 for s in res["category_scores"].values())
