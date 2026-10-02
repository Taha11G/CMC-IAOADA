import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
from data import df_uber

CARD_STYLE = {
    "border": "none",
    "border-radius": "12px",
    "box-shadow": "0 4px 6px rgba(0,0,0,0.3)",
    "background-color": "#1e1e1e",
    "color": "#e0e0e0",
    "transition": "transform 0.2s"
}

def layout():
    return html.Div(id="rate-content")

@callback(
    Output("rate-content", "children"),
    [Input('global-month', 'value'),
     Input('global-vehicle', 'value'),
     Input('global-payment', 'value'),
     Input('global-status', 'value')]
)
def update_rating(month, vehicle, payment, status):
    data = df_uber.copy()
    if month and month != 'All': data = data[data['Month'] == month]
    if vehicle and vehicle != 'All': data = data[data['Vehicle_Type'] == vehicle]
    if payment and payment != 'All': data = data[data['Payment_Method'] == payment]
    if status and status != 'All': data = data[data['Status'] == status]

    if data.empty:
        return html.Div("Aucune donnée pour les filtres sélectionnés", className="text-center mt-5")

    fig1 = px.box(data, x='Vehicle_Type', y='Rating', color='Vehicle_Type', 
                  title="Distribution des Notes par Type de Véhicule", template="plotly_dark")
    fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

    fig2 = px.histogram(data, x='Rating', nbins=10, title="Distribution des Notes", 
                        color_discrete_sequence=['#ffea00'], template="plotly_dark")
    fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    
    fig3 = px.scatter(data, x='Distance', y='Price', color='Vehicle_Type', 
                      title="Distance vs Prix", render_mode='webgl', template="plotly_dark")
    fig3.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

    return html.Div([
        html.H4("Satisfaction & Rentabilité", className="mb-4 fw-bold"),
        dbc.Row([
            dbc.Col(dbc.Card(dcc.Graph(figure=fig1), style=CARD_STYLE), width=12, className="mb-4")
        ]),
        dbc.Row([
            dbc.Col(dbc.Card(dcc.Graph(figure=fig2), style=CARD_STYLE), width=4),
            dbc.Col(dbc.Card(dcc.Graph(figure=fig3), style=CARD_STYLE), width=8)
        ])
    ])
