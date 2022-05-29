import requests
import plotly.graph_objs as go
import json
import yfinance
import pandas as pd
from dash import html, dcc
import dash_bootstrap_components as dbc
from datetime import datetime
import numpy as np

# internal libraries
from project_variables import mkt_over_info, project_colors, ticker_df, CONTAINER_STYLE

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
    fig.update_layout(title_font_color='#FFFFFF', font_color='#FFFFFF')

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
    # drop na
    hist_sp = hist_sp.dropna()
    hist_crypto = hist_crypto.dropna()
    # setup column names for plot df
    column_names = ["Date", "CloseCrypto", "CloseStock", 'InvestCryptoVal', 'InvestStockVal']
    # create plot df
    df_plot = pd.DataFrame(columns=column_names)
    # populate date, stock and crypto prices
    df_plot = df_plot.assign(Date=hist_crypto['Date'], CloseCrypto=hist_crypto['Close'], CloseStock=hist_sp['Close'])
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
    fig.add_trace(go.Scatter(x=df_plot['Date'],
                             y=df_plot['InvestCryptoVal'],
                             mode='lines',
                             name='Crypto Index (CMC Crypto 200)',
                             line_color=project_colors['gold']))

    fig.add_trace(go.Scatter(x=df_plot['Date'],
                             y=df_plot['InvestStockVal'],
                             mode='lines',
                             name='Stock Index (S&P 500)',
                             line_color=project_colors['bright-blue']))

    fig.add_hline(y=1000, opacity=1, line_color=project_colors['pink'])

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

    fig.update_layout(title_font_color='#FFFFFF', font_color='#FFFFFF')
    fig.update_xaxes(gridcolor='rgba(255,255,255,0.2)')
    fig.update_yaxes(gridcolor='rgba(255,255,255,0.2)')

    return fig, df_plot

##########################
# INDICATORS FOR SIMULATION
# used on market_over
##########################

def crypto_sim_ind(df_plot):
    value_sim = df_plot['InvestCryptoVal'].tail(1).tolist()[0]

    fig = go.Figure()
    decreasing={'color':project_colors['red']}
    increasing = {'color': project_colors['green']}

    fig.add_trace(go.Indicator(
        mode="number+delta",
        value=value_sim,
        number={'valueformat': "$,.0f", 'font': {'color': project_colors['gold']}},
        delta={'reference': 1000, 'relative': True, 'valueformat': ".1%", 'decreasing':decreasing, 'increasing': increasing}
    ))

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin={'t': 0, 'l': 0, 'r': 0, 'b': 0},

    )

    return fig


def stock_sim_ind(df_plot):
    value_sim = df_plot['InvestStockVal'].tail(1).tolist()[0]
    decreasing = {'color': project_colors['red']}
    increasing = {'color': project_colors['green']}

    fig = go.Figure()

    fig.add_trace(go.Indicator(
        mode="number+delta",
        value=value_sim,
        number={'valueformat': "$,.0f", 'font': {'color': project_colors['bright-blue']}},
        # domain={'x': [0, 0.5], 'y': [0, 0.5]},
        delta={'reference': 1000, 'relative': True, 'valueformat': ".1%", 'decreasing':decreasing, 'increasing': increasing}
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
    bear_bull = df_table['BearBull']
    last_close_price_form = ['${:,.2f}'.format(member) for member in last_close_price]

    table_header = [
        html.Tr([
            html.Th(""),
            html.Th("Coin",style={'color':'#ffffff'}),
            html.Th("Last Price",style={'color':'#ffffff','text-align':'right'}),
            html.Th("")
        ])
    ]

    rows = []

    for i in range(0,10):

        row = html.Tr([
            html.Td(html.Img(src=coin_image[i], style={'width': '20px', 'height': '20px'}), style={'width': '25px'}),
            html.Td(coin_name[i], style={'color': '#ffffff'}),
            html.Td(last_close_price_form[i], style={'color': '#ffffff','text-align':'right'}),
            html.Td(html.Img(src='assets/' + bear_bull[i] + '.png', style={'width': '20px', 'height': '20px'}))
        ])

        rows.append(row)

    table_header.extend(rows)

    table = dbc.Table([html.Tbody(table_header)], bordered=False, responsive=True, style={'border-bottom': '1px solid rgba(255,255,255,0.1)'})

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
            html.Div(html.H6(children=('by: ' + story['source']),
                             style={'color':'rgba(255,255,255,0.5)'}),
                     style={'float':'left'}),
            html.Div(html.H6(children=('on: ' + datetime.utcfromtimestamp(story['published_on']).strftime('%Y-%m-%d %H:%M:%S')),
                             style={'color':'rgba(255,255,255,0.5)'}),
                     style={'float':'left','padding-left':'20px','padding-right':'20px'}),
            html.Div(dcc.Link("LINK", href=story['guid']))
        ], style={'margin-left':0,'padding-left':0,'padding-right':0})

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

    ], style={'margin-bottom':'50px','margin-left':0, 'padding-right':0, 'padding-left':0})



    return final_layout

##########################
# FEAR AND GREED INDEX
# used on market_over
##########################

