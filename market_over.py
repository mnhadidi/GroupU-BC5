# -*- coding: utf-8 -*-

from dash import html
import dash_bootstrap_components as dbc
from dash import dcc

# import internal project libraries
from project_variables import CONTENT_STYLE, project_colors, CONTAINER_STYLE
from market_overv_func import get_top_ten_API_call, create_top_ten_coins_chart, get_simulation_plot
from market_overv_func import crypto_sim_ind, stock_sim_ind,get_top_ten_coins_data, get_fear_greed_gauge
from market_overv_func import get_stories, get_stories_card,get_top_coins_tbl, get_row_of_index_plots

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
df_table = get_top_ten_coins_data(resp)
top_coin_table = get_top_coins_tbl(df_table)
response_stories = get_stories()
stories_card = get_stories_card(response_stories)
fear_and_greed_gauge = get_fear_greed_gauge()
world_stock_ind_chart = get_row_of_index_plots()


####################
# FINAL LAYOUT
####################

market_over = html.Div([

    dbc.Container([
        # first row with title
        dbc.Container([
            html.H1('Market Overview', style={'color':project_colors['white'],'font-weight': 'bold'})
        ], style=CONTAINER_STYLE),

        # second row with crypto vs stock simulation
        dbc.Container([
            html.H2('World Stock Indices Trending'),
            world_stock_ind_chart
        ], style=CONTAINER_STYLE),

        # second row with crypto vs stock simulation
        dbc.Container([
            dbc.Row([
                dbc.Col(
                    dbc.Container([
                        html.H2('Crypto vs Stock Simulation'),
                        html.P('If you had invested $1000 in Crypto or Stocks one year ago...',
                                   style={'color': '#ffffff', 'size':'16px'}),
                        dbc.Row([
                            dbc.Col(dcc.Graph(figure=simulation_plot), width=9),
                            dbc.Col(
                                html.Div([

                                    html.Div([
                                        html.H5('Stock Portfolio Value', style={'text-align':'center','color': project_colors['bright-blue']}),
                                        dcc.Graph(figure=stock_sim_ind, style={'height':'100px'}),
                                    ], style={"background-color": project_colors['dark-blue'],"margin-bottom":"20px",'padding':'10px'}),

                                    html.Div([
                                        html.H5('Crypto Portfolio Value', style={'text-align':'center','color': project_colors['gold']}),
                                        dcc.Graph(figure=crypto_sim_ind, style={'height':'100px'}),
                                    ], style={"background-color": project_colors['dark-blue'],
                                              'padding':'10px'})
                                ]),
                                width=3)
                        ], className='align-items-center')
                    ], style=CONTAINER_STYLE), width=12),

                ]
            )
        ], style=CONTAINER_STYLE),

        # third row with top 10 crypto bar chart and bull vs bear table
        dbc.Container([
            dbc.Row([
                dbc.Col(
                    dbc.Container([
                        html.H2('Top 10 Crypto Market Cap'),
                        dcc.Graph(figure=top_ten_coin_mkt_cap)
                    ], style=CONTAINER_STYLE),
                    width=8),

                dbc.Col(
                    dbc.Container([
                        html.H2('Bull vs Bear'),
                        top_coin_table
                    ], style=CONTAINER_STYLE),
                    width=4)
                ]
            )], style=CONTAINER_STYLE),



        # fourth row with latest crypto stories
        dbc.Container([
            dbc.Row([

                dbc.Col(
                    dbc.Container([
                        html.H2('Fear and Greed Index'),
                        dcc.Graph(figure=fear_and_greed_gauge, style={'margin-top':'15px'}),
                    ], style=CONTAINER_STYLE), width=5
                ),

                dbc.Col(
                    dbc.Container([
                        html.H2('Latest Stories on Crypto'),
                        stories_card
                    ], style=CONTAINER_STYLE), width=7
                ),
            ])
        ], style=CONTAINER_STYLE)


    ]),

], style=CONTENT_STYLE
)
