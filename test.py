import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set the stock symbol and interval
stock_symbol = "AAPL"
interval = "1m"  # 1 minute intervals, change as needed


# Function to update the graph with real-time data
def update_graph(i):
    # Fetch real-time stock data
    df = yf.download(stock_symbol, period="1d", interval=interval)

    # Update the plotly figure
    fig = make_subplots(rows=1, cols=1, subplot_titles=[f"Real-time Stock Price - {stock_symbol}"])

    # Plot candlestick chart
    candlestick = go.Candlestick(x=df.index,
                                 open=df['Open'],
                                 high=df['High'],
                                 low=df['Low'],
                                 close=df['Close'],
                                 name='Candlesticks')

    fig.add_trace(candlestick)

    # Update the layout
    fig.update_layout(xaxis_rangeslider_visible=False)

    # Show the plot
    fig.show()


# Set up the animation
ani = FuncAnimation(plt.gcf(), update_graph, interval=60000)  # Update every 1 minute (60000 milliseconds)

# Show the plot
plt.show()
