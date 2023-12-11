import yfinance as yf
from dash import dcc, html, Dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from plotly.subplots import make_subplots
import plotly.graph_objs as go
import pandas as pd
import base64
import io

# making app using dash
app = Dash(__name__)

# app layout
app.layout = html.Div(children=[
    # drag and drop csv upload
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
            'backgroundColor': 'lightgreen',
        },
        multiple=False
    ),

    # Display box for uploaded file information
    html.Div(id='upload-info-box', style={'margin': '10px', 'padding': '10px', 'border': '1px solid #ccc'}),

    html.Label("Select Graph Type:"),
    dcc.Dropdown(
        id='graph-type-dropdown',
        options=[
            {'label': 'Candlestick', 'value': 'candlestick'},
            {'label': 'Line', 'value': 'line'}
        ],
        value='Line',  # default line since the majority of users are more familiar with this style of graph
        style={'width': '100%'}
    ),

    html.Label("Enter Stock Ticker:"),
    dcc.Input(id='stock-ticker-input', type='text', value='AAPL'),
    html.Button('Update Chart', id='update-button', n_clicks=0),
    dcc.Graph(id='real-time-graph', style={'height': '80vh'}),
])

# updates candlestick vs linechart
@app.callback(Output('real-time-graph', 'figure'),
              [Input('update-button', 'n_clicks')],
              [State('stock-ticker-input', 'value'),
               State('graph-type-dropdown', 'value')])
def update_graph(n_clicks, stock_symbol, graph_type):
    if n_clicks > 0:
        # realtime stock data
        df = yf.download(stock_symbol, period="1d", interval="1m")

        # creates chart
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

        fig.update_layout(xaxis_rangeslider_visible=False)

        return fig
    else:
        return go.Figure()

@app.callback(Output('upload-info-box', 'children'),
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename')])
def upload_file(contents, filename):
    if contents is None:
        raise PreventUpdate

    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))

    # looks for column containing 'tick' or 'symb'
    tick_symb_columns = [col for col in df.columns if 'tick' in col.lower() or 'symb' in col.lower()]
    unique_values = []

    info_text = []
    for column in tick_symb_columns:
        unique_values.extend(df[column].unique())
    unique_values = list(set(unique_values))

    data = pd.read_csv('SP 500 ESG Risk Ratings.csv')
    for i in unique_values:
        def get_esg_data(ticker):
            filtered_data = data[data['Symbol'] == ticker]
            if filtered_data.empty:
                return "Ticker not found"
            esg_data = filtered_data[['Total ESG Risk score', 'Environment Risk Score', 'Governance Risk Score',
                                      'Social Risk Score', 'Controversy Level']].values.tolist()
            return esg_data

        ticker_input = i
        result = get_esg_data(ticker_input)

        if result == "Ticker not found":
            info_text.append(result)
        else:
            label = f'{i}, Total ESG Risk score'
            info_text.append(label + ": " + str(result[0][0]))

    return info_text

# runs app
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
