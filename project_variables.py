####################
# project variables
####################

project_colors = {
    'background':'#1A1A2E',
    'dark-blue':'#16213E',
    'navy-blue':'#0F3460',
    'pink':'#E94560',
    'white':'#FFFFFF',
    'red':'#F6465D',
    'green':'#0ECB81'
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

# get all coins in existence of mankind
import pandas as pd
coins_df = pd.read_csv('/assets/coin-list.csv')
coin_dict_v2 = coins_df.to_dict()

coin_dict = [
    {'label': "Cardano (ADA)", 'value': "ADA"},
    {'label': "Cosmos (ATOM)", 'value': "ATOM"},
    {'label': "Avalanche (AVAX)", 'value': "AVAX"},
    {'label': "Axie Infinity (AXS)", 'value': "AXS"},
    {'label': "Bitcoin (BTC)", 'value': "BTC"},
    {'label': "Ethereum (ETH)", 'value': "ETH"},
    {'label': "Chainlink (LINK)", 'value': "LINK"},
    {'label': "Terra (LUNA1)", 'value': "LUNA1"},
    {'label': "Polygon (MATIC)", 'value': "MATIC"},
    {'label': "Solana (SOL)", 'value': "SOL"},
    {'label': "Binance Coin (BNB)", 'value': "BNB"},
    {'label': "Polkadot (DOT)", 'value': "DOT"},
    {'label': "Lido stETH (STETH)", 'value': "STETH"}
]

timeframe_tranf = {
    '1d': 1, '5d': 5, '1mo': 30
    , '3mo': 90, '6mo': 180, '1y': 365
    , '2y': 730, '5y': 1825, '10y': 3650
    , 'max': 9999999}



timeframe_full_name = {
    '1d': '1 day', '5d': '5 days', '1mo': '1 month'
    , '3mo': '3 months', '6mo': '6 months', '1y': '1 year'
    , '2y': '2 years', '5y': '5 years', '10y': '10 years'
    , 'max': 'All time'
}

start_info = {
    # make sure the coin name is one of the 'values' of coin_dict
    'coin':'ADA',
    # this is the selected intial timeframe for the crypto insights dash
    'time':'1y',
    # this is the time between data gathered from yfinance, started with 1d
    'interval':'1d'
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