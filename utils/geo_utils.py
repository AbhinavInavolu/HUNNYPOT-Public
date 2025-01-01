from math import radians, sin, cos, sqrt, atan2


def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0

    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)

    delta_lat = lat2_rad - lat1_rad
    delta_lon = lon2_rad - lon1_rad

    a = sin(delta_lat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(delta_lon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c

def get_city_name(cities_df, target_lat, target_lon, max_distance_km=50):
    cities_df = cities_df.copy()
    cities_df['distance'] = cities_df.apply(
        lambda row: haversine(target_lat, target_lon, row['lat'], row['lng']), axis=1
    )
    
    filtered_cities = cities_df[
        (cities_df['distance'] <= max_distance_km) &
        (cities_df['population'] > 100000)
    ]
    
    closest_city = filtered_cities.loc[filtered_cities['distance'].idxmin(), 'city'] if not filtered_cities.empty else None
    
    return closest_city
