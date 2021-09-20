import streamlit as st
import datetime
import talib
import ta
import pandas as pd
import requests

import pandas as pd
import numpy as np
from tqdm import tqdm
from datetime import timedelta
from datetime import datetime
import time
import os

api_key=os.getenv(ALPHAVANTAGE_API_KEY)

def request_stock_price_hist_for_100days(symbol, token, sample = False):
    if sample == False:
        q_string = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={}&outputsize=full&apikey={}'
    else:
        q_string = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={}&apikey={}'

    print("Retrieving stock price data from Alpha Vantage (This may take a while)...")

    r = requests.get(q_string.format(symbol, token))
    print("Data has been successfully downloaded...")
    date = []
    colnames = list(range(0, 7))
    df = pd.DataFrame(columns = colnames)
    print("Sorting the retrieved data into a dataframe...")
    for i in tqdm(r.json()['Time Series (Daily)'].keys()):
        date.append(i)
        row = pd.DataFrame.from_dict(r.json()['Time Series (Daily)'][i], orient='index').reset_index().T[1:]
        df = pd.concat([df, row], ignore_index=True)
    df.columns = ["open", "high", "low", "close", "adjusted close", "volume", "dividend amount", "split cf"]
    df['date'] = date
    df = df[0:100]
    return df

st.sidebar.header('User Input Parameters')

today = datetime.date.today()
one_month_ago = (today.replace(day=1) - timedelta(days=1)).replace(day=today.day)
def user_input_features():
    ticker = st.sidebar.text_input("Ticker", 'AAPL')
    start_date = st.sidebar.text_input("Start Date", f'{one_month_ago}')
    end_date = st.sidebar.text_input("End Date", f'{today}')
    return ticker, start_date, end_date

symbol, start, end = user_input_features()

start = pd.to_datetime(start)
end = pd.to_datetime(end)

# Read data
data = request_stock_price_hist_for_100days(symbol, api_key)
###
# Adjusted Close Price
st.header(f"Adjusted Close Price\n {company_name}")
st.line_chart(data['adjusted close'])
