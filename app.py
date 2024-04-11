import streamlit as st
from prophet import Prophet
import plotly.express as px 
import pandas as pd 
import numpy as np
import yfinance as yf 
from prophet.plot import plot_plotly
from datetime import date, timedelta, datetime
from stocknews import StockNews

# def do_stuff_on_page_load(...):
#     st.set_page_config(layout="wide")

def format_market_cap(n):
    if n >= 1e12:  # Trillion
        return '${:.2f} T'.format(n / 1e12)
    elif n >= 1e9:  # Billion
        return '${:.2f} B'.format(n / 1e9)
    elif n >= 1e6:  # Million
        return '${:.2f} M'.format(n / 1e6)
    elif n >= 1e3:  # Thousand
        return '${:.2f} K'.format(n / 1e3)
    else:
        return '${:.2f}'.format(n)



st.set_page_config(layout="wide", initial_sidebar_state="expanded")


st.title("Stock Dashboard")
sidebar = st.sidebar
with sidebar:
    ticker = st.text_input("Ticker", value="GOOGL")
    start_date = st.date_input("Start Date", value=datetime.strptime("2023/01/01", '%Y/%m/%d').date())
    end_date = st.date_input("End Date")
    # button = st.button("Generate")# CHANGE THIS
    data = yf.download(ticker, start_date, end_date + timedelta(1))
    col = st.selectbox("Select column",data.columns)
    # ticker_obj = yf.Ticker(ticker)
    # info = ticker_obj.info 
    # CEO_name = info['companyOfficers'][0]['name']
    # CEO_title = info['companyOfficers'][0]['title']
    # business_summary = info['longBusinessSummary']
    # phone_number = info['phone']
    # website = info['website']
    # industry = info['industry']
    # name = ticker_obj.info['longName']

# if button: 
#     try:
#         data = yf.download(ticker, start_date, end_date + timedelta(1))
#         col = st.selectbox("Select column",data.columns)
#         ticker_obj = yf.Ticker(ticker)
#         info = ticker_obj.info 
#         CEO_name = info['companyOfficers'][0]['name']
#         CEO_title = info['companyOfficers'][0]['title']
#         # CEO_pay = info['companyOfficers'][0]['pay']
#         business_summary = info['longBusinessSummary']
#         phone_number = info['phone']
#         website = info['website']
#         industry = info['industry']
#         name = ticker_obj.info['longName']
#     except:
#         st.warning("Ticker does not exist")
            
ticker_obj = yf.Ticker(ticker)
info = ticker_obj.info 
CEO_name = info['companyOfficers'][0]['name']
CEO_title = info['companyOfficers'][0]['title']
business_summary = info['longBusinessSummary']
phone_number = info['phone']
website = info['website']
industry = info['industry']
name = ticker_obj.info['longName']
st.subheader(name)

overview_tab, forecast_tab, info_tab ,news_tab = st.tabs(['Overview', 'Forecast', 'Info', 'News'])

with overview_tab:
    today = date.today()
    yesterday = today - timedelta(1)
    current_price = round(data.tail(1)['Close'].values.tolist()[0], 2)
    yesterday_price = round(data['Close'].iloc[-2], 2)
    percentage_change = round(((yesterday_price - current_price)/yesterday_price)*100, 2)
    current_volume = data.tail(1)['Volume'].values.tolist()[0]
    previous_volume = data['Volume'].iloc[-2]
    ticker_obj = yf.Ticker(ticker)
    info = ticker_obj.info 
    market_cap = info['marketCap']
    data.reset_index(inplace=True)
    data['Date'] = data['Date'].dt.date
    data.set_index('Date', inplace=True)
    fig = px.line(data, x=data.index, y=data[col])
    fig.update_xaxes(tickformat="%d %b %y")
    st.plotly_chart(fig)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            label="Price",
            value=current_price,
            delta=f"{-percentage_change}%"
        )
    with col2: 
        st.metric(
            label="Volume",
            value=current_volume,
            delta=int(previous_volume) - current_volume
        )
    with col3: 
        st.metric(
            label="Market Cap(current)",
            value=format_market_cap(market_cap)
        )
    

with forecast_tab:
    st.write("Tip: Works better with larger datasets")
    forecast_date = st.date_input("Forecast to", value=datetime.strptime("2025/01/01", '%Y/%m/%d').date())
    df = data.reset_index()[['Date', col]]
    df.columns = ['ds', 'y'] 

    m = Prophet(interval_width=0.95, seasonality_mode='additive', yearly_seasonality=True, weekly_seasonality=True)
    model = m.fit(df)
    forecast_date_range = m.make_future_dataframe((forecast_date - end_date).days, freq='D')
    forecast = m.predict(forecast_date_range)
    # st.dataframe(forecast)
    tomorrow = end_date + timedelta(1)
    tomorrow = datetime.combine(tomorrow, datetime.min.time())
    expected_price_df = forecast[forecast['ds'] == tomorrow]
    expected_price = round((expected_price_df['yhat'].values)[0], 2)
    end_date_dt = datetime.combine(end_date, datetime.min.time())
    expected_end_date_df = forecast[forecast['ds'] == end_date_dt]
    expected_end_price = round((expected_end_date_df['yhat'].values)[0], 2)
    percentage_change = round(((expected_end_price - expected_price)/expected_end_price)*100, 2)
    #st.write(expected_price)
    st.metric(label="Price (Next Day)", value=expected_price, delta=f"{-percentage_change}%")
    plot = plot_plotly(m, forecast)
    plot.update_xaxes(tickformat="%d %b %y")
    plot.update_layout(xaxis_title = None, yaxis_title= None)
    for trace in plot.data:
        if trace.name == 'Actual':
            trace.marker.color = 'white'
    st.plotly_chart(plot)

with info_tab:
    st.write(name)
    st.write("Contact:", phone_number)
    st.write("Website:", website)

    st.write("CEO:", CEO_name, ", ", CEO_title)
    st.write("Industry:", industry)
    st.write("Summary:", business_summary)

with news_tab:
    #st.subheader(f'News of {ticker}')
    sn = StockNews(ticker, save_news=False)
    df_news = sn.read_rss()
    for i in range(10):
        st.subheader(f"News {df_news['published'][i]}")
        #st.write(df_news['published'][i])
        st.write(df_news['title'][i])
        st.write(df_news['summary'][i])
        title_sentiment = df_news['sentiment_title'][i]
        st.write(f'Title Sentiment {title_sentiment}')
        news_sentiment = df_news['sentiment_summary'][i]
        st.write(f'News Sentiment {news_sentiment}')


# info = ticker_obj.info 
# CEO_name = info['companyOfficers'][0]['name']
# CEO_title = info['companyOfficers'][0]['title']
# business_summary = info['longBusinessSummary']
# phone_number = info['phone']
# website = info['website']
# industry = info['industry']
# name = ticker_obj.info['longName']