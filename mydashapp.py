import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import datetime
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from xgboost.sklearn import XGBRegressor
from itertools import cycle
import plotly.express as px
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

coin = coin_dict[0]['value']

####################
# data setup
####################

coin_df = yf.download(tickers=(coin + '-USD'), period='1y', interval='1d')

# get date last updated
date = "Data last updated: " + pd.to_datetime(str(coin_df.index.values[-1])).strftime("%b %d %Y, %H:%M")


####################
# XGBOOST MODEL
####################

# function to create model and plot train and test data
def prep_data(coin, coindf):
    # reset index
    coindf = coindf.reset_index()
    # shape of close dataframe of coin
    closedf = coindf[['Date', 'Close']]
    # total data for prediction
    closedf = closedf[closedf['Date'] > '2020-01-01']
    close_stock = closedf.copy()
    # delete date
    del closedf['Date']
    # scaling data
    scaler = MinMaxScaler(feature_range=(0, 1))
    closedf = scaler.fit_transform(np.array(closedf).reshape(-1, 1))
    # training data
    training_size = int(len(closedf) * 0.70)
    train_data, test_data = closedf[0:training_size, :], closedf[training_size:len(closedf), :1]

    return train_data, test_data, scaler, closedf, close_stock


# convert an array of values into a dataset matrix
def create_dataset(dataset, time_step=1):
    dataX, dataY = [], []
    for i in range(len(dataset) - time_step - 1):
        a = dataset[i:(i + time_step), 0]
        dataX.append(a)
        dataY.append(dataset[i + time_step, 0])
    return np.array(dataX), np.array(dataY)


# function to create model
def original_vs_test(train_data, test_data, scaler, closedf, close_stock, coin):
    # get train and test data
    time_step = 21
    X_train_xg, y_train_xg = create_dataset(train_data, time_step)

    # fit model
    my_model = XGBRegressor(colsample_bytree=0.7, learning_rate=0.1, max_depth=3, n_estimators=1000)
    my_model.fit(X_train_xg, y_train_xg, verbose=False)

    return test_data, closedf, time_step, my_model


# function to compare last 20 days vs next 10 days
def compare_last20d_to10d(test_data, closedf, time_step, my_model, scaler):
    x_input = test_data[len(test_data) - time_step:].reshape(1, -1)
    temp_input = list(x_input)
    temp_input = temp_input[0].tolist()

    lst_output = []
    i = 0
    pred_days = 10
    while (i < pred_days):

        if (len(temp_input) > time_step):
            x_input = np.array(temp_input[1:])
            x_input = x_input.reshape(1, -1)
            yhat = my_model.predict(x_input)
            temp_input.extend(yhat.tolist())
            temp_input = temp_input[1:]
            lst_output.extend(yhat.tolist())
            i = i + 1

        else:
            yhat = my_model.predict(x_input)

            temp_input.extend(yhat.tolist())
            lst_output.extend(yhat.tolist())

            i = i + 1

    # get last days and prediction days
    last_days = np.arange(1, time_step + 1)

    # plot graph
    temp_mat = np.empty((len(last_days) + pred_days + 1, 1))
    temp_mat[:] = np.nan
    temp_mat = temp_mat.reshape(1, -1).tolist()[0]

    last_original_days_value = temp_mat
    next_predicted_days_value = temp_mat

    last_original_days_value[0:time_step + 1] = \
        scaler.inverse_transform(closedf[len(closedf) - time_step:]).reshape(1, -1).tolist()[0]
    next_predicted_days_value[time_step + 1:] = \
        scaler.inverse_transform(np.array(lst_output).reshape(-1, 1)).reshape(1, -1).tolist()[0]

    return lst_output, my_model


# function to plot whole closing price with prediction
def plot_whole_price_w_predict(closedf, lst_output, my_model, scaler, coin):
    my_model = closedf.tolist()
    my_model.extend((np.array(lst_output).reshape(-1, 1)).tolist())
    my_model = scaler.inverse_transform(my_model).reshape(1, -1).tolist()[0]

    names = cycle(['Close Price'])

    graph_title = coin + ' Plotting whole closing price with prediction'

    fig = px.line(my_model, labels={'value': 'Close price', 'index': 'Timestamp'})
    fig.update_layout(title_text=graph_title,
                      plot_bgcolor='white', font_size=15, font_color='black', legend_title_text='Stock')
    fig.for_each_trace(lambda t: t.update(name=next(names)))
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)

    return fig


# combine all previous functions
def get_coin_pred_plots(coin, coin_df):
    train_data, test_data, scaler, closedf, close_stock = prep_data(coin, coin_df)
    test_data, closedf, time_step, my_model = original_vs_test(train_data, test_data, scaler, closedf, close_stock,
                                                               coin)
    lst_output, my_model = compare_last20d_to10d(test_data, closedf, time_step, my_model, scaler)
    fig = plot_whole_price_w_predict(closedf, lst_output, my_model, scaler, coin)
    return fig


####################
# visuals
####################
prediction_plot = get_coin_pred_plots(coin, coin_df)

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Github", href="https://github.com/mnhadidi/GroupU-BC5")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("More pages", header=True),
                dbc.DropdownMenuItem("Page 2", href="#"),
                dbc.DropdownMenuItem("Page 3", href="#"),
            ],
            nav=True,
            in_navbar=True,
            label="More",
        ),
    ],
    brand="Cryptocurrency Dashboard",
    brand_href="#",
    color="primary",
    dark=True,
)

button_group = html.Div(
    [
        dbc.RadioItems(
            id="radios",
            className="btn-group",
            inputClassName="btn-check",
            labelClassName="btn btn-outline-primary",
            labelCheckedClassName="active",
            options=[
                {"label": "5 days", "value": '5d'},
                {"label": "1 month", "value": '1mo'},
                {"label": "6 months", "value": '6mo'},
                {"label": "1 year", "value": '1y'},
                {"label": "Full", "value": 'max'},
                # acceptable periods
                # “1d”, “5d”, “1mo”, “3mo”, “6mo”, “1y”, “2y”, “5y”, “10y”, “ytd”, “max”
            ],
            value='1y',
        ),
    ],
    className="radio-group",
)


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

app.layout = html.Div([

    navbar,

    html.Div([

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

                dbc.Col(html.H5(date, id='date', className='text-right'), width=3)
            ]),
        ]),

        button_group,

        html.Div([
            dcc.Graph(
                id='Graph1',
                figure=candlesthtick_fig
            )
        ]),

        html.Div([
            dcc.Graph(
                id='PredictGraph',
                figure=prediction_plot
            )
        ])
    ],
        style={'width': '80%', 'margin': 'auto'
               # 'padding-left': 'var(--bs-gutter-x,.75rem)', 'padding-right': 'var(--bs-gutter-x,.75rem)'
            , 'padding-top': '20px', 'padding-bottom': '20px'
               }),

],

)


####################
# app callback
####################
@app.callback(
    [Output(component_id='Graph1', component_property='figure'),
     Output(component_id='date', component_property='children')],
    [Input(component_id='my_dropdown', component_property='value'),
     Input(component_id="radios", component_property="value")]
)
def update_dashboard(my_dropdown, radios):
    coin_df = yf.download(tickers=(my_dropdown + '-USD'), period=radios, interval='1d')

    # get date last updated

    date = "Data last updated: " + pd.to_datetime(str(coin_df.index.values[-1])).strftime("%b %d %Y, %H:%M")

    candlesthtick_fig = candlestick_fig_create(coin_df, my_dropdown)

    return candlesthtick_fig, date


if __name__ == '__main__':
    app.run_server(debug=True)