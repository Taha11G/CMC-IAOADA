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

def create_kpi_card(title, value, subtext, icon, color):
    return dbc.Card(
        dbc.CardBody([
            html.Div([
                html.Div([
                    html.P(title, className="text-muted mb-1", style={'font-size':'0.8rem', 'text-transform':'uppercase'}),
                    html.H4(value, className="card-title fw-bold mb-0"),
                ]),
                html.Div(
                    html.I(className=icon, style={"font-size": "1.2rem", "color": "white"}),
                    style={"background-color": color, "width": "40px", "height": "40px", "border-radius": "10px", "display": "flex", "align-items": "center", "justify-content": "center"}
                )
            ], className="d-flex justify-content-between align-items-center mb-2"),
            html.Small(subtext, className="text-secondary")
        ]),
        style=CARD_STYLE,
        className="mb-4 h-100"
    )

def layout():
    return html.Div(id="home-content")

@callback(
    Output("home-content", "children"),
    [Input('global-month', 'value'),
     Input('global-vehicle', 'value'),
     Input('global-payment', 'value'),
     Input('global-status', 'value')]
)
def update_home(month, vehicle, payment, status):
    data = df_uber.copy()
    if month and month != 'All': data = data[data['Month'] == month]
    if vehicle and vehicle != 'All': data = data[data['Vehicle_Type'] == vehicle]
    if payment and payment != 'All': data = data[data['Payment_Method'] == payment]
    if status and status != 'All': data = data[data['Status'] == status]

    if data.empty:
        return html.Div("Aucune donnée pour les filtres sélectionnés", className="text-center mt-5")

    total_rides = len(data)
    completed_df = data[data['Status'] == 'Terminé']
    cancelled_df = data[data['Status'] == 'Annulé']
    
    success_rate = (len(completed_df) / total_rides) * 100 if total_rides > 0 else 0
    cancel_rate = (len(cancelled_df) / total_rides) * 100 if total_rides > 0 else 0
    revenue = data['Price'].sum()
    rating = data['Rating'].mean()

    status_counts = data['Status'].value_counts().reset_index()
    status_counts.columns = ['Status', 'Count']
    fig_pie = px.pie(status_counts, names='Status', values='Count', title="Statut des Réservations", hole=0.6, 
                     color='Status', color_discrete_map={'Terminé': '#00e5ff', 'Annulé': '#ff0055'})
    fig_pie.update_layout(template="plotly_dark", margin=dict(l=10, r=10, t=30, b=10), showlegend=True, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

    monthly_data = data.groupby('Month').size().reindex(['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']).reset_index(name='Count')
    fig_line = px.line(monthly_data, x='Month', y='Count', markers=True, template="plotly_dark", title="Tendance Mensuelle")
    fig_line.update_traces(line_color='#00e5ff')
    fig_line.update_layout(margin=dict(l=20, r=20, t=30, b=20), yaxis=dict(showgrid=False), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

    fig_hist = px.histogram(data, x='Price', nbins=50, title="Distribution de la Valeur des Réservations", color_discrete_sequence=['#ff0055'], template="plotly_dark")
    fig_hist.update_layout(margin=dict(l=20, r=20, t=30, b=20), xaxis_title="Valeur de la Réservation (Prix)", yaxis_title="Nombre", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

    return html.Div([
        html.H4("Vue d'ensemble", className="mb-4 fw-bold"),
        dbc.Row([
            dbc.Col(create_kpi_card("Total Réservations", f"{total_rides:,.0f}", "Trajets totaux", "fa-solid fa-users", "#333333")),
            dbc.Col(create_kpi_card("Taux de Réussite", f"{success_rate:.1f}%", "Trajets complétés", "fa-solid fa-check-circle", "#00e5ff")),
            dbc.Col(create_kpi_card("Taux d'Annulation", f"{cancel_rate:.1f}%", "Trajets annulés", "fa-solid fa-circle-xmark", "#ff0055")),
            dbc.Col(create_kpi_card("Revenu Total", f"₹{revenue:,.0f}", "Valeur brute", "fa-solid fa-wallet", "#b000ff")),
            dbc.Col(create_kpi_card("Note Moyenne", f"{rating:.2f}" if pd.notna(rating) else "N/A", "Avis clients", "fa-solid fa-star", "#ffb300")),
        ], className="mb-4", style={"display": "flex", "flexWrap": "nowrap", "overflowX": "auto"}),
        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardBody(dcc.Graph(figure=fig_line))
            ], style=CARD_STYLE), width=8),
            dbc.Col(dbc.Card([
                dbc.CardBody(dcc.Graph(figure=fig_pie))
            ], style=CARD_STYLE), width=4)
        ], className="mb-4"),
        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardBody(dcc.Graph(figure=fig_hist))
            ], style=CARD_STYLE), width=12)
        ])
    ])
