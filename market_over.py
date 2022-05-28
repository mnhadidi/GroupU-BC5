from dash import html
import dash_bootstrap_components as dbc
from dash import dcc

from project_variables import CONTENT_STYLE, project_colors
from market_overv_func import get_top_ten_API_call, create_top_ten_coins_chart,get_simulation_plot,crypto_sim_ind,stock_sim_ind

####################
# DATA
####################
resp = get_top_ten_API_call()

####################
# VISUALS
####################
top_ten_coin_mkt_cap = create_top_ten_coins_chart(resp)
simulation_plot, simulation_data = get_simulation_plot()
crypto_sim_ind = crypto_sim_ind(simulation_data)
stock_sim_ind = stock_sim_ind(simulation_data)


####################
# FINAL LAYOUT
####################

market_over = html.Div([

    dbc.Container([
        html.Div([
            html.H1('Market Overview')
        ],
            style={'padding-top': '20px', 'padding-bottom': '20px'}),

        html.Div([

            dbc.Row([
                dbc.Col(
                    html.Div([
                        html.H2('Top 10 Crypto Market Cap'),
                        dcc.Graph(figure=top_ten_coin_mkt_cap)
                    ]), width=6),

                dbc.Col(
                    html.Div([
                        html.H2('bleblebleb'),
                        # dcc.Graph(figure=top_ten_coin_mkt_cap)
                    ]), width=3),

                dbc.Col(
                    html.Div([
                        html.H2('bleblebleb'),
                        # dcc.Graph(figure=top_ten_coin_mkt_cap)
                    ]), width=3),


                ],
                style={'padding-top': '20px', 'padding-bottom': '20px'}
            ),

            dbc.Row([
                dbc.Col(
                    html.Div([
                        html.H2('Crypto vs Stock Simulation'),
                        html.P('If you had invested $1000 in Crypto or Stocks one year ago...',
                                   style={'color': '#ffffff'}),
                        dbc.Row([
                            dbc.Col(dcc.Graph(figure=simulation_plot), width=8),
                            dbc.Col(
                                html.Div([

                                    html.Div([
                                        html.H4('Crypto Portfolio Value', style={'text-align':'center','color':'#ffffff'}),
                                        dcc.Graph(figure=crypto_sim_ind, style={'height':'100px'}),
                                    ], style={"background-color": project_colors['dark-blue'],
                                              "margin-bottom":"20px",'padding':'10px'}),

                                    html.Div([
                                        html.H4('Stock Portfolio Value', style={'text-align':'center','color':'#ffffff'}),
                                        dcc.Graph(figure=stock_sim_ind, style={'height':'100px'}),
                                    ], style={"background-color": project_colors['dark-blue'],'padding':'10px'}),

                                ]),
                                width=4)
                        ], className='align-items-center')
                    ]), width=9),

                dbc.Col(
                    html.Div([
                        html.H2('bleblebleb'),
                        # dcc.Graph(figure=top_ten_coin_mkt_cap)
                    ]), width=3)

                ],
                style={'padding-top': '20px', 'padding-bottom': '20px'}
            )

        ])

    ]),

], style=CONTENT_STYLE
)
