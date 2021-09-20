import yfinance as yf
import streamlit as st
import datetime
import talib
import ta
import pandas as pd
import requests

yf.pdr_override()


st.sidebar.header('User Input Parameters')

today = datetime.date.today()
one_month_ago = (today.replace(day=1) - timedelta(days=1)).replace(day=today.day)
def user_input_features():
    ticker = st.sidebar.text_input("Ticker", 'AAPL')
    start_date = st.sidebar.text_input("Start Date", f'{one_month_ago}')
    end_date = st.sidebar.text_input("End Date", f'{today}')
    return ticker, start_date, end_date

symbol, start, end = user_input_features()

def get_symbol(symbol):
    url = "http://d.yimg.com/autoc.finance.yahoo.com/autoc?query={}&region=1&lang=en".format(symbol)
    result = requests.get(url).json()
    for x in result['ResultSet']['Result']:
        if x['symbol'] == symbol:
            return x['name']
company_name = get_symbol(symbol.upper())

start = pd.to_datetime(start)
end = pd.to_datetime(end)

# Read data
data = yf.download(symbol,start,end)
###
# Adjusted Close Price
st.header(f"Adjusted Close Price\n {company_name}")
st.line_chart(data['Adj Close'])
