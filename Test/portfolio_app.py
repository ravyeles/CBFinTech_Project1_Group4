import streamlit as st
import datetime
import alpaca_trade_api as tradeapi
import pandas as pd
import numpy as np
import hvplot
import hvplot.pandas
import holoviews as hv
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.express as px
from MCForecastTools import MCSimulation
import random

#Full list of stocks available for selection. Got from the list of companies in SP500.
full_tickers = ["MSFT","AAPL","AMZN","NKE","TSLA","GOOG","AMD","NVDA","BAC","JPM"]

#Define App Title
st.title('Portfolio Dashboard')
st.markdown("-----")

#Fetch all stock data upfront and filter the dataframe using the inputs submitted by the user. 
def fetch_stock_data():
    #hardcoded variables to be replaced
    tickers = ['MSFT','AAPL','AMZN','NKE','TSLA','GOOG','AMD','NVDA','BAC','JPM']
    start_date = datetime.date(2013,1,1)
    end_date = datetime.date(2023,2,1)

    #Function
    alpaca_api_key = 'PKURMS5ELMEHV4ZGBXTQ'
    alpaca_secret_key = 'NhYNWSU4szskB7qUMl2FXPqYoQZXwL50ahf54jds'
    timeframe = '1D'
    alpaca = tradeapi.REST(
        alpaca_api_key,
        alpaca_secret_key,
        api_version="v2")
    # Get current price data for tickers
    alpaca_df = alpaca.get_bars(
        tickers,
        timeframe,
        start = start_date,
        end = end_date
    ).df
    #Drop time from the index
    alpaca_df.index = alpaca_df.index.date
    #Rename the index to date
    alpaca_df.index.name = 'date'
    #Reorder the columns so that the order of columns is date, ticker, open, high, low, close, volume.
    alpaca_df = alpaca_df[['symbol', 'open', 'high', 'low', 'close', 'volume']]
    #calculate the daily returns
    alpaca_df['daily_return'] = alpaca_df['close'].pct_change()
    #Calculate volatility of returns annualized to a 252 day trading year with a window of 10 days.
    alpaca_df['volatility'] = alpaca_df['daily_return'].rolling(window=10).std() * (252**0.5)
    alpaca_df['30_ma'] = alpaca_df['close'].rolling(30).mean()
    return(alpaca_df)
    
#Fetch the dataframe 
alpaca_df = fetch_stock_data()

#Create Sidebar with sections for user inputs
with st.sidebar:
    #Define user input dialog boxes
    investment_amount = st.number_input("How much would you like to invest", min_value = 100000, max_value = 1000000000,value=100000,step=10000 , placeholder="How much would you like to invest")
    stock_1 = st.selectbox(
       "Pick your first stock",
       options = full_tickers,
       index=None,
       placeholder="",
    )
    stock_2 = st.selectbox(
       "Pick your second stock",
       options = full_tickers,
       index=None,
       placeholder="",
    )
    investment_horizon = st.number_input("How long would you like to invest for", min_value = 2, max_value = 100,value=5,step=1 , placeholder="How long would you like to invest")
    simulation_count = st.number_input("How simulations would you like to run", min_value = 100, max_value = 1000,value=500,step=100 , placeholder="How many weights would you like to simulate")
    start_date = st.date_input('Start Date', 
                                   value=datetime.date(2020,1,1),
                                   min_value=datetime.date(2018,1,1),
                                   max_value=datetime.date(2023,2,1))
    end_date = st.date_input('End Date', 
                                  value=datetime.date(2020,2,1),
                                  min_value=datetime.date(2018,1,1),
                                  max_value=datetime.date(2023,2,1))
    #message = f"You've chosen to invest $ {investment_amount} in {stock_1} and {stock_2} for {investment_horizon} years"

#Filter Alpaca DF based on user inputs
selected_stocks = [stock_1,stock_2]
portfolio_df = alpaca_df.query(
    'date >= @start_date and date <= @end_date and symbol in @selected_stocks'
    )
