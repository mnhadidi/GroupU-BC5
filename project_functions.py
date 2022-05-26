from dash import html, dash_table, dcc
import dash_bootstrap_components as dbc
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import plotly.graph_objs as go
import pandas as pd
from datetime import datetime

# import internal project libraries
from project_variables import timeframe_tranf, timeframe_full_name
from project_variables import project_colors, time_frame_options, start_info

##########################
# CANDLESTICK FIGURE
# used on ind_coins_layout
##########################
def candlestick_fig_create(coin_df):
    candlestick_fig = go.Figure(data=[go.Candlestick(x=coin_df.index.values,
                                                     open=coin_df["Open"],
                                                     high=coin_df["High"],
                                                     low=coin_df["Low"],
                                                     close=coin_df["Close"],
                                                     increasing_line_color=project_colors['green'],
                                                     decreasing_line_color=project_colors['red'])])

    # Edit the layout
    candlestick_fig.update_layout(xaxis_title='Date', yaxis_title='Price USD', plot_bgcolor='rgba(0,0,0,0)',
                                  paper_bgcolor='rgba(0,0,0,0)')
    candlestick_fig.update_layout(title_font_color='#FFFFFF', font_color='#FFFFFF')
    candlestick_fig.update_layout(xaxis_rangeslider_visible=False,margin=dict(l=20, r=16, t=20, b=20))

    return candlestick_fig


##########################
# LINEAR REGRESSION MODEL
# used on ind_coins_layout
##########################

def run_linear_regression(orig_coin_df):
    orig_coin_df.dropna(inplace=True)
    orig_coin_df = orig_coin_df.reset_index()
    coin_plot_df = orig_coin_df
    coin_df_train = orig_coin_df[-60:]

    required_features = ['Open', 'High', 'Low', 'Volume']
    output_label = 'Close'

    x_train, x_test, y_train, y_test = train_test_split(
        coin_df_train[required_features],
        coin_df_train[output_label],
        test_size=0.2,
        random_state=0,
        shuffle=False
    )

    model = LinearRegression()
    model.fit(x_train, y_train)

    future_set = orig_coin_df.shift(periods=30).tail(30)

    prediction = model.predict(x_test)

    dates = pd.date_range(start=datetime.today(), periods=30).to_pydatetime().tolist()

    prediction = prediction[0:30]

    return orig_coin_df, prediction, dates


##########################
# LINEAR REGRESSION PLOT
# used on ind_coins_layout
##########################
def create_pred_plot(orig_coin_df, prediction, dates):


    prediction_fig = go.Figure()
    # Create and style traces
    prediction_fig = prediction_fig.add_trace(go.Scatter(x=orig_coin_df['Date'][-180:], y=orig_coin_df["Close"][-180:], name='Historical',
                             line=dict(color=project_colors['pink'])))
    prediction_fig = prediction_fig.add_trace(go.Scatter(x=dates, y=prediction, name = 'Prediction',
                             line=dict(color='goldenrod')))

    # Edit the layout
    prediction_fig = prediction_fig.update_layout(xaxis_title='Date',
                       yaxis_title='Price USD')

    prediction_fig = prediction_fig.update_layout(margin=dict(l=20, r=16, t=20, b=20))

    prediction_fig.update_layout(xaxis_title='Date', yaxis_title='Price USD', plot_bgcolor='rgba(0,0,0,0)',
                                  paper_bgcolor='rgba(0,0,0,0)')
    prediction_fig.update_layout(title_font_color='#FFFFFF', font_color='#FFFFFF')

    prediction_fig = prediction_fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))

    return prediction_fig

##########################
# TABLE WITH NEXT PREDICTED PRICES
# used on ind_coins_layout
##########################

