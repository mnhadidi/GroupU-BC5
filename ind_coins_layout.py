import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from pandas import to_datetime
from yfinance import download
from dash.dependencies import Input, Output
from sidebar import sidebar

# import internal project libraries
from project_functions import candlestick_fig_create, run_linear_regression, create_pred_plot,create_kpi_div,get_pred_pric_tab
from project_variables import coin_dict

# initializing coin
coin = coin_dict[0]['value']

# initializing coin df
coin_df = download(tickers=(coin + '-USD'), period='1y', interval='1d')

# get date last updated
date = "Data last updated: " + to_datetime(str(coin_df.index.values[-1])).strftime("%b %d %Y, %H:%M")


####################
# visuals
####################

# currency dropdown

currency_dropdown = html.Div([
                        html.Label(['Currency']),
                        dcc.Dropdown(
                            id='coin_dropdown',
                            options=coin_dict,
                            value=coin,
                            multi=False,
                            clearable=False,
                            style={"min-width": "1rem"}
                        ),
                    ])
# buttons for date period
button_group = html.Div(
    [
        dbc.RadioItems(
            id="data_radio",
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
    style={'text-align': 'right', 'padding-right': '16px'}
)

# create KPI div
kpi_div = create_kpi_div('1y', coin_df)

# create candlestick graphs
candlestick_fig = candlestick_fig_create(coin_df)

# linear regression plot
coin_df_new, prediction, future_set, coin_df_for_plot = run_linear_regression(coin_df, coin_df)
prediction_fig = create_pred_plot(coin_df_for_plot, prediction, future_set, '1y')
pred_pric_tab = get_pred_pric_tab(future_set)

# add some padding.
CONTENT_STYLE = {
    "margin-left": "17rem",
    "margin-right": "0",
    "padding": "1rem 1rem",
}

# layout for main dash app
ind_coins_layout = html.Div([

    dbc.Container([
        html.Div([
            dbc.Row([
                dbc.Col(html.Img(src='', id='symbol'), width=1),
                dbc.Col(currency_dropdown, width=4),

                dbc.Col(
                    html.Div([
                        html.H5(date, id='date', style={'text-align': 'right', 'padding-right': '16px'}),
                        button_group
                    ])
                    , width=7
                )]
                , style={'padding-top': '20px', 'padding-bottom': '20px'})
        ]),

        html.Div(id='kpiDiv', children=[kpi_div]),

        html.Div([
            html.H2('Price Analysis'),
            dcc.Graph(id='Graph1') #, figure=candlestick_fig
        ] , style={'padding-top': '20px'}),

        html.Div([
            dbc.Row([
                dbc.Col(
                    html.Div([
                        html.H2('Plotting whole closing price with prediction'),
                        dcc.Graph( id='PredictGraph', figure=prediction_fig),
                    ]), width=8
                ),

                dbc.Col(
                    html.Div([
                        html.H2('Next 5 day prediction'),
                        dcc.Graph( id='PredictTable', figure=pred_pric_tab),
                    ]), width=4
                )

            ])



        ] , style={'padding-top': '40px'})
    ]),


], style=CONTENT_STYLE
)