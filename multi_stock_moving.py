import yfinance as yf
import streamlit as st
import datetime
import time
import pandas as pd

st.set_page_config(layout="wide")

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
        outp = tickerDf[['Close']].rename(columns={'Close': s})
        outv = tickerDf[['Volume']].rename(columns={'Volume': s})
        firstable=False
    else:
        outp[s] = tickerDf['Close']
        outv[s] = tickerDf['Volume']
    haveResult = True

if haveResult:
    dfp = pd.DataFrame(columns=outp.columns,index=outp.index)
    stock_chart = st.line_chart(dfp)
    for index, row in outp.iterrows():
        # df.loc[len(df.index)] = row
        dfp.loc[index] = row
        time.sleep(0.1)
        stock_chart.line_chart(dfp)