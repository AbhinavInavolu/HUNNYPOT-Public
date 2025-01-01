from utils.constants import WORLD_MAP, WORLD_CITIES_CSV
from utils.ip_utils import lookup_ip
from utils.geo_utils import get_city_name

from sklearn.cluster import DBSCAN
from operator import itemgetter
import plotly.express as px
import pandas as pd
import numpy as np


def create_map(source_ip_counts):
    print("here")
    sorted_ips = sorted(source_ip_counts.items(), key=itemgetter(1), reverse=True)

    data = []
    for ip, count in sorted_ips:
        ip_info = lookup_ip(ip)
        data.append([ip, count, ip_info.get("City"), ip_info.get("Country"), ip_info.get("Latitude"), ip_info.get("Longitude")])

    df = convert_data(data)

    fig = px.scatter_mapbox(
        df,
        lat='lat',
        lon='long',
        size='frequency',
        hover_name="city",
        size_max=75,
        center=dict(lat=0, lon=0),
        zoom=1,
        mapbox_style="carto-positron"
    )

    fig.update_layout(
        title="World Map with Frequency-Based Circles",
        margin={"r":0, "t":0, "l":0, "b":0}
    )

    fig.write_html(WORLD_MAP)
    fig.write_image("./analysis/parsed/map.png", engine="kaleido")

def convert_data(enriched_data):
    data = []

    for attack in enriched_data:
        ip = attack[0]
        frequency = attack[1]
        city = attack[2]
        latitude = attack[4]
        longitude = attack[5]

        data.append([ip, frequency, city, latitude, longitude])

    df = pd.DataFrame(data, columns=['IP', 'frequency', 'city', 'lat', 'long'])

    kms_per_radian = 6371.0088
    epsilon = 10 / kms_per_radian
    coords = np.radians(df[['lat', 'long']].values)

    db = DBSCAN(eps=epsilon, min_samples=1, algorithm='ball_tree', metric='haversine')
    labels = db.fit_predict(coords)

    df['cluster'] = labels
    consolidated_data = consolidate_clusters(df)

    return consolidated_data

def consolidate_clusters(df):
    consolidated_data = []

    cities_df = pd.read_csv(WORLD_CITIES_CSV, encoding="utf-8")
    cities_df[['lat', 'lng']] = cities_df[['lat', 'lng']].astype(float)

    for _, group in df.groupby('cluster'):
        largest_city_row = group.loc[group['frequency'].idxmax()]

        city = largest_city_row['city']
        if not city:
            city = get_city_name(cities_df, largest_city_row['lat'], largest_city_row['long'])
            
        consolidated_data.append({
            'IP': largest_city_row['IP'],
            'frequency': group['frequency'].sum(),
            'lat': largest_city_row['lat'],
            'long': largest_city_row['long'],
            'city': city
        })

    return pd.DataFrame(consolidated_data)
