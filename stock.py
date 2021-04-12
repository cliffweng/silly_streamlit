import yfinance as yf
import streamlit as st
import datetime

st.write("""
# Simple Stock Price App
Shown are the stock closing price and volume of the stock!
""")

# stock = st.selectbox('Select one symbol', ( 'AAPL', 'MSFT',"SPY",'WMT'))
stock = st.sidebar.text_input("Stock ticker here", "AAPL")

startdate = st.sidebar.date_input(label='Start', value=(datetime.date(2019,7,6)))
enddate = st.sidebar.date_input(label='End', value=( datetime.date.today()))

tickerDf = yf.Ticker(stock).history(period='1d', start=startdate, end=enddate)
# Open	High	Low	Close	Volume	Dividends	Stock Splits

st.line_chart(tickerDf.Close)
st.line_chart(tickerDf.Volume)