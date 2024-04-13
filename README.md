# Stock-Dashboard

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://stockforecastdashboard.streamlit.app/)
[![Linkedin](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/bonga-dumakude)

## Description
A stock dashbooard that displays information relating to a company and has 4 tabs of information. The user may choose the start and end date for the information they wish to analyse.

### 1. Overview Tab
A plot of the stock prices - the user may choose to view a plot of Open, Close, High, Low and Volume values. 

### 2. Forecasting Tab
- The user may input a future date to forecast stock prices.
- A Facebook Prophet model is used to generate a forecast and show a plot with error bars

### 3. Info Tab
- Contains basic information about the company including, name, CEO, contact, website, industry and a summary of the company's services

### 4. News 
- Contains the last 10 news stories published about the company along with a measure of the sentiment towards both the article title and the article content.
