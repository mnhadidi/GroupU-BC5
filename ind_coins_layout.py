import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from pandas import to_datetime
from yfinance import download
from dash.dependencies import Input, Output
from sidebar import sidebar

# import internal project libraries
from project_functions import candlestick_fig_create, run_linear_regression, create_pred_plot
from project_functions import func_currency_dropdown, create_kpi_div, get_pred_pric_tab, func_button_group
from project_variables import coin_dict, project_colors, CONTENT_STYLE
from project_variables import start_info as si


####################
# DATA
####################

# initializing coin
coin = si['coin']

# initializing coin df
coin_df = download(tickers=(coin + '-USD'), period=si['time'], interval=si['interval'])

# get date last updated
date = "Data last updated: " + to_datetime(str(coin_df.index.values[-1])).strftime("%b %d %Y, %H:%M")


####################
# VISUALS
####################

# create currency dropdown
currency_dropdown = func_currency_dropdown(coin_dict, coin)

# create button group for date period
button_group = func_button_group()

# create KPI div
kpi_div = create_kpi_div('1y', coin_df)

# create candlestick graph
candlestick_fig = candlestick_fig_create(coin_df)

# linear regression plot
coin_df_new, prediction, future_set, coin_df_for_plot = run_linear_regression(coin_df, coin_df)
prediction_fig = create_pred_plot(coin_df_for_plot, prediction, future_set, '1y')
pred_pric_tab = get_pred_pric_tab(future_set)


####################
# FINAL LAYOUT
####################

ind_coins_layout = html.Div([

    dbc.Container([
        html.Div([
            dbc.Row([
                dbc.Col(html.Img(src='', id='symbol'), width=1),
                dbc.Col(currency_dropdown, width=4),

                dbc.Col(
                    html.Div([
                        html.H5(date, id='date', style={'text-align': 'right', 'padding-right': '16px','color':'white'}),
                        button_group
                    ])
                    , width=7
                )]
                , style={'padding-top': '20px', 'padding-bottom': '20px'}, className='align-items-center')
        ]),

        html.Div(id='kpiDiv', children=[kpi_div], style={'padding-top': '40px'}),

        html.Div([
            html.H2('Price Analysis'),
            dcc.Graph(id='priceGraph', figure=candlestick_fig)
        ], style={'padding-top': '40px'}),

        html.Div([
            dbc.Row([
                dbc.Col(
                    html.Div([
                        html.H2('Historical and Predicted Values'),
                        dcc.Graph( id='PredictGraph', figure=prediction_fig),
                    ]), width=8
                ),

                dbc.Col(
                    html.Div([
                        html.H2('Next 10 Days Prediction'),
                        html.Div(children=[pred_pric_tab],id='table_pred')
                    ]), width=4
                )
            ])
        ] , style={'padding-top': '40px'})
    ]),


], style=CONTENT_STYLE
)