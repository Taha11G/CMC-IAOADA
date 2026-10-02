<<<<<<< HEAD
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, callback
import pages.home
import pages.cancelations
import pages.vehicle_type
import pages.zones


external_stylesheets = [
    dbc.themes.CYBORG,
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css",
    "https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@300;400;500;600&display=swap"
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)
server = app.server


from data import df_uber

months = sorted(list(df_uber['Month'].dropna().unique()))
vehicle_types = sorted(list(df_uber['Vehicle_Type'].dropna().unique()))
payment_methods = sorted(list(df_uber['Payment_Method'].dropna().unique()))
statuses = sorted(list(df_uber['Status'].dropna().unique()))

sidebar = html.Div(
    [
        html.Div([
            html.Div([
                html.H2("UBER", className="display-5 sidebar-title ms-2 mb-0"),
            ], className="d-flex align-items-center justify-content-center"),
            html.Hr(style={'borderColor': 'rgba(255,255,255,0.1)', 'margin': '1.5rem 0'}),
        ], className="sidebar-header"),
        
        dbc.Nav(
            [
                dbc.NavLink([html.I(className="fa-solid fa-gauge"), " Tableau de bord"], href="/", active="exact"),
                dbc.NavLink([html.I(className="fa-solid fa-ban"), " Annulations"], href="/cancelations", active="exact"),
                dbc.NavLink([html.I(className="fa-solid fa-taxi"), " Véhicules"], href="/vehicle-type", active="exact"),
                dbc.NavLink([html.I(className="fa-solid fa-map-location-dot"), " Zones"], href="/zones", active="exact"),
            ],
            vertical=True,
            pills=True,
            className="mb-4"
        )
    ],
    className="sidebar",
)

topbar = html.Div([
    dbc.Row([
        dbc.Col([
            html.Label("Mois", className="fw-bold mb-1", style={'font-size': '0.85rem'}),
            dcc.Dropdown(id='global-month', options=[{'label': 'Tous', 'value': 'All'}] + [{'label': m, 'value': m} for m in months], value='All', clearable=False),
        ], width=3),
        dbc.Col([
            html.Label("Type de Véhicule", className="fw-bold mb-1", style={'font-size': '0.85rem'}),
            dcc.Dropdown(id='global-vehicle', options=[{'label': 'Tous', 'value': 'All'}] + [{'label': v, 'value': v} for v in vehicle_types], value='All', clearable=False),
        ], width=3),
        dbc.Col([
            html.Label("Méthode de Paiement", className="fw-bold mb-1", style={'font-size': '0.85rem'}),
            dcc.Dropdown(id='global-payment', options=[{'label': 'Tous', 'value': 'All'}] + [{'label': p, 'value': p} for p in payment_methods], value='All', clearable=False),
        ], width=3),
        dbc.Col([
            html.Label("Statut de Réservation", className="fw-bold mb-1", style={'font-size': '0.85rem'}),
            dcc.Dropdown(id='global-status', options=[{'label': 'Tous', 'value': 'All'}] + [{'label': s, 'value': s} for s in statuses], value='All', clearable=False),
        ], width=3),
    ], className="mb-4 p-3 shadow-sm", style={'border-radius': '12px', 'background-color': '#1e1e1e', 'color': 'white'})
])

content = html.Div([
    topbar,
    html.Div(id="page-content")
], className="content")

app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar, 
    content
])

@callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(path):
    if path == "/cancelations": return pages.cancelations.layout()
    if path == "/vehicle-type": return pages.vehicle_type.layout()
    if path == "/zones": return pages.zones.layout()
    return pages.home.layout()

if __name__ == "__main__":
    app.run(debug=True,port=8051)
=======
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])


SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",          
    "padding": "2rem 1rem",    
    "background-color": "#f8f9fa", 
}

CONTENT_STYLE = {
    "margin-left": "18rem",    
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Retail Dash", className="display-4", style={"fontSize": "1.5rem", "marginBottom": "2rem", "fontWeight": "bold"}),
        html.Hr(),
        html.P(
            "Navigation", className="lead", style={"fontSize": "1rem", "color": "#6c757d"}
        ),
        dbc.Nav(
            [

                dbc.NavLink("📊 Vue Globale", href="/", active="exact"),
                dbc.NavLink("👥 Clients & Produits", href="/customer", active="exact"),
                dbc.NavLink("💳 Paiements", href="/payment", active="exact"),
            ],
            vertical=True,
            pills=True, 
            className="my-2"
        ),
    ],
    style=SIDEBAR_STYLE, 
)

app.layout = html.Div(
    [
        sidebar,
        
 
        html.Div(dash.page_container, style=CONTENT_STYLE) 
    ]
)

if __name__ == "__main__":
    app.run(debug=True)
    #note test
