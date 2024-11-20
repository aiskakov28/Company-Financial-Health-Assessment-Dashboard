from dash import dcc, html
from dash.dependencies import Input, Output, State
from financial_metrics_analysis import METRICS, assess_financial_health

def create_layout():
    return html.Div([
        html.H1("Financial Health Dashboard", style={'fontSize': '48px', 'textAlign': 'center', 'marginBottom': '20px'}),
        html.Div([
            html.Div([
                html.Label(metric, style={'fontSize': '18px', 'marginBottom': '5px'}),
                dcc.Input(
                    id=f'metric-input-{i}',
                    type='number',
                    placeholder=f"Enter {metric}",
                    style={'fontSize': '16px', 'width': '100%', 'height': '30px', 'marginBottom': '10px'}
                )
            ]) for i, metric in enumerate(METRICS)
        ], style={'width': '90%', 'margin': 'auto', 'columnCount': '2', 'columnGap': '20px'}),
        html.Button(
            'Calculate Financial Health',
            id='submit-button',
            n_clicks=0,
            style={
                'fontSize': '20px',
                'padding': '10px 20px',
                'marginTop': '20px',
                'marginBottom': '20px',
                'backgroundColor': '#4CAF50',
                'color': 'white',
                'border': 'none',
                'borderRadius': '5px',
                'cursor': 'pointer'
            }
        ),
        html.Div(id='financial-health-output', style={'fontSize': '24px', 'textAlign': 'center'})
    ], style={'padding': '30px', 'maxWidth': '800px', 'margin': 'auto'})

def register_callbacks(app):
    @app.callback(
        Output('financial-health-output', 'children'),
        [Input('submit-button', 'n_clicks')],
        [State(f'metric-input-{i}', 'value') for i in range(len(METRICS))]
    )
    def update_output(n_clicks, *input_values):
        if n_clicks == 0:
            return "Please enter financial metrics and click 'Calculate Financial Health'."
        processed_inputs = {metric: float(value) if value is not None else None
                            for metric, value in zip(METRICS, input_values)}
        if any(value is None for value in processed_inputs.values()):
            return "Please enter all required financial metrics."
        assessment_result = assess_financial_health(processed_inputs)
        health_assessment = assessment_result["overall_health"]
        category_scores = [
            html.P(f"{category}: {score:.2f}%")
            for category, score in assessment_result["category_scores"].items()
        ]
        return html.Div([
            html.H2(f"Financial Health Assessment: {health_assessment}", style={'fontSize': '24px'}),
            html.Div(category_scores)
        ])