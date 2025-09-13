from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go

from core.financial_metrics_analysis import (
    METRIC_CATEGORIES,
    assess_financial_health,
    assess_metric,
    parse_metric_value,
)
from core.constants import CATEGORY_COLORS, ASSESSMENT_COLORS
from collectors.finviz import get_finviz_data


app = Dash(__name__, external_stylesheets=[
    "https://codepen.io/chriddyp/pen/bWLwgP.css"
])

app.title = "QuickFin — Financial Health Dashboard"

app.layout = html.Div([
    html.H1("QuickFin — Company Financial Health", className="header-title"),

    dcc.Input(id="ticker-input", type="text", placeholder="Enter stock ticker"),
    html.Button("Analyze", id="submit-button", className="submit-button"),

    html.Div(id="financial-health-output", className="output-container"),

    html.Div([
        dcc.Graph(id="radar-chart", className="chart"),
        dcc.Graph(id="category-bar-chart", className="chart"),
    ], className="charts-container"),

    html.Div(id="metric-details", className="metric-details"),
])


def _radar_figure(category_scores: dict) -> go.Figure:
    cats = list(category_scores.keys())
    vals = list(category_scores.values())
    fig = go.Figure(
        data=go.Scatterpolar(
            r=vals + vals[:1],
            theta=cats + cats[:1],
            fill="toself",
            name="Financial Health",
        )
    )
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=False,
        title="Financial Health Radar Chart",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def _bar_figure(category_scores: dict) -> go.Figure:
    cats = list(category_scores.keys())
    vals = list(category_scores.values())
    fig = go.Figure(data=[
        go.Bar(
            x=cats,
            y=vals,
            text=[f"{v:.1f}%" for v in vals],
            textposition="auto",
            marker_color=[CATEGORY_COLORS[c] for c in cats],
        )
    ])
    fig.update_layout(
        title="Category Scores (Click a bar for details)",
        xaxis_title="Categories",
        yaxis_title="Score (%)",
        yaxis=dict(range=[0, 100]),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    return fig


@app.callback(
    [
        Output("financial-health-output", "children"),
        Output("radar-chart", "figure"),
        Output("category-bar-chart", "figure"),
        Output("metric-details", "children"),
    ],
    [Input("submit-button", "n_clicks"),
     Input("category-bar-chart", "clickData")],
    [State("ticker-input", "value")],
)
def update_output(n_clicks, click_data, ticker):
    import dash
    ctx = dash.callback_context

    if not ctx.triggered:
        return "Enter a ticker and click Analyze.", {}, {}, ""

    trigger = ctx.triggered[0]["prop_id"]

    if trigger == "submit-button.n_clicks":
        if not ticker:
            return "Enter a ticker and click Analyze.", {}, {}, ""

        finviz_data = get_finviz_data(ticker)
        if not finviz_data:
            return f"No data found for {ticker}.", {}, {}, ""

        result = assess_financial_health(finviz_data)
        overall = result["overall_health"]
        scores = result["category_scores"]

        # header + compact grid summary
        color = next(
            (c for k, c in ASSESSMENT_COLORS.items() if k in overall),
            "#222"
        )
        header = html.H2(
            f"Financial Health for {ticker.upper()}: {overall}",
            className="assessment-header",
            style={"color": color},
        )

        grid = html.Div([
            html.Div([
                html.H4(cat, className="category-title",
                        style={"color": CATEGORY_COLORS[cat]}),
                html.P(f"{score:.2f}%", className="category-score",
                       style={"color": CATEGORY_COLORS[cat]}),
                html.Div(className="progress-bar",
                         style={"width": f"{score}%",
                                "backgroundColor": CATEGORY_COLORS[cat]}),
            ], className="category-score-container")
            for cat, score in scores.items()
        ], className="category-scores-grid")

        return html.Div([header, grid]), _radar_figure(scores), _bar_figure(scores), ""

    if trigger == "category-bar-chart.clickData" and click_data:
        if not ticker:
            return dash.no_update, dash.no_update, dash.no_update, ""

        category = click_data["points"][0]["x"]
        metrics = METRIC_CATEGORIES[category]
        finviz_data = get_finviz_data(ticker)

        rows = [
            html.Tr([
                html.Td(metric),
                html.Td(finviz_data.get(metric, "N/A")),
                html.Td(assess_metric(metric, parse_metric_value(finviz_data.get(metric, "N/A")))),
            ])
            for metric in metrics
        ]

        details = html.Div([
            html.H3(f"{category} — detailed metrics"),
            html.Table([
                html.Tr([html.Th("Metric"), html.Th("Value"), html.Th("Assessment")]),
                *rows
            ], className="metric-table"),
        ], className="metric-details")

        return dash.no_update, dash.no_update, dash.no_update, details

    return dash.no_update, dash.no_update, dash.no_update, ""


if __name__ == "__main__":
    app.run_server(debug=True)
