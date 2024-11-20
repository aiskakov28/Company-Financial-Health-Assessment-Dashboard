import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas as pd
import requests
from bs4 import BeautifulSoup
from financial_metrics_analysis import METRICS, METRIC_CATEGORIES, assess_financial_health

app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

CATEGORY_COLORS = {
    'Valuation': '#FF6B6B',
    'Profitability': '#4ECDC4',
    'Liquidity': '#45B7D1',
    'Solvency': '#FFA07A',
    'Dividend': '#98D8C8',
    'Growth': '#FFBE0B',
    'Ownership': '#9B59B6'
}

ASSESSMENT_COLORS = {
    'Excellent': '#006400',
    'Good': '#32CD32',
    'OK': '#FFA500',
    'Needs Improvement': '#FF0000'
}

def get_finviz_data(ticker):
    url = f"https://finviz.com/quote.ashx?t={ticker}&p=d"
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.content, 'html.parser')
    data = {}
    for metric in METRICS:
        if metric == "Dividend %":
            dividend_row = soup.find('td', string="Dividend")
            if dividend_row:
                dividend_value = dividend_row.find_next('td').text.strip()
                if dividend_value != "-":
                    data[metric] = dividend_value.split()[-1].strip('()')
                else:
                    data[metric] = "0%"
        elif metric == "Payout":
            payout_row = soup.find('td', string="Payout")
            if payout_row:
                payout_value = payout_row.find_next('td').text.strip()
                if payout_value != "-":
                    data[metric] = payout_value
                else:
                    data[metric] = "0%"
        else:
            value = soup.find('td', string=lambda text: text and metric in text)
            if value:
                data[metric] = value.find_next('td').text.strip()
    return data

app.layout = html.Div([
    html.H1("Financial Health Analysis by Abylay Iskakov", className="header-title"),
    dcc.Input(id='ticker-input', type='text', placeholder='Enter stock ticker'),
    html.Button('Analyze', id='submit-button', className="submit-button"),
    html.Div(id='financial-health-output', className="output-container"),
    html.Div([
        dcc.Graph(id='radar-chart', className="chart"),
        dcc.Graph(id='category-bar-chart', className="chart")
    ], className="charts-container"),
    html.Div(id='metric-details', className="metric-details"),
    dcc.Loading(
        id="loading",
        type="circle",
        children=html.Div(id="loading-output")
    )
])

@app.callback(
    [Output('financial-health-output', 'children'),
     Output('radar-chart', 'figure'),
     Output('category-bar-chart', 'figure'),
     Output('metric-details', 'children'),
     Output("loading-output", "children")],
    [Input('submit-button', 'n_clicks'),
     Input('category-bar-chart', 'clickData')],
    [State('ticker-input', 'value')]
)
def update_output(n_clicks, click_data, ticker):
    ctx = dash.callback_context
    if not ctx.triggered:
        return "Please enter a stock ticker and click 'Analyze'.", {}, {}, "", ""

    if ctx.triggered[0]['prop_id'] == 'submit-button.n_clicks':
        if not ticker:
            return "Please enter a stock ticker and click 'Analyze'.", {}, {}, "", ""

        finviz_data = get_finviz_data(ticker)
        if not finviz_data:
            return f"No data found for ticker {ticker}.", {}, {}, "", ""

        assessment_result = assess_financial_health(finviz_data)
        health_assessment = assessment_result["overall_health"]
        category_scores = assessment_result["category_scores"]

        radar_chart = create_radar_chart(category_scores)
        bar_chart = create_bar_chart(category_scores)

        assessment_color = next(
            (color for assessment, color in ASSESSMENT_COLORS.items() if assessment in health_assessment), '#000000')

        output = html.Div([
            html.H2(f"Financial Health Assessment for {ticker}: {health_assessment}",
                    className="assessment-header",
                    style={'color': assessment_color}),
            html.Div([
                html.Div([
                    html.H4(category, className="category-title", style={'color': CATEGORY_COLORS[category]}),
                    html.P(f"{score:.2f}%", className="category-score", style={'color': CATEGORY_COLORS[category]}),
                    html.Div(className="progress-bar",
                             style={'width': f'{score}%', 'background-color': CATEGORY_COLORS[category]})
                ], className="category-score-container")
                for category, score in category_scores.items()
            ], className="category-scores-grid")
        ])

        return output, radar_chart, bar_chart, "", ""

    elif ctx.triggered[0]['prop_id'] == 'category-bar-chart.clickData':
        if click_data is None:
            return dash.no_update, dash.no_update, dash.no_update, "", ""

        category = click_data['points'][0]['x']
        metrics = METRIC_CATEGORIES[category]
        finviz_data = get_finviz_data(ticker)

        metric_details = html.Div([
            html.H3(f"Detailed Metrics for {category}"),
            html.Table([
                html.Tr([html.Th("Metric"), html.Th("Value"), html.Th("Assessment")]),
                *[html.Tr([
                    html.Td(metric),
                    html.Td(finviz_data.get(metric, "N/A")),
                    html.Td(assess_metric(metric, parse_metric_value(finviz_data.get(metric, "N/A"))))
                ]) for metric in metrics]
            ], className="metric-table")
        ])

        return dash.no_update, dash.no_update, dash.no_update, metric_details, ""

def create_radar_chart(category_scores):
    categories = list(category_scores.keys())
    values = list(category_scores.values())

    fig = go.Figure(data=go.Scatterpolar(
        r=values + values[:1],
        theta=categories + categories[:1],
        fill='toself',
        name='Financial Health'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100]),
            angularaxis=dict(
                tickfont=dict(color='#2c3e50')
            )
        ),
        showlegend=False,
        title="Financial Health Radar Chart",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )

    return fig

def create_bar_chart(category_scores):
    categories = list(category_scores.keys())
    values = list(category_scores.values())

    fig = go.Figure(data=[go.Bar(
        x=categories,
        y=values,
        marker_color=[CATEGORY_COLORS[cat] for cat in categories],
        text=values,
        textposition='auto',
    )])

    fig.update_layout(
        title="Category Scores (Click for details)",
        xaxis_title="Categories",
        yaxis_title="Score (%)",
        yaxis=dict(range=[0, 100]),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)