stock1_df = alpaca_df.query(
    'date >= @start_date and date <= @end_date and symbol == @stock_1'
    )
stock2_df = alpaca_df.query(
    'date >= @start_date and date <= @end_date and symbol == @stock_2'
    )

#Calculate charts and visuals for display
#stock1_returns = px.line(stock1_df, x=stock1_df.index, y=stock1_df['close'], title=f'{stock_1} returns')
#stock2_returns = px.line(stock2_df, x=stock2_df.index, y=stock2_df['close'], title=f'{stock_2} returns')

#Calculate metrics:
def calculate_stock_metrics(stock_df):
    try:
        #lowest close
        metric1 = round(stock_df.close.min(),2)
        #highest close
        metric2 = round(stock_df.close.max(),2)
        #average return
        metric3 = round(stock_df.daily_return.mean(), 3)
        #first_close = stock2_df[stock1_df.index == stock2_df.index.min()]['close']
        #last_close = stock2_df[stock1_df.index == stock2_df.index.max()]['close']
        #total_gain
        metric4 = round(metric2-metric1) #last_close - first_close
        #average_volatility
        metric5 = round(stock1_df['volatility'].mean(),2)
        return metric1, metric2, metric3, metric4, metric5, stock_recommendation
    except:
        return 0,0,0,0,0,"Select a Stock"

#Function to simulate weights for the stocks to use in portfolio construction. It takes the list of tickers as input and the # of combinations the user would like to use
def simulate_weights(no_of_assets, no_of_trials):
    numOfAssets=no_of_assets
    trials = no_of_trials
    overall_weights=[]
    total = 0
    for i in range(trials):
        weights=[]
        for i in range(numOfAssets):
            weights.append(random.random())
        total = sum(weights)
        for i in range(len(weights)):
            weights[i]=round(weights[i]/total,2)
        overall_weights.append(weights)
    #return weights list
    return(overall_weights)
    
simulation_count = 2
no_of_assets = 2
#mc_weights = simulate_weights(no_of_assets,simulation_count)
# Configuring a Monte Carlo simulation to forecast five years cumulative returns
#MC_sim_results = MCSimulation(
#    portfolio_data = portfolio_df,
#    weights = mc_weights,
#    num_simulation = simulation_count,
#    num_trading_days = 252*5
#)

#def create_portfolio(portfolio_df):
#    mean = portfolio_df.groupby('symbol').close.mean()
#    return mean
# Run the Monte Carlo simulation to forecast five years cumulative returns
#MC_fiveyear.calc_cumulative_return()
#tbl = MC_fiveyear.summarize_cumulative_return()

#Create candlestick chart:
def get_candlestick_plot(stock_df):
    fig = make_subplots(
        rows = 2,
        cols = 1,
        shared_xaxes = True,
        vertical_spacing = 0.1,
        subplot_titles = ('Stock Price', 'Volume Chart'),
        row_width = [0.3, 0.7]
    )
    fig.add_trace(
        go.Candlestick(
            x = stock_df.index,
            open = stock_df['open'], 
            high = stock_df['high'],
            low = stock_df['low'],
            close = stock_df['close'],
            name = 'Candlestick chart'
        ),
        row = 1,
        col = 1,
    )
    fig.add_trace(
        go.Bar(x = stock_df.index, y = stock_df['volume'], name = 'volume'),
        row = 2,
        col = 1,
    )
    fig['layout']['xaxis2']['title'] = 'Date'
    fig['layout']['yaxis']['title'] = 'Price'
    fig['layout']['yaxis2']['title'] = 'Volume'
    fig.update_xaxes(
        rangebreaks = [{'bounds': ['sat', 'mon']}],
        rangeslider_visible = False,
    )
    return fig


#Create main panel area where we will house the various tabs:
user_guide, stock_performance, portfolio_composition, portfolio_recommendations = st.tabs(['User Guide', 'Stock Returns', 'Portfolio Composition', 'Portfolio Recommendations'])

