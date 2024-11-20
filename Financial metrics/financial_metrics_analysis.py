import numpy as np

METRICS = [
    'Gross Margin (%)',
    'Operating Margin (%)',
    'Net Margin (%)',
    'FCF Margin (%)',
    'ROIC (%)',
    'ROCE (%)',
    'Current Ratio (decimals)',
    'Debt to EBITDA Ratio (decimals)',
    'Payout Ratio (%)',
    'Free Cash Flow Payout Ratio (%)',
    'Next Year Projected EPS Growth (%)',
    'Next Year Projected Revenue Growth (%)',
    'Next Year Projected EBITDA Growth (%)'
]

METRIC_CATEGORIES = {
    'Profitability': ["Gross Margin (%)", "Operating Margin (%)", "Net Margin (%)", "FCF Margin (%)"],
    'Efficiency': ["ROIC (%)", "ROCE (%)"],
    'Financial Health': ["Current Ratio (decimals)", "Debt to EBITDA Ratio (decimals)"],
    'Dividend': ["Payout Ratio (%)", "Free Cash Flow Payout Ratio (%)"],
    'Growth': ["Next Year Projected EPS Growth (%)", "Next Year Projected Revenue Growth (%)",
               "Next Year Projected EBITDA Growth (%)"]
}

def assess_metric(metric: str, value: float) -> str:
    assessments = {
        "Gross Margin (%)": lambda
            x: "Excellent" if x > 40 else "Good" if 30 < x <= 40 else "OK" if 20 <= x <= 30 else "Bad",
        "Operating Margin (%)": lambda
            x: "Excellent" if x > 20 else "Good" if 10 < x <= 20 else "OK" if 5 <= x <= 10 else "Bad",
        "Net Margin (%)": lambda
            x: "Excellent" if x > 15 else "Good" if 10 < x <= 15 else "OK" if 5 <= x <= 10 else "Bad",
        "FCF Margin (%)": lambda
            x: "Excellent" if x > 15 else "Good" if 10 < x <= 15 else "OK" if 5 <= x <= 10 else "Bad",
        "ROIC (%)": lambda x: "Excellent" if x > 15 else "Good" if 10 < x <= 15 else "OK" if 5 <= x <= 10 else "Bad",
        "ROCE (%)": lambda x: "Excellent" if x > 20 else "Good" if 15 < x <= 20 else "OK" if 10 <= x <= 15 else "Bad",
        "Current Ratio (decimals)": lambda
            x: "Excellent" if x > 2 else "Good" if 1.5 < x <= 2 else "OK" if 1 <= x <= 1.5 else "Bad",
        "Debt to EBITDA Ratio (decimals)": lambda
            x: "Excellent" if x < 1 else "Good" if 1 <= x < 2 else "OK" if 2 <= x < 3 else "Bad",
        "Payout Ratio (%)": lambda x: "Excellent" if 40 <= x <= 50 else "Good" if (30 <= x < 40) or (
                    50 < x <= 60) else "OK" if (20 <= x < 30) or (60 < x <= 80) else "Bad",
        "Free Cash Flow Payout Ratio (%)": lambda
            x: "Excellent" if x < 40 else "Good" if 40 <= x < 60 else "OK" if 60 <= x < 80 else "Bad",
        "Next Year Projected EPS Growth (%)": lambda
            x: "Excellent" if x > 10 else "Good" if 5 < x <= 10 else "OK" if 0 <= x <= 5 else "Bad",
        "Next Year Projected Revenue Growth (%)": lambda
            x: "Excellent" if x > 10 else "Good" if 5 < x <= 10 else "OK" if 0 <= x <= 5 else "Bad",
        "Next Year Projected EBITDA Growth (%)": lambda
            x: "Excellent" if x > 10 else "Good" if 5 < x <= 10 else "OK" if 0 <= x <= 5 else "Bad"
    }
    return assessments.get(metric, lambda x: "Unknown")(value)

def score_assessment(assessment: str) -> float:
    scores = {"Excellent": 100, "Good": 75, "OK": 50, "Bad": 25}
    return scores.get(assessment, 0)

def assess_financial_health(metrics: dict) -> dict:
    category_scores = {}
    for category, metric_list in METRIC_CATEGORIES.items():
        category_assessments = [assess_metric(metric, metrics[metric]) for metric in metric_list if metric in metrics]
        category_scores[category] = np.mean([score_assessment(assessment) for assessment in category_assessments])
    overall_score = np.mean(list(category_scores.values()))
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