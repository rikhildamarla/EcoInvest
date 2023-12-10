#rand_portfolio.py: generates a random financial stock portfolio for us to do ESG checks/recommendations on
import pandas as pd
import yfinance as yf
from datetime import datetime
import numpy as np


#real time stock prices
def get_current_price(ticker):
    stock = yf.Ticker(ticker)
    return stock.info.get("regularMarketPrice", np.nan)


#historical prices
def get_historical_prices(ticker, start_date, end_date):
    stock = yf.Ticker(ticker)
    try:
        data = stock.history(start=start_date, end=end_date)
        return data['Close'].values
    except:
        return []


#get random transaction amounts within a range for realistic values
def generate_random_transaction_amount(ticker, shares):
    start_date = datetime.now() - pd.DateOffset(years=1)
    end_date = datetime.now()
    historical_prices = get_historical_prices(ticker, start_date, end_date)

    #gets random value between 52 week high and low to
    if len(historical_prices) > 0:
        high = max(historical_prices)
        low = min(historical_prices)
        return np.random.uniform(low, high) * shares
    else:
        return np.nan


#example data for average portfolio
data = {
    'Date Bought': pd.to_datetime(
        ['2023-01-01', '2023-02-15', '2023-03-20', '2023-04-10', '2023-05-05', '2023-06-12', '2023-07-18', '2023-08-22',
         '2023-09-30', '2023-10-15', '2023-11-01', '2023-12-05']),
    'Transaction Type': ['Buy', 'Buy', 'Buy', 'Sell', 'Buy', 'Sell', 'Buy', 'Sell', 'Buy', 'Buy', 'Buy', 'Buy'],
    'Total Transaction Amount': [generate_random_transaction_amount('AAPL', 15),
                                 generate_random_transaction_amount('GOOGL', 8),
                                 generate_random_transaction_amount('MSFT', 12),
                                 generate_random_transaction_amount('AMZN', 5),
                                 generate_random_transaction_amount('TSLA', 6),
                                 generate_random_transaction_amount('META', 10),
                                 generate_random_transaction_amount('NFLX', 7),
                                 generate_random_transaction_amount('V', 9),
                                 generate_random_transaction_amount('JPM', 11),
                                 generate_random_transaction_amount('WMT', 15),
                                 generate_random_transaction_amount('SPY', 20),
                                 generate_random_transaction_amount('VTSMX', 25)],
    'Company': ['Apple', 'Alphabet', 'Microsoft', 'Amazon', 'Tesla', 'Facebook', 'Netflix', 'Visa', 'JPMorgan',
                'Walmart', 'SPDR S&P 500 ETF Trust', 'Vanguard Total Stock Market Index Fund'],
    'Ticker': ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA', 'META', 'NFLX', 'V', 'JPM', 'WMT', 'SPY', 'VTSMX'],
    'Industry': ['Technology', 'Technology', 'Technology', 'E-Commerce', 'Automotive', 'Technology', 'Entertainment',
                 'Finance', 'Finance', 'Retail', 'ETF', 'Mutual Fund'],
    'Shares': [15, 8, 12, 5, 6, 10, 7, 9, 11, 15, 20, 25],
}

#make dataframe
df = pd.DataFrame(data)

#current price
df['Current Price'] = df['Ticker'].apply(get_current_price)

#get historical prices for realism
start_date = min(df['Date Bought'])
end_date = max(df['Date Bought'])
df['52 Week High'] = df['Ticker'].apply(lambda x: max(get_historical_prices(x, start_date, end_date), default=np.nan))
df['52 Week Low'] = df['Ticker'].apply(lambda x: min(get_historical_prices(x, start_date, end_date), default=np.nan))
df['Market Value'] = df['Shares'] * df['Current Price']
df['% Breakdown'] = (df['Market Value'] / df['Market Value'].sum()) * 100
df['$ Day Change'] = np.random.uniform(-0.02, 0.02, len(df))

#save to csv
csv_file_path = 'portfolio_tracking.csv'
df.to_csv(csv_file_path, index=False)

print(f"csv saved at: {csv_file_path}")