#Create a section for a user guide
with user_guide:
    st.header("User Guide")
    st.markdown("-----")
    st.subheader("Add Text here and let's play with some shiz")

#Create a section for the user to evaluate individual stock performance
with stock_performance:
    stock1_tab, stock2_tab, dataframe = st.tabs([f"{stock_1 or 'Please pick a stock'}",f"{stock_2 or 'Please pick a stock'}","Data"])
    with stock1_tab:
        #Get metrics
        #metric1, metric2, metric3, metric4, metric5, stock_recommendation = calculate_stock_metrics(stock1_df)
        metric1 = round(stock1_df.close.min(),2)
        metric2 = round(stock1_df.close.max(),2)
        metric3 = round(stock1_df.daily_return.mean(), 5)
        #first_close = stock2_df[stock1_df.index == stock2_df.index.min()]['close']
        #last_close = stock2_df[stock1_df.index == stock2_df.index.max()]['close']
        metric4 = round(metric2-metric1) #last_close - first_close
        metric5 = round(stock1_df['volatility'].mean(),2)
        stock_recommendation = 'Buy'
        #Create columns
        col1, col2, col3 = st.columns(3)
        with col1:
            st.subheader(f"High: {metric1}")
        with col2:
            st.subheader(f"Low: {metric2}")
        with col3:
            st.subheader(f"Return: {metric3}")
        col4, col5, col6 = st.columns(3)
        with col4:
            st.subheader(f"Stock Gain: {metric4} ")
        with col5:
            st.subheader(f"Volatility: {metric5}")
        with col6:
            st.subheader(f"Signal: {stock_recommendation}")
        st.markdown("-----")
        st.plotly_chart(get_candlestick_plot(stock1_df),use_container_width = True)
    with stock2_tab:
        #Get metrics
        #metric1, metric2, metric3, metric4, metric5, stock_recommendation = calculate_stock_metrics(stock2_df)
        metric1 = round(stock2_df.close.min(),2)
        metric2 = round(stock2_df.close.max(),2)
        metric3 = round(stock2_df.daily_return.mean(), 5)
        #first_close = stock2_df[stock1_df.index == stock2_df.index.min()]['close']
        #last_close = stock2_df[stock1_df.index == stock2_df.index.max()]['close']
        metric4 = round(metric2-metric1) #last_close - first_close
        metric5 = round(stock2_df['volatility'].mean(),2)
        stock_recommendation = 'Buy'
        #Create columns
        col1, col2, col3 = st.columns(3)
        with col1:
            st.subheader(f"High: {metric1}")
        with col2:
            st.subheader(f"Low: {metric2}")
        with col3:
            st.subheader(f"Return: {metric3}")
        col4, col5, col6 = st.columns(3)
        with col4:
            st.subheader(f"Stock Gain: {metric4} ")
        with col5:
            st.subheader(f"Volatility: {metric5}%")
        with col6:
            st.subheader(f"Signal: {stock_recommendation}")
        st.markdown("-----")
        st.plotly_chart(get_candlestick_plot(stock2_df),use_container_width = True)
    with dataframe:
        st.write(portfolio_df)
        
#Create a section to review portfolio composition
with portfolio_composition:
    st.header("Portfolio Composition")
    st.markdown("-----")
    st.write(MC_sim_results)
   #st.write(portfolio_chart))

#Create a section to review portfolio performance
with portfolio_recommendations:
    st.header("We have three recommendations for you to select from based on your Risk Tolerance")
    st.markdown("-----")
    aggressive, defensive, balanced = st.tabs(["Agressive Returns", "Defensive Risk", "Balanced Portfolio"])
    with aggressive:
        st.header("Aggressive Portfolio Returns")
        st.markdown("-----")
       #st.write(individual_chart2))
    with defensive:
        st.header("Aggressive Portfolio Returns")
        st.markdown("-----")
       #st.write(individual_chart2))
    with balanced:
        st.header("Aggressive Portfolio Returns")
        st.markdown("-----")
       #st.write(individual_chart2))
