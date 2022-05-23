####################
# setup variables
####################
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