import requests
import plotly.graph_objs as go
import json
import yfinance
import pandas as pd
from dash import dash_table
from dash import html, dcc
import dash_bootstrap_components as dbc
from datetime import datetime

from project_variables import mkt_over_info, project_colors, ticker_df, ticker_df

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

##########################
# TOP TEN DATA TABLE DATA
# used on market_over
##########################
def get_top_ten_coins_data(resp):
    coin = []
    coin_name = []
    last_close_price = []
    thirty_day_prc_change = []
    one_day_prc_change = []
    bear_bull = []
    coin_image = []


    for line in resp['Data']:
        coin.append(line['CoinInfo']['Name'])
        coin_name.append(line['CoinInfo']['FullName'])
        long_form = ticker_df.loc[ticker_df['Symbol'] == line['CoinInfo']['Name'], 'Name'].iloc[0]

        # long_form = ticker_df['yf'][line['CoinInfo']['Name']]
        url_begin = 'https://cryptologos.cc/logos/'
        url_end = '-logo.png?v=022'
        long_form = long_form.lower().replace("(", "").replace(")", "").replace(" ", "-")
        full_url = url_begin + long_form + url_end

        r = requests.get(full_url)
        if 200 <= r.status_code <= 299:
            coin_image.append(full_url)
        else:
            coin_image.append('/assets/other.png')

    for ind_coin in coin:
        data = yfinance.download(ind_coin + "-USD", start="2022-04-27", end="2022-05-27")
        thirty_change = (data['Close'][-1] / data['Close'][0]) -1
        one_change = (data['Close'][-1] / data['Close'][-2]) -1

        thirty_day_prc_change.append(thirty_change)
        one_day_prc_change.append(one_change)

        last_close_price.append(data['Close'][-1])
        if one_change >= 0:
            bear_bull.append('bull')
        else:
            bear_bull.append('bear')


    column_names = ["Coin", "CoinName", 'LastClosePrice', 'ThirtyDayPrcChng','OneDayPrcChg', 'BearBull','CoinImage']
    # create plot df
    df_table = pd.DataFrame(columns=column_names)
    df_table = df_table.assign(Coin=coin, CoinName=coin_name, LastClosePrice=last_close_price,
                                ThirtyDayPrcChng=thirty_day_prc_change,OneDayPrcChg=one_day_prc_change,
                                BearBull=bear_bull, CoinImage=coin_image)

    return df_table

##########################
# TOP TEN DATA TABLE
# used on market_over
##########################

def get_top_coins_tbl(df_table):
    coin_image = df_table['CoinImage']
    coin_name = df_table['CoinName']
    last_close_price = df_table['LastClosePrice']
    one_day_change = df_table['OneDayPrcChg']
    bear_bull = df_table['BearBull']


    last_close_price_form = ['${:,.2f}'.format(member) for member in last_close_price]

    header = [
        html.H2('Bear vs Bull'),
        dbc.Row([
            dbc.Col(html.P('', style={'color': '#ffffff'}), width=1),
            dbc.Col(html.P('Coin', style={'color': project_colors['pink'],'font-weight': 'bold'}), width=4),
            dbc.Col(html.P('Last Close', style={'color': project_colors['pink'],'font-weight': 'bold','text-align':'right'}), width=4),
            dbc.Col(html.P('', style={'color': '#ffffff'}), width=2)
        ])]

    rows = []

    for i in range(0, 10):
        row = dbc.Row([
            dbc.Col(html.Img(src=coin_image[i],style={'width': '20px', 'height': '20px'}),
                    width= 1),
            dbc.Col(coin_name[i],
                    style={'color':'#ffffff'},
                    width= 4),
            dbc.Col(last_close_price_form[i],
                    style={'color':'#ffffff','text-align':'right'},
                    width= 5),
            dbc.Col(html.Img(src='assets/' + bear_bull[i] + '.png', style={'width': '20px', 'height': '20px'}),
                    width= 2)
        ])

        rows.append(row)

    header.extend(rows)

    table = dbc.Container(header,
                          style={"background-color": project_colors['dark-blue'],
                                         'padding-top':'10px','padding-bottom':'10px'})

    return table


def get_top_coins_tbl_v2(df_table):
    coin_image = df_table['CoinImage']
    coin_name = df_table['CoinName']
    last_close_price = df_table['LastClosePrice']
    bear_bull = df_table['BearBull']
    last_close_price_form = ['${:,.2f}'.format(member) for member in last_close_price]

    table_header = [
        html.Thead(html.Tr([html.Th("Coin"),
                            html.Th("Coin",style={'color':'#ffffff'}),
                            html.Th("Last Price",style={'color':'#ffffff'}),
                            html.Th("Bear")])
                   )
    ]

    rows = []

    for i in range(0,10):
        row = html.Tr([html.Td(html.Img(src=coin_image[i], style={'width': '20px', 'height': '20px'}), style={'width': '25px'}),
                        html.Td(coin_name[i], style={'color': '#ffffff'}),
                        html.Td(last_close_price_form[i], style={'color': '#ffffff'}),
                        html.Td(
                            html.Img(src='assets/' + bear_bull[i] + '.png', style={'width': '20px', 'height': '20px'})
                        )
                        ])

        rows.append(row)

    table_header.extend(rows)

    table = dbc.Table([html.Tbody(table_header)], bordered=False)

    return table


##########################
# GET STORIES
# used on market_over
##########################

def get_stories():
    response = requests.get("https://min-api.cryptocompare.com/data/v2/news/?lang=EN")
    response_json = response.json()
    return response_json['Data'][0:5]

def get_stories_card(response_stories):
    def create_card(story):
        news_story = dbc.Container([
            html.H5(story['title'],style={'color':'#ffffff'}),
            html.Div(html.H6('by: ' + story['source']),style={'float':'left'}),
            html.Div(html.H6('on: ' + datetime.utcfromtimestamp(story['published_on']).strftime('%Y-%m-%d %H:%M:%S')),
                     style={'float':'left','padding-left':'20px','padding-right':'20px'}),
            html.Div(dcc.Link("LINK", href=story['guid']))
        ], style={'margin-left':0,'padding-left':0})


        return news_story

    final_layout = dbc.Container([
        create_card(response_stories[0]),
        html.Hr(),
        create_card(response_stories[1]),
        html.Hr(),
        create_card(response_stories[2]),
        html.Hr(),
        create_card(response_stories[3]),
        html.Hr(),
        create_card(response_stories[4])
,
    ], style={'padding-left':0,'margin-bottom':'50px','margin-left':0})



    return final_layout