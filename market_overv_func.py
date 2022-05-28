import requests
import plotly.graph_objs as go
import json
import yfinance
import pandas as pd

from project_variables import mkt_over_info, project_colors

##########################
# API CALL DEF
# used on market_over
##########################
def get_top_ten_API_call():
    try:
        print('Started API call')
        resp = requests.get(mkt_over_info['api_link_top_ten'] + mkt_over_info['api_key'])
        resp = resp.json()
        print('get_top_ten_API_call called API successfully')

    except:
        f = open('data/crypto_data_backup.json')
        resp = json.load(f)
        print('get_top_ten_API_call error out on API call, getting data locally')

    # get json from query
    return resp

##########################
# TOP TEN COINS MARKET CAP
# used on market_over
##########################
def create_top_ten_coins_chart(resp):
    coin_name = []
    coin_cap = []

    for i in range(0, 10):
        coin_name.append(resp['Data'][i]['CoinInfo']['FullName'])
        coin_cap.append(resp['Data'][i]['RAW']['USD']['MKTCAP'])

    coin_name_sort = [coin_name for _, coin_name in sorted(zip(coin_cap, coin_name))]
    coin_cap_sort = sorted(coin_cap)
    formatted_cap = ['${:,.1f}B'.format(member / 1000000000) for member in coin_cap_sort]

    fig = go.Figure(data=go.Bar(
        x=coin_cap_sort,
        y=coin_name_sort,
        text=formatted_cap,
        orientation='h',
        marker_color=project_colors['gold'],
        marker_line_color="rgba(0,0,0,0)",
        textfont_color="#fff"
    ))

    fig.update_layout(xaxis_visible=False,
                      xaxis_showticklabels=False,
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)',
                      margin={'t': 20, 'l': 20, 'r': 30, 'b': 20}
                      )

    fig.update_traces(textposition='outside',cliponaxis=False)
    return fig


##########################
# CRYPTO STOCK SIMULATION PLOT
# used on market_over
##########################
def get_simulation_plot():
    #### CLEANUP DATA
    # get full data from yahoo finance
    s_p = yfinance.Ticker("^GSPC")
    crypto_index = yfinance.Ticker("^CMC200")
    # get historical data for 1y
    hist_sp = s_p.history(period="1y")
    hist_crypto = crypto_index.history(period="1y")
    # reset index to get date as column
    hist_sp = hist_sp.reset_index()
    hist_crypto = hist_crypto.reset_index()
    # setup column names for plot df
    column_names = ["Date", "CloseCrypto", "CloseStock", 'InvestCryptoVal', 'InvestStockVal']
    # create plot df
    df_plot = pd.DataFrame(columns=column_names)
    # populate date, stock and crypto prices
    df_plot = df_plot.assign(Date=hist_crypto['Date'], CloseCrypto=hist_crypto['Close'], CloseStock=hist_sp['Close'])
    # remove empties of last 2 rows
    df_plot = df_plot[0:-2]
    # getting percent change day to day
    df_plot['InvestCryptoChang'] = df_plot['CloseCrypto'].pct_change() + 1
    df_plot['InvestStockChang'] = df_plot['CloseStock'].pct_change() + 1
    # initializing the investment with $1000
    df_plot.loc[0:0, ('InvestCryptoVal', 'InvestBondVal', 'InvestStockVal')] = 1000
    # calculate how much that 1000 would change day to day
    for i in range(1, len(df_plot)):
        df_plot.loc[i, 'InvestCryptoVal'] = df_plot.loc[i - 1, 'InvestCryptoVal'] * df_plot.loc[i, 'InvestCryptoChang']
        df_plot.loc[i, 'InvestStockVal'] = df_plot.loc[i - 1, 'InvestStockVal'] * df_plot.loc[i, 'InvestStockChang']

    #### CREATE CHART
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_plot['Date'], y=df_plot['InvestCryptoVal'],
                             mode='lines',
                             name='Crypto Index (CMC Crypto 200)'))

    fig.add_trace(go.Scatter(x=df_plot['Date'], y=df_plot['InvestStockVal'],
                             mode='lines',
                             name='Stock Index (S&P 500)'))
    fig.add_hline(y=1000, opacity=0.5)
    fig.update_layout(
        margin={'t': 20, 'l': 20, 'r': 20, 'b': 20},
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )

    return fig, df_plot

##########################
# INDICATORS FOR SIMULATION
# used on market_over
##########################

def crypto_sim_ind(df_plot):
    value_sim = df_plot['InvestCryptoVal'].tail(1).tolist()[0]

    fig = go.Figure()

    fig.add_trace(go.Indicator(
        mode="number+delta",
        value=value_sim,
        number={'valueformat': "$,.0f", 'font': {'color': '#ffffff'}},
        # domain={'x': [0, 1], 'y': [0, 1]},
        delta={'reference': 1000, 'relative': True, 'valueformat': ".1%"}
    ))

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin={'t': 0, 'l': 0, 'r': 0, 'b': 0},

    )

    return fig


def stock_sim_ind(df_plot):
    value_sim = df_plot['InvestStockVal'].tail(1).tolist()[0]

    fig = go.Figure()

    fig.add_trace(go.Indicator(
        mode="number+delta",
        value=value_sim,
        number={'valueformat': "$,.0f", 'font': {'color': '#ffffff'}},
        # domain={'x': [0, 0.5], 'y': [0, 0.5]},
        delta={'reference': 1000, 'relative': True, 'valueformat': ".1%"}
    ))

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin={'t': 0, 'l': 0, 'r': 0, 'b': 0},
    )

    return fig