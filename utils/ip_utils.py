from utils.constants import GEO_IP_DATABASE

import geoip2.database
import ipaddress


def is_private_ip(ip_str):
    try:
        ip = ipaddress.ip_address(ip_str)
        return ip.is_private
    except ValueError:
        return False

def lookup_ip(ip_address):
    with geoip2.database.Reader(GEO_IP_DATABASE) as reader:
        response = reader.city(ip_address)
        return {
            "City": response.city.name,
            "Country": response.country.iso_code,
            "Latitude": response.location.latitude,
            "Longitude": response.location.longitude
        }
