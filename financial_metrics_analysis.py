import numpy as np

METRICS = [
    'P/E', 'Forward P/E', 'PEG', 'P/S', 'P/B', 'P/C', 'P/FCF',
    'Quick Ratio', 'Current Ratio', 'Debt/Eq', 'LT Debt/Eq',
    'ROA', 'ROE', 'ROI', 'Gross Margin', 'Oper. Margin', 'Profit Margin',
    'Payout', 'EPS Q/Q', 'EPS Y/Y', 'Sales Q/Q', 'EPS next 5Y',
    'Sales past 5Y', 'EPS past 5Y', 'Insider Own', 'Insider Trans',
    'Inst Own', 'Inst Trans', 'Float Short', 'Dividend %'
]

METRIC_CATEGORIES = {
    'Valuation': ['P/E', 'Forward P/E', 'PEG', 'P/S', 'P/B', 'P/C', 'P/FCF'],
    'Liquidity': ['Quick Ratio', 'Current Ratio'],
    'Solvency': ['Debt/Eq', 'LT Debt/Eq'],
    'Profitability': ['ROA', 'ROE', 'ROI', 'Gross Margin', 'Oper. Margin', 'Profit Margin'],
    'Dividend': ['Payout', 'Dividend %'],
    'Growth': ['EPS Q/Q', 'EPS Y/Y', 'Sales Q/Q', 'EPS next 5Y', 'Sales past 5Y', 'EPS past 5Y'],
    'Ownership': ['Insider Own', 'Insider Trans', 'Inst Own', 'Inst Trans', 'Float Short']
}

def assess_metric(metric: str, value: float) -> str:
    assessments = {
        "P/E": lambda x: "Excellent" if x < 15 else "Good" if 15 <= x < 25 else "OK" if 25 <= x < 35 else "Bad",
        "Forward P/E": lambda x: "Excellent" if x < 12 else "Good" if 12 <= x < 20 else "OK" if 20 <= x < 30 else "Bad",
        "PEG": lambda x: "Excellent" if x < 1 else "Good" if 1 <= x < 1.5 else "OK" if 1.5 <= x < 2 else "Bad",
        "P/S": lambda x: "Excellent" if x < 1 else "Good" if 1 <= x < 2 else "OK" if 2 <= x < 3 else "Bad",
        "P/B": lambda x: "Excellent" if x < 1 else "Good" if 1 <= x < 2 else "OK" if 2 <= x < 3 else "Bad",
        "P/C": lambda x: "Excellent" if x < 10 else "Good" if 10 <= x < 15 else "OK" if 15 <= x < 20 else "Bad",
        "P/FCF": lambda x: "Excellent" if x < 15 else "Good" if 15 <= x < 25 else "OK" if 25 <= x < 35 else "Bad",
        "Quick Ratio": lambda x: "Excellent" if x > 1.5 else "Good" if 1 < x <= 1.5 else "OK" if 0.5 <= x <= 1 else "Bad",
        "Current Ratio": lambda x: "Excellent" if 1.5 < x <= 3 else "Good" if 1.2 < x <= 1.5 or 3 < x <= 4 else "OK" if 1 <= x <= 1.2 or x > 4 else "Bad",
        "Debt/Eq": lambda x: "Excellent" if x < 0.3 else "Good" if 0.3 <= x < 0.5 else "OK" if 0.5 <= x < 1 else "Bad",
        "LT Debt/Eq": lambda x: "Excellent" if x < 0.3 else "Good" if 0.3 <= x < 0.5 else "OK" if 0.5 <= x < 1 else "Bad",
        "ROA": lambda x: "Excellent" if x > 10 else "Good" if 7 < x <= 10 else "OK" if 5 <= x <= 7 else "Bad",
        "ROE": lambda x: "Excellent" if x > 20 else "Good" if 15 < x <= 20 else "OK" if 10 <= x <= 15 else "Bad",
        "ROI": lambda x: "Excellent" if x > 15 else "Good" if 10 < x <= 15 else "OK" if 5 <= x <= 10 else "Bad",
        "Gross Margin": lambda x: "Excellent" if x > 40 else "Good" if 30 < x <= 40 else "OK" if 20 <= x <= 30 else "Bad",
        "Oper. Margin": lambda x: "Excellent" if x > 20 else "Good" if 10 < x <= 20 else "OK" if 5 <= x <= 10 else "Bad",
        "Profit Margin": lambda x: "Excellent" if x > 15 else "Good" if 10 < x <= 15 else "OK" if 5 <= x <= 10 else "Bad",
        "Payout": lambda x: "Excellent" if 30 <= x <= 50 else "Good" if (20 <= x < 30) or (50 < x <= 60) else "OK" if (10 <= x < 20) or (60 < x <= 75) else "Bad",
        "EPS Q/Q": lambda x: "Excellent" if x > 25 else "Good" if 10 < x <= 25 else "OK" if 0 <= x <= 10 else "Bad",
        "EPS Y/Y": lambda x: "Excellent" if x > 25 else "Good" if 10 < x <= 25 else "OK" if 0 <= x <= 10 else "Bad",
        "Sales Q/Q": lambda x: "Excellent" if x > 20 else "Good" if 10 < x <= 20 else "OK" if 0 <= x <= 10 else "Bad",
        "EPS next 5Y": lambda x: "Excellent" if x > 15 else "Good" if 10 < x <= 15 else "OK" if 5 <= x <= 10 else "Bad",
        "Sales past 5Y": lambda x: "Excellent" if x > 15 else "Good" if 10 < x <= 15 else "OK" if 5 <= x <= 10 else "Bad",
        "EPS past 5Y": lambda x: "Excellent" if x > 15 else "Good" if 10 < x <= 15 else "OK" if 5 <= x <= 10 else "Bad",
        "Insider Own": lambda x: "Excellent" if x > 30 else "Good" if 15 < x <= 30 else "OK" if 5 <= x <= 15 else "Bad",
        "Insider Trans": lambda x: "Excellent" if x > 0 else "Good" if x == 0 else "OK" if -10 <= x < 0 else "Bad",
        "Inst Own": lambda x: "Excellent" if 60 < x <= 90 else "Good" if 40 <= x <= 60 else "OK" if 20 <= x < 40 or 90 < x <= 95 else "Bad",
        "Inst Trans": lambda x: "Excellent" if x > 0 else "Good" if x == 0 else "OK" if -5 <= x < 0 else "Bad",
        "Float Short": lambda x: "Excellent" if x < 5 else "Good" if 5 <= x < 10 else "OK" if 10 <= x < 20 else "Bad",
        "Dividend %": lambda x: "Excellent" if x > 2 else "Good" if 1 < x <= 2 else "OK" if 0 < x <= 1 else "Bad" if x == 0 else "Unknown",
    }
    return assessments.get(metric, lambda x: "Unknown")(value)

