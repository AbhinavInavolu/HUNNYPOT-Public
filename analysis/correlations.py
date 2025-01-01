from utils.ip_utils import lookup_ip
from utils.geo_utils import haversine
from constants import CORRELATION_THRESHOLD

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def find_correlations(data):
    processed_data = []
    for entry in data.values():
        _, _, lat, lon = lookup_ip(entry['Source_IP']).values()

        processed_data.append({
            'Latitude': lat,
            'Longitude': lon,
            'Configuration': entry['Configuration'],
            'Duration': entry['Duration'],
            'Client_ID': entry['Client_ID'],
            'Number_of_Commands': len(entry['Commands']), 
            'Start_Time': int(entry['Start_Time'].timestamp()), 
            "Mode": int(entry['Noninteractive_Mode'])
        })

    df = pd.DataFrame(processed_data)

    cp_lat, cp_lon = 38.9897, -76.9378
    df['Distance_From_CP'] = df.apply(
        lambda row: haversine(row['Latitude'], row['Longitude'], cp_lat, cp_lon),
        axis=1
    )

    df['Configuration'] = pd.factorize(df['Configuration'])[0]
    df['Client_ID'] = pd.factorize(df['Client_ID'])[0]

    columns_to_analyze = [
        'Configuration', 'Duration', 'Client_ID',
        'Number_of_Commands', 'Distance_From_CP', 'Start_Time', 'Mode'
    ]

    correlation_matrix = df[columns_to_analyze].corr()

    for col1 in columns_to_analyze:
        for col2 in columns_to_analyze:
            if col1 != col2:
                corr = correlation_matrix.loc[col1, col2]

                if abs(corr) >= CORRELATION_THRESHOLD:
                    print(f"Significant Correlation Found: {col1} vs {col2} (r = {corr:.2f})")

                    plt.figure(figsize=(10, 6))
                    x = df[col1]
                    y = df[col2]

                    plt.scatter(x, y, alpha=0.6, edgecolors='k', label=f'r = {corr:.2f}')
                    
                    m, b = np.polyfit(x, y, 1)
                    plt.plot(x, m * x + b, color='red', label='Best Fit Line')

                    plt.title(f"Scatter Plot: {col1} vs {col2}")
                    plt.xlabel(col1)
                    plt.ylabel(col2)
                    plt.legend()
                    plt.grid(True)
                    plt.show()
