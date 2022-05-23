import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

#### USE THIS INFORMATION TO MAKE THE SIDEBAR BETTER ########################################
# nav bar
navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src='/assets/logo.png', height="30px")),
                        dbc.Col(dbc.NavbarBrand("CryptoDash", className="ms-2")),
                    ],
                    align="left",
                    className="g-0",
                ),
                href="#",
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.NavItem(dbc.NavLink("Github", href="https://github.com/mnhadidi/GroupU-BC5"))
        ]
    ),

)


html.Footer([
        html.Div([
            html.H5('made with 🧡 and 🍕 by Group U', style={'text-align': 'center', 'font-size': '12pt'}),
            html.H5('Beatriz Ferreira | Beatriz Peres | Diogo Marques | Miriam Hadidi Pereira'
                    , style={'text-align': 'center', 'font-size': '8pt', 'color': '#808080'})
        ], style={'padding': '20px', 'padding-top': '20px', 'backgroundColor': '#F5F5F5', 'margin-top': '10px'})
    ])
########################################################################################################################



# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

sidebar = html.Div(
    [
        dbc.Row([
            dbc.Col(html.Img(src='/assets/logo.png',className='img-fluid w-100')),
            dbc.Col(html.H2("CryptoDash"))
        ]),
        html.Hr(),
        html.P(
            "Crypto dashboard for coin predictions", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Crypto Insights", href="/", active="exact"),
                dbc.NavLink("Market Overview", href="/market", active="exact"),
                html.Hr(),
                dbc.NavLink("Github", href="https://github.com/mnhadidi/GroupU-BC5", target='_blank'),
            ],
            vertical=True,
            pills=True,
        ),
        html.Hr(),
        html.H5('made with 🧡 and 🍕', style={'text-align': 'center', 'font-size': '12pt'}),
        html.H5('by Group U', style={'text-align': 'center', 'font-size': '12pt'}),
        html.H5('Beatriz Ferreira | Beatriz Peres | Diogo Marques | Miriam Hadidi Pereira'
                , style={'text-align': 'center', 'font-size': '8pt', 'color': '#808080','bottom':0})
    ],
    style=SIDEBAR_STYLE,
)