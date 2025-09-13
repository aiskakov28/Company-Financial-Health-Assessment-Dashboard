import numpy as np

METRICS = [
    "P/E", "Forward P/E", "PEG", "P/S", "P/B", "P/C", "P/FCF",
    "Quick Ratio", "Current Ratio", "Debt/Eq", "LT Debt/Eq",
    "ROA", "ROE", "ROI", "Gross Margin", "Oper. Margin", "Profit Margin",
    "Payout", "EPS Q/Q", "EPS Y/Y", "Sales Q/Q", "EPS next 5Y",
    "Sales past 5Y", "EPS past 5Y", "Insider Own", "Insider Trans",
    "Inst Own", "Inst Trans", "Float Short", "Dividend %"
]

METRIC_CATEGORIES = {
    "Valuation": ["P/E", "Forward P/E", "PEG", "P/S", "P/B", "P/C", "P/FCF"],
    "Liquidity": ["Quick Ratio", "Current Ratio"],
    "Solvency": ["Debt/Eq", "LT Debt/Eq"],
    "Profitability": ["ROA", "ROE", "ROI", "Gross Margin", "Oper. Margin", "Profit Margin"],
    "Dividend": ["Payout", "Dividend %"],
    "Growth": ["EPS Q/Q", "EPS Y/Y", "Sales Q/Q", "EPS next 5Y", "Sales past 5Y", "EPS past 5Y"],
    "Ownership": ["Insider Own", "Insider Trans", "Inst Own", "Inst Trans", "Float Short"],
}

def assess_metric(metric: str, value: float) -> str:
    assessments = {
        "P/E": lambda x: "Excellent" if x < 15 else "Good" if x < 25 else "OK" if x < 35 else "Bad",
        "Forward P/E": lambda x: "Excellent" if x < 12 else "Good" if x < 20 else "OK" if x < 30 else "Bad",
        "PEG": lambda x: "Excellent" if x < 1 else "Good" if x < 1.5 else "OK" if x < 2 else "Bad",
        "P/S": lambda x: "Excellent" if x < 1 else "Good" if x < 2 else "OK" if x < 3 else "Bad",
        "P/B": lambda x: "Excellent" if x < 1 else "Good" if x < 2 else "OK" if x < 3 else "Bad",
        "P/C": lambda x: "Excellent" if x < 10 else "Good" if x < 15 else "OK" if x < 20 else "Bad",
        "P/FCF": lambda x: "Excellent" if x < 15 else "Good" if x < 25 else "OK" if x < 35 else "Bad",
        "Quick Ratio": lambda x: "Excellent" if x > 1.5 else "Good" if x > 1 else "OK" if x >= 0.5 else "Bad",
        "Current Ratio": lambda x: "Excellent" if 1.5 < x <= 3 else "Good" if 1.2 < x <= 1.5 or 3 < x <= 4 else "OK" if 1 <= x <= 1.2 or x > 4 else "Bad",
        "Debt/Eq": lambda x: "Excellent" if x < 0.3 else "Good" if x < 0.5 else "OK" if x < 1 else "Bad",
        "LT Debt/Eq": lambda x: "Excellent" if x < 0.3 else "Good" if x < 0.5 else "OK" if x < 1 else "Bad",
        "ROA": lambda x: "Excellent" if x > 10 else "Good" if x > 7 else "OK" if x >= 5 else "Bad",
        "ROE": lambda x: "Excellent" if x > 20 else "Good" if x > 15 else "OK" if x >= 10 else "Bad",
        "ROI": lambda x: "Excellent" if x > 15 else "Good" if x > 10 else "OK" if x >= 5 else "Bad",
        "Gross Margin": lambda x: "Excellent" if x > 40 else "Good" if x > 30 else "OK" if x >= 20 else "Bad",
        "Oper. Margin": lambda x: "Excellent" if x > 20 else "Good" if x > 10 else "OK" if x >= 5 else "Bad",
        "Profit Margin": lambda x: "Excellent" if x > 15 else "Good" if x > 10 else "OK" if x >= 5 else "Bad",
        "Payout": lambda x: "Excellent" if 30 <= x <= 50 else "Good" if (20 <= x < 30) or (50 < x <= 60) else "OK" if (10 <= x < 20) or (60 < x <= 75) else "Bad",
        "EPS Q/Q": lambda x: "Excellent" if x > 25 else "Good" if x > 10 else "OK" if x >= 0 else "Bad",
        "EPS Y/Y": lambda x: "Excellent" if x > 25 else "Good" if x > 10 else "OK" if x >= 0 else "Bad",
        "Sales Q/Q": lambda x: "Excellent" if x > 20 else "Good" if x > 10 else "OK" if x >= 0 else "Bad",
        "EPS next 5Y": lambda x: "Excellent" if x > 15 else "Good" if x > 10 else "OK" if x >= 5 else "Bad",
        "Sales past 5Y": lambda x: "Excellent" if x > 15 else "Good" if x > 10 else "OK" if x >= 5 else "Bad",
        "EPS past 5Y": lambda x: "Excellent" if x > 15 else "Good" if x > 10 else "OK" if x >= 5 else "Bad",
        "Insider Own": lambda x: "Excellent" if x > 30 else "Good" if x > 15 else "OK" if x >= 5 else "Bad",
        "Insider Trans": lambda x: "Excellent" if x > 0 else "Good" if x == 0 else "OK" if x >= -10 else "Bad",
        "Inst Own": lambda x: "Excellent" if 60 < x <= 90 else "Good" if 40 <= x <= 60 else "OK" if 20 <= x < 40 or 90 < x <= 95 else "Bad",
        "Inst Trans": lambda x: "Excellent" if x > 0 else "Good" if x == 0 else "OK" if x >= -5 else "Bad",
        "Float Short": lambda x: "Excellent" if x < 5 else "Good" if x < 10 else "OK" if x < 20 else "Bad",
        "Dividend %": lambda x: "Excellent" if x > 2 else "Good" if x > 1 else "OK" if x > 0 else "Bad" if x == 0 else "Unknown",
    }
    return assessments.get(metric, lambda x: "Unknown")(value)


