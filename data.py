import pandas as pd
import numpy as np
import datetime
import os

def load_data():
    # Get the directory of the current script to ensure relative paths work correctly
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "ride_bookings.csv")
    df = pd.read_csv(file_path)

    df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], errors='coerce')
    df['Month'] = df['Datetime'].dt.month_name()
    months_fr = {'January': 'Janvier', 'February': 'Février', 'March': 'Mars', 'April': 'Avril', 'May': 'Mai', 'June': 'Juin', 'July': 'Juillet', 'August': 'Août', 'September': 'Septembre', 'October': 'Octobre', 'November': 'Novembre', 'December': 'Décembre'}
    df['Month'] = df['Month'].map(months_fr)
    df['Day_of_Week'] = df['Datetime'].dt.day_name()
    df['Hour'] = df['Datetime'].dt.hour
    
    df['Status'] = df['Booking Status'].apply(lambda x: 'Terminé' if x == 'Completed' else 'Annulé')
    
    def get_reason(row):
        if pd.notna(row.get('Reason for cancelling by Customer')): return row['Reason for cancelling by Customer']
        if pd.notna(row.get('Driver Cancellation Reason')): return row['Driver Cancellation Reason']
        if pd.notna(row.get('Incomplete Rides Reason')): return row['Incomplete Rides Reason']
        return "Inconnu"
    df['Cancellation_Reason'] = df.apply(get_reason, axis=1)

    df['Payment_Method'] = df['Payment Method'].fillna('Inconnu').astype(str)
    df['Distance'] = pd.to_numeric(df['Ride Distance'], errors='coerce')

    df = df.rename(columns={
        'Vehicle Type': 'Vehicle_Type',
        'Pickup Location': 'Pickup_Location',
        'Drop Location': 'Drop_Location'
    })
    
    df['Vehicle_Type'] = df['Vehicle_Type'].fillna('Inconnu')
    df['Price'] = pd.to_numeric(df['Booking Value'], errors='coerce')
    df['Wait_Time'] = pd.to_numeric(df['Avg VTAT'], errors='coerce')
    df['Rating'] = pd.to_numeric(df['Driver Ratings'], errors='coerce')
    
    return df

df_uber = load_data()