def get_fear_greed_gauge():
    response = requests.get("https://api.alternative.me/fng/?limit=1")
    response_json = response.json()
    fear_greed_index = response_json['data'][0]['value']

    plot_bgcolor = "rgba(0,0,0,0)"
    quadrant_colors = [plot_bgcolor, '#009900', '#39e600', '#77ff33',
                       '#ccff33', '#ffff00', '#ffcc00', '#ff9933', '#ff6600', '#ff0000']
    quadrant_text = ["", "Extreme Greed", "", "", "", "", "", "", "", "Extreme Fear"]
    n_quadrants = len(quadrant_colors) - 1

    current_value = float(fear_greed_index)
    min_value = 0
    max_value = 100
    hand_length = np.sqrt(2) / 4
    hand_angle = np.pi * (1 - (max(min_value, min(max_value, current_value)) - min_value) / (max_value - min_value))

    fig = go.Figure(
        data=[
            go.Pie(
                values=[0.5] + (np.ones(n_quadrants) / 2 / n_quadrants).tolist(),
                rotation=90,
                hole=0.5,
                marker_colors=quadrant_colors,
                text=quadrant_text,
                textinfo="text",
                hoverinfo="skip",
            ),
        ],
        layout=go.Layout(
            showlegend=False,
            margin=dict(b=0, t=10, l=10, r=10),
            # width=450,
            # height=450,
            paper_bgcolor=plot_bgcolor,
            annotations=[
                go.layout.Annotation(
                    text=f"<b>Fear & Greed Index</b><br>{current_value}",
                    x=0.5, xanchor="center", xref="paper",
                    y=0.25, yanchor="bottom", yref="paper",
                    showarrow=False, font=dict(size=20)
                )
            ],
            shapes=[
                go.layout.Shape(
                    type="circle",
                    x0=0.48, x1=0.52,
                    y0=0.48, y1=0.52,
                    fillcolor="#ffffff",
                    line_color="#ffffff",
                ),
                go.layout.Shape(
                    type="line",
                    x0=0.5, x1=0.5 + hand_length * np.cos(hand_angle),
                    y0=0.5, y1=0.5 + hand_length * np.sin(hand_angle),
                    line=dict(color="#ffffff", width=4)
                )
            ]
        )
    )

    fig.update_layout(title_font_color='#FFFFFF', font_color='#FFFFFF')

    return fig


##########################
# WORLD STOCK INDICES LINE CHARTS
# used on market_over
##########################

def get_data_indices():
    SP500 = yfinance.download(tickers=('^GSPC'), period='1y', interval='1d').reset_index()
    FTSE = yfinance.download(tickers=('^FTSE'), period='1y', interval='1d').reset_index()
    IBOVESPA = yfinance.download(tickers=('^BVSP'), period='1y', interval='1d').reset_index()
    Nikkei225 = yfinance.download(tickers=('^N225'), period='1y', interval='1d').reset_index()
    SSEComposite = yfinance.download(tickers=('000001.SS'), period='1y', interval='1d').reset_index()

    return SP500, FTSE, IBOVESPA, Nikkei225, SSEComposite

def get_index_plot(df, color):
    #### CREATE CHART
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Date'],
                             y=df['Close'],
                             mode='lines',
                             line_color=color))

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
        height=150
    )

    fig.update_layout(title_font_color='rgba(255,255,255,0.2)', font_color='rgba(255,255,255,0.2)')
    fig.update_xaxes(showgrid=False, visible=False)
    fig.update_yaxes(showgrid=False, visible=False)

    return fig


def get_index_row(exchange_name,currency, df, color):

    last_price = df['Close'].iloc[-1]
    day_change_pct = (last_price - df['Close'].iloc[-2]) / df['Close'].iloc[-2]

    last_price_str = '{:,.0f}'.format(last_price)
    day_change_pct_str = '{:+,.3f}%'.format(day_change_pct)

    if day_change_pct >= 0:
        color_change=project_colors['green']
    else:
        color_change = project_colors['red']

    content_list = [
        html.H4(exchange_name, style={'color': 'white'}),
        html.P(children=[currency], style={'color': 'rgba(255,255,255,0.5'}),

        dbc.Row([
            dbc.Col([html.H5(last_price_str, style={'color': project_colors['bright-blue'], 'margin-bottom':'2px'})]),
            dbc.Col([html.H5(day_change_pct_str, style={'color':color_change,'text-align':'right', 'margin-bottom':'2px'})]),
        ], style={'margin-bottom':0}),

        dbc.Row([
            dbc.Col([html.P(children=['Last price'], style={'color': 'rgba(255,255,255,0.5'})]),
            dbc.Col([html.P(children=['Day change'], style={'color': 'rgba(255,255,255,0.5', 'text-align': 'right'})]),
        ], style={'margin-top':'2px'}),

        dcc.Graph(figure=get_index_plot(df, color))
    ]

    return content_list


def get_row_of_index_plots():
    SP500, FTSE, IBOVESPA, Nikkei225, SSEComposite = get_data_indices()


    return_row = dbc.Container([
        dbc.Row([
            dbc.Col(get_index_row('S&P500', 'USD', SP500, project_colors['bright-blue']),
                    style={'padding':'20px 20px 0 20px','margin-right':'30px', "background-color": project_colors['dark-blue']}),
            dbc.Col(get_index_row('FTSE100', 'GBP', FTSE, project_colors['bright-blue']),
                    style={'padding':'20px 20px 0 20px','margin-right':'30px',"background-color": project_colors['dark-blue']}),
            dbc.Col(get_index_row('IBOVESPA', 'BRL', IBOVESPA, project_colors['bright-blue']),
                    style={'padding':'20px 20px 0 20px','margin-right':'30px',"background-color": project_colors['dark-blue']}),
            dbc.Col(get_index_row('SSEComp.', 'CNY', SSEComposite, project_colors['bright-blue']),
                    style={'padding':'20px 20px 0 20px',"background-color": project_colors['dark-blue']}),

        ])
    ], style=CONTAINER_STYLE)

    return return_row
