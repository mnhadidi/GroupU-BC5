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
    'green': '#0ECB81',
    'gold':'goldenrod'
}

# content style for right side of dashboard
CONTENT_STYLE = {
    "margin-left": "17rem",
    "margin-right": "0",
    "padding": "1rem 1rem",
}


####################
# asset insight variables
####################
# information to initialize asset insight layout
start_info = {
    # asset ticker
    'asset': 'BTC-USD',
    # this is the selected initial timeframe for the insights dash
    'time': '1y',
    # this is the time between data gathered from yfinance, started with 1d
    'interval': '1d'
}

# get all tickers
def cleanup_ticker_info():
    stock_list = pd.read_csv("data/stock-full-list.csv")
    coin_list = pd.read_csv("data/coin-full-list.csv")

    #add stock to type
    stock_list['type'] = 'stock'
    # add text for dropdown
    stock_list['text'] = stock_list.apply(lambda x: '[ST] ' + x['Name'] + ' (' + x['Symbol'] + ')', axis=1)
    stock_list['yf'] = stock_list.apply(lambda x: x['Symbol'], axis=1)
    # add coin to type
    coin_list['type'] = 'coin'
    # rename column to match stock csv
    coin_list = coin_list.rename(columns={"Coin": "Symbol"})
    # add text for dropdown
    coin_list['text'] = coin_list.apply(lambda x: x['Name'], axis=1)
    coin_list['yf'] = coin_list.apply(lambda x: x['Symbol'] + '-USD', axis=1)
    # join the two tables
    # full_coin_stock_list = stock_list.append(coin_list, ignore_index=True)
    full_coin_stock_list = pd.concat([stock_list, coin_list], axis=0, ignore_index=True)
    full_coin_stock_list = full_coin_stock_list.sort_values(by=['Symbol'], ignore_index=True)

    return full_coin_stock_list

ticker_df = cleanup_ticker_info()

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

# these are the options for the button group on the asset insights
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
    # THESE ARE THE CORRECT AVALUES
    # 'api_key': '{d4462bd4925c7c2d3d2adad9221d5e897dd7178ddac5a0558f76c978df7bd8da}',
    # 'api_link_top_ten':'https://min-api.cryptocompare.com/data/top/mktcapfull?limit=10&tsym=USD&api_key='

    'api_key': '{}',
    'api_link_top_ten':''
}