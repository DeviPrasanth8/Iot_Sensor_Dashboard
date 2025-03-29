import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import requests

# Initialize Dash app
app = dash.Dash(__name__)
server = app.server  # for deployment if needed

# Dashboard layout
app.layout = html.Div([
    html.H1("📡 Real-Time IoT Sensor Dashboard", style={'textAlign': 'center'}),

    html.A("⬇️ Download CSV", href="http://localhost:5000/api/export_csv", target="_blank", style={
        'display': 'inline-block',
        'margin': '10px',
        'fontSize': '18px',
        'textDecoration': 'none',
        'color': 'white',
        'backgroundColor': '#007bff',
        'padding': '10px 20px',
        'borderRadius': '8px',
    }),

    dcc.Graph(id='live-chart'),

    dcc.Interval(
        id='interval-component',
        interval=5*1000,
        n_intervals=0
    )
])

# Function to fetch data from Flask API
def fetch_data():
    try:
        response = requests.get("http://localhost:5000/api/sensor_data")
        return response.json()
    except Exception as e:
        print("Error fetching data:", e)
        return []

# Callback to update chart
@app.callback(
    Output('live-chart', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_chart(n):
    data = fetch_data()

    # Filter data
    temp_data = [d for d in data if d['field'] == 'temperature']
    hum_data = [d for d in data if d['field'] == 'humidity']

    # Temperature
    x_temp = [d['time'] for d in temp_data]
    y_temp = [d['value'] for d in temp_data]

    # Humidity
    x_hum = [d['time'] for d in hum_data]
    y_hum = [d['value'] for d in hum_data]

    fig = {
        'data': [
            go.Scatter(
                x=x_temp,
                y=y_temp,
                mode='lines+markers',
                name='Temperature (°C)',
                line=dict(color='red'),
                yaxis='y1'
            ),
            go.Scatter(
                x=x_hum,
                y=y_hum,
                mode='lines+markers',
                name='Humidity (%)',
                line=dict(color='blue'),
                yaxis='y2'
            )
        ],
        'layout': go.Layout(
            title='Temperature & Humidity Over Time',
            xaxis=dict(title='Time'),
            yaxis=dict(
                title='Temperature (°C)',
                side='left',
                showgrid=True
            ),
            yaxis2=dict(
                title='Humidity (%)',
                side='right',
                overlaying='y',
                showgrid=False
            ),
            height=500,
            legend=dict(x=0, y=1.1, orientation='h')
        )
    }

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
