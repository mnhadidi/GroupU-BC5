import pandas as pd

####################
# project variables
####################

project_colors = {
    'background': '#1A1A2E',
    'dark-blue': '#16213E',
    'navy-blue': '#0F3460',
    'pink': '#E94560',
    'white': '#FFFFFF',
    'red': '#F6465D',
    'green': '#0ECB81'
}

# content style for right side of dashboard
CONTENT_STYLE = {
    "margin-left": "17rem",
    "margin-right": "0",
    "padding": "1rem 1rem",
}


####################
# crypto variables
####################
# information to initialize individual coin layout
start_info = {
    # make sure the coin name is one of the 'values' of coin_dict
    'coin': 'ADA',
    # this is the selected initial timeframe for the crypto insights dash
    'time': '1y',
    # this is the time between data gathered from yfinance, started with 1d
    'interval': '1d'
}

# get all coins
coins_df = pd.read_csv("data/coin-full-list.csv")
coin_dict_v2 = coins_df.set_index('Coin')['Name'].to_dict()

# get available timeframes for yfinance
timeframe_tranf = {
    '1d': 1, '5d': 5, '1mo': 30,
    '3mo': 90, '6mo': 180, '1y': 365,
    '2y': 730, '5y': 1825, '10y': 3650,
    'max': 9999999}

# translator for timeframe into actual text
timeframe_full_name = {
    '1d': '1 day', '5d': '5 days', '1mo': '1 month',
    '3mo': '3 months', '6mo': '6 months', '1y': '1 year',
    '2y': '2 years', '5y': '5 years', '10y': '10 years',
    'max': 'All time'
}

# these are the options for the button group on the crypto insights
# make sure it matches timeframe_full_name options
time_frame_options = [
    {"label": "5 days", "value": '5d'},
    {"label": "1 month", "value": '1mo'},
    {"label": "6 months", "value": '6mo'},
    {"label": "1 year", "value": '1y'},
    {"label": "Full", "value": 'max'}
]

####################
# market overview variables
####################

mkt_over_info = {
    # THIS IS THE CORRECT API KEY
    # 'api_key': '{d4462bd4925c7c2d3d2adad9221d5e897dd7178ddac5a0558f76c978df7bd8da}',
    'api_key': '{}',

    'api_link_top_ten':'https://min-api.cryptocompare.com/data/top/mktcapfull?limit=10&tsym=USD&api_key='
}