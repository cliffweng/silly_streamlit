import yfinance as yf
import streamlit as st
import datetime
import pandas as pd

st.write("""
# Simple Multiple Stock Price App
Shown are the stock closing price and volume of the stocks!
""")
Snp500=pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]

stocks = st.multiselect('Select stocks', Snp500.Symbol.values.tolist())
##stock = st.sidebar.text_input("Stock ticker here", "AAPL")

startdate = st.sidebar.date_input(label='Start', value=(datetime.date(2019,1,1)))
enddate = st.sidebar.date_input(label='End', value=( datetime.date.today()))

firstable=True
haveResult = False

for s in stocks:
    tickerDf = yf.Ticker(s).history(period='1d', start=startdate, end=enddate)
    if firstable==True:
        outputdf = tickerDf[['Close']].rename(columns={'Close': s})
        voldf = tickerDf[['Volume']].rename(columns={'Volume': s})
        firstable=False
    else:
        outputdf[s] = tickerDf['Close']
        voldf[s] = tickerDf['Volume']
    haveResult = True

if haveResult:
    st.line_chart(outputdf)
    st.line_chart(voldf)