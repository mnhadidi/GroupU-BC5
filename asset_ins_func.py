import numpy as np
from dash import html, dash_table, dcc
import dash_bootstrap_components as dbc
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import plotly.graph_objs as go
import pandas as pd
from datetime import datetime
import datetime as dt
from typing import Callable

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
    candlestick_fig.update_layout(xaxis_rangeslider_visible=False, margin=dict(l=20, r=16, t=20, b=20))

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
    prediction_fig = prediction_fig.add_trace(
        go.Scatter(x=orig_coin_df['Date'][-180:], y=orig_coin_df["Close"][-180:], name='Historical',
                   line=dict(color=project_colors['pink'])))
    prediction_fig = prediction_fig.add_trace(
        go.Scatter(x=dates, y=prediction, name='Prediction',
                   line=dict(color=project_colors['gold'])))

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
    d = {'Date': dates[0:len(prediction)], 'Close': prediction}
    new_data = pd.DataFrame(d)
    new_data['Close (USD)'] = new_data['Close'].map('{:,.2f}'.format)
    new_data['Date'] = new_data['Date'].dt.strftime('%d/%m/%Y')
    new_data = new_data[['Date', 'Close (USD)']][0:10]

    # ALTERNATIVE

    table_header = [
        html.Thead(html.Tr([html.Th("Date"), html.Th("Close (USD)")]))
    ]

    row_list = []

    for row in range(0, len(new_data.index)):
        new_data.apply(lambda x: row_list.append(
            html.Tr([html.Td(new_data['Date'][row]),
                     html.Td(new_data['Close (USD)'][row])])))


    table_body = [html.Tbody(row_list)]

    table = dbc.Table(table_header + table_body, bordered=False)

    return table


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
    rsi_value = get_rsi_value(coin_df)

    # format numbers
    current_price_str = "${:,.2f}".format(current_price)
    day_change_str = "${:+,.2f}".format(day_change) + " " + "({:+,.2f}%)".format(day_change_perc)
    max_price = "${:,.2f}".format(max_price_of_period)
    min_price = "${:,.2f}".format(min_price_of_period)
    rsi_value = "{:,.2f}".format(rsi_value)

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
                ), style={'backgroundColor': project_colors['navy-blue'], 'border-radius': '0px', 'border': '0px',
                          'color': 'white'}
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
                ), style={'backgroundColor': project_colors['navy-blue'], 'border-radius': '0px', 'border': '0px',
                          'color': 'white'}
            )
        ], width=2),

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
                ), style={'backgroundColor': project_colors['navy-blue'], 'border-radius': '0px', 'border': '0px',
                          'color': 'white'}
            )
        ], width=2),

        dbc.Col([
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H4(rsi_value, className="card-title", style={'color': '#ffffff'}),
                        html.P(
                            'RSI',
                            className="card-text",
                        ),
                    ]
                ), style={'backgroundColor': project_colors['navy-blue'], 'border-radius': '0px', 'border': '0px',
                          'color': 'white'}
            )
        ], width=2)

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
            clearable=False,  # this one was false
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


##########################
# RSI CALCULATIONS
# used on ind_coins_layout
##########################

