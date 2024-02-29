#Initial Impors
import panel as pn
import hvplot.pandas
import pandas as pd
import numpy as np
import alpaca_trade_api as tradeapi
pn.extension(design='material')#, embed=True, sizing_mode='stretch_width', logo='https://www.newtraderu.com/wp-content/uploads/12-Principles-of-Building-Wealth-Eye-opening.jpg')
#hardcoded variables to be replaced by user input and environment variable calls in the future
tickers = ['MSFT','GOOG', 'AAPL', 'AMZN', 'TSLA']
start_date = '2018-01-01'
end_date = '2023-12-31'
timeframe = '1D'
alpaca_api_key = 'PKURMS5ELMEHV4ZGBXTQ'
alpaca_secret_key = 'NhYNWSU4szskB7qUMl2FXPqYoQZXwL50ahf54jds' 
# Create the Alpaca API object
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

def transform_data(variable, window, sigma):
    ''' Calculates the rolling average and the outliers '''
    avg = alpaca_df[variable].rolling(window=window).mean()
    residual = alpaca_df[variable] - avg
    std = residual.rolling(window=window).std()
    outliers = np.abs(residual) > std * sigma
    return avg, avg[outliers]

def create_plot(variable='close', window=30, sigma=10):
    ''' Plots the rolling average and the outliers '''
    avg, highlight = transform_data(variable, window, sigma)
    return avg.hvplot(height=300, width=400, legend=False) * highlight.hvplot.scatter(
        color="orange", padding=0.1, legend=False
    )
variable_widget = pn.widgets.Select(name="variable", value="close", options=list(alpaca_df.columns))
window_widget = pn.widgets.IntSlider(name="window", value=30, start=1, end=60)
sigma_widget = pn.widgets.IntSlider(name="sigma", value=10, start=0, end=20)
bound_plot = pn.bind(create_plot, variable=variable_widget, window=window_widget, sigma=sigma_widget)

first_app = pn.Column(variable_widget, window_widget, sigma_widget, bound_plot)
first_app.servable()
