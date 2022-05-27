import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from pandas import to_datetime
from yfinance import download
from dash.dependencies import Input, Output
import requests

# import internal project libraries
from project_functions import candlestick_fig_create, run_linear_regression, create_pred_plot, create_kpi_div, \
    get_pred_pric_tab
from project_variables import project_colors, coin_dict_v2
from project_variables import start_info as si
from ind_coins_layout import ind_coins_layout
from sidebar import sidebar
from market_over import market_over

# setup dash app and heroku server info
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
app.title = 'CryptoDash'
server = app.server

# get content
content = html.Div(ind_coins_layout, id="page-content")
content_market_over = html.Div(market_over, id='market_over')

# gets sidebar from sidebar.py
app.layout = html.Div([dcc.Location(id="url"), sidebar, content],
                      style={"background-color": project_colors['background']})


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
        return content_market_over
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
    orig_coin_df, prediction, dates = run_linear_regression(coin_df)

    # update graphs
    candlestick_fig = candlestick_fig_create(coin_df)
    prediction_fig = create_pred_plot(orig_coin_df, prediction, dates)

    pred_pric_tab = get_pred_pric_tab(prediction, dates)

    # update kpis div
    kpi_div = create_kpi_div(data_radio, coin_df)

    return candlestick_fig, date, prediction_fig, kpi_div, pred_pric_tab


# coin image call back
@app.callback(Output(component_id='symbol', component_property='src')
    , Input(component_id='coin_dropdown', component_property='value'))
def update_coin_image(coin_dropdown):
    long_form = coin_dict_v2[coin_dropdown]
    url_begin = 'https://cryptologos.cc/logos/'
    url_end = '-logo.png?v=022'
    long_form = long_form.lower().replace("(", "").replace(")", "").replace(" ", "-")
    full_url = url_begin + long_form + url_end

    r = requests.get(full_url)
    if 200 <= r.status_code <= 299:
        return full_url
    else:
        return '/assets/other.png'


if __name__ == '__main__':
    app.run_server(debug=True)
