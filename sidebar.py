import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html
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
    "color":project_colors['white']
}

SIDEBAR_BOTTOM = {
    "position": "fixed",
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
}

sidebar_top = html.Div([
        # html.Div([
        #         html.Img(src='assets/logo-blue.png',
        #              style={'width': '60px', 'height': '60px'},
        #              )
        #     ], style={'display': 'flex', 'justify-content': 'center', 'margin-bottom':'20px'}),

        html.Img(src='assets/logo-blue-alt.png',
                 style={'width': '100%', 'height': 'auto', 'margin-bottom':'50px'},
                 ),
        # html.H2("MarketDash", style={"color":project_colors['white'],"padding-bottom":'2rem','text-align':'center'}),
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
    html.H5('made with 🧡 and 🍕', style={'text-align': 'center', 'font-size': '12pt', 'color': 'rgba(255,255,255,0.8)'}),
    html.H5('by Group U', style={'text-align': 'center', 'font-size': '12pt', 'color': 'rgba(255,255,255,0.8)'}),
    html.H5('Beatriz Ferreira | Beatriz Peres | Diogo Marques | Miriam Hadidi Pereira'
            , style={'text-align': 'center', 'font-size': '8pt', 'color': 'rgba(255,255,255,0.7)', 'margin-bottom':'30px'}),
    html.Div([
        html.Img(src='assets/nova_ims.png',
             style={'width': '64px', 'height': '64px'},
             )
    ], style={'display': 'flex', 'justify-content': 'center'})


],style=SIDEBAR_BOTTOM)

sidebar = html.Div([
    sidebar_top,
    sidebar_bottom
])