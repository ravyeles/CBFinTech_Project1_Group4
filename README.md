# CBFinTech_Project1_Group4
Repository for Project 1 in the Columbia FinTech Bootcamp (Group 4)



# Overview:

Our Financial Application will take the following inputs from a user:
1. A minimum of 5 stocks.
2. A time horizon for investment.
3. A initial investment amount.


It will then fetch the stock return information using the ALPACA API. 
It will then assess the following details for each stock:
1. Volatility (Risk)
2. Actual Returns 


1. Randomize the creation of different portfolios:
2. For each of the stocks randomly assign weights such that the total = 100%
3. Run a monte carlo simulation for each of the weight combinations for the portfolio
4. Capture the expected return, and the volatilty for each of the weight combinations/portfolios. (-ive weights are possible and we are short selling)
5. Rank order them based on highest returns; lowest risk; and some middle ground options
6. Plot the various options for the user to visually distinguish
7. Present the options for the user to choose from


Those three options and the associated metrics (like expected return, Total Profit)
will be presented to the user with detailed charts (HVplot)
Two levels:
1. Each options (1a, 1b, 1c)
a - Berakout of stock composition within option. We will see portfolio growth and volatility (candlestick visual) 
2. Compare all options against each other.
    Overlay the grapsh and provide visual indicators of discrepancies.

Look up representing Risk. Risk Adjusted Returns (Sharpe, Sortino, Downside, Drawdown)

Libraries:
1. Pandas
2. Requests
3. Json
4. Alpaca
5. HVPLot
6. UI Libraries (to generate the widgets for Input) 
7. Plotly
8. Finta (Financial Libraries)
9. Pyton MC packages

