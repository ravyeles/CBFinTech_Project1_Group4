# Initial imports
import os
import requests
import json
import pandas as pd
from dotenv import load_dotenv
import alpaca_trade_api as tradeapi
from MCForecastTools import MCSimulation
import random 
from warnings import simplefilter
simplefilter(action="ignore", category=pd.errors.PerformanceWarning)

# Load .env environment variables
alpaca_api_key = 'PKURMS5ELMEHV4ZGBXTQ'
alpaca_secret_key = 'NhYNWSU4szskB7qUMl2FXPqYoQZXwL50ahf54jds'  

#Load Alpaca API details
start_date = '2018-01-01'
end_date = '2023-12-31'
timeframe = '1D'

#Define a function that presents the user with an input dialog where they can input the total $ amount they'd like to invest, the total time they'd like to stay invested for, and 5 stocks they'd like to invest in.
def get_user_input():
    capital = float(input("How much money would you like to invest?"))
    time = int(input("How long would you like to stay invested for?"))
    tickers[0] = input("Enter the first stock you'd like to invest in:")
    tickers[1] = input("Enter the second stock you'd like to invest in:")
    tickers[2] = input("Enter the third stock you'd like to invest in:")
    tickers[3] = input("Enter the fourth stock you'd like to invest in:")
    tickers[4] = input("Enter the fifth stock you'd like to invest in:")
    print(f"You would like to invest ${capital} for {time} years in the following stocks: {tickers[0]}, {tickers[1]}, {tickers[2]}, {tickers[3]}, {tickers[4]}")