def score_assessment(assessment: str) -> float:
    scores = {"Excellent": 100, "Good": 75, "OK": 50, "Bad": 25}
    return scores.get(assessment, 0)

def assess_financial_health(metrics: dict) -> dict:
    category_scores = {}
    for category, metric_list in METRIC_CATEGORIES.items():
        category_assessments = []
        for metric in metric_list:
            if metric in metrics and metrics[metric] not in ['-', '', 'N/A']:
                try:
                    value = parse_metric_value(metrics[metric])
                    category_assessments.append(assess_metric(metric, value))
                except ValueError:
                    pass  # Skip metrics that can't be parsed

        if category_assessments:
            category_scores[category] = np.mean([score_assessment(assessment) for assessment in category_assessments])
        else:
            category_scores[category] = 0  # Set to 0 if no valid assessments

    valid_scores = [score for score in category_scores.values() if score > 0]
    overall_score = np.mean(valid_scores) if valid_scores else 0

    if overall_score >= 80:
        assessment = "Excellent"
    elif overall_score >= 60:
        assessment = "Good"
    elif overall_score >= 40:
        assessment = "OK"
    else:
        assessment = "Needs Improvement"

    return {
        "overall_health": f"{assessment} ({overall_score:.2f}%)",
        "overall_score": overall_score,
        "category_scores": category_scores
    }

def parse_metric_value(value: str) -> float:
    value = value.strip()
    if value in ["N/A", "-"]:
        return 0.0
    if value.endswith('%'):
        return float(value[:-1])
    elif value.lower().endswith('b'):
        return float(value[:-1]) * 1e9
    elif value.lower().endswith('m'):
        return float(value[:-1]) * 1e6
    elif value.lower().endswith('k'):
        return float(value[:-1]) * 1e3
    else:
        try:
            return float(value)
        except ValueError:
            return 0.0