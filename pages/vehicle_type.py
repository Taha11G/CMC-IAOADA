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
    return html.Div(id="veh-content")

@callback(
    Output("veh-content", "children"),
    [Input('global-month', 'value'),
     Input('global-vehicle', 'value'),
     Input('global-payment', 'value'),
     Input('global-status', 'value')]
)
def update_vehicles(month, vehicle, payment, status):
    data = df_uber.copy()
    if month and month != 'All': data = data[data['Month'] == month]
    if vehicle and vehicle != 'All': data = data[data['Vehicle_Type'] == vehicle]
    if payment and payment != 'All': data = data[data['Payment_Method'] == payment]
    if status and status != 'All': data = data[data['Status'] == status]

    if data.empty:
        empty_fig = px.bar(title="Aucune Donnée")
        return html.Div([
            html.H4("Performances de la Flotte & des Véhicules", className="mb-4 fw-bold"),
            dbc.Row(dbc.Col(dbc.Card(dcc.Graph(figure=empty_fig), style=CARD_STYLE)))
        ])

    usage = data['Vehicle_Type'].value_counts().reset_index()
    usage.columns = ['Véhicule', 'Trajets']
    
    fig_usage = px.bar(usage, x='Véhicule', y='Trajets', title="Nombre Total de Trajets par Type de Véhicule", 
                       color='Trajets', color_continuous_scale="Plasma")
    fig_usage.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    
    success = data.groupby('Vehicle_Type')['Status'].apply(lambda x: (x == 'Terminé').mean() * 100).reset_index()
    success.columns = ['Véhicule', 'Taux de Réussite']
    success = success.sort_values('Taux de Réussite', ascending=False)
    
    fig_success = px.bar(success, x='Véhicule', y='Taux de Réussite', 
                         title="Taux de Réussite (%) par Véhicule",
                         color='Taux de Réussite', color_continuous_scale='ice')
    fig_success.update_layout(template="plotly_dark", yaxis_title="% Réussite", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

    rev_total = data.groupby('Vehicle_Type')['Price'].sum().reset_index()
    rev_total.columns = ['Véhicule', 'Revenu Total']
    rev_total = rev_total.sort_values('Revenu Total', ascending=False)
    
    fig_total_rev = px.bar(rev_total, x='Véhicule', y='Revenu Total',
                           title="Revenu Total Généré",
                           color='Véhicule', color_discrete_sequence=px.colors.qualitative.Prism)
    fig_total_rev.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

    completed_data = data[data['Status'] == 'Terminé']
    if completed_data.empty:
        fig_avg_rev = px.bar(title="Aucun Trajet Complété pour le Revenu Moyen")
    else:
        rev_avg = completed_data.groupby('Vehicle_Type')['Price'].mean().reset_index()
        rev_avg.columns = ['Véhicule', 'Prix Moyen']
        rev_avg = rev_avg.sort_values('Prix Moyen', ascending=False)
        
        fig_avg_rev = px.bar(rev_avg, x='Véhicule', y='Prix Moyen',
                             title="Revenu Moyen par Trajet",
                             color='Prix Moyen', color_continuous_scale='magenta')
        fig_avg_rev.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

    return html.Div([
        html.H4("Performances de la Flotte & des Véhicules", className="mb-4 fw-bold"),
        dbc.Row([
            dbc.Col(dbc.Card(dcc.Graph(figure=fig_usage), style=CARD_STYLE), width=6),
            dbc.Col(dbc.Card(dcc.Graph(figure=fig_success), style=CARD_STYLE), width=6)
        ], className="mb-4"),
        dbc.Row([
            dbc.Col(dbc.Card(dcc.Graph(figure=fig_total_rev), style=CARD_STYLE), width=6),
            dbc.Col(dbc.Card(dcc.Graph(figure=fig_avg_rev), style=CARD_STYLE), width=6)
        ])
    ])
