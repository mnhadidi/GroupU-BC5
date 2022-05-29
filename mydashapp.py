# -*- coding: utf-8 -*-

import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from pandas import to_datetime
from yfinance import download
from dash.dependencies import Input, Output

# import internal project libraries
from asset_ins_func import candlestick_fig_create, run_linear_regression
from asset_ins_func import create_pred_plot, create_kpi_div, get_pred_pric_tab_v2
from project_variables import project_colors, ticker_df
from asset_insight_layout import ind_coins_layout
from sidebar import sidebar
from market_over import market_over

# setup dash app and heroku server info
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
app.title = 'CryptoDash'
server = app.server

# get content
content = html.Div(children=[ind_coins_layout], id="page-content")
# content_market_over = html.Div(market_over, id='market_over')

# gets sidebar from sidebar.py
app.layout = html.Div([dcc.Location(id="url"), sidebar, content],
                      style={"background-color": project_colors['background']})


####################
# CALLBACKS
####################

# sidebar callback
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return content
    elif pathname == "/market":
        return html.Div(market_over, id='market_over')
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


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
    asset_picked = ticker_df.loc[ticker_df['text'] == coin_dropdown, 'yf'].iloc[0]

    # update data
    coin_df = download(tickers=asset_picked, period=data_radio, interval='1d')

    # get date last updated
    date = "Data last updated: " + to_datetime(str(coin_df.index.values[-1])).strftime("%b %d %Y")

    # update prediction
    orig_coin_df, prediction, dates = run_linear_regression(coin_df)

    # update graphs
    candlestick_fig = candlestick_fig_create(coin_df)
    prediction_fig = create_pred_plot(orig_coin_df, prediction, dates)

    pred_pric_tab = get_pred_pric_tab_v2(prediction, dates)

    # update kpis div
    kpi_div = create_kpi_div(data_radio, coin_df)

    return candlestick_fig, date, prediction_fig, kpi_div, pred_pric_tab


# deploy app
if __name__ == '__main__':
    app.run_server(debug=True)
