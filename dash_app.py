import yfinance as yf
from dash import dcc, html, Dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from plotly.subplots import make_subplots
import plotly.graph_objs as go
import pandas as pd
import base64
import io
from esg_analysis import analyze_esg

# Create Dash app
app = Dash(__name__)

# Layout of the app
app.layout = html.Div(children=[
    # Upload box at the top
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px',
            'backgroundColor': 'lightgreen',  # Light green color
        },
        multiple=False
    ),

    # Dropdown menu for graph type
    html.Label("Select Graph Type:"),
    dcc.Dropdown(
        id='graph-type-dropdown',
        options=[
            {'label': 'Candlestick', 'value': 'candlestick'},
            {'label': 'Line', 'value': 'line'}
        ],
        value='candlestick',  # Default to candlestick
        style={'width': '100%'}
    ),

    # Rest of the app
    html.Label("Enter Stock Ticker:"),
    dcc.Input(id='stock-ticker-input', type='text', value='AAPL'),
    html.Button('Update Chart', id='update-button', n_clicks=0),
    dcc.Graph(id='real-time-graph', style={'height': '80vh'}),  # Adjusted height
])

# Function to update the candlestick or line chart
@app.callback(Output('real-time-graph', 'figure'),
              [Input('update-button', 'n_clicks')],
              [State('stock-ticker-input', 'value'),
               State('graph-type-dropdown', 'value')])
def update_graph(n_clicks, stock_symbol, graph_type):
    if n_clicks > 0:
        # Fetch real-time stock data
        df = yf.download(stock_symbol, period="1d", interval="1m")

        # Create chart based on selected type
        fig = make_subplots(rows=1, cols=1, subplot_titles=[f"Real-time Stock Price - {stock_symbol}"])

        if graph_type == 'candlestick':
            trace = go.Candlestick(x=df.index,
                                   open=df['Open'],
                                   high=df['High'],
                                   low=df['Low'],
                                   close=df['Close'],
                                   name='Candlesticks')
        else:
            trace = go.Scatter(x=df.index,
                               y=df['Close'],
                               mode='lines',
                               name='Line')

        fig.add_trace(trace)

        # Update layout
        fig.update_layout(xaxis_rangeslider_visible=False)

        return fig
    else:
        # Return an empty figure initially
        return go.Figure()

# Callback to handle file upload
@app.callback(Output('upload-data', 'children'),
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename')])
def upload_file(contents, filename):
    if contents is None:
        raise PreventUpdate

    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))

    # Output a list of unique values in columns containing 'tick' or 'symb'
    tick_symb_columns = [col for col in df.columns if 'tick' in col.lower() or 'symb' in col.lower()]
    unique_values = []

    for column in tick_symb_columns:
        unique_values.extend(df[column].unique())
    unique_values = list(set(unique_values))
    print(unique_values)

    # for i in unique_values:
    #     lambda




    return f'file {filename} uploaded successfully!'

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