def get_rsi_value(data_for_rsi):
    # Window length for moving average
    length = 14
    data_for_rsi = data_for_rsi.reset_index()
    # Dates
    start, end = dt.datetime.today() - dt.timedelta(
        days=30), dt.datetime.today() - dt.timedelta(days=1)

    # create mask to get data between start and end date
    mask = (data_for_rsi['Date'] >= start) & (data_for_rsi['Date'] <= end)
    data_for_rsi = data_for_rsi.loc[mask]
    # get only close price from data
    close = data_for_rsi['Close']

    # Define function to calculate the RSI
    def calc_rsi(over: pd.Series, fn_roll: Callable) -> pd.Series:
        # Get the difference in price from previous step
        delta = over.diff()
        # Get rid of the first row, which is NaN since it did not have a previous row to calculate the differences
        delta = delta[1:]

        # Make the positive gains (up) and negative gains (down) Series
        up, down = delta.clip(lower=0), delta.clip(upper=0).abs()

        roll_up, roll_down = fn_roll(up), fn_roll(down)
        rs = roll_up / roll_down
        rsi = 100.0 - (100.0 / (1.0 + rs))

        # Avoid division-by-zero if `roll_down` is zero
        # This prevents inf and/or nan values.
        rsi[:] = np.select([roll_down == 0, roll_up == 0, True], [100, 0, rsi])
        rsi.name = 'rsi'

        # Assert range
        valid_rsi = rsi[length - 1:]
        assert ((0 <= valid_rsi) & (valid_rsi <= 100)).all()
        # Note: rsi[:length - 1] is excluded from above assertion because it is NaN for SMA.

        return rsi

    # Calculate RSI using RMA
    rsi_rma = calc_rsi(close, lambda s: s.ewm(alpha=1 / length).mean()).to_frame()  # Approximates TradingView.

    return rsi_rma['rsi'].iloc[-1]


##########################
# RSI GAUGE
# used on ind_coins_layout
##########################
#
# def create_rsi_gauge(rsi_value):
#     # plot_bgcolor = "rgba(0,0,0,0)"
#     # quadrant_colors = [plot_bgcolor, "#2bad4e", "#85e043", "#eff229", "#f2a529", "#f25829"]
#     # quadrant_text = ["", "<b>High</b>", "", "", "", "<b>Low</b>"]
#     # n_quadrants = len(quadrant_colors) - 1
#     #
#     # min_value = 0
#     # max_value = 100
#     # hand_length = np.sqrt(2) / 4
#     # hand_angle = np.pi * (1 - (max(min_value, min(max_value, rsi_value)) - min_value) / (max_value - min_value))
#     #
#     # fig = go.Figure(
#     #     data=[
#     #         go.Pie(
#     #             values=[0.5] + (np.ones(n_quadrants) / 2 / n_quadrants).tolist(),
#     #             rotation=90,
#     #             hole=0.5,
#     #             # marker_colors=quadrant_colors,
#     #             text=quadrant_text,
#     #             textinfo="text",
#     #             hoverinfo="skip",
#     #         ),
#     #     ],
#     #     layout=go.Layout(
#     #         showlegend=False,
#     #         margin=dict(b=0,t=10,l=10,r=10),
#     #         width=450,
#     #         height=450,
#     #         paper_bgcolor=plot_bgcolor,
#     #         annotations=[
#     #             go.layout.Annotation(
#     #                 text=f"<b>Relative Strength Index</b><br>{rsi_value}",
#     #                 x=0.5, xanchor="center", xref="paper",
#     #                 y=0.25, yanchor="bottom", yref="paper",
#     #                 showarrow=False,
#     #             )
#     #         ],
#     #         shapes=[
#     #             go.layout.Shape(
#     #                 type="circle",
#     #                 x0=0.48, x1=0.52,
#     #                 y0=0.48, y1=0.52,
#     #                 fillcolor="#333",
#     #                 # line_color="#333",
#     #             ),
#     #             go.layout.Shape(
#     #                 type="line",
#     #                 x0=0.5, x1=0.5 + hand_length * np.cos(hand_angle),
#     #                 y0=0.5, y1=0.5 + hand_length * np.sin(hand_angle),
#     #                 line=dict(color="#333", width=4)
#     #             )
#     #         ]
#     #     )
#     # )
#
#     fig = go.Figure(go.Indicator(
#         mode="gauge+number",
#         value=rsi_value,
#         gauge={
#             'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "black"},
#             'bar': {'color': "rgba(0,0,0,0)"},
#             'borderwidth': 0,
#             'steps': [
#                 {'range': [0, 25], 'color': '#f25829'},
#                 {'range': [25, 50], 'color': '#eff229'},
#                 {'range': [50, 75], 'color': '#85e043'},
#                 {'range': [75, 100], 'color': '#2bad4e'}],
#             'threshold': {
#                 'line': {'color': "black", 'width': 10},
#                 'thickness': 0.75,
#                 'value': rsi_value}}))
#
#     return fig
