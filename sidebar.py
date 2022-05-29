import dash
import dash_bootstrap_components as dbc
from dash import html
from project_variables import project_colors

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": project_colors['dark-blue'],
    "color": project_colors['white']
}

SIDEBAR_BOTTOM = {
    "position": "fixed",
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
}

sidebar_top = html.Div([
        html.Div([
            html.Img(src='assets/logo-blue-alt.png',
                     style={'width': 'auto', 'height': '12rem', 'max-height': '15vh', 'margin': '0 auto 2rem auto'})
        ], style={'display': 'flex', 'justify-content': 'center'}),


        dbc.Nav(
            [
                dbc.NavLink("Asset Insights", href="/", active="exact"),
                dbc.NavLink("Market Overview", href="/market", active="exact"),
                html.Hr(),
                dbc.NavLink("Github", href="https://github.com/mnhadidi/GroupU-BC5", target='_blank'),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

sidebar_bottom = html.Div([

    html.P('Group U', style={'text-align': 'left', 'color': 'rgba(255,255,255,0.8)', 'font-weight': 'bold'}),
    html.P(['Beatriz Ferreira', html.Br(), 'Beatriz Peres', html.Br(),
            'Diogo Marques', html.Br(), 'Miriam Hadidi Pereira'],
           style={'text-align': 'left', 'color': 'rgba(255,255,255,0.7)', 'margin-bottom': '15px'}),
    html.Div([
        html.Img(src='assets/nova_ims.png',
                 style={'width': 'auto', 'height': '6rem', 'max-height': '10rem'}
                 )
    ])
], style=SIDEBAR_BOTTOM)

sidebar = html.Div([
    sidebar_top,
    sidebar_bottom
])
