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