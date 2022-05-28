import requests
import plotly.graph_objs as go
import json

from project_variables import mkt_over_info

# function for API call
def get_top_ten_API_call():
    resp = requests.get(mkt_over_info['api_link_top_ten'] + mkt_over_info['api_key'])

    if resp['Response'] == 'Error':
        print('get_top_ten_API_call error out on API call')
        f = open('data/crypto_data_backup.json')
        resp = json.load(f)
    else:
        resp = resp.json()

    # get json from query
    return resp

# function to create bar chart for top ten market cap coins
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
        marker_color='#FFC300',
        marker_line_color="rgba(0,0,0,0)",
        textfont_color="#fff"
    ))

    fig.update_layout(xaxis_visible=False,
                      xaxis_showticklabels=False,
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)',
                      )

    return fig