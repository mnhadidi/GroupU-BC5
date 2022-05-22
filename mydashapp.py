import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from pandas import to_datetime
from yfinance import download
from dash.dependencies import Input, Output

# import internal project libraries
from project_functions import candlestick_fig_create, run_linear_regression, create_pred_plot,create_kpi_div,get_pred_pric_tab
from project_variables import coin_dict

# setup dash app and heroku server info
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = 'CryptoDash'
server = app.server

# initializing coin
coin = coin_dict[0]['value']

# initializing coin df
coin_df = download(tickers=(coin + '-USD'), period='1y', interval='1d')

# get date last updated
date = "Data last updated: " + to_datetime(str(coin_df.index.values[-1])).strftime("%b %d %Y, %H:%M")

####################
# visuals
####################

# nav bar
navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src='/assets/logo.png', height="30px")),
                        dbc.Col(dbc.NavbarBrand("CryptoDash", className="ms-2")),
                    ],
                    align="left",
                    className="g-0",
                ),
                href="#",
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.NavItem(dbc.NavLink("Github", href="https://github.com/mnhadidi/GroupU-BC5"))
        ]
    ),

)

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

####################
# create layout
####################

app.layout = html.Div([

    navbar,

    dbc.Container([
        html.Div([
            dbc.Row([
                dbc.Col(html.Img(src='/assets/BTC.png', id='symbol'), width=1),
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
            dcc.Graph(id='Graph1', figure=candlestick_fig)
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
                        html.H2('NEext 5 day prediction'),
                        dcc.Graph( id='PredictTable', figure=pred_pric_tab),
                    ]), width=4
                )

            ])



        ] , style={'padding-top': '40px'})
    ]),

    html.Footer([
        html.Div([
            html.H5('made with 🧡 and 🍕 by Group U', style={'text-align': 'center', 'font-size': '12pt'}),
            html.H5('Beatriz Ferreira | Beatriz Peres | Diogo Marques | Miriam Hadidi Pereira'
                    , style={'text-align': 'center', 'font-size': '8pt', 'color': '#808080'})
        ], style={'padding': '20px', 'padding-top': '20px', 'backgroundColor': '#F5F5F5', 'margin-top': '10px'})
    ])
])

####################
# app callback
####################
@app.callback(
    [Output(component_id='Graph1', component_property='figure'),
     Output(component_id='date', component_property='children'),
     Output(component_id='PredictGraph', component_property='figure'),
     Output(component_id='kpiDiv', component_property='children')],
    [Input(component_id='coin_dropdown', component_property='value'),
     Input(component_id="data_radio", component_property="value")]
)
def update_dashboard(coin_dropdown, data_radio):
    # update data
    coin_df = download(tickers=(coin_dropdown + '-USD'), period=data_radio, interval='1d')
    prediction_coin_df = download(tickers=(coin_dropdown + '-USD'), period='1y', interval='1d')

    # get date last updated
    date = "Data last updated: " + to_datetime(str(coin_df.index.values[-1])).strftime("%b %d %Y, %H:%M")

    # update prediction
    coin_df_new, prediction, future_set, coin_df_for_plot = run_linear_regression(prediction_coin_df, coin_df)

    # update graphs
    candlestick_fig = candlestick_fig_create(coin_df)
    prediction_fig = create_pred_plot(coin_df_for_plot, prediction, future_set, data_radio)

    # update kpis div
    kpi_div = create_kpi_div(data_radio, coin_df)

    return candlestick_fig, date, prediction_fig, kpi_div

@app.callback(Output(component_id='symbol', component_property='src')
    ,Input(component_id='coin_dropdown', component_property='value'))

def update_coin_image(coin_dropdown):
    new_src = "/assets/" + coin_dropdown + '.png'
    return new_src

if __name__ == '__main__':
    app.run_server(debug=True)