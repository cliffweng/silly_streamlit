import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import yfinance as yf
import datetime

st.set_page_config(layout="wide")
st.title('S&P 500 App')

st.markdown("""
**Data source:** [Wikipedia](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies).
""")

st.sidebar.header('User Input Features')
startdate = st.sidebar.date_input(label='Start', value=(datetime.date(2019,1,1)))
enddate = st.sidebar.date_input(label='End', value=( datetime.date.today()))

# Web scraping of S&P 500 data
@st.cache
def load_data():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    html = pd.read_html(url, header = 0)
    df = html[0]
    return df

df = load_data()
sector = df.groupby('GICS Sector')

# Sidebar - Sector selection
sorted_sector_unique = sorted( df['GICS Sector'].unique() )
selected_sector = st.sidebar.multiselect('Sector', sorted_sector_unique)

df_selected_sector = df[ (df['GICS Sector'].isin(selected_sector)) ]
stocks = st.sidebar.multiselect('Select stocks', df_selected_sector.Symbol.values.tolist())

st.write('Number of Stocks selected: ' + str(df_selected_sector.shape[0]))
st.dataframe(df_selected_sector, width=1200)

# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="SP500.csv">Download CSV File</a>'
    return href
st.markdown(filedownload(df_selected_sector), unsafe_allow_html=True)

@st.cache
def load_stock(ticker):
    return yf.Ticker(s).history(period='1d', start=startdate, end=enddate)


if stocks != None:
    firstable=True
    haveResult = False

    for s in stocks:
        tickerDf = load_stock(s)
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


