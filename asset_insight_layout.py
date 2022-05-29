# import external libraries
from dash import html, dcc
import dash_bootstrap_components as dbc
from pandas import to_datetime
from yfinance import download

# import internal project libraries
from asset_ins_func import candlestick_fig_create, run_linear_regression, create_pred_plot
from asset_ins_func import func_currency_dropdown, create_kpi_div, get_pred_pric_tab_v2, func_button_group
from project_variables import CONTENT_STYLE,project_colors, CONTAINER_STYLE
from project_variables import start_info as si, ticker_df


####################
# DATA
####################

# initializing coin
asset = si['asset']

# initializing coin df
coin_df = download(tickers=(asset), period=si['time'], interval=si['interval'])

# get date last updated
date = "Data last updated: " + to_datetime(str(coin_df.index.values[-1])).strftime("%b %d %Y")

####################
# VISUALS
####################

# create currency dropdown
currency_dropdown = func_currency_dropdown(ticker_df['text'],ticker_df.loc[ticker_df['yf'] == asset, 'Name'].iloc[0])

# create button group for date period
button_group = func_button_group()

# create KPI div
kpi_div = create_kpi_div('1y', coin_df)

# create candlestick graph
candlestick_fig = candlestick_fig_create(coin_df)

# linear regression plot
orig_coin_df, prediction, dates = run_linear_regression(coin_df)
prediction_fig = create_pred_plot(orig_coin_df, prediction, dates)
pred_pric_tab = get_pred_pric_tab_v2(prediction, dates)

####################
# FINAL LAYOUT
####################

ind_coins_layout = html.Div([

    dbc.Container([
        dbc.Container([
            html.H1('Asset Insights', style={'color':project_colors['white'],'font-weight': 'bold'})
        ], style=CONTAINER_STYLE),


        dbc.Container([
            dbc.Row([
                dbc.Col(currency_dropdown, width=5),
                dbc.Col(
                    html.Div([
                        html.H6(date, id='date', style={'text-align': 'right',
                                                        'padding-right': '16px',
                                                        'color': 'white'}),
                        button_group
                    ]),
                    width=7
                )], className='align-items-center')
        ], style=CONTAINER_STYLE),

        dbc.Container(id='kpiDiv', children=[kpi_div], style=CONTAINER_STYLE),

        dbc.Container([
            html.H2('Price Analysis'),
            dcc.Graph(id='priceGraph', figure=candlestick_fig)
        ], style=CONTAINER_STYLE),

        dbc.Container([
            dbc.Row([
                dbc.Col(
                    dbc.Container([
                        html.H2('Historical and Predicted Values'),
                        dcc.Graph(id='PredictGraph', figure=prediction_fig),
                    ], style=CONTAINER_STYLE),
                    width=8
                ),

                dbc.Col(
                    dbc.Container([
                        html.H2('Next 10 Days Prediction'),
                        html.Div(children=[pred_pric_tab], id='table_pred')
                    ], style=CONTAINER_STYLE),
                    width=4
                )
            ])
        ], style=CONTAINER_STYLE)
    ], style=CONTAINER_STYLE),


], style=CONTENT_STYLE
)
