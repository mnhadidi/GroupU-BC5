import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import datetime
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json
import requests
from bs4 import BeautifulSoup
import requests
import time
import yfinance as yf
import plotly.graph_objs as go
from dash.dependencies import Input, Output

# setup dash app and heroku server info
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

####################
# setup variables
####################
colors = {
    'background': '#8ecae6',
    'text': '#023047',
    'yellow': '#ffb703',
    'orange': '#fb8500',
    'accent_blue': '#219ebc'
}

coin_dict = [
    {'label':"Cardano (ADA)", 'value':"ADA"},
    {'label':"Cosmos (ATOM)", 'value':"ATOM"},
    {'label':"Avalanche (AVAX)", 'value':"AVAX"},
    {'label':"Axie Infinity (AXS)", 'value':"AXS"},
    {'label':"Bitcoin (BTC)", 'value':"BTC"},
    {'label':"Ethereum (ETH)", 'value':"ETH"},
    {'label':"Chainlink (LINK)", 'value':"LINK"},
    {'label':"Terra (LUNA1)", 'value':"LUNA1"},
    {'label':"Polygon (MATIC)", 'value':"MATIC"},
    {'label':"Solana (SOL)", 'value':"SOL"}
]

coin = coin_dict[0]['value']



####################
# data setup
####################

coin_df = yf.download(tickers=(coin + '-USD'), period='1y', interval='1d')

# get date last updated
date = "Data last updated: " + pd.to_datetime(str(coin_df.index.values[-1])).strftime("%b %d %Y, %H:%M")

####################
# visuals
####################

def candlestick_fig_create(coin_df, coin_name):

    candlesthtick_fig = go.Figure(data=[go.Candlestick(x=coin_df.index.values,
                                                           open=coin_df["Open"],
                                                           high=coin_df["High"],
                                                           low=coin_df["Low"],
                                                           close=coin_df["Close"])])

    candlesthtick_fig = candlesthtick_fig.update_layout(title=coin_name + " Price Analysis",
                                                        xaxis_rangeslider_visible=False)

    return candlesthtick_fig


# initializing graphs

candlesthtick_fig = candlestick_fig_create(coin_df, coin)

####################
# create layout
####################

row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(html.Div("One of two columns"), width=10),
                dbc.Col(html.Div("One of two columns"), width=2),
            ]
        ),
    ]
)



app.layout = html.Div([


    html.Div([
            dbc.Row([
                dbc.Col(html.Div([
                    html.Label(['Currency']),
                    dcc.Dropdown(
                        id='my_dropdown',
                        options=coin_dict,
                        value=coin,
                        multi=False,
                        clearable=False,
                        style={"width": "50%"}
                    ),
                ])
                , width=9),

                dbc.Col(html.H5(date,id='date',className='text-right'), width=3)
            ]),
    ]),

    html.Div([
        dcc.Graph(
            id='Graph1',
            figure=candlesthtick_fig
        )
    ])
],

style = {'padding' : '5%'})


####################
# app callback
####################
@app.callback(
    [Output(component_id='Graph1', component_property='figure'),
     Output(component_id='date', component_property='children')],
    [Input(component_id='my_dropdown', component_property='value')]
)
def update_graph(my_dropdown):
    coin_df = yf.download(tickers=(my_dropdown + '-USD'), period='1y', interval='1d')
    # get date last updated

    date = "Data last updated: " + pd.to_datetime(str(coin_df.index.values[-1])).strftime("%b %d %Y, %H:%M")

    candlesthtick_fig = candlestick_fig_create(coin_df, my_dropdown)

    return (candlesthtick_fig,date)


if __name__ == '__main__':
    app.run_server(debug=True)