def get_pred_pric_tab(prediction, dates):
    d = {'Date':dates[0:len(prediction)],'Close':prediction}
    new_data = pd.DataFrame(d)
    new_data['Close (USD)'] = new_data['Close'].map('{:,.2f}'.format)
    new_data['Date'] = new_data['Date'].dt.strftime('%d/%m/%Y')
    new_data = new_data[['Date','Close (USD)']][0:10]

    # pred_pric_tab = go.Figure(data=[go.Table(header=dict(values=['Date', 'Pred price']),
    #                                          cells=dict(values=[new_data['Date'][0:10], new_data['Close'][0:10]]))
    #                                 ])

    pred_pric_tab = dash_table.DataTable(
        data=new_data.to_dict('records'),
        columns=[{"name": i, "id": i} for i in new_data.columns],
        style_cell={'textAlign': 'center'},
        style_header={
            'backgroundColor': 'rgba(0,0,0,0.1)',
            'color': 'white'
        },
        style_data={
            'backgroundColor': 'rgba(0,0,0,0)',
            'color': 'white'
        },
        id = 'tbl'
    )
    return pred_pric_tab

##########################
# KPI DIV
# used on ind_coins_layout
##########################
def create_kpi_div(timeframe, coin_df):
    # get values
    current_price = coin_df['Close'][-1]
    last_day = coin_df['Close'][-2]
    day_change = current_price - last_day
    day_change_perc = ((current_price - last_day) / last_day) * 100
    max_price_of_period = coin_df['Close'].max()
    min_price_of_period = coin_df['Close'].min()

    # format numbers
    current_price_str = "${:,.2f}".format(current_price)
    day_change_str = "${:+,.2f}".format(day_change) + " " + "({:+,.2f}%)".format(day_change_perc)
    max_price = "${:,.2f}".format(max_price_of_period)
    min_price = "${:,.2f}".format(min_price_of_period)

    # change string names
    high_string = timeframe_full_name[timeframe] + " high"
    low_string = timeframe_full_name[timeframe] + " low"

    # get color to format day change
    if day_change >= 0:
        color = project_colors['green']
    else:
        color = project_colors['red']

    kpi_div = dbc.Row([
                dbc.Col([
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4(current_price_str, className="card-title", style={'color': '#ffffff'}),
                                html.P(
                                    "Current price",
                                    className="card-text",
                                ),
                            ]
                        ), style={'backgroundColor': project_colors['navy-blue'], 'border-radius': '0px', 'border': '0px',
                                  'color': '#ffffff'}
                    )
                ], width=3),

                dbc.Col([
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4(day_change_str, className="card-title", style={'color': color}),
                                html.P(
                                    "Last day change",
                                    className="card-text",
                                ),
                            ]
                        ), style={'backgroundColor': project_colors['navy-blue'], 'border-radius': '0px', 'border': '0px','color':'white'}
                    )
                ], width=3),

                dbc.Col([
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4(max_price, className="card-title", style={'color': '#ffffff'}),
                                html.P(
                                    high_string,
                                    className="card-text",
                                ),
                            ]
                        ), style={'backgroundColor': project_colors['navy-blue'], 'border-radius': '0px', 'border': '0px','color':'white'}
                    )
                ], width=3),

                dbc.Col([
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4(min_price, className="card-title", style={'color': '#ffffff'}),
                                html.P(
                                    low_string,
                                    className="card-text",
                                ),
                            ]
                        ), style={'backgroundColor': project_colors['navy-blue'], 'border-radius': '0px', 'border': '0px','color':'white'}
                    )
                ], width=3)

            ])

    return kpi_div


"""
CURRENCY DROPDOWN
used on ind_coins_layout
"""

def func_currency_dropdown(coin_dict, coin):
    currency_dropdown = html.Div([
                            dcc.Dropdown(
                                id='coin_dropdown',
                                options=coin_dict,
                                value=coin,
                                placeholder="Write a coin or ticker",
                                multi=False,
                                clearable=True, # this one was false
                                style={"min-width": "1rem"}
                            ),
                        ], className='align-middle')

    return currency_dropdown

##########################
# BUTTON GROUP
# used on ind_coins_layout
##########################

def func_button_group():

    button_group = html.Div(
        [
            dbc.RadioItems(
                id="data_radio",
                className="btn-group",
                inputClassName="btn-check",
                labelClassName="btn btn-outline-primary",
                labelCheckedClassName="active",
                options=time_frame_options,
                value=start_info['time'],

            ),
        ],
        className="radio-group",
        style={'text-align': 'right', 'padding-right': '16px'}
    )

    return button_group