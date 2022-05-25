import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from pandas import to_datetime
from yfinance import download
from dash.dependencies import Input, Output


# import internal project libraries
from project_functions import candlestick_fig_create, run_linear_regression, create_pred_plot,create_kpi_div,get_pred_pric_tab
from project_variables import coin_dict,project_colors
from project_variables import start_info as si
from ind_coins_layout import ind_coins_layout
from sidebar import sidebar

# get all coins in existence of mankind
import pandas as pd
coins_df = pd.read_csv('/assets/coin-list.csv')
coin_dict_v2 = coins_df.to_dict()



# setup dash app and heroku server info
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
app.title = 'CryptoDash'
server = app.server

# get content
content = html.Div(ind_coins_layout, id="page-content")

# gets sidebar from sidebar.py
app.layout = html.Div([dcc.Location(id="url"), sidebar,content],style={"background-color": project_colors['background']})


####################
# CALLBACKS
####################


############################################################################################################################################
# this sidebar doesn't look correct, double check before continuing
############################################################################################################################################

# sidebar callback
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return content
    elif pathname == "/market":
        return html.P("This is the content of page 1. Yay!")
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )

############################################################################################################################################
############################################################################################################################################

# app callback
@app.callback(
    [Output(component_id='priceGraph', component_property='figure'),
     Output(component_id='date', component_property='children'),
     Output(component_id='PredictGraph', component_property='figure'),
     Output(component_id='kpiDiv', component_property='children'),
     Output(component_id='table_pred', component_property='children')],
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

    pred_table = get_pred_pric_tab(future_set)

    # update kpis div
    kpi_div = create_kpi_div(data_radio, coin_df)

    return candlestick_fig, date, prediction_fig, kpi_div, pred_table

# coin image call back
@app.callback(Output(component_id='symbol', component_property='src')
    ,Input(component_id='coin_dropdown', component_property='value'))
def update_coin_image(coin_dropdown):
    new_src = "/assets/" + coin_dropdown + '.png'
    return new_src

if __name__ == '__main__':
    app.run_server(debug=True)