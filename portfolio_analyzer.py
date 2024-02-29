#Initial imports
import pandas as pd
import hvplot.pandas
import alpaca_trade_api as tradeapi
import customtkinter as ctk
import random as random
import panel as pn

#Ignore verbose warnings
from warnings import simplefilter
simplefilter(action="ignore", category=pd.errors.PerformanceWarning)

#Get data for Dataframe
url = 'https://raw.githubusercontent.com/shoukewei/data/main/data-pydm/gdp_china_outlier_treated.csv'
df = pd.read_csv(url)
df.columns=['Province','GDP Rank','Year','GDP','Population','Fix Investment','Trade','Fiscal Expenditure','Urban Income']

# Create a Tkinter window
root = tk.Tk()
root.title("Holoviews in Tkinter")

# Generate a Holoviews scatter plot
plot = df.hvplot.scatter(x='Province', y='GDP', by='Year')

