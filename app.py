#Create the virtual environment:  venv myvenv

#Activate the virtual environment: source myvenv/bin/activate

import streamlit as st
import datetime
import pandas as pd
import requests

import pandas as pd
import numpy as np
from tqdm import tqdm
from datetime import datetime, date, timedelta
import time
import os
import altair as alt

#api_key=os.getenv(ALPHAVANTAGE_API_KEY)
api_key="14BSIHSALEHSPS93"

def request_stock_price_hist_for_100days(symbol, token):
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={}&apikey={}'

    r = requests.get(url.format(symbol, token))
    date = []
    colnames = list(range(0, 7))
    df = pd.DataFrame(columns = colnames)

    for i in tqdm(r.json()['Time Series (Daily)'].keys()):
        date.append(i)
        row = pd.DataFrame.from_dict(r.json()['Time Series (Daily)'][i], orient='index').reset_index().T[1:]
        df = pd.concat([df, row], ignore_index=True)
    df.columns = ["open", "high", "low", "close", "adjusted close", "volume", "dividend amount", "split coefficient"]
    df['date'] = date
    df = df[0:100]
    #df = df.rename(columns={'date':'index'}).set_index('index')
    return df

st.sidebar.header('User Input Parameters')

today = date.today()
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
st.header(f"TDI Milestone Project\n Stock Closing Price : {symbol}")
#st.line_chart(data['close'], width = 900, height = 500)
###
chart = alt.Chart(data).mark_line().encode(
  x=alt.X('date:T'),
  y=alt.Y('close:Q'),
  color=alt.Color("name:N")
).properties(title="", width=900, height=500)
st.altair_chart(chart, use_container_width=True)
