import dash
from financial_metrics_analysis import METRICS, assess_financial_health
from dashboard_layout import create_layout, register_callbacks

app = dash.Dash(__name__)
app.layout = create_layout()
register_callbacks(app)  # Add this line

if __name__ == '__main__':
    app.run_server(debug=True)