def score_assessment(assessment: str) -> float:
    return {"Excellent": 100, "Good": 75, "OK": 50, "Bad": 25}.get(assessment, 0.0)


def assess_financial_health(metrics: dict) -> dict:
    category_scores = {}
    for category, metric_list in METRIC_CATEGORIES.items():
        assessments = []
        for metric in metric_list:
            raw = metrics.get(metric)
            if raw and raw not in ("-", "", "N/A"):
                try:
                    value = parse_metric_value(raw)
                    assessments.append(assess_metric(metric, value))
                except Exception:
                    # ignore unparsable values
                    pass
        category_scores[category] = (
            float(np.mean([score_assessment(a) for a in assessments]))
            if assessments else 0.0
        )

    valid = [s for s in category_scores.values() if s > 0]
    overall_score = float(np.mean(valid)) if valid else 0.0

    if overall_score >= 80:
        overall_label = "Excellent"
    elif overall_score >= 60:
        overall_label = "Good"
    elif overall_score >= 40:
        overall_label = "OK"
    else:
        overall_label = "Needs Improvement"

    return {
        "overall_health": f"{overall_label} ({overall_score:.2f}%)",
        "overall_score": overall_score,
        "category_scores": category_scores,
    }


def parse_metric_value(value: str) -> float:
    v = value.strip()
    if v in {"N/A", "-"}:
        return 0.0
    if v.endswith("%"):
        return float(v[:-1])
    v_low = v.lower()
    if v_low.endswith("b"):
        return float(v[:-1]) * 1e9
    if v_low.endswith("m"):
        return float(v[:-1]) * 1e6
    if v_low.endswith("k"):
        return float(v[:-1]) * 1e3
    try:
        return float(v)
    except ValueError:
        return 0.0
