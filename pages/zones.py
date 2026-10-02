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
    return html.Div(id="zone-content")

@callback(
    Output("zone-content", "children"),
    [Input('global-month', 'value'),
     Input('global-vehicle', 'value'),
     Input('global-payment', 'value'),
     Input('global-status', 'value')]
)
def update_zones(month, vehicle, payment, status):
    data = df_uber.copy()
    if month and month != 'All': data = data[data['Month'] == month]
    if vehicle and vehicle != 'All': data = data[data['Vehicle_Type'] == vehicle]
    if payment and payment != 'All': data = data[data['Payment_Method'] == payment]
    if status and status != 'All': data = data[data['Status'] == status]

    if data.empty:
        return html.Div("Aucune donnée pour les filtres sélectionnés", className="text-center mt-5")

    pickup_counts = data['Pickup_Location'].value_counts().reset_index()
    pickup_counts.columns = ['Lieu', 'Prises en charge']
    drop_counts = data['Drop_Location'].value_counts().reset_index()
    drop_counts.columns = ['Lieu', 'Dépôts']
    
    loc_stats = pd.merge(pickup_counts, drop_counts, on='Lieu', how='outer').fillna(0)
    loc_stats['Total'] = loc_stats['Prises en charge'] + loc_stats['Dépôts']
    top_locs = loc_stats.sort_values('Total', ascending=False).head(10)
    
    melted = top_locs.melt(id_vars='Lieu', value_vars=['Prises en charge', 'Dépôts'], var_name='Type', value_name='Nombre')
    
    fig_freq = px.bar(melted, x='Lieu', y='Nombre', color='Type', barmode='group',
                      title="Top 10 des Zones à Forte Activité",
                      color_discrete_map={'Prises en charge': '#00e5ff', 'Dépôts': '#ff0055'})
    fig_freq.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    
    rev_by_zone = data.groupby('Pickup_Location')['Price'].sum().sort_values(ascending=False).head(10).reset_index()
    fig_rev = px.bar(rev_by_zone, x='Pickup_Location', y='Price', title="Top 10 des Zones par Revenu",
                     color='Price', color_continuous_scale='magenta')
    fig_rev.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    
    cancel_data = data[data['Status'] == 'Annulé'].copy()
    
    if cancel_data.empty:
         fig_cancel = px.bar(title="Aucune Annulation dans la Sélection")
    else:
        def get_source(row):
            if pd.notna(row.get('Reason for cancelling by Customer')): return 'Client'
            if pd.notna(row.get('Driver Cancellation Reason')): return 'Chauffeur'
            return 'Inconnu'
        
        cancel_data['Source'] = cancel_data.apply(get_source, axis=1)
        top_cancel_zones = cancel_data['Pickup_Location'].value_counts().head(10).index.tolist()
        final_cancel_data = cancel_data[cancel_data['Pickup_Location'].isin(top_cancel_zones)]
        grouped_cancel = final_cancel_data.groupby(['Pickup_Location', 'Source']).size().reset_index(name='Nombre')
        
        fig_cancel = px.bar(grouped_cancel, x='Pickup_Location', y='Nombre', 
                            title="Top 10 des Zones : Annulations par Source",
                            color='Source', 
                            color_discrete_map={'Client': '#ff0055', 'Chauffeur': '#00e5ff', 'Inconnu': '#b000ff'},
                            barmode='stack')
        fig_cancel.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    
    return html.Div([
        html.H4("Analyse Géographique", className="mb-4 fw-bold"),
        dbc.Row([
            dbc.Col(dbc.Card(dcc.Graph(figure=fig_freq), style=CARD_STYLE), width=6),
            dbc.Col(dbc.Card(dcc.Graph(figure=fig_rev), style=CARD_STYLE), width=6)
        ], className="mb-4"),
        dbc.Row([
            dbc.Col(dbc.Card(dcc.Graph(figure=fig_cancel), style=CARD_STYLE), width=12)
        ])
    ])
