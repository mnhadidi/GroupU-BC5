import requests
import plotly.graph_objs as go
import json

# function for API call
def get_top_ten_API_call():
    api_key = '{d4462bd4925c7c2d3d2adad9221d5e897dd7178ddac5a0558f76c978df7bd8da}'
    resp = requests.get(f'https://min-api.cryptocompare.com/data/top/mktcapfull?limit=10&tsym=USD&api_key={api_key}')

    if resp['Response']=='Error':
        resp = resp.json()
    else:
        f = open('./data/crypto_data.json')
        resp = json.load(f)
    # get json from query

    return resp

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