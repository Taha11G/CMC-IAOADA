import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, callback
import plotly.express as px
from data import df_uber
import pandas as pd

CARD_STYLE = {
    "border": "none",
    "border-radius": "12px",
    "box-shadow": "0 4px 6px rgba(0,0,0,0.3)",
    "background-color": "#1e1e1e",
    "color": "#e0e0e0",
    "transition": "transform 0.2s"
}

def layout():
    return html.Div(id="cancel-content")

@callback(
    Output("cancel-content", "children"),
    [Input('global-month', 'value'),
     Input('global-vehicle', 'value'),
     Input('global-payment', 'value'),
     Input('global-status', 'value')]
)
def update_cancellations(month, vehicle, payment, status):
    data = df_uber.copy()
    if month and month != 'All': data = data[data['Month'] == month]
    if vehicle and vehicle != 'All': data = data[data['Vehicle_Type'] == vehicle]
    if payment and payment != 'All': data = data[data['Payment_Method'] == payment]
    if status and status != 'All': data = data[data['Status'] == status]

    sub_df = data[data['Status'] == 'Annulé']
    
    if sub_df.empty:
        return html.Div([
            html.H4("Aperçu des Annulations", className="mb-4 fw-bold"),
            dbc.Row(dbc.Col(dbc.Card(dcc.Graph(figure=px.bar(title="Aucune Annulation")), style=CARD_STYLE)))
        ])
    
    pie_fig = px.pie(sub_df, names='Vehicle_Type', title="Annulations par Véhicule", 
                     hole=0.6, color_discrete_sequence=px.colors.qualitative.Plotly)
    pie_fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    
    hourly_data = sub_df.groupby('Hour').size().reset_index(name='Nombre')
    all_hours = pd.DataFrame({'Hour': range(24)})
    hourly_data = pd.merge(all_hours, hourly_data, on='Hour', how='left').fillna(0)
    
    line_fig = px.line(hourly_data, x='Hour', y='Nombre', 
                       title="Annulations par Heure",
                       markers=True, line_shape='spline')
    line_fig.update_traces(line_color='#ff0055', line_width=3)
    line_fig.update_layout(template="plotly_dark", xaxis={'tickmode': 'linear', 'tick0': 0, 'dtick': 1}, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    
    reason_counts = sub_df['Cancellation_Reason'].value_counts().reset_index()
    reason_counts.columns = ['Raison', 'Nombre']
    bar_fig = px.bar(reason_counts, x='Nombre', y='Raison', orientation='h', title="Principales Raisons d'Annulation", 
                     color='Nombre', color_continuous_scale="Purples")
    bar_fig.update_layout(template="plotly_dark", yaxis={'categoryorder':'total ascending'}, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    
    return html.Div([
        html.H4("Aperçu des Annulations", className="mb-4 fw-bold"),
        dbc.Row([
            dbc.Col(dbc.Card(dcc.Graph(figure=pie_fig), style=CARD_STYLE), width=6),
            dbc.Col(dbc.Card(dcc.Graph(figure=line_fig), style=CARD_STYLE), width=6)
        ], className="mb-4"),
        dbc.Row(dbc.Col(dbc.Card(dcc.Graph(figure=bar_fig), style=CARD_STYLE), width=12))
    ])
